from portra.component.tags import *
from portra.component.xmp import has_metadata
from portra.component.xmp import get_tonecurve
from portra.component.xmp import xmp_get_lr_settings

from portra.utils import tc_format_js

### Adobe Lightroom values that are stored as arrays.
LR_ARRAY_TAGS = {
    'ToneCurvePV2012',
    'ToneCurvePV2012Blue',
    'ToneCurvePV2012Green',
    'ToneCurvePV2012Red'}

def get_lightroom_settings(xmp):
    """
    Returns a properly formatted dictionary of Adobe Lightroom values for the frontend.
    All internal XMP values are converted to their corresponding value strings.
    """
    if has_metadata(xmp):
        lightroom = get_crs_metadata(xmp)
        lightroom['ProcessVersion'] = PROCESS_VERSION[lightroom['ProcessVersion']]
        lightroom['PostCropVignetteStyle'] = VIGNETTE_STYLE[int(lightroom['PostCropVignetteStyle'])]
        lightroom['ToneCurvePV2012'] = tc_format_js(lightroom['ToneCurvePV2012'])
        lightroom['ToneCurvePV2012Red'] = tc_format_js(lightroom['ToneCurvePV2012Red'])
        lightroom['ToneCurvePV2012Green'] = tc_format_js(lightroom['ToneCurvePV2012Green'])
        lightroom['ToneCurvePV2012Blue'] = tc_format_js(lightroom['ToneCurvePV2012Blue'])
        return lightroom

def get_crs_metadata(xmp, wb=True, exposure=True, contrast=True, highlights=True,
                shadows=True, white=True, black=True, clarity=True, tc=True,
                treatment=True, adjustments=True, saturation=True, vibrance=True,
                sharpening=True, grain=True, vignette=True, dehaze=True, st=True,
                d_luminance=True, d_color=True, pv=True, cc=True):
    """
    Returns a dictionary of Adobe Camera Raw parameters from the .xmp file.
    The remaining arguments are booleans which determine the parameters included.
    Refer to tags.py for all the available values.
    """
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

def lr_white_balance(xmp):
    return xmp_get_lr_settings(xmp, LR_WHITE_BALANCE)

def lr_tone(xmp, exposure, contrast, highlights, shadows, white, black, clarity):
    tone = xmp_get_lr_settings(xmp, LR_TONE)
    if not exposure:
        tone.pop('Exposure2012')
    if not contrast:
        tone.pop('Contrast2012')
    if not highlights:
        tone.pop('Highlights2012')
    if not shadows:
        tone.pop('Shadows2012')
    if not white:
        tone.pop('Whites2012')
    if not black:
        tone.pop('Blacks2012')
    if not clarity:
        tone.pop('Clarity2012')
    return tone

def lr_tone_curve(xmp):
    tc = get_tonecurve(xmp)
    lrt = xmp_get_lr_settings(xmp, LR_TONE_CURVE)
    for t in LR_ARRAY_TAGS:
        if tc[t]:
            lrt[t] = tc_format(tc[t])
    return lrt

def lr_color(xmp, treatment, adjustments, saturation, vibrance):
    color = xmp_get_lr_settings(xmp, LR_COLOR)
    if not treatment:
        color.pop('ConvertToGrayscale')
    if not saturation:
        color.pop('Saturation')
    if not vibrance:
        color.pop('Vibrance')

    if adjustments:
        color.update(lr_color_adjustments(xmp))
    else:
        color.pop('EnableColorAdjustments')
    return color

def lr_color_adjustments(xmp):
    return xmp_get_lr_settings(xmp, LR_COLOR_ADJUSTMENTS)

def lr_sharpening(xmp):
    return xmp_get_lr_settings(xmp, LR_SHARPENING)

def lr_effects(xmp, grain, vignette, dehaze):
    effects = xmp_get_lr_settings(xmp, LR_EFFECTS)
    if not dehaze:
        effects.pop('Dehaze')

    if grain:
        effects.update(xmp_get_lr_settings(xmp, LR_EFFECTS_GRAIN))
    if vignette:
        effects.update(xmp_get_lr_settings(xmp, LR_EFFECTS_VIGNETTE))

    if not grain and not vignette:
        effects.pop('EnableEffects')
    return effects

def lr_split_toning(xmp):
    return xmp_get_lr_settings(xmp, LR_SPLIT_TONING)

def lr_detail(xmp, luminance, color):
    detail = {}
    if luminance or color:
        detail = xmp_get_lr_settings(xmp, LR_DETAIL)
        if luminance:
            detail.update(xmp_get_lr_settings(xmp, LR_DETAIL_LUMINANCE))
        if color:
            detail.update(xmp_get_lr_settings(xmp, LR_DETAIL_COLOR))
    return detail

def lr_process_version(xmp):
    return xmp_get_lr_settings(xmp, LR_PROCESS_VERSION)

def lr_camera_calibration(xmp):
    return xmp_get_lr_settings(xmp, LR_CAMERA_CALIBRATION)

def tc_format(arr):
    """Formats an array into the style used in .lrtemplate files."""
    return '{' + ', '.join(arr) + ',}'
