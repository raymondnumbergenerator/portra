import os

from flask import url_for
from PIL import Image
from portra.app import app

ONE_KB = 2**10
ONE_MB = 2**20

def tc_format_js(arr):
    """Formats an array for use in templating."""
    l = arr[1:-2].split(', ')
    lst = []
    for i in range(0, len(l), 2):
        lst.append([int(l[i]), 255 - int(l[i+1])])
    return lst

def get_img_file(filename):
    return os.path.join(app.root_path, 'static/i/' + filename)

def get_img_url(filename):
    return url_for('static', filename='i/' + filename)

def parse_exif_val(val):
    nums = val.split('/')
    if len(nums) == 1:
        return float(nums[0])
    return float(nums[0]) / float(nums[1])

def get_img_dimensions(file):
    """
    Returns image dimensions, resolution (in megapixels) and aspect ratio.
    """
    with Image.open(file) as img:
        width, height = img.size
    dim = "%s x %s" % (str(width), str(height))
    res = str(img_resolution(width, height)) + ' MP'
    ar = str(img_aspect_ratio(width, height))
    return dim, res, ar

def img_resolution(width, height):
    res = (width * height) / (1000000)
    return round(res, 2)

def img_aspect_ratio(width, height):
    return round(width/height, 2)

def get_file_size(file):
    size = os.stat(file).st_size
    if size >= ONE_MB:
        return '{:.2f} MB'.format(size / ONE_MB)
    elif size >= ONE_KB:
        return '{:.2f} KB'.format(size / ONE_KB)
    return '{} {}'.format(size, pluralize('byte', size))
