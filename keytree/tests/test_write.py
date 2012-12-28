
from unittest import TestCase
from xml.etree import ElementTree as etree

from keytree import element

KML = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
  </Document>
</kml>
"""

class ElementWriterTestCase(TestCase):
    def setUp(self):
        self.doc = etree.fromstring(KML)
    def failUnlessCoordsAlmostEqual(self, a, b, precision=7):
        for x, y in zip(a, b):
            self.failUnlessAlmostEqual(x, y, precision)

    def test_element(self):
        f = {
            'id': '1',
            'geometry': {'type': 'Point', 'coordinates': (0.0, 0.0)},
            'properties': {
                'title': 'one',
                'summary': 'Point one' } }
        elem = element(self.doc, f)
        self.failUnlessEqual(
            elem.tag, '{http://www.opengis.net/kml/2.2}Placemark' )
        self.failUnlessEqual(
            elem.find('{http://www.opengis.net/kml/2.2}name').text,
            'one' )
        self.failUnlessEqual(
            elem.find('{http://www.opengis.net/kml/2.2}Point').find(
                '{http://www.opengis.net/kml/2.2}coordinates').text,
            '0.000000,0.000000,0.0' )
