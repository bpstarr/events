from flask import Flask
import os,logging
from os.path import join,dirname,realpath
UPLOAD_FOLDER_EVENT = join(dirname(realpath(__file__)),'static/event_pics')
UPLOAD_FOLDER_PROFILE = join(dirname(realpath(__file__)),'static/profile_pics')
app = Flask(__name__)
app.config['UPLOAD_FOLDER_EVENTS'] = UPLOAD_FOLDER_EVENT
app.config['UPLOAD_FOLDER_PROFILE'] = UPLOAD_FOLDER_PROFILE
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
ALLOWED_EXTENSIONS = {'jpeg','jpg','png'}