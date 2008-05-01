"""
Geometry classes
"""

GEOM_TYPES = [
    'Point',
    'LineString',
    'LinearRing',
    'Polygon',
    'MultiGeometry'
    ]

class Geometry(object):

    def __init__(self, type, coordinates):
        self.type = type
        self.coordinates = coordinates
    
    @property
    def __geo_interface__(self):
        return dict(type=self.type, coordinates=self.coordinates)


class Feature(object):

    def __init__(self, geometry):
        self.geometry = geometry

    @property
    def __geo_interface__(self):
        return dict(geometry=self.geometry.__geo_interface__)
