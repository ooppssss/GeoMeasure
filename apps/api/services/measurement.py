from shapely.geometry import Polygon, LineString, Point


def calculate_measurement(geometry):
    """
    Calculate the measurement for a geometry.

    Polygon    -> area
    LineString -> length
    Point      -> no measurement
    """

    if isinstance(geometry, Polygon):
        return {
            "measurement_type": "area",
            "value": geometry.area,
            "unit": "square_meters",
        }

    if isinstance(geometry, LineString):
        return {
            "measurement_type": "length",
            "value": geometry.length,
            "unit": "meters",
        }

    if isinstance(geometry, Point):
        return {
            "measurement_type": None,
            "value": None,
            "unit": None,
        }

    return {
        "measurement_type": None,
        "value": None,
        "unit": None,
    }