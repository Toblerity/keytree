from unittest import TestCase
from xml.etree import ElementTree as etree

from keytree import feature

KML = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <Placemark>
      <name>point</name>
      <Snippet>Point test</Snippet>
      <description>Blah, blah, blah</description>
      <Point>
        <coordinates>
          -122.364383,37.824664,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>linestring</name>
      <Snippet>LineString test</Snippet>
      <description>Blah, blah, blah</description>
      <LineString>
        <coordinates>
          -122.364383,37.824664,0 -122.364152,37.824322,0 
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>polygon</name>
      <Snippet>Polygon test</Snippet>
      <description>Blah, blah, blah</description>
      <Polygon>
        <outerBoundaryIs>
          <LinearRing>
            <coordinates>
            -122.366278,37.818844,30
            -122.365248,37.819267,30
            -122.365640,37.819861,30
            -122.366669,37.819429,30
            -122.366278,37.818844,30
            </coordinates>
          </LinearRing>
        </outerBoundaryIs>
        <innerBoundaryIs>
          <LinearRing>
            <coordinates>
            -122.366212,37.818977,30
            -122.365424,37.819294,30
            -122.365704,37.819731,30
            -122.366488,37.819402,30
            -122.366212,37.818977,30
            </coordinates>
          </LinearRing>
        </innerBoundaryIs>
      </Polygon>
    </Placemark>
  </Document>
</kml>
"""


class FeatureReaderTestCase(TestCase):
    def setUp(self):
        self.doc = etree.fromstring(KML)
        self.placemarks = self.doc.findall(
            "*/{http://www.opengis.net/kml/2.2}Placemark"
        )

    def failUnlessCoordsAlmostEqual(self, a, b, precision=7):
        for x, y in zip(a, b):
            self.assertAlmostEqual(x, y, precision)

    def test_properties_context(self):
        f = feature(self.placemarks[0])
        props = f.properties
        self.assertTrue("name" in props["@context"])
        self.assertTrue("snippet" in props["@context"])
        self.assertTrue("description" in props["@context"])

    def test_point(self):
        f = feature(self.placemarks[0])
        self.assertTrue(f.geometry.type == f["geometry"]["type"] == "Point")
        coords = f.geometry.coordinates
        self.failUnlessCoordsAlmostEqual(coords, (-122.36438, 37.82466, 0.0), 5)
        self.assertTrue(f.properties["name"] == f["properties"]["name"] == "point")
        self.assertTrue(
            f.properties["snippet"] == f["properties"]["snippet"] == "Point test"
        )
        self.assertTrue(
            f.properties["description"]
            == f["properties"]["description"]
            == "Blah, blah, blah"
        )

    def test_linestring(self):
        f = feature(self.placemarks[1])
        self.assertTrue(f.geometry.type == f["geometry"]["type"] == "LineString")
        coords0 = f.geometry.coordinates[0]
        self.failUnlessCoordsAlmostEqual(coords0, (-122.36438, 37.82466, 0.0), 5)
        self.assertTrue(f.properties["name"] == f["properties"]["name"] == "linestring")
        self.assertTrue(
            f.properties["snippet"] == f["properties"]["snippet"] == "LineString test"
        )
        self.assertTrue(
            f.properties["description"]
            == f["properties"]["description"]
            == "Blah, blah, blah"
        )

    def test_polygon(self):
        f = feature(self.placemarks[2])
        self.assertTrue(f.geometry.type == f["geometry"]["type"] == "Polygon")
        coords0 = f.geometry.coordinates[0][0]
        self.failUnlessCoordsAlmostEqual(coords0, (-122.366278, 37.81884, 30.0), 5)
        self.assertTrue(f.properties["name"] == f["properties"]["name"] == "polygon")
        self.assertTrue(
            f.properties["snippet"] == f["properties"]["snippet"] == "Polygon test"
        )
        self.assertTrue(
            f.properties["description"]
            == f["properties"]["description"]
            == "Blah, blah, blah"
        )
        coords1 = f.geometry.coordinates[1][0]
        self.failUnlessCoordsAlmostEqual(coords1, (-122.366212, 37.818977, 30.0), 5)
