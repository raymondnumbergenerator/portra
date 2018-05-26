import xml.dom.minidom as minidom
import xml.etree.ElementTree as et

from libxmp import XMPError
from libxmp.consts import XMP_NS_CameraRaw as NS_CRS
from libxmp.utils import file_to_dict, XMPFiles

from portra.component.tags import LR_WHITE_BALANCE
from portra.component.tags import LR_TONE
from portra.component.tags import LR_TONE_CURVE
from portra.component.tags import LR_COLOR
from portra.component.tags import LR_COLOR_ADJUSTMENTS
from portra.component.tags import LR_SHARPENING
from portra.component.tags import LR_EFFECTS
from portra.component.tags import LR_EFFECTS_GRAIN
from portra.component.tags import LR_EFFECTS_VIGNETTE
from portra.component.tags import LR_SPLIT_TONING
from portra.component.tags import LR_DETAIL
from portra.component.tags import LR_DETAIL_LUMINANCE
from portra.component.tags import LR_DETAIL_COLOR
from portra.component.tags import LR_PROCESS_VERSION
from portra.component.tags import LR_CAMERA_CALIBRATION
from portra.component.tags import LR_STRING_TAGS
from portra.component.tags import LR_ARRAY_TAGS

from portra.component.tags import TC_TAGS_STRING
from portra.component.tags import TC_TAGS_ARRAY
from portra.component.tags import XMP_TC_TAGS
from portra.component.tags import XMP_TC_TEXT

def xmp_export_full(filename):
    try:
        xmpfile = XMPFiles(file_path=filename)
    except:
        return None
    return xmpfile.get_xmp()

def xmp_export_tonecurve(xmp):
    tc = crs_tonecurve(xmp)

    x_xmpmeta = et.Element(XMP_TC_TAGS[0][0])
    x_xmpmeta.set(XMP_TC_TAGS[0][1], XMP_TC_TEXT[0][1])
    x_xmpmeta.set(XMP_TC_TAGS[0][2], XMP_TC_TEXT[0][2])

    rdf_rdf = et.SubElement(x_xmpmeta, XMP_TC_TAGS[1][0])
    rdf_rdf.set(XMP_TC_TAGS[1][1], XMP_TC_TEXT[1][1])

    rdf_description = et.SubElement(rdf_rdf, XMP_TC_TAGS[2][0])
    rdf_description.set(XMP_TC_TAGS[2][1], XMP_TC_TEXT[2][1])
    rdf_description.set(XMP_TC_TAGS[2][2], XMP_TC_TEXT[2][2])
    rdf_description.set(XMP_TC_TAGS[2][3], tc[TC_TAGS_STRING[0]])
    rdf_description.set(XMP_TC_TAGS[2][4], tc[TC_TAGS_STRING[1]])
    rdf_description.set(XMP_TC_TAGS[2][5], tc[TC_TAGS_STRING[2]])
    rdf_description.set(XMP_TC_TAGS[2][6], tc[TC_TAGS_STRING[3]])

    for t in TC_TAGS_ARRAY:
        node = et.SubElement(rdf_description, 'crs:' + t)
        seq = et.SubElement(node, 'rdf:Seq')
        for p in tc[t]:
            li = et.SubElement(seq, 'rdf:li')
            li.text = p

    rough_xmp_output = et.tostring(x_xmpmeta, 'UTF-8')
    xmp_output = minidom.parseString(rough_xmp_output).toprettyxml(indent=' ')
    return xmp_output

def lr_export_lrtemplate(xmp, name):
    return crs_full(xmp)

def crs_tonecurve(xmp):
    tc = {}

    for t in TC_TAGS_ARRAY:
        tc[t] = xmp_get_array(xmp, NS_CRS, t)
    for t in TC_TAGS_STRING:
        tc[t] = xmp.get_property(NS_CRS, t)

    return tc

def lr_white_balance(xmp):
    return lr_get_settings(xmp, LR_WHITE_BALANCE)

