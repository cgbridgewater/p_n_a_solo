from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users
from flask import flash
import datetime
from pprint import pprint


### ACTIVITY CLASS
class Activity:
    def __init__(self,data):
        self.id = data['id']
        self.activity = data['activity']
        self.location = data['location']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.attendee = None
        self.attenders = []


### ACTIVITIES FORM VALIDATIONS CHECK (activitiesController)
    @staticmethod
    def activity_validation_check(activity):
        is_valid = True
        try:
            datetime.datetime.strptime(activity['date'], '%Y-%m-%d')
            if datetime.datetime.strptime(activity['date'], '%Y-%m-%d') < datetime.datetime.now():
                flash("Date must be in future", "activity")
                is_valid = False
        except ValueError:
            flash("A date must be provided.", "activity")
            is_valid = False
        if len(activity['location']) < 3:
            flash("Location must be at least 3 charactors", "activity")
            is_valid = False
        if len(activity['activity']) < 1:
            flash("Please select an activity", "activity")
            is_valid = False
        return is_valid 


    ### CREATE ACTIVITY FORM ACTION (activitiesController)
    @classmethod
    def create_activity_form_action(cls,data):
        query = """
            INSERT INTO activities (user_id, activity, location, date)
            VALUES (%(user_id)s, %(activity)s, %(location)s, %(date)s)
        """
        return connectToMySQL('test_app').query_db(query,data)


    ### UPDATE ACTIVITY FORM ACTION (activitiesController)
    @classmethod
    def update_activity_form_action(cls,data):
        query = """
            UPDATE activities 
            SET activity = %(activity)s , location = %(location)s , date = %(date)s 
            WHERE id = %(id)s;
        """
        return connectToMySQL('test_app').query_db(query,data)


    ### GET ACTIVITY BY ID with attendees  (activitiesController)
    @classmethod
    def get_one_activity_by_id_with_attendees(cls,data):
        query = """
            SELECT * FROM activities
            JOIN users AS creator ON activities.user_id = creator.id
            LEFT JOIN join_activity ON activities.id = join_activity.activity_id
            LEFT JOIN users AS attendee ON join_activity.user_id = attendee.id
            WHERE activities.id =  %(id)s;
        """
        results = connectToMySQL('test_app').query_db(query,data)
        pprint(results)
        one_activity = cls(results[0])
        one_activity.creator = users.User({
                "id": results[0]['creator.id'],
                "first_name": results[0]['first_name'],
                "last_name": results[0]['last_name'],
                "email": results[0]['email'],
                "image_file": results[0]['image_file'],
                "password": None,
                "created_at": results[0]['created_at'],
                "updated_at": results[0]['updated_at'],
        })
        for row in results:
                attendee = ({
                "id": row['attendee.id'],
                "first_name": row['attendee.first_name'],
                "last_name": row['attendee.last_name'],
                "image_file": row['attendee.image_file'],
                "email": row['attendee.email'],
                "password": None,
                "created_at": row['attendee.created_at'],
                "updated_at": row['attendee.updated_at'],
            })
                one_activity.attenders.append(users.User(attendee))
        return one_activity


