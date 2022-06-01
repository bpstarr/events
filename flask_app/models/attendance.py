from sqlite3 import connect
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash,session

class Attendance():
    def __init__(self,data):
        self.id = data['id']
        self.attending = data['attending']
        self.user_id = data['user_id']
        self.event_id = data['event_id']

    @classmethod
    def show_attendance_by_user_id_and_event_id(cls,data):
        query = "SELECT * FROM attendance WHERE user_id = %(id)s AND event_id = %(event_id)s;"
        results = connectToMySQL('events').query_db(query,data)
        if len(results) < 1:
            return None
        else:
            status = cls(results[0])
            print(status)
            return status
    @classmethod
    def show_all_attendance_by_event_id(cls,data):
        query = "SELECT * FROM attendance WHERE event_id = %(event_id)s;"
        results = connectToMySQL('events').query_db(query,data)

        all_attendance = []

        for attending in results:
            all_attendance.append(attending)
        return all_attendance

    @classmethod
    def add_attendance(cls,data):
        query = 'INSERT INTO attendance(attending, user_id, event_id) VALUES(%(attending_status)s,%(user_id)s, %(event_id)s);'
        results = connectToMySQL('events').query_db(query,data)
        print(results)
        return results

    @classmethod 
    def change_attendance(cls,data):
        query = "UPDATE attendance SET attending = %(attending_status)s WHERE event_id = %(event_id)s AND user_id = %(user_id)s;"
        results = connectToMySQL('events').query_db(query,data)
        print(results)
        return results

    @classmethod 
    def destroy_event_attendance(cls,data):
        query = "DELETE FROM attendance WHERE event_id =%(event_id)s;"
        results = connectToMySQL('events').query_db(query,data)
        print(results)
        return results

    @classmethod
    def destroy_event_attendance_by_user_id(cls,data):
        query = "DELETE FROM attendance WHERE user_id = %(id)s"
        results = connectToMySQL('events').query_db(query,data)
        print(results)
        return results
        


    

