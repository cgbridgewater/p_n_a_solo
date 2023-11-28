from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import activities
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


### USER CLASS
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.image_file = data['image_file']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.friend = None
        self.activities_list = []


### REGISTRATION VALIDATIONS (uiController)
    @staticmethod
    def registration_validation_check(user):
        is_valid = True 
        if len(user['first_name']) < 3:
            flash("First Name must be at least 3 characters!", "firstName")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last Name must be at least 3 characters!", "lastName")
            is_valid = False
        if len(user['password']) < 3:
            flash("Password must be a valid password!", "password")
            is_valid = False
        if len(user['confirm_password']) < 1:
            flash("Passwords must match!", "confirm")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords must match!", "confirm")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email address invalid!", "email")
            is_valid = False
        if User.check_for_email_exists(user):
            flash("This email is already taken!", "email")
            is_valid = False
        return is_valid


### LOGIN VALIDATIONS (uiController)
    @staticmethod
    def login_validation_check(user):
        is_valid = True
        if len(user['email']) < 3:
            flash("Email must be a valid email.", "login")
            is_valid = False
        if len(user['password']) < 3:
            flash("Password must be a valid password.", "login")
            is_valid = False
        return is_valid


### UPDATE VALIDATIONS (usersController)
    @staticmethod
    def update_validation_check(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("Must be at least 3 charactors long.", "update_first_name")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Must be at least 3 charactors long.", "update_last_name")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email!", "update_email")
            is_valid = False
        return is_valid


### CHECK FOR EXISTING EMAIL (uiController)
    @classmethod 
    def check_for_email_exists(cls,data):
        query = """
        SELECT * 
        FROM users 
        WHERE email = %(email)s;
        """
        result = connectToMySQL("test_app").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])


### CREATE AND SAVE NEW USER (uiController)
    @classmethod
    def create_user(cls,data):
        query = """
        INSERT INTO users (first_name, last_name, email, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s );
        """
        return connectToMySQL('test_app').query_db(query,data)


### GET USER BY ID (usersController + Activities)
    @classmethod
    def get_user_by_id_with_activities(cls,data):
        query = """
        SELECT * 
        FROM users 
        JOIN activities ON users.id = activities.user_id
        WHERE activities.user_id = %(id)s;
        """
        results = connectToMySQL('test_app').query_db(query,data)
        one_user = cls(results[0])
        for row in results:
                activity =  ({
                "id": row['activities.id'],
                "activity": row['activity'],
                "date": row['date'],
                "location": row['location'],
                "created_at": row['activities.created_at'],
                "updated_at": row['activities.updated_at'],
            })
        one_user.activities_list.append(activities.Activity(activity))
        return one_user


### GET USER BY ID (usersController + Activities)
    @classmethod
    def get_user_by_id(cls,data):
        query = """
        SELECT * 
        FROM users 
        WHERE id = %(id)s;
        """
        result = connectToMySQL('test_app').query_db(query,data)
        if len(result) == 0:
            return None
        else:
            return cls(result[0])


### DELETE USER BY ID (usersController)
    @classmethod
    def delete_user(cls,data):
        query = """
        DELETE FROM users 
        WHERE id = %(id)s;
        """
        print("Deleted!!!")
        return connectToMySQL('test_app').query_db(query,data) 


### UPDATE USER BY ID (usersController)
    @classmethod
    def update_user_by_id(cls,data):
        query = """
        UPDATE users 
        SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s 
        WHERE id = %(id)s;
        """
        return connectToMySQL('test_app').query_db(query,data)


### GET ALL USERS EXCLUDING LOGGED IN (usersController)
    @classmethod
    def get_all_users_excluding_logged_in_user(cls,data):
        query = """
        SELECT * 
        FROM users 
        WHERE id <> %(id)s 
        ORDER BY users.first_name;
        """
        results = connectToMySQL('test_app').query_db(query,data)
        users = []
        for i in results:
            users.append(cls(i))
        return users


#### FOLLOW USER (usersConrtoller)
    @classmethod
    def follow_user(cls,data): 
        query = """
            INSERT INTO friends(user_id, friend_id)
            VALUES (%(user_id)s, %(friend_id)s);
            """
        connectToMySQL('test_app').query_db(query,data)


### UNFOLLOW USER (usersController)
    @classmethod
    def unfollow_user(cls,data):  
        query = """
            DELETE FROM friends 
            WHERE user_id = %(user_id)s AND friend_id = %(friend_id)s;
            """
        connectToMySQL('test_app').query_db(query,data)


    ### GET ALL USERS FOLLERS (usersController)
    @classmethod
    def all_followers(cls,data):
        query = """
            SELECT *
            FROM users
            JOIN friends ON friends.user_id = users.id
            JOIN users AS friends_made ON friends.friend_id = friends_made.id
            WHERE users.id = %(id)s 
            ORDER BY friends_made.first_name
        """
        results = connectToMySQL('test_app').query_db(query,data)
        user_and_friends = []
        for row in results:
            user = cls(row)
            user.friend = cls({
                "id": row['friends_made.id'],
                "first_name": row['friends_made.first_name'],
                "last_name": row['friends_made.last_name'],
                "image_file": row['friends_made.image_file'],
                "email": row['friends_made.email'],
                "password": row['friends_made.password'],
                "created_at": row['friends_made.created_at'],
                "updated_at": row['friends_made.updated_at'],
            })
            user_and_friends.append(user)
        return user_and_friends


### UPDATE USER IMAGE BY ID (usersController)
    @classmethod
    def update_user_image(cls,data):
        query = """
        UPDATE users 
        SET image_file = %(image_file)s
        WHERE id = %(id)s;
        """
        return connectToMySQL('test_app').query_db(query,data)
