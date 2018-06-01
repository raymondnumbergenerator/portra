import os

IMAGES_PATH = os.environ['DEFAULT_IMAGES_PATH']
UPLOAD_FOLDER = IMAGES_PATH

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

SECRET_KEY = os.environ['SECRET_KEY']
