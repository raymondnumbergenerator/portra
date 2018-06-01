import os
import uuid

from flask import url_for

from portra.app import app

def get_img_file(filename):
    return os.path.join(app.config['IMAGES_PATH'], filename)

def get_img_url(filename):
    return url_for('img', filename=filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_file(file):
    filename = random_filename()
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

def random_filename():
    return uuid.uuid4().hex[0:8] + '.jpg'
