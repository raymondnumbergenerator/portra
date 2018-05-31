from libxmp import XMPError
from libxmp.consts import XMP_NS_CameraRaw as NS_CRS
from libxmp.consts import XMP_NS_DC as NS_DC

from portra.component.tags import TC_TAGS_ARRAY
from portra.component.tags import TC_TAGS_STRING

def has_metadata(xmp):
    return xmp.does_property_exist(NS_DC, 'format')

def crs_tonecurve(xmp):
    """Returns a dictionary of all Adobe Camera Raw parameters from the provided .xmp file."""
    tc = {}

    for t in TC_TAGS_ARRAY:
        tc[t] = xmp_get_array(xmp, NS_CRS, t)
    for t in TC_TAGS_STRING:
        tc[t] = xmp.get_property(NS_CRS, t)

    return tc

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

def lr_get_settings(xmp, settings):
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
            print('Missing tag ' + option + ': using default value of ' + str(val)) # for debugging purposes
        s[option] = val
    return s
