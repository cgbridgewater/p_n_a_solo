from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



### REDIRECT TO DOMAIN CONTROL ROUTE
@app.route('/')
def index():
    return redirect("/getoutside")


### REGISTER FORM 
@app.route('/getoutside/register')
def register_page():
    return render_template("register.html")


### TO REGISTRATION PAGE
@app.route("/getoutside/toregister")
def redirect_to_landing():
    session.clear()
    return redirect("/getoutside")


### TO LOGIN PAGE
@app.route("/getoutside/tologin")
def redirect_to_login():
    session.clear()
    return redirect("/getoutside/login")


### REGISTRATION FORM POST ACTION
@app.route('/getoutside/register', methods= ['POST'])
def register():
    if not User.registration_validation_check(request.form):
        session["first_name"] = request.form["first_name"]
        session["last_name"] = request.form["last_name"]
        session["email"] = request.form["email"]
        return redirect('/getoutside/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.create_user(data)
    session.pop("first_name", None)
    session.pop("last_name", None)
    session.pop("email", None)
    session['user_id'] = user_id
    return redirect("/getoutside/myprofile")


### LOGIN FORM 
@app.route('/getoutside/login')
def login_page():
    return render_template("login.html")


### LOGIN FORM POST ACTION
@app.route('/getoutside/login', methods= ['POST'])
def login():
    session["email2"] = request.form["email"]
    data = { "email" : request.form["email"] }
    user_in_db = User.check_for_email_exists(data)
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/getoutside/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect("/getoutside/login")
    if not User.login_validation_check(request.form):
        return redirect('/getoutside/login')
    session["user_id"] = user_in_db.id
    session.pop("email2", None)
    return redirect("/getoutside/myprofile")


### ROUTE FOR LOGOUT 
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/getoutside/login")


### CATCH ALL DINO GAME
@app.route('/', defaults = {'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("catch_all_dinosaur.html")