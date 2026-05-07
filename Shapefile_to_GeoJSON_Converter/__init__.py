
def classFactory(iface):
    from .shapefile_to_geojson import ShapeToGeoJSON
    return ShapeToGeoJSON(iface)
