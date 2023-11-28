from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models.users import User
from flask_app.models.comments import Comment
from flask_app.models.activities import Activity
from dotenv import load_dotenv
load_dotenv()
import os


###  Landing Page
@app.route('/getoutside')
@app.route('/getoutside/')
def dashboard():
    return render_template("landing_page.html")


###  ACTIVITY DASH BOARD
@app.route('/getoutside/activities')
@app.route('/getoutside/activities/')
def activity_dashboard():
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("activity_dashboard.html", user = User.get_user_by_id(data), activities = Activity.get_all_activities(),attending = Activity.get_all_activities_and_attendees(data))


### NEW ACTIVITY FORM
@app.route('/getoutside/activities/new')
def new_activity_form_page():
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("activity_new_form.html")


### NEW ACTIVITY FORM
@app.route('/getoutside/activities/new2')
def new_activity_form_page_2():
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("activity_new_form_2.html")


### NEW ACTIVITY POST ACTION RETURN TO NEW ACTIVITY CREATED
@app.route('/getoutside/activities/new', methods=["POST"])
def create_activity_form_action():
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    if not Activity.activity_validation_check(request.form):
        session["activity"] = request.form["activity"]
        session["location"] = request.form["location"]
        session["date"] = request.form["date"]
        return redirect('/getoutside/activities/new') 
    new_activity_id = Activity.create_activity_form_action(request.form)
    session.pop("activity", None)
    session.pop("location", None)
    session.pop("date", None)
    return redirect(f"/getoutside/activity/{new_activity_id}") 


### UPDATE ACTIVITY FORM (Protected)
@app.route('/getoutside/activity/<int:id>/edit')
def edit_activity_by_id(id):
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    data = {
        'id': id,
    }
    user ={
        'id': session['user_id']
    }
    activity = Activity.get_activity_by_id(data)
    if session['user_id'] != activity.creator.id:
        return redirect('/logout')
    return render_template("activity_edit_form.html", activity = Activity.get_one_activity_by_id_with_attendees(data))


### POST ACTION ROUTE TO UPDATE ACTIVITY (Protected)
@app.route('/getoutside/activity/<int:id>/edit', methods=["POST"])
def edit_activity_form_action(id):
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    data = {
        "id" : id,
        "activity" : request.form["activity"],
        "location" : request.form["location"],
        "date" : request.form["date"],
        }
    activity = Activity.get_activity_by_id(data)
    if session['user_id'] != activity.creator.id:
        return redirect('/logout')
    if not Activity.activity_validation_check(data):
        return redirect(f'/getoutside/activity/{id}/edit') 
    Activity.update_activity_form_action(data) 
    return redirect(f'/getoutside/activity/{id}') 


### VIEW ONE ACTIVITY BY ID
@app.route('/getoutside/activity/<int:id>')
def view_one_activity_by_id(id):
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    data = {
        'id': id,
    }
    user ={
        'id': session['user_id']
    }
    return render_template("activity_one_view.html", activity = Activity.get_one_activity_by_id_with_attendees(data), user = User.get_user_by_id(user), comments = Comment.get_comments_by_activity_id(data) )


### ATTEND ACTIVITY ROUTE WITH HOMEPAGE RETURN
@app.route('/getoutside/activity/<int:id>/join')
def attend_activity_return_to_home_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'activity_id' : id,
        'user_id' : session['user_id']
    }
    Activity.attend_activity(data)
    return redirect("/getoutside/activities")


### ATTEND ACTIVITY ROUTE WITH ATHLETE DASH RETURN
@app.route('/getoutside/activity/<int:id>/join2')
def attend_activity_return_to_activity_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'activity_id' : id,
        'user_id' : session['user_id']
    }
    Activity.attend_activity(data)
    return redirect(f"/getoutside/activity/{id}")

### ATTEND ACTIVITY ROUTE WITH TO DASHBOARD
@app.route('/getoutside/activity/<int:id>/join3')
def attend_activity_return_to_activity_dash(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'activity_id' : id,
        'user_id' : session['user_id']
    }
    Activity.attend_activity(data)
    return redirect("/getoutside/activities")


### UNATTEND ACTIVITY RETURN TO ACTIVITY PAGE
@app.route('/getoutside/activity/<int:id>/unjoin')
def unattend_activity(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'activity_id' : id,
        'user_id' : session['user_id']
    }
    Activity.unattend_activity(data)
    return redirect(f"/getoutside/activity/{id}")

### UNATTEND ACTIVITY RETURN TO PROFILE PAGE
@app.route('/getoutside/activity/<int:id>/remove')
def remove_activity(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'activity_id' : id,
        'user_id' : session['user_id']
    }
    Activity.unattend_activity(data)
    return redirect(f"/getoutside/myprofile")

### UNATTEND ACTIVITY RETURN TO ACTIVITY DASHBOARD
@app.route('/getoutside/activity/<int:id>/un-join')
def remove_activity_to_dashboard(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'activity_id' : id,
        'user_id' : session['user_id']
    }
    Activity.unattend_activity(data)
    return redirect(f"/getoutside/activities")


### DELETE ACTIVITY BY ID (Protected)
@app.route('/getoutside/activity/<int:id>/delete')
def delete_activity_by_id(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : id,
    }
    activity = Activity.get_activity_by_id(data)
    if session['user_id'] != activity.creator.id:
        return redirect('/logout')
    Activity.delete_activity_by_id(data)
    return redirect("/getoutside/myprofile")