"""
Feature classes
"""

from keytree.model import Geometry, Feature
from keytree.model import GEOM_TYPES

def feature(placemark_element):
    kmlns = placemark_element.tag.split('}')[0][1:]
    for geom_type in GEOM_TYPES:
        tag = '{%s}%s' % (kmlns, geom_type)
        geometry_element = placemark_element.find(tag)
        if geometry_element is not None:
            g = geometry(geometry_element)
            return Feature(g)
    return Feature(None)

def geometry(geometry_element):
    tp = geometry_element.tag.split('}')
    kmlns = tp[0][1:]
    geom_type = tp[1]
    return geometry_factory[geom_type](geometry_element, kmlns)

def geometry_Point(geometry_element, kmlns):
    t = geometry_element.findtext('{%s}coordinates' % kmlns)
    tv = t.split(',')
    return Geometry('Point', tuple([float(v) for v in tv]))

geometry_factory = {
    'Point': geometry_Point,
    }
