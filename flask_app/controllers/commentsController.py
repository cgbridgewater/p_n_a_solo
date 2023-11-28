from flask_app import app
from flask import redirect, session, request
from flask_app.models.comments import Comment
# from flask_app.models.activities import Activity


### NEW ACTIVITY POST ACTION 
@app.route('/getoutside/activities/<int:id>/comment', methods=["POST"])
def comment_form_action(id):
    if 'user_id' not in session:
        msg = "you must be logged in!"
        return redirect('/logout')
    data = {
        "activity_id" : id,
        "text" : request.form["text"],
        "commenter" : request.form["commenter"],
        }
    if not Comment.comment_validation_check(data):
        return redirect(f'/getoutside/activity/{id}#comments') 
    Comment.create_comment(data)
    return redirect(f'/getoutside/activity/{id}#comments')