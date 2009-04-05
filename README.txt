Keytree
=======

Keytree provides several functions for manipulating KML using the ElementTree API. Elements can be adapted to the Python geo interface and then used with packages like Shapely_::

  >>> data = """<?xml version="1.0" encoding="UTF-8"?>
  ... <kml xmlns="http://www.opengis.net/kml/2.2">
  ...   <Document>
  ...     <Placemark>
  ...       <name>point</name>
  ...       <description>Point test</description>
  ...       <Point>
  ...         <coordinates>
  ...           -122.364383,37.824664,0
  ...         </coordinates>
  ...       </Point>
  ...     </Placemark>
  ...   </Document>
  ... </kml>
  ... """
  >>> from xml.etree import ElementTree
  >>> tree = ElementTree.fromstring(data)
  >>> kmlns = tree.tag.split('}')[0][1:]
  >>> placemarks = tree.findall('*/{%s}Placemark' % kmlns)
  >>> p0 = placemarks[0]
  >>> import keytree
  >>> f = keytree.feature(p0)
  >>> from shapely.geometry import asShape
  >>> shape = asShape(f.geometry)
  >>> shape.buffer(1.5).exterior.length
  9.4209934708642571

Objects like those from geojson_ that provide the Python geo interface can also be converted to ElementTree API Elements::

  >>> from geojson import Feature
  >>> f = Feature('1', 
  ...             geometry={
  ...                 'type': 'Point', 
  ...                 'coordinates': (-122.364383, 37.824663999999999)
  ...                 },
  ...             title='Feature 1', 
  ...             summary='The first feature', 
  ...             content='Blah, blah, blah.'
  ...             )

A Shapely (or geojson) geometry could also be used in place of the dict::

  >>> from shapely.geometry import Point
  >>> f = Feature('1', 
  ...             geometry=Point(-122.364383, 37.824664),
  ...             title='Feature 1', 
  ...             summary='The first feature', 
  ...             content='Blah, blah, blah.'
  ...             )
  
The first argument to the keytree.element function is an XML context, the created element will have the same namespace as that element::

  >>> elem = keytree.element(tree, f)
  >>> import pprint
  >>> pprint.pprint((elem.tag, elem.text, list(elem)))
  ('{http://www.opengis.net/kml/2.2}Placemark',
   None,
   [<Element {http://www.opengis.net/kml/2.2}name at ...>,
    <Element {http://www.opengis.net/kml/2.2}Snippet at ...>,
    <Element {http://www.opengis.net/kml/2.2}description at ...>,
    <Element {http://www.opengis.net/kml/2.2}Point at ...>])
  >>> pprint.pprint(list((e.tag, e.text, list(e)) for e in elem))
  [('{http://www.opengis.net/kml/2.2}name', 'Feature 1', []),
   ('{http://www.opengis.net/kml/2.2}Snippet', 'The first feature', []),
   ('{http://www.opengis.net/kml/2.2}description', 'Blah, blah, blah.', []),
   ('{http://www.opengis.net/kml/2.2}Point',
    None, 
    [<{http://www.opengis.net/kml/2.2}Element coordinates at ...>])]
  
.. _Shapely: http://pypi.python.org/pypi/Shapely
.. _geojson: http://pypi.python.org/pypi/geojson



