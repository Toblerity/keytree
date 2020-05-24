import pytest

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
""".encode()  # lxml doesn't like unencoded strings with an encoding declaration


#         self.placemarks = self.doc.findall(
#             "*/{http://www.opengis.net/kml/2.2}Placemark"
#         )


@pytest.fixture
def doc(etree):
    return etree.fromstring(KML)


@pytest.fixture
def placemarks(doc):
    return doc.findall(".//kml:Placemark")


def test_properties_context(placemarks):
    f = feature(placemarks[0])
    props = f.properties
    assert "name" in props["@context"]
    assert "snippet" in props["@context"]
    assert "description" in props["@context"]


def test_point(placemarks):
    f = feature(placemarks[0])
    assert f.geometry.type == f["geometry"]["type"] == "Point"
    coords = f.geometry.coordinates
    assert coords == pytest.approx((-122.36438, 37.82466, 0.0), 5)
    assert f.properties["name"] == f["properties"]["name"] == "point"
    assert f.properties["snippet"] == f["properties"]["snippet"] == "Point test"
    assert (
        f.properties["description"]
        == f["properties"]["description"]
        == "Blah, blah, blah"
    )


def test_linestring(placemarks):
    f = feature(placemarks[1])
    assert f.geometry.type == f["geometry"]["type"] == "LineString"
    coords0 = f.geometry.coordinates[0]
    assert coords0 == pytest.approx((-122.36438, 37.82466, 0.0), 5)
    assert f.properties["name"] == f["properties"]["name"] == "linestring"
    assert f.properties["snippet"] == f["properties"]["snippet"] == "LineString test"
    assert (
        f.properties["description"]
        == f["properties"]["description"]
        == "Blah, blah, blah"
    )


def test_polygon(placemarks):
    f = feature(placemarks[2])
    assert f.geometry.type == f["geometry"]["type"] == "Polygon"
    coords0 = f.geometry.coordinates[0][0]
    assert coords0 == pytest.approx((-122.366278, 37.81884, 30.0), 5)
    assert f.properties["name"] == f["properties"]["name"] == "polygon"
    assert f.properties["snippet"] == f["properties"]["snippet"] == "Polygon test"
    assert (
        f.properties["description"]
        == f["properties"]["description"]
        == "Blah, blah, blah"
    )
    coords1 = f.geometry.coordinates[1][0]
    assert coords1 == pytest.approx((-122.366212, 37.818977, 30.0), 5)
