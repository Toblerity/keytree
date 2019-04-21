Eaze Fork
=======

The version of Keytree on PyPi has some minor syntax errors that make it incompatible with Python 3. This fork is a (hopefully temporary) workaround so that we can use it. Ideally we'll want to contribute these changes back into the main Keytree codebase.

Keytree
=======

Keytree provides functions for reading and writing KML using the ElementTree
API. 

Reading KML
-----------

KML Placemark elements can be adapted to the Python geo interface and then used
with packages like Shapely_::

  >>> data = """<?xml version="1.0" encoding="UTF-8"?>
  ... <kml xmlns="http://www.opengis.net/kml/2.2">
  ...   <Document>
  ...     <Placemark id="pm_1">
  ...       <name>point</name>
  ...       <Snippet>Point test</Snippet>
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
  >>> doc = ElementTree.fromstring(data)
  >>> kmlns = doc.tag.split('}')[0][1:]
  >>> placemarks = doc.findall('*/{%s}Placemark' % kmlns)
  >>> p0 = placemarks[0]
  >>> import keytree
  >>> f = keytree.feature(p0)
  >>> print f.id, f.properties.name, f.properties.snippet
  pm_1, point, Point test
  >>> 
  >>> from shapely.geometry import shape
  >>> s = shape(f.geometry)
  >>> print s.buffer(1.5).exterior.length
  9.4209934708642571

Writing KML
-----------

Objects that provide the Python geo interface can also be converted to
ElementTree API Elements::

  >>> f = {
  ...     'id': 'pm_2', 
  ...     'geometry': {
  ...         'type': 'Point', 
  ...         'coordinates': (-122.364383, 37.824663999999999) },
  ...     'properties': {
  ...         'title': 'Feature 2', 
  ...         'description': 'The second feature', }

The first argument to the keytree.element function is an XML context, the
created element will have the same namespace as that element::

  >>> data = """<?xml version="1.0" encoding="UTF-8"?>
  ... <kml xmlns="http://www.opengis.net/kml/2.2">
  ...   <Document>
  ...   </Document>
  ... </kml>
  ... """
  >>> doc = ElementTree.fromstring(data)
  >>> elem = element(doc, f)
  >>> print elem
  <Element {http://www.opengis.net/kml/2.2}Placemark at ...>
  >>> pprint(list(elem))
  [<Element {http://www.opengis.net/kml/2.2}name at ...>,
   <Element {http://www.opengis.net/kml/2.2}Snippet at ...>,
   <Element {http://www.opengis.net/kml/2.2}description at ...>,
   <Element {http://www.opengis.net/kml/2.2}Point at ...>]

The created element is not automatically added to the KML context and must be
appended to its proper Document or Folder::

  >>> doc[0].append(elem)
  >>> print etree.tostring(doc)
  <ns0:kml xmlns:ns0="http://www.opengis.net/kml/2.2">
    <ns0:Document>
      <ns0:Placemark id="pm_2">
        <ns0:name>Number 2</ns0:name>
        <ns0:Snippet>Placemark number 2</ns0:Snippet>
        <ns0:description />
        <ns0:Point>
          <ns0:coordinates>0.000000,0.000000,0.0</ns0:coordinates>
        </ns0:Point>
      </ns0:Placemark>
    </ns0:Document>
  </ns0:kml>

KML Helpers
-----------

The keytree.kml module contains a few useful utility functions::

  >>> from keytree.kml import kml_ns, findall_placemarks
  >>> print kml_ns(doc)
  {http://www.opengis.net/kml/2.2}
  >>> findall_placemarks(doc)
  [<Element {http://www.opengis.net/kml/2.2}Placemark at ...>]

.. _Shapely: http://pypi.python.org/pypi/Shapely

