import os

from flask import url_for
from PIL import Image
from portra.app import app

ONE_KB = 2**10
ONE_MB = 2**20
COMMON_ASPECT_RATIOS = {
    '9:16': 0.56,
    '10:16': 0.63,
    '2:3': 0.67,
    '5:7': 0.71,
    '3:4': 0.75,
    '8.5:11': 0.77,
    '4:5': 0.80,
    '1:1': 1.00,
    '5:4': 1.25,
    '11:8.5': 1.29,
    '4:3': 1.33,
    '7:5': 1.40,
    '3:2': 1.50,
    '16:10': 1.60,
    '16:9': 1.78,
}

def tc_format_js(arr):
    """Formats an array for use in templating."""
    l = arr[1:-2].split(', ')
    lst = []
    for i in range(0, len(l), 2):
        lst.append([int(l[i]), 255 - int(l[i+1])])
    return lst

def get_img_file(filename):
    return os.path.join(app.config['IMAGES_PATH'], filename)

def get_img_url(filename):
    return url_for('img', filename=filename)

def parse_exif_val(val):
    """
    Sometimes EXIF values are stored in a fraction as a string.
    This will return the value as a decimal.
    """
    nums = val.split('/')
    if len(nums) == 1:
        return float(nums[0])
    return float(nums[0]) / float(nums[1])

def get_image_metadata(file):
    """
    Returns a dictionary of image metadata.
        Dimensions -- width pixels by height pixels
        AspectRatio - aspect ratio of the image
        Resolution - resolution in megapixels
        FileSize - file size in KB or MB
    """
    metadata = {}
    width, height = get_img_dimensions(file)
    metadata['Dimensions'] = "%s x %s" % (str(width), str(height))
    metadata['AspectRatio'] = str(img_aspect_ratio(width, height))
    metadata['Resolution'] = str(img_resolution(width, height)) + ' MP'
    metadata['FileSize'] = get_file_size(file)
    return metadata

def get_img_dimensions(file):
    """
    Returns image dimensions, resolution (in megapixels) and aspect ratio.
    """
    with Image.open(file) as img:
        width, height = img.size
    return width, height

def img_resolution(width, height):
    """
    Returns the image's resolution in megapixels.
    """
    res = (width * height) / (1000000)
    return round(res, 2)

def img_aspect_ratio(width, height):
    """
    Returns an image's aspect ratio.
    If the image has a common aspect ratio, returns the aspect ratio in the format x:y,
    otherwise, just returns width/height.
    """
    ratio = round(width/height, 2)
    for ar, val in COMMON_ASPECT_RATIOS.items():
        if ratio <= val + 0.01 and ratio >= val - 0.01:
            ratio = ar
            break
    return ratio

def get_file_size(file):
    """
    Returns the file size in a human readable format. (e.g. 700.79 KB, 19.55 MB)
    """
    size = os.stat(file).st_size
    if size >= ONE_MB:
        return '{:.2f} MB'.format(size / ONE_MB)
    elif size >= ONE_KB:
        return '{:.2f} KB'.format(size / ONE_KB)
    return '{} {}'.format(size, 'byte(s)')
