import xml.dom.minidom as minidom
import xml.etree.ElementTree as et

from libxmp import XMPError
from libxmp.consts import XMP_NS_CameraRaw as NS_CRS
from libxmp.utils import file_to_dict, XMPFiles

from portra.component.tags import LR_WHITE_BALANCE
from portra.component.tags import LR_TONE
from portra.component.tags import LR_COLOR
from portra.component.tags import LR_COLOR_ADJUSTMENTS
from portra.component.tags import LR_SHARPENING
from portra.component.tags import LR_EFFECTS
from portra.component.tags import LR_EFFECTS_GRAIN
from portra.component.tags import LR_EFFECTS_VIGNETTE
from portra.component.tags import LR_SPLIT_TONING
from portra.component.tags import LR_PROCESS_VERSION
from portra.component.tags import LR_CAMERA_CALIBRATION

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
    tc = {}

    for t in TC_TAGS_ARRAY:
        tc[t] = xmp_get_array(xmp, NS_CRS, t)
    for t in TC_TAGS_STRING:
        tc[t] = xmp.get_property(NS_CRS, t)

    return tc

def crs_full(xmp):
    cr = {}

    for t in LR_TAGS:
        print(t)
        cr[t] = xmp.get_property(NS_CRS, t)
    cr.update(crs_tonecurve(xmp))

    return cr
