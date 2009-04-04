
def element(context, ob, **kw):
    """Make a KML element by calling context.makeelement and fleshing it out
    with data from the provided object and keyword arguments.
    
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
      >>> ElementTree.tostring(elem)
      '<Point><coordinates>0.000000,0.000000,0.0</coordinates></Point>'
    
    Placemark:
      
      >>> from keytree.model import Feature
      >>> f = Feature('1', geometry=g, title='Feature 1', summary='The first feature', content='Blah, blah, blah.')
      >>> elem = element(doc, f)
      >>> list(elem) # doctest: +ELLIPSIS
      [<Element name at ...>, <Element Snippet at ...>, <Element description at ...>, <Element Point at ...>]
      >>> ElementTree.tostring(elem)
      '<Placemark id="1"><name>Feature 1</name><Snippet>The first feature</Snippet><description>Blah, blah, blah.</description><Point><coordinates>0.000000,0.000000,0.0</coordinates></Point></Placemark>'
      
    """
    ns = context.tag.split('}')[0][1:]
    geo = getattr(ob, '__geo_interface__') or ob
    if geo.has_key('id') or geo.has_key('geometry'): # is a feature
        elem = placemark_element(context, geo, **kw)
    elif geo.has_key('type'): # is a geometry
        elem = geometry_element(context, geo)
    return elem

def coords_to_kml(geom):
    gtype = geom['type']
    if gtype == 'Point':
        coords = (geom['coordinates'],)
    elif gtype == 'Polygon':
        coords = geom['coordinates'][0]
    else:
        coords = geom['coordinates']
    if len(coords[0]) == 2:
        tuples = ('%f,%f,0.0' % tuple(c) for c in coords)
    elif len(coords[0]) == 3:
        tuples = ('%f,%f,%f' % tuple(c) for c in coords)
    else:
        raise ValueError, "Invalid dimensions"
    return ' '.join(tuples)

def geometry_element(context, ob):
    gtype = ob['type']
    geom_elem = context.makeelement(gtype, {})
    if gtype in ['Point', 'LineString']:
        sub_coords_elem = context.makeelement('coordinates', {})
        sub_coords_elem.text = coords_to_kml(ob)
    else:
        pass
    geom_elem.append(sub_coords_elem)
    return geom_elem

def placemark_element(context, ob, **kw):
    pm_elem = context.makeelement('Placemark', {})
    pm_elem.attrib['id'] = ob.get('id') or kw.get('id')
    sub_name_elem = context.makeelement('name', {})
    sub_name_elem.text = ob.get('properties', {}).get('title') or kw.get('name')
    pm_elem.append(sub_name_elem)
    sub_snippet_elem = context.makeelement('Snippet', {})
    sub_snippet_elem.text = ob.get('properties', {}).get('summary') or kw.get('snippet')
    pm_elem.append(sub_snippet_elem)
    sub_description_elem = context.makeelement('description', {})
    sub_description_elem.text = ob.get('properties', {}).get('content') or kw.get('description')
    pm_elem.append(sub_description_elem)
    if ob.has_key('geometry'):
        sub_geom_elem = geometry_element(context, ob.get('geometry'))
        pm_elem.append(sub_geom_elem)
    return pm_elem
