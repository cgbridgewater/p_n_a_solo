from flask_app import app
from flask import render_template, request, redirect, session, flash, url_for
from flask_app.models.users import User
from flask_app.models.activities import Activity
from flask_app.models.comments import Comment
import os
from werkzeug.utils import secure_filename



### ATHLETE DASHBOARD
@app.route('/getoutside/myprofile')
def user_dashboard():
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("user_profile.html", user = User.get_user_by_id(data), activities = Activity.get_all_activities(), joined = Activity.get_all_activities_and_attendees(data), followers = User.all_followers(data), counts = Activity.get_all_activities_by_user_id(data), all_joined = Activity.get_all_events_attending_by_user_with_id(data), comments = Comment.get_all_comments())


### UPDATE ATHLETE FORM (protected)
@app.route('/getoutside/myprofile/edit')
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
@app.route('/getoutside/myprofile/edit', methods =['POST'])
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
        return redirect('/getoutside/myprofile/edit')
    User.update_user_by_id(data)
    return redirect("/getoutside/myprofile") 


### ATHLETUS DELETUS (protected)
@app.route('/getoutside/myprofile/delete')
def delete_user_route():
    if 'user_id' not in session:
        print("ERROR 1!!")
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user_check = User.get_user_by_id(data)
    if session['user_id'] != user_check.id:
        return redirect('/logout')
    print("ERROR 2!!")
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
    logged_user ={
        'id': session['user_id']
    }
    return render_template("user_one_view.html", user = User.get_user_by_id(data), activities = Activity.get_all_activities(), joined = Activity.get_all_events_attending_by_user_with_id(data), followers = User.all_followers(logged_user), counts = Activity.get_all_activities_by_user_id(data), comments = Comment.get_all_comments())


### FOLLOW FRIEND /RETURN TO FRIEND SEARCH
@app.route('/getoutside/athlete/<int:id>/follow')
def follow_user_return_to_search(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'friend_id' : id,
        'user_id' : session['user_id']
    }
    User.follow_user(data)
    return redirect("/getoutside/friends")

### FOLLOW FRIEND / RETURN TO USER BY ID
@app.route('/getoutside/athlete/<int:id>/followbyid')
def follow_user_return_to_userbyid(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'friend_id' : id,
        'user_id' : session['user_id']
    }
    User.follow_user(data)
    return redirect(f"/getoutside/athlete/{id}")


### UNFOLLOW FRIEND / RETURN TO FIND FRIEND
@app.route('/getoutside/athlete/<int:id>/unfollow')
def unfollow_user_return_to_search(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'friend_id' : id,
        'user_id' : session['user_id']
    }
    User.unfollow_user(data)
    return redirect("/getoutside/friends")

### UNFOLLOW FRIEND / RETURN TO USER BY ID
@app.route('/getoutside/athlete/<int:id>/unfollowbyid')
def unfollow_user_return_to_userbyid(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'friend_id' : id,
        'user_id' : session['user_id']
    }
    User.unfollow_user(data)
    return redirect(f"/getoutside/athlete/{id}")

### UNFOLLOW FRIEND / RETURN TO USER BY ID
@app.route('/getoutside/athlete/<int:id>/unfollowing')
def unfollow_user_return_to_profile(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'friend_id' : id,
        'user_id' : session['user_id']
    }
    User.unfollow_user(data)
    return redirect(f"/getoutside/myprofile")


### FRIEND SEARCH SINGLE PAGE FORM/RESULTS
@app.route('/getoutside/friends')
def friend_search_page():
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("friends_search.html", allusers = User.get_all_users_excluding_logged_in_user(data), followers = User.all_followers(data)) 


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
                flash("Image must have a file name", "image")
                return redirect("/getoutside/myprofile/edit") 
            # # check if file size is allowed
            # if not allowed_image_filesize(request.cookies.get("filesize")):
            #     flash("File exceeded maximum size", "image")
            #     return redirect("/getoutside/myprofile/edit")

            # check for allowed file extension type
            if not allowed_image(image.filename):
                flash("That image extension is not allowed", "image")
                return redirect("/getoutside/myprofile/edit") 
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
            return redirect("/getoutside/myprofile") 
    return redirect("/getoutside/myprofile/edit") 
