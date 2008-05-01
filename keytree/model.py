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

    def __init__(self, kid=None, geometry=None, properties=None, **kw):
        self.id = kid
        self.geometry = geometry
        self.properties = properties or {}
        self.properties.update(kw)

    @property
    def __geo_interface__(self):
        return dict(
            id=self.id,
            geometry=self.geometry.__geo_interface__,
            properties=dict(self.properties)
            )
