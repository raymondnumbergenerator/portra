import os

STORAGE_BACKEND = {
    'type': 'file',
    'img_path': os.environ['DEFAULT_IMAGES_PATH'],
    'met_path': os.environ['DEFAULT_METADATA_PATH'],
    'met_extension': '.met',
}
SECRET_KEY = os.environ['SECRET_KEY']

################################################
### DO NOT CONFIGURE VALUES BELOW THIS POINT ###
################################################

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
