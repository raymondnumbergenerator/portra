from libxmp import XMPError

from libxmp.consts import XMP_NS_CameraRaw as NS_CRS

from libxmp.utils import file_to_dict, XMPFiles

def xmp_export_full(filename):
    xmpfile = XMPFiles(file_path=filename)
    return xmpfile.get_xmp()

def xmp_get_array(xmp, schema_ns, array_name):
    ret = []
    i = 1

    try: 
        while True:
            ret.append(xmp.get_array_item(schema_ns, array_name, i))
            i = i + 1
    except XMPError:
        return ret

    return ret

def crs_tonecurve(xmp):
    string_tags = ['Version', 'ToneCurveName', 'ToneCurveName2012', 'HasSettings']
    array_tags = ['ToneCurve', 'ToneCurveRed', 'ToneCurveGreen', 'ToneCurveBlue',
            'ToneCurvePV2012', 'ToneCurvePV2012Red', 'ToneCurvePV2012Green', 'ToneCurvePV2012Blue']

    tc = {}

    for t in array_tags:
        tc[t] = xmp_get_array(xmp, NS_CRS, t)
    for t in string_tags:
        tc[t] = xmp.get_property(NS_CRS, t)

    return tc
