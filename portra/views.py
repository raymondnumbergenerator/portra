import json
import os

from flask import render_template
from flask import Response
from flask import url_for
from flask import send_from_directory

from portra.app import app
from portra.component.export import lr_export_lrtemplate
from portra.component.export import xmp_export_full
from portra.component.export import xmp_export_tonecurve
from portra.component.lr import crs_full_all
from portra.component.tags import VIGNETTE_STYLE
from portra.component.tags import PROCESS_VERSION
from portra.component.xmp import has_metadata
from portra.component.xmp import exif_metadata

from portra.utils import get_image_metadata
from portra.utils import get_img_file
from portra.utils import get_img_url
from portra.utils import tc_format_js

@app.route('/img/<path:filename>')
def img(filename):
    return send_from_directory(app.config['IMAGES_PATH'], filename)

@app.route('/', methods={'GET', 'POST'})
def home():
    return render_template(
        'base.html',
        image_url="",
        metadata={},
        exif={},
        lightroom={},
        tonecurve={},
    )

@app.route('/<filename>', methods={'GET', 'POST'})
def image(filename):
    file = get_img_file(filename)
    if not os.path.isfile(file):
        return render_template(
            'base.html',
            image_url="",
            metadata={},
            exif={},
            lightroom={},
            tonecurve={},
        )

    xmp = xmp_export_full(file)
    met = get_image_metadata(file)
    if not has_metadata(xmp):
        return render_template(
            'base.html',
            image_url=get_img_url(filename),
            metadata=met,
            exif={},
            lightroom={},
            tonecurve={},
        )

    crs = crs_full_all(xmp)
    crs['ProcessVersion'] = PROCESS_VERSION[crs['ProcessVersion']]
    crs['PostCropVignetteStyle'] = VIGNETTE_STYLE[crs['PostCropVignetteStyle']]
    return render_template(
        'base.html',
        image_url=get_img_url(filename),
        metadata=met,
        exif=exif_metadata(xmp),
        lightroom=crs,
        tonecurve={
            'rgb': json.dumps(tc_format_js(crs['ToneCurvePV2012'])),
            'red': json.dumps(tc_format_js(crs['ToneCurvePV2012Red'])),
            'green': json.dumps(tc_format_js(crs['ToneCurvePV2012Green'])),
            'blue': json.dumps(tc_format_js(crs['ToneCurvePV2012Blue'])),
        }
    )

@app.route('/<filename>/xmp')
def xmp(filename):
    file = get_img_file(filename)
    xmp = xmp_export_full(file)
    return Response(str(xmp), mimetype='text/plain')

@app.route('/<filename>/tc')
def tc(filename):
    file = get_img_file(filename)
    xmp = xmp_export_full(file)
    tc = xmp_export_tonecurve(xmp)
    return Response(str(tc), mimetype='text/plain')

@app.route('/<filename>/lrt')
def lrt(filename):
    file = get_img_file(filename)
    xmp = xmp_export_full(file)
    lrt = lr_export_lrtemplate(xmp, os.path.splitext(filename)[0])
    return Response(str(lrt), mimetype='text/plain')
