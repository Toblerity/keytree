Keytree
=======

Keytree provides several functions for manipulating KML using the ElementTree API. Elements can be adapted to the Python geo interface and then used with packages like Shapely::

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

Objects that provide the Python geo interface can also be converted to ElementTree API Elements::

  >>> from geojson import Feature
  >>> f = Feature('1', geometry={'type': 'Point', 'coordinates': (-122.364383, 37.824663999999999)}, title='Feature 1', summary='The first feature', content='Blah, blah, blah.')
  
The first argument to the keytree.element function is an XML context, the created element will have the same namespaces as that element::

  >>> elem = keytree.element(tree, f)
  >>> print list(elem)
  [<Element name at ...>, <Element Snippet at ...>, <Element description at ...>, <Element Point at ...>]
  >>> ElementTree.tostring(elem)
  '<Placemark id="1"><name>Feature 1</name><Snippet>The first feature</Snippet><description>Blah, blah, blah.</description><Point><coordinates>0.000000,0.000000,0.0</coordinates></Point></Placemark>'
  




