import mimetypes
from flask import Blueprint, jsonify, render_template, request,redirect,session,flash,url_for
from urllib3 import HTTPResponse
from flask_app import app
from PIL import Image
from flask_app.models.event import Event
from flask_app.models.user import User
from flask_app.models.attendance import Attendance
from flask_app import ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
import os,json


def allowed_file(pics):
    return '.' in pics and \
        pics.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/event')
def show_add_events():
    profile_pics = url_for('static', filename = 'profile_pics/')
    if 'user_id' in session:
        data = {
            'id':session['user_id']
        }
        return render_template('event.html',user = User.show_single_user(data),profile_pics= profile_pics)
    else: 
        return redirect('/')

@app.route('/add_event', methods = ['POST'])
def add_event():
    if 'user_id' not in session:
        return redirect('/logout')   
    data = {
        'name':request.form['name'],
        'description':request.form['description'],
        'type':request.form['type'],
        'address':request.form['address'],
        'date_time':request.form['date_time'],
        'user_id':session['user_id'],
        }
    valid = Event.event_validator(data)
    if valid:
        print('Event successfully added')
        Event.add_event(data)
        print(data['user_id'])
        flash('Event Successfully Added', category = 'success')
        return redirect('/dashboard')
    return redirect('/event')

@app.route('/show_event/<int:id>')
def show_single_event_page(id):
    profile_pics = url_for('static', filename = 'profile_pics/')
    event_image_file = url_for('static', filename = 'event_pics/')
    event_data = {
            'event_id':id
        }
    if 'user_id' in session:
        user_data = {
            'id':session['user_id'],
        }
        user_and_event_data = {
            'id': session['user_id'],
            'event_id': id
        }
        return render_template('show_single_event.html',user = User.show_single_user(user_data),event_image_file = event_image_file,events = Event.show_single_event(event_data),profile_pics = profile_pics,attending = User.get_users_and_attendance_status_attending(event_data),not_attending = User.get_users_and_attendance_status_not_attending(event_data),maybe_attending = User.get_users_and_attendance_status_maybe_attending(event_data),show_single_user = Event.get_all_users_and_event_status_by_event_id_and_user_id(user_and_event_data), attending_status = Attendance.show_attendance_by_user_id_and_event_id(user_and_event_data))

    else:
        event_data = {
            'event_id':id
        }
        return render_template('show_single_event.html',event_image_file = event_image_file,events = Event.show_single_event(event_data), profile_pics = profile_pics,attending = User.get_users_and_attendance_status_attending(event_data),not_attending = User.get_users_and_attendance_status_not_attending(event_data),maybe_attending = User.get_users_and_attendance_status_maybe_attending(event_data))

@app.route('/add_attending_status', methods = ['post'])
def add_attending_status():
    if 'user_id' not in session:
        data = request.form['event_id']
        print(data)
        flash('please login to change attendance status', category = 'error')
        return redirect(f'/show_event/{data}')
    profile_pics = url_for('static', filename = 'profile_pics/')

    data = {
        'event_id':request.form['event_id'],
        'user_id':session['user_id'],
        'attending_status':request.form['attending_status']
    }
    
    event_data = {
        'event_id':request.form['event_id']
    }

    user_data = {
        'id':session['user_id']
    }
    user_and_event_data = {
        'event_id':request.form['event_id'],
        'id':session['user_id']
    }
    print(data)
    user = User.show_single_user(user_data)
    print(user)
    Attendance.add_attendance(data)
    return jsonify({'data' : render_template('add_attending_status.html',events = Event.show_single_event(event_data), profile_pics = profile_pics,attending = User.get_users_and_attendance_status_attending(event_data),not_attending = User.get_users_and_attendance_status_not_attending(event_data),maybe_attending = User.get_users_and_attendance_status_maybe_attending(event_data),attending_status = Attendance.show_attendance_by_user_id_and_event_id(user_and_event_data))})

@app.route('/change_attending_status', methods = ['POST'])
def change_attending_status():
    print('start')
    if 'user_id' not in session:
        flash('please login to change attendance status', category = 'error')
        return redirect('/show_event/<int:id>')
    profile_pics = url_for('static', filename = 'profile_pics/')

    data = {
        'event_id':request.form['event_id'],
        'user_id':session['user_id'],
        'attending_status':request.form['attending_status']
    }

    event_data = {
        'event_id':request.form['event_id']
    }

    user_data = {
        'id':session['user_id']
    }
    print(data)
    user = User.show_single_user(user_data)
    print(user)
    Attendance.change_attendance(data)
    return jsonify({'data' : render_template('update_attending_status.html',events = Event.show_single_event(event_data), profile_pics = profile_pics,attending = User.get_users_and_attendance_status_attending(event_data),not_attending = User.get_users_and_attendance_status_not_attending(event_data),maybe_attending = User.get_users_and_attendance_status_maybe_attending(event_data))})
    

