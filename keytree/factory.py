"""
Factories for features and geometries
"""

from typing import Mapping, Union

import keytree.compat
from keytree.model import GEOM_TYPES, NSMAP, Feature, Geometry


def feature(element, kmlns: Union[str, Mapping] = NSMAP) -> Feature:
    kid = element.attrib.get("id")
    name = element.findtext("kml:name", namespaces=kmlns) or element.findtext(
        "kml:Name", namespaces=kmlns
    )
    snippet = element.findtext("kml:Snippet", namespaces=kmlns)
    description = element.findtext(
        "kml:description", namespaces=kmlns
    ) or element.findtext("kml:Description", namespaces=kmlns)
    for geom_type in GEOM_TYPES:
        geom_element = element.find(geom_type, namespaces=kmlns)
        if geom_element is not None:
            g = geometry(geom_element, kmlns=kmlns)
            return Feature(kid, g, name=name, snippet=snippet, description=description)
    return Feature(kid, None, name=name, snippet=snippet, description=description)


def geometry(element, kmlns: Mapping = NSMAP) -> Geometry:
    tp = element.tag.split("}")
    if kmlns is None:
        kmlns = {"": tp[0][1:]}
    geom_type = tp[1]
    # geom_type = element.tag
    return geometry_factory[geom_type](element, kmlns)


def geometry_Point(element, kmlns: Mapping = NSMAP):
    t = element.findtext("kml:coordinates", namespaces=kmlns)
    tv = t.split(",")
    return Geometry("Point", tuple([float(v) for v in tv]))


def geometry_LineString(element, kmlns: Mapping = NSMAP):
    text = element.findtext("kml:coordinates", namespaces=kmlns)
    ts = text.split()
    coords = []
    for t in ts:
        tv = t.split(",")
        coords.append(tuple([float(v) for v in tv]))
    return Geometry("LineString", tuple(coords))


def geometry_Track(element, kmlns: Mapping = NSMAP):
    sourcecoords = element.findall("gx:coord", namespaces=kmlns)
    coords = []
    for coord in sourcecoords:
        tv = coord.text.split()
        coords.append(tuple([float(v) for v in tv]))
    return Geometry("LineString", tuple(coords))


def geometry_MultiTrack(element, kmlns: Mapping = NSMAP):
    geometries = []
    for i in [el for el in element if el.tag.split("}")[1] == "Track"]:
        geometries.append(geometry(i, kmlns=kmlns))
    return Geometry("MultiLineString", geometries)


def geometry_Polygon(element, kmlns: Mapping = NSMAP):
    shell = element.find("kml:outerBoundaryIs", namespaces=kmlns)
    text = shell.findtext("*/kml:coordinates", namespaces=kmlns)
    ts = text.split()
    shell_coords = []
    for t in ts:
        tv = t.split(",")
        shell_coords.append(tuple([float(v) for v in tv]))
    poly_coords = []
    poly_coords.append(tuple(shell_coords))

    holes = element.findall("kml:innerBoundaryIs", namespaces=kmlns)
    for hole in holes:
        text = hole.findtext("*/kml:coordinates", namespaces=kmlns)
        ts = text.split()
        hole_coords = []
        for t in ts:
            tv = t.split(",")
            hole_coords.append(tuple([float(v) for v in tv]))
        poly_coords.append(tuple(hole_coords))

    return Geometry("Polygon", tuple(poly_coords))


def geometry_Multi(element, kmlns: Mapping = NSMAP):
    geometries = []
    geometry_type = multi_geometry[
        [
            el.tag.split("}")[1]
            for el in element
            if el.tag.split("}")[1] in multi_geometry.keys()
        ][0]
    ]
    for i in element:
        geometries.append(geometry(i, kmlns=kmlns).coordinates)
    return Geometry(geometry_type, geometries)


geometry_factory = {
    "Point": geometry_Point,
    "LineString": geometry_LineString,
    "Track": geometry_Track,
    "MultiTrack": geometry_MultiTrack,
    "Polygon": geometry_Polygon,
    "MultiGeometry": geometry_Multi,
}

multi_geometry = {
    "Point": "MultiPoint",
    "LineString": "MultiLineString",
    "Polygon": "MultiPolygon",
}
