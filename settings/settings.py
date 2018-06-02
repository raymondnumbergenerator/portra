import os

IMAGES_PATH = os.environ['DEFAULT_IMAGES_PATH']
SECRET_KEY = os.environ['SECRET_KEY']

################################################
### DO NOT CONFIGURE VALUES BELOW THIS POINT ###
################################################

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
UPLOAD_FOLDER = IMAGES_PATH
