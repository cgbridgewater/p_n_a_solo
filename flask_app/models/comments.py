from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import datetime

### COMMMENT CLASS
class Comment:
    def __init__(self,data):
        self.id = data['id']
        self.text = data['text']
        self.commenter = data['commenter']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


### VALIDATE COMMENT
    @staticmethod
    def comment_validation_check(comment):
        is_valid = True
        if len(comment['text']) < 3:
            flash("Minimum 3 charactors required", "comment")
            is_valid = False
        return is_valid 


### CREATE COMMENT FORM ACTION
    @classmethod
    def create_comment(cls,data):
        query = """
            INSERT INTO comments (activity_id, text, commenter)
            VALUES (%(activity_id)s, %(text)s, %(commenter)s)
        """
        return connectToMySQL('test_app').query_db(query,data)


### GET COMMENTS BY ACTIVITY ID
    @classmethod
    def get_comments_by_activity_id(cls,data):
        query = """
            SELECT * FROM comments WHERE activity_id = %(id)s;
        """
        result = connectToMySQL("test_app").query_db(query,data)
        all_comments = []
        for row in result:
            one_comment = cls({
                "id": row['id'],
                "activity_id": row['activity_id'],
                "commenter" : row['commenter'],
                "text" : row['text'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
            })
            all_comments.append(one_comment)
        return all_comments


### GET ALL COMMENTS
    @classmethod
    def get_all_comments(cls):
        query = """
            SELECT * FROM comments;
        """
        result = connectToMySQL("test_app").query_db(query)
        all_comments = []
        for row in result:
            one_comment = cls({
                "id": row['id'],
                "activity_id": row['activity_id'],
                "commenter" : row['commenter'],
                "text" : row['text'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
            })
            all_comments.append(one_comment)
        return all_comments