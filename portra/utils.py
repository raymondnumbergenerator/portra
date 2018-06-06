import random
import string

from portra.app import app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def random_filename(length=8):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length)) + '.jpg'

def tc_format_js(arr):
    """Formats a tone curve array for use in templating."""
    l = arr[1:-2].split(', ')
    lst = []
    for i in range(0, len(l), 2):
        lst.append([int(l[i]), 255 - int(l[i+1])])
    return lst