### GET ONE ACTIVITY ID (WORKING)
    @classmethod
    def get_activity_by_id(cls,data):
        query = """SELECT * FROM activities
            LEFT JOIN users AS creator ON activities.user_id = creator.id
            WHERE activities.id = %(id)s;"""
        result = connectToMySQL('test_app').query_db(query,data)
        pprint(result)
        one_activity = cls(result[0])
        one_activity.creator = users.User({
            "id": result[0]['creator.id'],
            "first_name": result[0]['first_name'],
            "last_name": result[0]['last_name'],
            "image_file": None,
            "email": None,
            "password": None,
            "created_at": result[0]['creator.created_at'],
            "updated_at": result[0]['creator.updated_at'],
        })
        return one_activity



    # ### READ ALL ACTIVITIES + USER  for home page!!               TESTING!!!   THIS IS A HAWT MESS!
    # @classmethod
    # def all_activities_with_joined_attenders(cls,data): #get all activities and the creator WITH ATTENDERS
    #     query = """
    #          SELECT  * FROM activities
    #         JOIN users AS creator on activities.user_id = creator.id
    #         LEFT JOIN join_activity ON activities.id = activity_id
    #         LEFT JOIN users AS attendee ON join_activity.user_id = attendee.id
    #         WHERE date > CURRENT_DATE AND activities.user_id != %(id)s
    #         ORDER BY date ASC;
    #     """
    #     results = connectToMySQL('test_app').query_db(query, data)
    #     pprint(results)
    #     all_activities = []
    #     for row in results:
    #         one_activity = cls(row)
        
    #         one_activity.creator = users.User({
    #             "id": row['id'],
    #             "first_name": row['first_name'],
    #             "last_name": row['last_name'],
    #             "image_file": row['image_file'],
    #             "email": row['email'],
    #             "password": None,
    #             "created_at": row['created_at'],
    #             "updated_at": row['updated_at'],
    #         })
    #         attendee = users.User({
    #             "id": row['attendee.id'],
    #             "first_name": row['attendee.first_name'],
    #             "last_name": row['attendee.last_name'],
    #             "image_file": row['attendee.image_file'],
    #             "email": row['attendee.email'],
    #             "password": None,
    #             "created_at": row['attendee.created_at'],
    #             "updated_at": row['attendee.updated_at'],
    #         })
    #         all_activities.append(one_activity)
    #         one_activity.attenders.append(attendee)
    #     return all_activities





    # ### READ ALL ACTIVITIES + USER  for home page!!               TESTING!!!   THIS IS A HAWT MESS!
    # @classmethod
    # def all_activities_with_joined_attenders(cls,data): #get all activities and the creator WITH ATTENDERS
    #     query = """
    #          SELECT  * FROM activities
    #         JOIN users AS creator on activities.user_id = creator.id
    #         LEFT JOIN join_activity ON activities.id = activity_id
    #         LEFT JOIN users AS attendee ON join_activity.user_id = attendee.id
    #         WHERE date > CURRENT_DATE AND activities.user_id != %(id)s
    #         ORDER BY date ASC;
    #     """
    #     results = connectToMySQL('test_app').query_db(query, data)
    #     pprint(results)
    #     pprint("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    #     all_activities = []
    #     pprint("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
    #     for row in results:
    #         one_activity = cls(row) 
    #         one_activity.creator = users.User({
    #             "id": row['creator.id'],
    #             "first_name": row['first_name'],
    #             "last_name": row['last_name'],
    #             "image_file": row['image_file'],
    #             "email": row['email'],
    #             "password": None,
    #             "created_at": row['creator.created_at'],
    #             "updated_at": row['creator.updated_at'],
    #         })
    #         attendee = ({
    #             "id": row['attendee.id'],
    #             "first_name": row['attendee.first_name'],
    #             "last_name": row['attendee.last_name'],
    #             "image_file": row['attendee.image_file'],
    #             "email": row['attendee.email'],
    #             "password": None,
    #             "created_at": row['attendee.created_at'],
    #             "updated_at": row['attendee.updated_at'],
    #         })
    #         all_activities.append(one_activity)
    #         one_activity.attenders.append(users.User(attendee))
    #     return all_activities


    ### GET ALL ACTIVITIES AND ATTENDEES (usersController)
    @classmethod
    def get_all_activities_and_attendees(cls,data):
        query = """
        SELECT * FROM users AS creator
        JOIN activities ON creator.id = activities.user_id
        LEFT JOIN join_activity ON activities.id = activity_id
        WHERE date > DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND join_activity.user_id = %(id)s AND creator.id != %(id)s ORDER BY date ASC;
        """
        results = connectToMySQL('test_app').query_db(query, data)
        pprint(results)
        all_activities = []
        for row in results:
            one_activity = cls({
                "id": row['activities.id'],
                "activity" : row['activity'],
                "location" : row['location'],
                "date" : row['date'],    
                "created_at" : row['activities.created_at'],
                "updated_at" : row['activities.updated_at'],
            })
            one_activity.creator = users.User({
                "id": row['user_id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "image_file": row['image_file'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at'],
            })
            all_activities.append(one_activity)
        return all_activities


    ### GET ALL ACTIVITIES WITH CREATOR (usersController)
    @classmethod
    def get_all_activities(cls):
        query = """
            SELECT activities.id, activities.created_at, activities.updated_at, activity, location, date, 
            users.id as user_id, first_name, last_name, email, password, image_file, users.created_at as uc, users.updated_at as uu
            FROM activities
            JOIN users on users.id = activities.user_id
            WHERE date > DATE_SUB(CURDATE(), INTERVAL 1 DAY) ORDER BY date ASC;
        """
        results = connectToMySQL('test_app').query_db(query)
        pprint(results)
        all_activities = []
        for row in results:
            one_activity = cls(row)
            one_activity.creator = users.User({
                "id": row['user_id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "image_file": row['image_file'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['uc'],
                "updated_at": row['uu'],
            })
            all_activities.append(one_activity)
        return all_activities


#### JOIN (activitiesController)
    @classmethod
    def attend_activity(cls,data):
        query = """
            INSERT INTO join_activity (user_id, activity_id)
            VALUES (%(user_id)s, %(activity_id)s);
            """
        connectToMySQL('test_app').query_db(query,data)


### UNATTEND (activitiesController)
    @classmethod
    def unattend_activity(cls,data):
        query = """
            DELETE FROM join_activity 
            WHERE user_id = %(user_id)s 
            AND activity_id = %(activity_id)s;
            """
        connectToMySQL('test_app').query_db(query,data)



    ### DELETE ACTIVITY BY ID   (activitiesController)
    @classmethod
    def delete_activity_by_id(cls,data):
        query = """
            DELETE FROM activities 
            WHERE id = %(id)s;
        """
        return connectToMySQL('test_app').query_db(query,data) 


### GET ALL ATTENDIES TO EVENT  (activitiesController)
    @classmethod
    def get_all_attendees(cls, data):
        query = """
            SELECT * FROM join_activity
            JOIN users ON join_activity.user_id = users.id
            WHERE join_activity.activity_id =  %(id)s;
        """
        results = connectToMySQL("test_app").query_db(query, data)
        pprint(results)
        all_attendees = [] 
        for row in results:
            one_attendee = (row)
            one_attendee = users.User({
                "id": row['user_id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "image_file": row['image_file'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at'],
            })
            all_attendees.append(one_attendee)
        return all_attendees



############################################## CUT LINE ############################################################

################################################### TESTING

#    ### READ ONE ACTIVITy + USERs JOINED  for view one page             TESTING!!! 
#     @classmethod
#     def all_users_joined_by_activity_id(cls,data): #get all activities and the creator
#         query = """
#            SELECT * FROM activities
#             JOIN users as creator ON activities.user_id = creator.id
# 			LEFT JOIN  join_activity ON join_activity.activity_id = activities.id
#             LEFT JOIN users AS joiners ON join_activity.user_id = joiners.id
#             WHERE activities.id =  %(id)s;
#         """
#         results = connectToMySQL('test_app').query_db(query, data)
#         pprint(results)
#         all_activities = [] # empty array to fill with each activity
#         for row in results:# Create a Activity class instance from the information from each db row
#             one_activity = cls({
#                 "id": row['id'],
#                 "activity" : row['activity'],
#                 "location" : row['location'],
#                 "date" : row['date'],    
#                 "created_at" : row['created_at'],
#                 "updated_at" : row['updated_at'],
#             })
#             one_activity.creator = users.User({
#                 "id": row['creator.id'],
#                 "first_name": row['first_name'],
#                 "last_name": row['last_name'],
#                 "image_file": row['image_file'],
#                 "email": row['email'],
#                 "password": None,
#                 "created_at": row['creator.created_at'],
#                 "updated_at": row['creator.updated_at'],
#             })
#             one_activity.joiners = users.User({
#                 "id": row['joiners.id'],
#                 "first_name": row['joiners.first_name'],
#                 "last_name": row['joiners.last_name'],
#                 "image_file": row['joiners.image_file'],
#                 "email": row['joiners.email'],
#                 "password": None,
#                 "created_at": row['joiners.created_at'],
#                 "updated_at": row['joiners.updated_at'],
#             })
#             all_activities.append(one_activity)### Append the activity and creator to the array
#         return all_activities

























    # ###Get activity by id                     (testing)
    # @classmethod
    # def get_one_activity(cls,data):
    #     query = """
    #         SELECT * FROM activities WHERE id = %(id)s;
    #     """
    #     result = connectToMySQL('test_app').query_db(query,data)
    #     print(result)
    #     if len(result) == 0: #if no activities found, return an empty list
    #         return None
    #     else: # if at least one activity is found
    #         return cls(result[0])




    # @classmethod
    # def all_activities_joined(cls):
    #     query = '''
    #         SELECT * FROM activities 
    #         JOIN users AS creator ON activities.user_id = creator.id
    #         JOIN join_activity ON activities.id = join_activity.activity_id
    #         LEFT JOIN users as joiners ON joiners.id = join_activity.user_id
    #         WHERE date > CURRENT_DATE ORDER BY date ASC;
    #     '''
    #     results = connectToMySQL("test_app").query_db(query)
    #     pprint(results)
    #     all_joined = []
    #     for row in results: # prevents issues if first time join
    #         if len(all_joined) == 0 or all_joined[len(all_joined)-1].id != row['id']:
    #             one_join = cls(row)
    #             creatorData ={
    #                 "id": row['creator.id'],
    #                 "first_name": row['first_name'],
    #                 "last_name": row['last_name'],
    #                 "image_file": row['image_file'],
    #                 "email": row['email'],
    #                 "password": row['password'],
    #                 "created_at": row['creator.created_at'],
    #                 "updated_at": row['creator.updated_at'],
    #                 }
    #             creatorObj = users.User(creatorData)
    #             one_join.creator = creatorObj
    #             if row['join_activity.user_id'] != None:
    #                 joinerData = {
    #                     "id": row['joiners.id'],
    #                     "first_name": row['joiners.first_name'],
    #                     "last_name": row['joiners.last_name'],
    #                     "image_file": row['joiners.image_file'],
    #                     "email": row['joiners.email'],
    #                     "password": row['joiners.password'],
    #                     "created_at": row['joiners.created_at'],
    #                     "updated_at": row['joiners.updated_at'],
    #                     }
    #                 joinerObj = users.User(joinerData)
    #                 one_join.joiners.append(joinerObj)
    #                 one_join.joinerIds.append(joinerObj.id)
    #             all_joined.append(one_join)
    #         else:
    #             joinerData = {
    #                 "id": row['joiners.id'],
    #                 "first_name": row['joiners.first_name'],
    #                 "last_name": row['joiners.last_name'],
    #                 "image_file": row['joiners.image_file'],
    #                 "email": row['joiners.email'],
    #                 "password": row['joiners.password'],
    #                 "created_at": row['joiners.created_at'],
    #                 "updated_at": row['joiners.updated_at'],
    #                 }
    #             joinerObj = users.User(joinerData)
    #             all_joined[len(all_joined)-1].joiners.append(joinerObj)
    #             all_joined[len(all_joined)-1].joinerIds.append(joinerObj.id)
    #     return all_joined










# ### GET ALL JOINED                TESTING!!!
#     @classmethod
#     def get_joined( cls ):
#         query = """
#             SELECT * FROM activities
#             JOIN users as creator on activities.user_id = creator.id
#             LEFT JOIN join_activity ON activities.id = join_activity.activity_id;
#         """
#         results = connectToMySQL("test_app").query_db(query)
#         for row in results:
#             for key in row:
#                 print(key, "\t\t", row[key])
#         allJoined = []
#         for row in results:
#             if len(allJoined) == 0 or allJoined[len(allJoined)-1].id != row["id"]:
#                 oneJoined = cls(row)
#                 if row['creator.id'] != None:
#                     creatorData ={
#                     "id" : row['creator.id'],
#                     "first_name": row['first_name'],
#                     "last_name": row['last_name'],
#                     "image_file": row['image_file'],
#                     "email": row['email'],
#                     "password": row['password'],
#                     "created_at": row['liker.created_at'],
#                     "updated_at": row['liker.updated_at']
#                         }
#                     creatorObj = User(creatorData)
#                     oneJoined.creators.append(creatorObj)
#                     onePost.creators_id.append(creatorObj.id)
#                 allJoined.append(oneJoined)
#             else:
#                 creatorData ={
#                     "id" : row['creator.id'],
#                     "first_name": row['first_name'],
#                     "last_name": row['last_name'],
#                     "image_file": row['image_file'],
#                     "email": row['email'],
#                     "password": row['password'],
#                     "created_at": row['liker.created_at'],
#                     "updated_at": row['liker.updated_at']
#                     }
#                 creatorObj = User(creatorData)
#                 allJoined[len(allJoined)-1].creator.append(creatorObj)
#                 allJoined[len(allJoined)-1].creator_ids.append(creatorObj.id)
#         return allJoined


