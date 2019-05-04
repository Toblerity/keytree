
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
    
    def test_element(self):
        f = {
            'id': '1',
            'geometry': {'type': 'Point', 'coordinates': (0.0, 0.0)},
            'properties': {
                'title': 'one',
                'description': 'Point one' } }
        elem = element(self.doc, f)
        self.assertEqual(
            elem.tag, '{http://www.opengis.net/kml/2.2}Placemark' )
        self.assertEqual(elem.attrib['id'], '1')
        self.assertEqual(
            elem.find('{http://www.opengis.net/kml/2.2}name').text,
            'one' )
        self.assertEqual(
            elem.find('{http://www.opengis.net/kml/2.2}Snippet').text,
            'Point one' )
        self.assertEqual(
            elem.find('{http://www.opengis.net/kml/2.2}Point').find(
                '{http://www.opengis.net/kml/2.2}coordinates').text,
            '0.000000,0.000000,0.0' )

    def test_element_kw(self):
        f = {
            'id': '1',
            'geometry': {'type': 'Point', 'coordinates': (0.0, 0.0)},
            'properties': {} }
        elem = element(self.doc, f, name='one', snippet='Point one')
        self.assertEqual(
            elem.tag, '{http://www.opengis.net/kml/2.2}Placemark' )
        self.assertEqual(elem.attrib['id'], '1')
        self.assertEqual(
            elem.find('{http://www.opengis.net/kml/2.2}name').text,
            'one' )
        self.assertEqual(
            elem.find('{http://www.opengis.net/kml/2.2}Snippet').text,
            'Point one' )

