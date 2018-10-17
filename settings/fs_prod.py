import os

STORAGE_BACKEND = {
    'type': 'file',
    'img_path': '/srv/portra/files/i',
    'met_path': '/srv/portra/files/m',
    'met_extension': '.met',
}
SECRET_KEY = 'srv/portra/SECRET_KEY'

################################################
### DO NOT CONFIGURE VALUES BELOW THIS POINT ###
################################################

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
