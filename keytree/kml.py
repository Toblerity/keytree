"""
Functions and factories for KML elements
"""

from typing import Mapping, Dict

import keytree.compat
from keytree.model import NSMAP


def kml_ns(element) -> str:
    return element.tag.split("}")[0][1:]


def kml_ns_map(element) -> Dict:
    """Returns an nsmap-style dict detected from the given element
    """
    return {"": element.tag.split("}")[0][1:]}


def findall_placemarks(element, kml_ns: Mapping = NSMAP) -> list:
    """Returns a list of Placemark elements that are children of the given element
    """
    return element.findall(".//kml:Placemark", namespaces=kml_ns)


def element(context, ob, **kw):
    """Make a KML element from an object that provides the Python geo
    interface.

    Calls context.makeelement and fleshes out the new element using properties
    of the object or keyword arguments.

    KML Placemark names derive from object 'title' properties or a 'name'
    argument. Snippets derive from object 'summary' properties or a 'snippet'
    argument. Descriptions derive from object 'content' properties or a
    'description' argument.

    Example:

      >>> kml = '<kml xmlns="http://www.opengis.net/kml/2.2"><Document></Document></kml>'
      >>> from xml.etree import ElementTree
      >>> tree = ElementTree.fromstring(kml)
      >>> doc = tree[0]
      >>> doc # doctest: +ELLIPSIS
      <Element {http://www.opengis.net/kml/2.2}Document at ...>

    First, with a geometry:

      >>> from keytree.kml import element
      >>> from keytree.model import Geometry
      >>> g = Geometry('Point', (0.0, 0.0))
      >>> elem = element(doc, g)
      >>> import pprint
      >>> pprint.pprint((elem.tag, elem.text, list(elem))) # doctest: +ELLIPSIS
      ('{http://www.opengis.net/kml/2.2}Point',
       None,
       [<Element {http://www.opengis.net/kml/2.2}coordinates at ...>])

    Placemark:

      >>> from keytree.model import Feature
      >>> f = Feature('1', geometry=g, title='Feature 1', summary='The first feature', content='Blah, blah, blah.')
      >>> elem = element(doc, f)
      >>> import pprint
      >>> pprint.pprint((elem.tag, elem.text, list(elem))) # doctest: +ELLIPSIS
      ('{http://www.opengis.net/kml/2.2}Placemark',
       None,
       [<Element {http://www.opengis.net/kml/2.2}name at ...>,
        <Element {http://www.opengis.net/kml/2.2}Snippet at ...>,
        <Element {http://www.opengis.net/kml/2.2}description at ...>,
        <Element {http://www.opengis.net/kml/2.2}Point at ...>])
      >>> pprint.pprint(list((e.tag, e.text, list(e)) for e in elem)) # doctest: +ELLIPSIS
      [('{http://www.opengis.net/kml/2.2}name', 'Feature 1', []),
       ('{http://www.opengis.net/kml/2.2}Snippet', 'The first feature', []),
       ('{http://www.opengis.net/kml/2.2}description', 'Blah, blah, blah.', []),
       ('{http://www.opengis.net/kml/2.2}Point',
        None,
        [<Element {http://www.opengis.net/kml/2.2}coordinates at ...>])]

    """
    ns = context.tag.split("}")[0][1:]
    geo = getattr(ob, "__geo_interface__", ob)
    if "geometry" in geo:  # is a feature
        elem = placemark_element(context, ns, geo, **kw)
    elif "coordinates" in geo:  # is a geometry
        elem = geometry_element(context, ns, geo)
    return elem


def subelement(parent, ob, **kw):
    """Append new element to the parent element.
    """
    parent.append(element(parent, ob, **kw))


def coords_to_kml(geom):
    gtype = geom["type"]
    if gtype == "Point":
        coords = (geom["coordinates"],)
    elif gtype == "Polygon":
        coords = geom["coordinates"][0]
    else:
        coords = geom["coordinates"]
    if len(coords[0]) == 2:
        tuples = ("%f,%f,0.0" % tuple(c) for c in coords)
    elif len(coords[0]) == 3:
        tuples = ("%f,%f,%f" % tuple(c) for c in coords)
    else:
        raise ValueError("Invalid dimensions")
    return " ".join(tuples)


def geometry_element(context, ns, ob):
    gtype = ob["type"]
    geom_elem = context.makeelement("{%s}%s" % (ns, gtype), {})
    if gtype in ["Point", "LineString"]:
        sub_coords_elem = context.makeelement("{%s}coordinates" % ns, {})
        sub_coords_elem.text = coords_to_kml(ob)
    else:
        pass
    geom_elem.append(sub_coords_elem)
    return geom_elem


def placemark_element(context, ns, ob, **kw):
    pm_elem = context.makeelement("{%s}Placemark" % ns, {})
    pm_elem.attrib["id"] = ob.get("id") or kw.get("id")
    sub_name_elem = context.makeelement("{%s}name" % ns, {})
    sub_name_elem.text = kw.get("name") or ob.get("properties", {}).get("title")
    pm_elem.append(sub_name_elem)
    sub_snippet_elem = context.makeelement("{%s}Snippet" % ns, {})
    sub_snippet_elem.text = kw.get("snippet") or ob.get("properties", {}).get(
        "description"
    )
    pm_elem.append(sub_snippet_elem)
    sub_description_elem = context.makeelement("{%s}description" % ns, {})
    sub_description_elem.text = kw.get("description") or ob.get("properties", {}).get(
        "content"
    )
    pm_elem.append(sub_description_elem)
    if "geometry" in ob:
        sub_geom_elem = geometry_element(context, ns, ob.get("geometry"))
        pm_elem.append(sub_geom_elem)
    return pm_elem
