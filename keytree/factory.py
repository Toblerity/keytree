"""
Factories for features and geometries
"""

import keytree.compat
from keytree.model import Geometry, Feature, GEOM_TYPES


def feature(element):
    kmlns = element.tag.split("}")[0][1:]
    kid = element.attrib.get("id")
    name = element.findtext("{%s}name" % kmlns)
    snippet = element.findtext("{%s}Snippet" % kmlns)
    description = element.findtext("{%s}description" % kmlns)
    for geom_type in GEOM_TYPES:
        tag = "{%s}%s" % (kmlns, geom_type)
        geom_element = element.find(tag)
        if geom_element is not None:
            g = geometry(geom_element)
            return Feature(kid, g, name=name, snippet=snippet, description=description)
    return Feature(kid, None, name=name, snippet=snippet, description=description)


def geometry(element):
    tp = element.tag.split("}")
    kmlns = tp[0][1:]
    geom_type = tp[1]
    return geometry_factory[geom_type](element, kmlns)


def geometry_Point(element, kmlns):
    t = element.findtext("{%s}coordinates" % kmlns)
    tv = t.split(",")
    return Geometry("Point", tuple([float(v) for v in tv]))


def geometry_LineString(element, kmlns):
    text = element.findtext("{%s}coordinates" % kmlns)
    ts = text.split()
    coords = []
    for t in ts:
        tv = t.split(",")
        coords.append(tuple([float(v) for v in tv]))
    return Geometry("LineString", tuple(coords))


def geometry_Polygon(element, kmlns):
    shell = element.find("{%s}outerBoundaryIs" % kmlns)
    text = shell.findtext("*/{%s}coordinates" % kmlns)
    ts = text.split()
    shell_coords = []
    for t in ts:
        tv = t.split(",")
        shell_coords.append(tuple([float(v) for v in tv]))
    poly_coords = []
    poly_coords.append(tuple(shell_coords))

    holes = element.findall("{%s}innerBoundaryIs" % kmlns)
    for hole in holes:
        text = hole.findtext("*/{%s}coordinates" % kmlns)
        ts = text.split()
        hole_coords = []
        for t in ts:
            tv = t.split(",")
            hole_coords.append(tuple([float(v) for v in tv]))
        poly_coords.append(tuple(hole_coords))

    return Geometry("Polygon", tuple(poly_coords))


geometry_factory = {
    "Point": geometry_Point,
    "LineString": geometry_LineString,
    "Polygon": geometry_Polygon,
}
