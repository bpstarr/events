from pymysql import connect
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask import flash,session
import re,os

bcrypy = Bcrypt(app)

class User():
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.user_picture = data['user_picture']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod 
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('events').query_db(query)

        users = []

        for user in results:
            users.append(cls(user))
        return user
    
    @classmethod 
    def add_user(user,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(hashed_pw)s);"
        return connectToMySQL('events').query_db(query,data)
    
    @classmethod
    def show_single_user(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('events').query_db(query,data)
        user = cls(results[0])
        print(user)
        return user

    @classmethod
    def user_validator(cls,data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
        is_valid = True
        if len(data['first_name']) <2:
            flash('First name needs to be at least two characters', category = 'error')
            is_valid = False
        if len(data['last_name']) <2:
            flash('Last name needs to be at least two characters',category = 'error')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Email is invalid. Please try again.',category = 'error')
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash('Password needs a minimum of eight characters,at least one letter,at least one number and at least one special character',category = 'error')
            is_valid = False
        if not PASSWORD_REGEX.match(data['verify_password']):
            flash('Password needs a minimum of eight characters,at least one letter,at least one number and at least one special character',category = 'error')
            is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('events').query_db(query,data)
        if len(results) != 0:
            flash('Email already exists.Please try logging in',category = 'error')
            is_valid = False
        if data['password'] != data['verify_password']:
            flash('Passwords must match. Please try again.',category = 'error')
            is_valid = False
        return is_valid

    @classmethod 
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('events').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod 
    def edit_user(cls,data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
        results = connectToMySQL('events').query_db(query,data)
        print(results)
        return results

    @classmethod
    def change_profile_picture(cls,data):
        query = "UPDATE users SET user_picture = %(user_picture)s WHERE id = %(id)s;"
        results = connectToMySQL('events').query_db(query,data)
        print(results)
        return results

    @classmethod
    def destroy_user(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
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
    def put_on_fk_restraint(cls):
        query = "SET FOREIGN_KEY_CHECKS = 1;"
        results = connectToMySQL('events').query_db(query)
        print(results)
        return results
    
    @classmethod
    def user_update_validator(cls,data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2:
            flash('First name needs to be at least two characters',category = 'error')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last name needs to be at least two characters', category = 'error')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Email is invalid. Please try again.', category = 'error')
            is_valid = False
        user_query = "SELECT * FROM users WHERE id = %(id)s;"
        user_result = connectToMySQL('events').query_db(user_query,data)
        user = cls(user_result[0])
        print(user)
        if data['email'] != session['user_email']:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            results = connectToMySQL('events').query_db(query,data)
            if len(results) !=0:
                flash('Email already exists.Please try logging in.',category = 'error')
                is_valid = False
        return is_valid
    @classmethod
    def edit_profile_validator_pics(cls,data):
        is_valid = True
        EXT = {'.jpeg','.jpg','.png'}
        root_ext = os.path.splitext(data['user_picture'])
        if root_ext[1] not in EXT:
            flash('file type must be jpg,jpeg or png.', category = 'error')
            is_valid = False
        return is_valid

    @classmethod
    def get_users_and_attendance_status_attending(cls,data):
        query = "SELECT * FROM users LEFT JOIN attendance ON users.id = attendance.user_id WHERE attendance.attending = 'attending' and attendance.event_id = %(event_id)s"
        results = connectToMySQL('events').query_db(query,data)
        list = []

        for object in results:
            user_data = {
                'id': object['id'],
                'first_name': object['first_name'],
                'last_name' :object['last_name'],
                'email':object['email'],
                'password' : object['password'],
                'user_picture' : object['user_picture'],
                'created_at': object['created_at'],
                'updated_at' : object['updated_at'],
                'id':object['attendance.id'],
                'attendance': object['attending'],
                'user_id':object['user_id'],
                'event_id':object['event_id']
            }
            t = cls(object)
            t.creator = User(user_data)
            list.append(t)
        return list

    @classmethod
    def get_users_and_attendance_status_not_attending(cls,data):
        query = "SELECT * FROM users LEFT JOIN attendance ON users.id = attendance.user_id WHERE attendance.attending = 'not attending' AND event_id = %(event_id)s"
        results = connectToMySQL('events').query_db(query,data)
        list = []

        for object in results:
            user_data = {
                'id': object['id'],
                'first_name': object['first_name'],
                'last_name' :object['last_name'],
                'email' :object['email'],
                'password' : object['password'],
                'user_picture' : object['user_picture'],
                'created_at': object['created_at'],
                'updated_at' : object['updated_at'],
                'id':object['attendance.id'],
                'attending': object['attending'],
                'user_id':object['user_id'],
                'event_id':object['event_id']
            }
            t = cls(object)
            t.creator = User(user_data)
            list.append(t)
        return list

    @classmethod
    def get_users_and_attendance_status_maybe_attending(cls,data):
        query = "SELECT * FROM users LEFT JOIN attendance ON users.id = attendance.user_id WHERE attendance.attending = 'maybe' AND event_id = %(event_id)s"
        results = connectToMySQL('events').query_db(query,data)
        list = []

        for object in results:
            user_data = {
                'id': object['id'],
                'first_name': object['first_name'],
                'last_name' :object['last_name'],
                'email':object['email'],
                'password' : object['password'],
                'user_picture' : object['user_picture'],
                'created_at': object['created_at'],
                'updated_at' : object['updated_at'],
                'id':object['attendance.id'],
                'attending': object['attending'],
                'user_id':object['user_id'],
                'event_id':object['event_id']
            }
            t = cls(object)
            t.creator = User(user_data)
            list.append(t)
        return list

    