@app.route('/show_by_all',methods = ['POST'])
def get_by_all():
    events = Event.get_all()
    event_image_file = url_for('static', filename = 'event_pics/')

    return jsonify({'data': render_template('event_change_ajax.html',events = events,event_image_file = event_image_file)})

@app.route('/show_by_type',methods = ['POST'])
def get_by_type():
    data = request.get_json()
    print(data)
    events = Event.select_by_type(data)
    event_image_file = url_for('static', filename = 'event_pics/')

    return jsonify({'data': render_template('event_change_ajax.html',events = events,event_image_file = event_image_file)})



posts = Blueprint('posts',__name__,template_folder = 'templates')

@app.route('/show_result', methods = ['get'])
def search():
    event_image_file = url_for('static', filename = 'event_pics/')
    profile_pics = url_for('static', filename = 'profile_pics/')    
    search = request.args.get('search')
    search_with_parenthesis = '%%'+search+'%%'
    
    data = {
        'search':search_with_parenthesis
    }

    if 'user_id' in session:
        user_data = {
            'id':session['user_id']
        }
        events = Event.select_by(data)
        print(events)
        return render_template('show_results.html', events = Event.select_by(data),user = User.show_single_user(user_data),event_image_file = event_image_file,profile_pics = profile_pics, search = search)

    else:
        events = Event.select_by(data)
        print(events)
        return render_template('show_results.html',event_image_file = event_image_file,profile_pics = profile_pics,events = Event.select_by(data),search = search)

@app.route('/edit_event/<int:id>')
def show_edit_event_page(id):
    if 'user_id' not in session:
        return redirect("/logout")
    event_pics = url_for('static',filename = 'event_pics/')
    profile_pics = url_for('static', filename = 'profile_pics/')  

    user_data = {
        'id':session['user_id']
    }
    event_data = {
        'event_id': id 
    }
    return render_template('edit_event.html', user = User.show_single_user(user_data),events = Event.show_single_event(event_data),profile_pics = profile_pics)  

@app.route('/update_event/<int:id>',methods = ['POST'])
def update_event(id):
    if 'user_id' not in session:
        return redirect('/logout')
    event_pics = url_for('static',filename = 'event_pics/')
    profile_pics = url_for('static', filename = 'profile_pics/')

    user_data = {
        'id':session['user_id']
    }
    event_data = {
        'event_id': request.form['event_id'],
        'name':request.form['name'],
        'description':request.form['description'],
        'type':request.form['type'],
        'address':request.form['address'],
        'date_time':request.form['date_time']
    }

    valid = Event.event_validator(event_data)
    if not valid:
        print('not valid')
        return redirect(f'/edit_event/{id}')
    if valid:
        event = Event.edit_event(event_data)
        print(event)
        flash('Updates successful',category  ='success')
        return redirect(f'/show_event/{id}')

@app.route('/update_event_picture/<int:id>', methods = ['POST'])
def update_event_picture(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if request.method == 'POST':
            if 'picture' not in request.files:
                flash('No File Selected', category='error')
                return redirect(f'/edit_event/{id}')
            file = request.files['picture']
            if file.filename == '':
                flash('Please Select file',category = 'error')
                return redirect(f'/edit_event/{id}')
            EXT = {'.jpeg','.jpg','.png'}
            root_ext = os.path.splitext(file.filename)
            print(root_ext)
            if root_ext[1] not in EXT:
                print(file.filename)
                flash('File type must be jpg,jpeg or png', category = 'error')
                return redirect(f'/edit_event/{id}')
            if file and allowed_file(file.filename):
                pics = secure_filename(file.filename)
                photo = request.files['picture']
                photo = Image.open(photo)
                photo = photo.resize((400,300))
                photo.save(os.path.join(app.config['UPLOAD_FOLDER_EVENTS'],pics))
    data = {
        'event_id':id,
        'picture':request.files['picture'].filename
    }
    print(data)
    valid = Event.event_picture_validator(data)
    print(valid)
    if not valid:
        return redirect(f'/edit_event/{id}')
    if valid:
        picture = Event.edit_image(data)
        print(picture)
        print(picture)
        print('picture changed')
        flash('Picture Updated',category = 'success')
        return redirect(f'/show_event/{id}')

@app.route('/destroy_event/<int:id>')
def destroy_event(id):
    if 'user_id' not in session:
        return('/logout')
    data = {
        'event_id':id
    }
    creator_of_event = Event.show_single_event(data)
    if session['user_id'] != creator_of_event['user_id']:
        return ('/logout')
    Event.take_off_fk_restraint()
    Attendance.destroy_event_attendance(data)
    Event.destroy_event(data)
    Event.put_on_fk_restraint()
    flash('Event Deleted successfully', category = 'success')
    return redirect(f'/dashboard')
    



    
