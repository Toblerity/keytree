"""
Geometry classes
"""

GEOM_TYPES = [
    "kml:Point",
    "kml:LineString",
    "kml:LinearRing",
    "kml:Polygon",
    "kml:MultiGeometry",
    "gx:Track",
    "gx:MultiTrack",
]

PROPERTIES_CONTEXT = {
    "name": "http://developers.google.com/kml/documentation/kmlreference#name",
    "snippet": "http://developers.google.com/kml/documentation/kmlreference#Snippet",
    "description": "http://developers.google.com/kml/documentation/kmlreference#description",
}

NSMAP = {
    "": "http://www.opengis.net/kml/2.2",
    "kml": "http://www.opengis.net/kml/2.2",
    "gx": "http://www.google.com/kml/ext/2.2",
    "atom": "http://www.w3.org/2005/Atom",
}


class Dictish:
    # Provides dict-like access to geo_interface items.
    def __getitem__(self, key):
        return self.__geo_interface__[key]


class Geometry(Dictish):
    def __init__(self, type, coordinates):
        self.type = type
        self.coordinates = coordinates

    @property
    def __geo_interface__(self):
        return {"type": self.type, "coordinates": self.coordinates}


class Feature(Dictish):
    def __init__(self, kid=None, geometry=None, properties=None, **kw):
        self.id = kid
        self.geometry = geometry
        self.properties = {"@context": PROPERTIES_CONTEXT}
        if properties:
            self.properties.update(properties)
        self.properties.update(kw)

    @property
    def __geo_interface__(self):
        return {
            "id": self.id,
            "geometry": self.geometry.__geo_interface__,
            "properties": self.properties,
        }
