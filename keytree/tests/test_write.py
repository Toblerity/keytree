import pytest

from keytree import element

KML = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
  </Document>
</kml>
""".encode()  # lxml doesn't like unencoded strings with an encoding declaration


@pytest.fixture
def doc(etree):
    return etree.fromstring(KML)


def test_element(doc):
    f = {
        "id": "1",
        "geometry": {"type": "Point", "coordinates": (0.0, 0.0)},
        "properties": {"title": "one", "description": "Point one"},
    }
    elem = element(doc, f)
    assert elem.tag == "{http://www.opengis.net/kml/2.2}Placemark"
    assert elem.attrib["id"] == "1"
    assert elem.find("{http://www.opengis.net/kml/2.2}name").text == "one"
    assert elem.find("{http://www.opengis.net/kml/2.2}Snippet").text == "Point one"

    assert (
        elem.find("{http://www.opengis.net/kml/2.2}Point")
        .find("{http://www.opengis.net/kml/2.2}coordinates")
        .text
        == "0.000000,0.000000,0.0"
    )


def test_element_kw(doc):
    f = {
        "id": "1",
        "geometry": {"type": "Point", "coordinates": (0.0, 0.0)},
        "properties": {},
    }
    elem = element(doc, f, name="one", snippet="Point one")
    assert elem.tag == "{http://www.opengis.net/kml/2.2}Placemark"
    assert elem.attrib["id"] == "1"
    assert elem.find("{http://www.opengis.net/kml/2.2}name").text == "one"
    assert elem.find("{http://www.opengis.net/kml/2.2}Snippet").text == "Point one"
