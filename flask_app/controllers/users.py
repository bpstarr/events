from flask import render_template,request,session,flash,redirect, url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models.event import Event
from flask_bcrypt import Bcrypt
from PIL import Image
from werkzeug.utils import secure_filename
import os
from flask_app import ALLOWED_EXTENSIONS
from flask_app.models.attendance import Attendance

bcrypt = Bcrypt(app)

def allowed_file(pics):
    return '.' in pics and \
        pics.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    profile_pics = url_for('static', filename = 'profile_pics/')
    if 'user_id' in session:
        data = {
            'id':session['user_id']
        }
        return render_template('index.html',user = User.show_single_user(data),profile_pics = profile_pics)
    else:
        return render_template('index.html',profile_pics = profile_pics)

@app.route('/registration')
def show_registration_page():
    if 'user_id' in session:
        return redirect('/logout')
    return render_template('registration.html')

@app.route('/user/registration', methods = ['POST'])
def register_user():  
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':request.form['password'],
        'verify_password':request.form['verify_password'],
    }
    valid = User.user_validator(data)
    if valid:
        hashed_pw = bcrypt.generate_password_hash(request.form['password'])
        data['hashed_pw'] = hashed_pw
        user = User.add_user(data)
        user_email = User.get_by_email(data)
        session['user_email'] = user_email.email
        session['user_id'] = user
        session['user_picture'] = user_email.user_picture
        print('User logged in.')
        flash('Login Successful', category = 'success')
        return redirect('/dashboard')
    return redirect('/registration')

@app.route('/login')
def show_login_page():
    if 'user_id' in session:
        return redirect('/logout')
    return render_template('login.html')

@app.route('/user/login', methods = ['POST'])
def login_user():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid email or password. Please try again.', category='error')
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash('Invalid email or password. Please try again', category='error')
        return redirect('/login')
    session['user_id'] = user.id
    session['user_email'] = user.email
    session['user_picture'] = user.user_picture
    print('Successful login')
    flash('Login Successful', category = 'success')
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    flash('logout successful',category = 'success')
    print('logout successful')
    return redirect('/')

@app.route('/user/<int:id>')
def show_user_edit_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    profile_pics = url_for('static', filename = 'profile_pics/')

    data = {
        'id':session['user_id']
    }
    return render_template('edit_account.html',user = User.show_single_user(data), profile_pics = profile_pics)

@app.route('/edit_user/<int:id>', methods = ['POST'])
def edit_user_information(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':id,
        'first_name': request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
    }
    valid = User.user_update_validator(data)
    if not valid:
        print('not valid')
        return redirect(f'/user/{id}')
    print(valid)
    if valid:
        user = User.edit_user(data)
        print(user)
        flash('Updates successful',category = 'success')
        return redirect('/dashboard')

@app.route('/update_picture/<int:id>', methods = ['POST'])
def update_profile_picture(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if request.method == 'POST':
        if 'picture' not in request.files:
            flash('No file selected',category = 'error')
            return redirect(f'/user/{id}')
        file = request.files['picture']
        if file.filename == '':
            flash('Please select file',category = 'error')
            return redirect(f'/user/{id}')
        if file and allowed_file(file.filename):
            pics = secure_filename(file.filename)
            photo = request.files['user_picture']
            photo = Image.open(photo)
            photo = photo.resize((400,300))
            photo.save(os.path.join(app.config['UPLOAD_FOLDER_PROFILE'],pics))
        data = {
            'id':id,
            'user_picture': request.files['user_picture'].filename
        }
        valid = User.edit_profile_validator_pics(data)
        if not valid:
            return redirect(f'/user/{id}')
        if valid:
            picture = User.change_profile_picture(data)
            print(picture)
            print('Picture changed')
            flash('Picture Updated',category = 'success')
            return redirect('/dashboard')

@app.route('/destroy_user/<int:id>')
def destroy_user(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':session['user_id']
    }
    User.take_off_fk_restraint()
    Attendance.destroy_event_attendance_by_user_id(data)
    User.destroy_user(data)
    User.put_on_fk_restraint()
    session.clear()
    flash('Account deleted',category='success')
    return redirect('/')

@app.route('/dashboard')
def show_dashboard():
    event_image_file = url_for('static', filename = 'event_pics/')
    profile_pics = url_for('static', filename = 'profile_pics/')
    if 'user_id' in session:
        data = {
            'id':session['user_id']
        }
        return render_template('dashboard.html', user = User.show_single_user(data),events = Event.get_all(),event_image_file = event_image_file, profile_pics = profile_pics)
    else:
        return render_template('dashboard.html',events = Event.get_all(),event_image_file = event_image_file,profile_pics = profile_pics)


