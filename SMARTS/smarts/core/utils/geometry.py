                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

from shapely.geometry import LineString, MultiPolygon, Polygon
from shapely.geometry.base import CAP_STYLE, JOIN_STYLE
from shapely.ops import triangulate


def buffered_shape(shape, width: float = 1.0) -> Polygon:
    """Generates a shape with a buffer of `width` around the original shape."""
    ls = LineString(shape).buffer(
        width / 2,
        1,
        cap_style=CAP_STYLE.flat,
        join_style=JOIN_STYLE.round,
        mitre_limit=5.0,
    )
    if isinstance(ls, MultiPolygon):
                                                                                                  
        ls = ls.convex_hull
    elif not isinstance(ls, Polygon):
        raise RuntimeError("Shapely `object.buffer` behavior may have changed.")
    return ls


def triangulate_polygon(polygon: Polygon):
    """Attempts to convert a polygon into triangles."""
                                                                              
    return [
        tri_face
        for tri_face in triangulate(polygon)
        if tri_face.centroid.within(polygon)
    ]