def lr_tone(xmp, exposure, contrast, highlights, shadows, white, black, clarity):
    tone = lr_get_settings(xmp, LR_TONE)
    if not exposure:
        tone.pop("Exposure2012")
    if not contrast:
        tone.pop("Contrast2012")
    if not highlights:
        tone.pop("Highlights2012")
    if not shadows:
        tone.pop("Shadows2012")
    if not white:
        tone.pop("Whites2012")
    if not black:
        tone.pop("Blacks2012")
    if not clarity:
        tone.pop("Clarity2012")
    return tone

def lr_tone_curve(xmp):
    tc = crs_tonecurve(xmp)
    lrt = lr_get_settings(xmp, LR_TONE_CURVE)
    for t in LR_ARRAY_TAGS:
        lrt[t] = tc_format(tc[t])
    return lrt

def lr_color(xmp, treatment, adjustments, saturation, vibrance):
    color = lr_get_settings(xmp, LR_COLOR)
    if not treatment:
        color.pop("ConvertToGrayscale")
    if not saturation:
        color.pop("Saturation")
    if not vibrance:
        color.pop("Vibrance")

    if adjustments:
        color.update(lr_color_adjustments(xmp))
    else:
        color.pop("EnableColorAdjustments")
    return color

def lr_color_adjustments(xmp):
    return lr_get_settings(xmp, LR_COLOR_ADJUSTMENTS)

def lr_sharpening(xmp):
    return lr_get_settings(xmp, LR_SHARPENING)

def lr_effects(xmp, grain, vignette, dehaze):
    effects = lr_get_settings(xmp, LR_EFFECTS)
    if not dehaze:
        effects.pop("Dehaze")

    if grain:
        effects.update(lr_get_settings(xmp, LR_EFFECTS_GRAIN))
    if vignette:
        effects.update(lr_get_settings(xmp, LR_EFFECTS_VIGNETTE))

    if not grain and not vignette:
        effects.pop("EnableEffects")
    return effects

def lr_split_toning(xmp):
    return lr_get_settings(xmp, LR_SPLIT_TONING)

def lr_detail(xmp, luminance, color):
    detail = {}
    if luminance or color:
        detail = lr_get_settings(xmp, LR_DETAIL)
        if luminance:
            detail.update(lr_get_settings(xmp, LR_DETAIL_LUMINANCE))
        if color:
            detail.update(lr_get_settings(xmp, LR_DETAIL_COLOR))
    return detail

def lr_process_version(xmp):
    return lr_get_settings(xmp, LR_PROCESS_VERSION)

def lr_camera_calibration(xmp):
    return lr_get_settings(xmp, LR_CAMERA_CALIBRATION)

def crs_full(xmp, wb=False, exposure=True, contrast=True, highlights=True,
                shadows=True, white=True, black=True, clarity=True, tc=True,
                treatment=True, adjustments=True, saturation=True, vibrance=True,
                sharpening=False, grain=True, vignette=False, dehaze=True, st=True,
                d_luminance=False, d_color=False, pv=True, cc=True):
    crs = {}
    wb and crs.update(lr_white_balance(xmp))
    crs.update(lr_tone(xmp, exposure, contrast, highlights, shadows, white, black, clarity))
    tc and crs.update(lr_tone_curve(xmp))
    crs.update(lr_color(xmp, treatment, adjustments, saturation, vibrance))
    sharpening and crs.update(lr_sharpening(xmp))
    crs.update(lr_effects(xmp, grain, vignette, dehaze))
    st and crs.update(lr_split_toning(xmp))
    crs.update(lr_detail(xmp, d_luminance, d_color))
    pv and crs.update(lr_process_version(xmp))
    cc and crs.update(lr_camera_calibration(xmp))
    return crs

def xmp_get_array(xmp, schema_ns, array_name):
    ret = []
    i = 1

    try:
        while True:
            ret.append(xmp.get_array_item(schema_ns, array_name, i))
            i = i + 1
    except XMPError:
        pass
    return ret

def lr_get_settings(xmp, settings):
    s = {}
    for option, val in settings.items():
        try:
            v = xmp.get_property(NS_CRS, option)
            if v:
                val = v
        except XMPError:
            print('Missing tag ' + option + ': using default value of ' + str(val)) # for debugging purposes
        if option in LR_STRING_TAGS:
            val = '\"' + val + '\"'
        s[option] = val
    return s

def tc_format(arr):
    return '{' + ', '.join(arr) + ',}'
