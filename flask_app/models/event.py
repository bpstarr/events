from time import strftime
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash,session
from flask_app.models.user import User
import os,re
from datetime import datetime

from flask_app.models.attendance import Attendance   


class Event():
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.type = data['type']
        self.address = data['address']
        self.date_time = data['date_time']
        self.picture = data['picture']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.users_attending_status = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM events;"
        results = connectToMySQL('events').query_db(query)

        events = []

        for event in results:
            events.append((event))
        return events

    @classmethod 
    def get_all_users_and_event_status_by_event_id_attending(cls,data):
        query = "SELECT * FROM events LEFT JOIN users on events.user_id = users.id LEFT JOIN attendance on events.id = attendance.event_id LEFT JOIN users AS users2 ON users.id = attendance.user_id WHERE events.id = %(event_id)s AND attendance.attending = 'attending';"
        results = connectToMySQL('events').query_db(query,data)
        list = []

        for object in results:
            new_status = True
            attendance_user_data = {
                'id': object['users2.id'],
                'first_name':object['users2.first_name'],
                'last_name':object['users2.last_name'],
                'email':object['users2.email'],
                'password':object['users2.email'],
                'user_picture':object['users2.user_picture'],
                'created_at':object['users2.created_at'],
                'updated_at':object['users2.updated_at']
            }
            if len(list) > 0 and list[len(list)-1].id == object['id']:
                list[len(list)-1].users_attending_status.append(User(attendance_user_data))
                new_status = False
            if new_status:
                poster_data = {
                    'id':object['users.id'],
                    'first_name':object['first_name'],
                    'last_name':object['last_name'],
                    'email':object['email'],
                    'password':object['password'],
                    'user_picture':object['user_picture'],
                    'created_at':object['users.created_at'],
                    'updated_at':object['users.updated_at']
                }
            t = cls(object)
            t.creator = User(poster_data)
            if object['users2.id'] is not None:
                t.users_attending_status.append(User(attendance_user_data))
            list.append(t)
        return list

    @classmethod 
    def get_all_users_and_event_status_by_event_id_not_attending(cls,data):
        query = "SELECT * FROM events LEFT JOIN users on events.user_id = users.id LEFT JOIN attendance on events.id = attendance.event_id LEFT JOIN users AS users2 ON users.id = attendance.user_id WHERE events.id = %(event_id)s AND attendance.attending = 'not attending';"
        results = connectToMySQL('events').query_db(query,data)
        list = []

        for object in results:
            new_status = True
            attendance_user_data = {
                'id': object['users2.id'],
                'first_name':object['users2.first_name'],
                'last_name':object['users2.last_name'],
                'email':object['users2.email'],
                'password':object['users2.email'],
                'user_picture':object['users2.user_picture'],
                'created_at':object['users2.created_at'],
                'updated_at':object['users2.updated_at']
            }
            if len(list) > 0 and list[len(list)-1].id == object['id']:
                list[len(list)-1].users_attending_status.append(User(attendance_user_data))
                new_status = False
            if new_status:
                poster_data = {
                    'id':object['users.id'],
                    'first_name':object['first_name'],
                    'last_name':object['last_name'],
                    'email':object['email'],
                    'password':object['password'],
                    'user_picture':object['user_picture'],
                    'created_at':object['users.created_at'],
                    'updated_at':object['users.updated_at']
                }
            t = cls(object)
            t.creator = User(poster_data)
            if object['users2.id'] is not None:
                t.users_attending_status.append(User(attendance_user_data))
            list.append(t)
        return list

    @classmethod 
    def get_all_users_and_event_status_by_event_id_maybe(cls,data):
        query = "SELECT * FROM events LEFT JOIN users on events.user_id = users.id LEFT JOIN attendance on events.id = attendance.event_id LEFT JOIN users AS users2 ON users.id = attendance.user_id WHERE events.id = %(event_id)s AND attendance.attending = 'maybe';"
        results = connectToMySQL('events').query_db(query,data)
        list = []

        for object in results:
            new_status = True
            attendance_user_data = {
                'id': object['users2.id'],
                'first_name':object['users2.first_name'],
                'last_name':object['users2.last_name'],
                'email':object['users2.email'],
                'password':object['users2.email'],
                'user_picture':object['users2.user_picture'],
                'created_at':object['users2.created_at'],
                'updated_at':object['users2.updated_at']
            }
            if len(list) > 0 and list[len(list)-1].id == object['id']:
                list[len(list)-1].users_attending_status.append(User(attendance_user_data))
                new_status = False
            if new_status:
                poster_data = {
                    'id':object['users.id'],
                    'first_name':object['first_name'],
                    'last_name':object['last_name'],
                    'email':object['email'],
                    'password':object['password'],
                    'user_picture':object['user_picture'],
                    'created_at':object['users.created_at'],
                    'updated_at':object['users.updated_at']
                }
            t = cls(object)
            t.creator = User(poster_data)
            if object['users2.id'] is not None:
                t.users_attending_status.append(User(attendance_user_data))
            list.append(t)
        return list

    @classmethod 
    def get_all_users_and_event_status_by_event_id_and_user_id(cls,data):
        query = "SELECT * FROM events LEFT JOIN users on events.user_id = users.id LEFT JOIN attendance on events.id = attendance.event_id LEFT JOIN users AS users2 ON users.id = attendance.user_id WHERE events.id = %(event_id)s AND users.id = %(id)s;"
        results = connectToMySQL('events').query_db(query,data)
        list = []

        for object in results:
            new_status = True
            attendance_user_data = {
                'id': object['users2.id'],
                'first_name':object['users2.first_name'],
                'last_name':object['users2.last_name'],
                'email':object['users2.email'],
                'password':object['users2.email'],
                'user_picture':object['users2.user_picture'],
                'created_at':object['users2.created_at'],
                'updated_at':object['users2.updated_at']
            }
            if len(list) > 0 and list[len(list)-1].id == object['id']:
                list[len(list)-1].users_attending_status.append(User(attendance_user_data))
                new_status = False
            if new_status:
                poster_data = {
                    'id':object['users.id'],
                    'first_name':object['first_name'],
                    'last_name':object['last_name'],
                    'email':object['email'],
                    'password':object['password'],
                    'user_picture':object['user_picture'],
                    'created_at':object['users.created_at'],
                    'updated_at':object['users.updated_at']
                }
            t = cls(object)
            t.creator = User(poster_data)
            if object['users2.id'] is not None:
                t.users_attending_status.append(User(attendance_user_data))
            list.append(t)
        if len(list) > 1:
            return list[0]
        else:
            return None


    @classmethod
    def add_event(cls,data):
        query = "INSERT INTO events (name,description,type,address,date_time,user_id) VALUES (%(name)s,%(description)s,%(type)s,%(address)s,%(date_time)s,%(user_id)s);"
        results = connectToMySQL('events').query_db(query,data)
        print(results)
        return results

    @classmethod 
    def update_profile_picture(cls,data):
        query = "UPDATE events SET picture = %(picture)s WHERE id = %(id)s;"
        results = connectToMySQL('events').query_db(query,data)
        print(results)
        return results
    
    @classmethod
    def take_off_fk_restraint(cls):
        query = "SET FOREIGN_KEY_CHECKS = 0;"
        results = connectToMySQL('events').query_db(query)
        print(results)
        return results

    @classmethod 
    def destroy_event(cls,data):
        query = "DELETE FROM events WHERE id = %(event_id)s;"
        results = connectToMySQL('events').query_db(query,data)
        print(results)
        return results

    @classmethod
    def put_on_fk_restraint(cls):
        query = "SET FOREIGN_KEY_CHECKS = 1;"
        results = connectToMySQL('events').query_db(query)
        print(results)
        return results


    @classmethod
    def edit_event(cls,data):
        query = "UPDATE events SET name = %(name)s, description = %(description)s,type = %(type)s, date_time = %(date_time)s, address = %(address)s WHERE id = %(event_id)s;"
        results = connectToMySQL('events').query_db(query,data)
        print(results)
        return results

    @classmethod
    def edit_image(cls,data):
        query = "UPDATE events SET picture = %(picture)s WHERE id = %(event_id)s;"
        results = connectToMySQL('events').query_db(query,data)
        print(results)
        return results

    @classmethod
    def show_single_event(cls,data):
        query = "SELECT * FROM events where id = %(event_id)s;"
        results = connectToMySQL('events').query_db(query,data)
        event = results[0]
        print(results)
        print(results[0])
        return event

    @classmethod
    def select_by(cls,data):
        query = "SELECT * FROM events WHERE name LIKE %(search)s OR description LIKE %(search)s OR address LIKE %(search)s or date_time LIKE %(search)s;"
        results = connectToMySQL('events').query_db(query,data)
        print(results)
        return results

    @classmethod
    def select_by_type(cls,data):
        query = "SELECT * FROM events WHERE type = %(type)s;"
        results = connectToMySQL('events').query_db(query,data)
        print(results)
        return results

    @classmethod 
    def event_validator(cls,data):
        DATE_REGEX = re.compile(r'(?=\d)^(?:(?!(?:10\D(?:0?[5-9]|1[0-4])\D(?:1582))|(?:0?9\D(?:0?[3-9]|1[0-3])\D(?:1752)))((?:0?[13578]|1[02])|(?:0?[469]|11)(?!\/31)(?!-31)(?!\.31)|(?:0?2(?=.?(?:(?:29.(?!000[04]|(?:(?:1[^0-6]|[2468][^048]|[3579][^26])00))(?:(?:(?:\d\d)(?:[02468][048]|[13579][26])(?!\x20BC))|(?:00(?:42|3[0369]|2[147]|1[258]|09)\x20BC))))))|(?:0?2(?=.(?:(?:\d\D)|(?:[01]\d)|(?:2[0-8])))))([-.\/])(0?[1-9]|[12]\d|3[01])\2(?!0000)((?=(?:00(?:4[0-5]|[0-3]?\d)\x20BC)|(?:\d{4}(?!\x20BC)))\d{4}(?:\x20BC)?)(?:$|(?=\x20\d)\x20))?((?:(?:0?[1-9]|1[012])(?::[0-5]\d){0,2}(?:\x20[aApP][mM]))|(?:[01]\d|2[0-3])(?::[0-5]\d){1,2})?$')
        is_valid = True
        if len(data['name']) < 2:
            flash('Name needs to be at least two characters.',category = 'error')
            is_valid = False
        if len(data['description']) < 2:
            flash('Description needs to be at least two characters.',category = 'error')
            is_valid = False
        if len(data['description']) > 255:
            flash('Description can only be 255 characters.')
            is_valid = False
        if data['type'] == 'Select a type':
            flash('Type needs to be selected.',category = 'error')
            is_valid  = False
        if len(data['address']) < 2:
            flash('Address needs to be at least 2 characters.')
            is_valid = False
        print(data['date_time'])
        if not DATE_REGEX.match(str(data['date_time'])):
            flash('Date and time are in incorrect format. Please try again',category = 'error')
            is_valid = False
        submitted_date_formatted = datetime.strptime(data['date_time'],'%m/%d/%Y %I:%M %p')
        present_time = datetime.now()
        present_time_string = present_time.strftime('%m/%d/%Y %-I:%M %p')
        present_time_formatted = datetime.strptime(present_time_string,'%m/%d/%Y %I:%M %p')
        if submitted_date_formatted < present_time_formatted:
            flash('Date must be in the future',category='error')
            is_valid = False
        return is_valid
    
    @classmethod
    def event_picture_validator(cls,data):
        is_valid = True
        EXT = {'.jpeg','.jpg','.png'}
        root_ext = os.path.splitext(data['picture'])
        if root_ext[1] not in EXT:
            flash('File type must be jpeg,jpg or png.')
        return is_valid
