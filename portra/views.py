import json
import os

from flask import flash
from flask import redirect
from flask import render_template
from flask import request, Response
from flask import url_for
from flask import send_from_directory

from werkzeug.utils import secure_filename

from portra.app import app
from portra.component.export import lr_export_lrtemplate
from portra.component.export import xmp_export_tonecurve

from portra.component.backend import backend

from portra.utils import allowed_file

@app.route('/', methods={'GET', 'POST'})
def home():
    if request.method == 'POST':
        return upload()

    return render_template(
        'image.html',
        image_url="",
        metadata={},
        exif={},
        lightroom={},
    )

@app.route('/<filename>', methods={'GET', 'POST'})
def image(filename):
    if request.method == 'POST':
        return upload()

    url = backend().get_img_url(filename)
    if not url:
        return render_template(
            'image.html',
            image_url='',
            filename='',
            metadata={},
            exif={},
            lightroom={},
        )

    info = backend().get_img_info(filename)
    return render_template(
        'image.html',
        image_url=url,
        filename=info['filename'],
        metadata=info['metadata'],
        exif=info['exif'],
        lightroom=info['lightroom'],
    )

@app.route('/<filename>/xmp')
def xmp(filename):
    xmp = backend().get_img_info(filename)['xmp']
    return Response(str(xmp), mimetype='text/plain')

@app.route('/<filename>/tc')
def tc(filename):
    xmp = backend().get_img_info(filename)['xmp']
    tc = xmp_export_tonecurve(xmp)
    return Response(str(tc), mimetype='text/plain')

@app.route('/<filename>/lrt')
def lrt(filename):
    xmp = backend().get_img_info(filename)['xmp']
    lrt = lr_export_lrtemplate(xmp, os.path.splitext(filename)[0])
    return Response(str(lrt), mimetype='text/plain')

@app.route('/img/<path:filename>')
def img(filename):
    return send_from_directory(app.config['STORAGE_BACKEND']['img_path'], filename)

def upload():
    if 'file' not in request.files:
        flash('No file provided.')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No file selected.')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        saved_filename = backend().save_image(file)
        return redirect(url_for('image', filename=saved_filename))
    return redirect(request.url)
