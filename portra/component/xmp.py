import math

from libxmp import XMPError
from libxmp.consts import XMP_NS_CameraRaw as NS_CRS
from libxmp.consts import XMP_NS_DC as NS_DC
from libxmp.consts import XMP_NS_TIFF as NS_TIFF
from libxmp.consts import XMP_NS_EXIF as NS_EXIF
from libxmp.consts import XMP_NS_EXIF_Aux as NS_EXIF_AUX

from portra.component.tags import TC_TAGS_ARRAY
from portra.component.tags import TC_TAGS_STRING

def has_metadata(xmp):
    return xmp.does_property_exist(NS_DC, 'format')

def get_tonecurve(xmp):
    """
    Returns a dictionary of all Adobe Camera Raw tone curve parameters from the provided .xmp file.
    Refer to TC_TAGS_ARRAY and TC_TAGS_STRING in tags.py for all the available values.
    """
    tc = {}

    for t in TC_TAGS_ARRAY:
        tc[t] = xmp_get_array(xmp, NS_CRS, t)
    for t in TC_TAGS_STRING:
        tc[t] = xmp.get_property(NS_CRS, t)

    return tc

def get_exif_metadata(xmp):
    """
    Returns a dictionary of EXIF metadata from the provided .xmp file.
        DateTimeOriginal -- ISO 8601 format datetime string

        Model -- camera model
        SerialNumber -- camera body serial number
        ImageNumber -- camera shutter count

        Lens -- lens
        LensID -- lens model ID
        FocalLength -- focal length of photo
        FocalLengthIn35mmFilm -- 35mm equivalent focal length
        ApproximateFocusDistance -- focusing distance

        ExposureTime -- shutter speed
        FNumber -- f-stop
        ISOSpeedRatings -- ISO
        ExposureProgram -- manual, aperture priority, shutter priority, etc.
        MeteringMode -- spot, matrix, pattern, etc.

        Flash -- whether the flash fired or not
    """
    exif = {}

    if xmp.does_property_exist(NS_EXIF, 'DateTimeOriginal'):
        dt = xmp.get_property(NS_EXIF, 'DateTimeOriginal')
        exif['DateTimeOriginal'] = dt

    if xmp.does_property_exist(NS_TIFF, 'Model'):
        exif['Model'] = xmp.get_property(NS_TIFF, 'Model')

    for option in ['ApproximateFocusDistance', 'ImageNumber', 'Lens', 'LensID', 'SerialNumber']:
        try:
            exif[option] = xmp.get_property(NS_EXIF_AUX, option)
        except XMPError:
            pass

    if 'ApproximateFocusDistance' in exif:
        exif['ApproximateFocusDistance'] = str(parse_exif_val(exif['ApproximateFocusDistance'])) + ' m'

    if xmp.does_property_exist(NS_EXIF, 'FocalLength'):
        exif['FocalLength'] = xmp.get_property(NS_EXIF, 'FocalLength')
        exif['FocalLength'] = str(int(parse_exif_val(exif['FocalLength']))) + ' mm'

    if xmp.does_property_exist(NS_EXIF, 'FocalLengthIn35mmFilm'):
        exif['FocalLengthIn35mmFilm'] = xmp.get_property(NS_EXIF, 'FocalLengthIn35mmFilm')
        exif['FocalLengthIn35mmFilm'] = str(int(parse_exif_val(exif['FocalLengthIn35mmFilm']))) + ' mm'

    if xmp.does_property_exist(NS_EXIF, 'ExposureTime'):
        exposure_time = xmp.get_property(NS_EXIF, 'ExposureTime')
        et = exposure_time.split('/')
        if et[1] == '1':
            exposure_time = et[0]
        exif['ExposureTime'] = exposure_time + ' s'

    if xmp.does_property_exist(NS_EXIF, 'FNumber'):
        exif['FNumber'] = xmp.get_property(NS_EXIF, 'FNumber')
        exif['FNumber'] = 'f/' + str(parse_exif_val(exif['FNumber']))

    iso = xmp_get_array(xmp, NS_EXIF, 'ISOSpeedRatings')
    if iso:
        exif['ISOSpeedRatings'] = iso[0]

    if xmp.does_property_exist(NS_EXIF, 'ExposureBiasValue'):
        ev = parse_exif_val(xmp.get_property(NS_EXIF, 'ExposureBiasValue'))
        ev = math.floor(ev * 10) / 10
        if ev > 0:
            ev = "+%s EV" % str(ev)
        else:
            ev = str(ev) + ' EV'
        exif['ExposureBiasValue'] = ev

    if xmp.does_property_exist(NS_EXIF, 'MeteringMode'):
        mm = int(xmp.get_property(NS_EXIF, 'MeteringMode'))
        if mm == 1:
            exif['MeteringMode'] = 'Average'
        elif mm == 2:
            exif['MeteringMode'] = 'Center-weighted'
        elif mm == 3:
            exif['MeteringMode'] = 'Spot'
        elif mm == 4:
            exif['MeteringMode'] = 'Matrix'
        elif mm == 5:
            exif['MeteringMode'] = 'Pattern'
        elif mm == 6:
            exif['MeteringMode'] = 'Partial'

    if xmp.does_property_exist(NS_EXIF, 'ExposureProgram'):
        ep = int(xmp.get_property(NS_EXIF, 'ExposureProgram'))
        if ep == 1:
            exif['ExposureProgram'] = 'Manual'
        elif ep == 2:
            exif['ExposureProgram'] = 'Normal'
        elif ep == 3:
            exif['ExposureProgram'] = 'Aperture Priority'
        elif ep == 4:
            exif['ExposureProgram'] = 'Shutter Priority'
        elif ep == 5:
            exif['ExposureProgram'] = 'Creative'
        elif ep == 6:
            exif['ExposureProgram'] = 'Action'
        elif ep == 7:
            exif['ExposureProgram'] = 'Portrait'
        elif ep == 8:
            exif['ExposureProgram'] = 'Landscape'

    if xmp.does_property_exist(NS_EXIF, 'Flash/exif:Fired'):
        flash = xmp.get_property(NS_EXIF, 'Flash/exif:Fired')
        if flash == 'True':
            exif['Flash'] = 'Fired'
        else:
            exif['Flash'] = 'Did not fire'

    # if xmp.does_property_exist(NS_EXIF, 'GPSLatitude'):
    #     exif['GPSLatitude'] = xmp.get_property(NS_EXIF, 'GPSLatitude')
    # if xmp.does_property_exist(NS_EXIF, 'GPSLongitude'):
    #     exif['GPSLongitude'] = xmp.get_property(NS_EXIF, 'GPSLongitude')
    #
    # if xmp.does_property_exist(NS_EXIF, 'GPSAltitude') and xmp.does_property_exist(NS_EXIF, 'GPSAltitudeRef'):
    #     ref = xmp.get_property(NS_EXIF, 'GPSAltitudeRef')
    #     alt = parse_exif_val(xmp.get_property(NS_EXIF, 'GPSAltitude'))
    #     if ref == 0:
    #         alt = alt + 'm a.s.l'
    #     elif ref == 1:
    #         alt = alt + 'm b.s.l'
    #     exif['GPSAltitude'] = alt

    return exif

def xmp_get_array(xmp, schema_ns, array_name):
    """Parses an xmp array object and returns it as an array."""
    arr = []
    idx = 1

    try:
        while True:
            arr.append(xmp.get_array_item(schema_ns, array_name, idx))
            idx = idx + 1
    except XMPError:
        pass
    return arr

def xmp_get_lr_settings(xmp, settings):
    """
    Returns a dictionary containing values all the provided Adobe Lightroom Settings.
    If the value is not defined in the xmp file, then the default value is used.

    settings -- dictionary of lightroom parameters to default values
    """
    s = {}
    for option, val in settings.items():
        try:
            v = xmp.get_property(NS_CRS, option)
            if v:
                val = v
        except XMPError:
            pass
        s[option] = val
    return s

def parse_exif_val(val):
    """
    Sometimes EXIF values are stored in a fraction as a string.
    This will return the value as a decimal.
    """
    nums = val.split('/')
    if len(nums) == 1:
        return float(nums[0])
    return float(nums[0]) / float(nums[1])
