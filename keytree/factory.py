"""
Factories for features and geometries
"""

from typing import Union

from keytree.model import GEOM_TYPES, Feature, Geometry


def feature(element, kmlns: Union[str, dict] = None) -> Feature:
    if kmlns is None:
        kmlns = {'': element.tag.split("}")[0][1:]}
    elif isinstance(kmlns, str):
        kmlns = {'': kmlns}
    kid = element.attrib.get("id")
    name = element.findtext("name", namespaces=kmlns) or \
        element.findtext("Name", namespaces=kmlns)
    snippet = element.findtext("Snippet", namespaces=kmlns)
    description = element.findtext("description", namespaces=kmlns) or \
        element.findtext("Description", namespaces=kmlns)
    for geom_type in GEOM_TYPES:
        geom_element = element.find(geom_type, namespaces=kmlns)
        if geom_element is not None:
            g = geometry(geom_element, kmlns=kmlns)
            return Feature(kid, g, name=name, snippet=snippet, description=description)
    return Feature(kid, None, name=name, snippet=snippet, description=description)


def geometry(element, kmlns: dict = None) -> Geometry:
    tp = element.tag.split("}")
    if kmlns is None:
        kmlns = {'': tp[0][1:]}
    geom_type = tp[1]
    # geom_type = element.tag
    return geometry_factory[geom_type](element, kmlns)


def geometry_Point(element, kmlns: dict):
    t = element.findtext("coordinates", namespaces=kmlns)
    tv = t.split(",")
    return Geometry("Point", tuple([float(v) for v in tv]))


def geometry_LineString(element, kmlns: dict):
    text = element.findtext("coordinates", namespaces=kmlns)
    ts = text.split()
    coords = []
    for t in ts:
        tv = t.split(",")
        coords.append(tuple([float(v) for v in tv]))
    return Geometry("LineString", tuple(coords))


def geometry_Track(element, kmlns: dict):
    sourcecoords = element.findall('gx:coord', namespaces=kmlns)
    coords = []
    for coord in sourcecoords:
        tv = coord.split()
        coords.append(tuple([float(v) for v in tv]))

    return Geometry("LineString", tuple(coords))


def geometry_Polygon(element, kmlns: dict):
    shell = element.find("outerBoundaryIs", namespaces=kmlns)
    text = shell.findtext("*/coordinates", namespaces=kmlns)
    ts = text.split()
    shell_coords = []
    for t in ts:
        tv = t.split(",")
        shell_coords.append(tuple([float(v) for v in tv]))
    poly_coords = []
    poly_coords.append(tuple(shell_coords))

    holes = element.findall("innerBoundaryIs", namespaces=kmlns)
    for hole in holes:
        text = hole.findtext("*/coordinates", namespaces=kmlns)
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
    "Track": geometry_Track,
    "Polygon": geometry_Polygon,
}
