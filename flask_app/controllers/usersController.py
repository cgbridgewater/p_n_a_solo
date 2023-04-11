from flask_app import app
from flask import render_template, request, redirect, session, flash, url_for
from flask_app.models.users import User
from flask_app.models.activities import Activity


### ATHLETE DASHBOARD
@app.route('/getoutside/athlete')
def user_dashboard():
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    # image_file = url_for('static', filename='profile_pics/' + user.image_file)
    data ={
        'id': session['user_id']
    }
    return render_template("user_dashboard.html", user = User.get_user_by_id(data), image_file = url_for('static', filename='images/profile_pics/' + User.get_user_by_id(data).image_file),activities = Activity.get_all_activities(), joined = Activity.get_all_activities_and_attendees(data), followers = User.all_followers(data))


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


### GET ATHLETE BY ID                 WHY DOESNT THE SINGLE METHOD WORK???
@app.route('/getoutside/athlete/<int:id>')
def get_user_by_id(id):
    data = {
    "id" : id
    }
    return render_template("user_one_view.html", user = User.get_user_by_id(data),activities = Activity.get_all_activities())
    # return render_template("user_one_view.html", user = User.get_user_by_id_with_activities(data))


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



############################################## CUT LINE ############################################################




# ### UPLOAD IMAGE ROUTE
# @app.route("/getoutside/addimage", methods=['POST'])
# def upload_image():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data ={
#         'id': session['user_id']
#     }
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect('/getoutside/athlete/update')
#     file = request.files['file']
#     if file.filename == '':
#         flash('No image selected for uploading')
#         return redirect('/getoutside/athlete/update')
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         #print('upload_image filename: ' + filename)
#         flash('Image successfully uploaded and displayed below')
#         return render_template("user_update.html", user = User.get_user_by_id(data), filename = filename)
#     else:
#         flash('Allowed image types are - png, jpg, jpeg, gif')
#         return redirect('/getoutside/athlete/update')
