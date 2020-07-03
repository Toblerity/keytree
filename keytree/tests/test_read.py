import pytest

from keytree import feature, kml

KML = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">
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
      <name>track</name>
      <Snippet>Track test</Snippet>
      <description>Blah, blah, blah</description>
      <gx:Track>
        <when>2020-12-13T07:33:02.94Z</when>
        <when>2020-12-13T07:33:04.04Z</when>
        <gx:coord>-122.364403 37.824664 0</gx:coord>
        <gx:coord>-122.364172 37.824322 0</gx:coord>
      </gx:Track>
    </Placemark>
    <Placemark>
      <name>multitrack</name>
      <Snippet>MultiTrack test</Snippet>
      <description>Blah, blah, blah</description>
      <gx:MultiTrack>
        <gx:Track>
          <when>2020-12-13T07:33:02.94Z</when>
          <when>2020-12-13T07:33:04.04Z</when>
          <gx:coord>-122.364423 37.824664 0</gx:coord>
          <gx:coord>-122.364192 37.824322 0</gx:coord>
        </gx:Track>
        <gx:Track>
          <when>2020-12-13T07:33:02.94Z</when>
          <when>2020-12-13T07:33:04.04Z</when>
          <gx:coord>-122.364463 37.824664 0</gx:coord>
          <gx:coord>-122.364212 37.824322 0</gx:coord>
        </gx:Track>
      </gx:MultiTrack>
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
    <Placemark>
      <name>multigeometry</name>
      <Snippet>MultiGeometry Lines</Snippet>
      <description>Blah, blah, blah</description>
      <MultiGeometry>
        <LineString>
          <coordinates>
            -122.364483,37.824664,0 -122.364252,37.824322,0 
          </coordinates>
        </LineString>
        <LineString>
          <coordinates>
            -122.364503,37.824664,0 -122.364272,37.824322,0 
          </coordinates>
        </LineString>
      </MultiGeometry>
    </Placemark>
  </Document>
</kml>
""".encode()  # lxml doesn't like unencoded strings with an encoding declaration


@pytest.fixture
def doc(etree):
    return etree.fromstring(KML)


@pytest.fixture
def placemarks(doc):
    return kml.findall_placemarks(doc)


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


def test_track(placemarks):
    f = feature(placemarks[2])
    assert f.geometry.type == f["geometry"]["type"] == "LineString"
    coords0 = f.geometry.coordinates[0]
    assert coords0 == pytest.approx((-122.36438, 37.82466, 0.0), 5)
    assert f.properties["name"] == f["properties"]["name"] == "track"
    assert f.properties["snippet"] == f["properties"]["snippet"] == "Track test"
    assert (
        f.properties["description"]
        == f["properties"]["description"]
        == "Blah, blah, blah"
    )


def test_multitrack(placemarks):
    f = feature(placemarks[3])
    assert f.geometry.type == f["geometry"]["type"] == "MultiLineString"


def test_polygon(placemarks):
    f = feature(placemarks[4])
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


def test_multilinestring(placemarks):
    f = feature(placemarks[5])
    assert f.geometry.type == f["geometry"]["type"] == "MultiLineString"
