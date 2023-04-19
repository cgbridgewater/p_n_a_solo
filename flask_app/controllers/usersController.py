from flask_app import app
from flask import render_template, request, redirect, session, flash, url_for
from flask_app.models.users import User
from flask_app.models.activities import Activity
import os
from werkzeug.utils import secure_filename



### ATHLETE DASHBOARD
@app.route('/getoutside/athlete')
def user_dashboard():
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("user_dashboard.html", user = User.get_user_by_id(data), activities = Activity.get_all_activities(), joined = Activity.get_all_activities_and_attendees(data), followers = User.all_followers(data))


### UPDATE ATHLETE FORM (protected)
@app.route('/getoutside/athlete/update')
def edit_user_form():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user_check = User.get_user_by_id(data)
    if session['user_id'] != user_check.id:
        return redirect('/logout')
    return render_template("user_update.html", user = User.get_user_by_id(data))


### ATHLETE UPDATE FORM POST ACTION (protected)
@app.route('/getoutside/athlete/update', methods =['POST'])
def update_user_form_action():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : session['user_id'],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"]
        }
    user_check = User.get_user_by_id(data)
    if session['user_id'] != user_check.id:
        return redirect('/logout')
    if not User.update_validation_check(data):
        return redirect('/getoutside/athlete/update')
    User.update_user_by_id(data)
    return redirect("/getoutside/athlete") 


### ATHLETUS DELETUS (protected)
@app.route('/getoutside/athlete/delete')
def delete_user_route():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user_check = User.get_user_by_id(data)
    if session['user_id'] != user_check.id:
        return redirect('/logout')
    User.delete_user(data)
    return redirect('/logout') 


### GET ATHLETE BY ID
@app.route('/getoutside/athlete/<int:id>')
def get_user_by_id(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
    "id" : id
    }
    return render_template("user_one_view.html", user = User.get_user_by_id(data), activities = Activity.get_all_activities())


### FOLLOW FRIEND 
@app.route('/getoutside/athlete/<int:id>/follow')
def follow_user_return_to_homepage(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'friend_id' : id,
        'user_id' : session['user_id']
    }
    User.follow_user(data)
    return redirect("/getoutside/athlete")


### UNFOLLOW FRIEND
@app.route('/getoutside/athlete/<int:id>/unfollow')
def unfollow_user(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'friend_id' : id,
        'user_id' : session['user_id']
    }
    User.unfollow_user(data)
    return redirect("/getoutside")


### FRIEND SEARCH SINGLE PAGE FORM/RESULTS
@app.route('/getoutside/friends')
def friend_search_page():
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("friends_search.html", allusers = User.get_all_users_excluding_logged_in_user(data)) 


### Image upload below
app.config["IMAGE_UPLOADS"] = 'flask_app/static/images'  #storage location
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", 'JPG', "JPEG", "GIF"]  #accepted file types
# app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024   #calculation for file size permitted
# check if extension exists ().filetype)
def allowed_image(filename):
    if not "." in filename:
        return False
    # extract file extensions to be checked
    ext = filename.rsplit(".", 1)[1]
    # check file extension type
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/getoutside/addimage", methods=['POST'])
def upload_image():
    if 'user_id' not in session:
        return redirect('/logout')
    if request.method == "POST":
        if request.files:
            # get file
            image = request.files["image"]
            # check that file name is not empty
            if image.filename == '':
                flash("Image must have a file name")
                return redirect("/getoutside/athlete/update") 
            # # check if file size is allowed
            # if not allowed_image_filesize(request.cookies.get("filesize")):
            #     flash("File exceeded maximum size")
            #     return redirect("/getoutside/athlete/update")

            # check for allowed file extension type
            if not allowed_image(image.filename):
                flash("That image extension is not allowed")
                return redirect("/getoutside/athlete/update") 
            # sanitize image
            else:
                filename = secure_filename(image.filename)
            # save file
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            # SQL to save file name
            data ={
                'id': session['user_id'],
                'image_file': image.filename
            }
            User.update_user_image(data)
            # return to profile page on success
            return redirect("/getoutside/athlete") 
    return redirect("/getoutside/athlete/update") 
