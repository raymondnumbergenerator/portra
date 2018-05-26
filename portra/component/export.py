import xml.dom.minidom as minidom
import xml.etree.ElementTree as et

from libxmp.utils import file_to_dict, XMPFiles

from portra.component.lr import crs_full
from portra.component.tags import TC_TAGS_ARRAY
from portra.component.tags import TC_TAGS_STRING
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

    rough_xmp_output = et.tostring(x_xmpmeta, encoding='UTF-8')
    xmp_output = minidom.parseString(rough_xmp_output).toprettyxml(indent=' ')
    return xmp_output.split('\n', 1)[1]

def lr_export_lrtemplate(xmp, name,
                wb=False, exposure=False, contrast=True, highlights=True,
                shadows=True, white=True, black=True, clarity=True, tc=True,
                treatment=True, adjustments=True, saturation=True, vibrance=True,
                sharpening=False, grain=True, vignette=False, dehaze=True, st=True,
                d_luminance=False, d_color=False, pv=True, cc=True):
    return crs_full(xmp, wb, exposure, contrast, highlights,
                shadows, white, black, clarity, tc,
                treatment, adjustments, saturation, vibrance,
                sharpening, grain, vignette, dehaze, st,
                d_luminance, d_color, pv, cc)
