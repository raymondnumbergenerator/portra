import os

STORAGE_BACKEND = {
    'type': 'file',
    'img_path': '/srv/portra/i',
    'met_path': '/srv/portra/m',
    'met_extension': '.met',
}
SECRET_KEY = 'src/portra/SECRET_KEY'

################################################
### DO NOT CONFIGURE VALUES BELOW THIS POINT ###
################################################

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
