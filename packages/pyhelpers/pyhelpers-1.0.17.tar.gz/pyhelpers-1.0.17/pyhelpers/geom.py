""" Geometry-related utilities """

import functools
import math

import numpy as np


# Convert British national grid (OSGB36) to latitude and longitude (WGS84)
def osgb36_to_wgs84(easting, northing):
    """
    :param easting: [numbers.Number]
    :param northing: [numbers.Number]
    :return: [tuple] (numbers.Number, numbers.Number)

    Convert British National grid coordinates (OSGB36 Easting, Northing) to WGS84 latitude and longitude.

    Testing e.g.
        easting, northing = 530034, 180381  # osgb36_to_wgs84(easting, northing) == (-0.12772404, 51.507407)
    """
    import pyproj
    osgb36 = pyproj.Proj(init='EPSG:27700')  # UK Ordnance Survey, 1936 datum
    wgs84 = pyproj.Proj(init='EPSG:4326')  # LonLat with WGS84 datum used by GPS units and Google Earth
    longitude, latitude = pyproj.transform(osgb36, wgs84, easting, northing)
    return longitude, latitude


# Convert latitude and longitude (WGS84) to British national grid (OSGB36)
def wgs84_to_osgb36(longitude, latitude):
    """
    :param longitude: [numbers.Number]
    :param latitude: [numbers.Number]
    :return: [tuple] ([numbers.Number], [numbers.Number])

    Converts coordinates from WGS84 (latitude, longitude) to British National grid (OSGB36) (easting, northing).

    Testing e.g.
        longitude, latitude = -0.12772404, 51.507407  # wgs84_to_osgb36(longitude, latitude) == (530034, 180381)
    """
    import pyproj
    wgs84 = pyproj.Proj(init='EPSG:4326')  # LonLat with WGS84 datum used by GPS units and Google Earth
    osgb36 = pyproj.Proj(init='EPSG:27700')  # UK Ordnance Survey, 1936 datum
    easting, northing = pyproj.transform(wgs84, osgb36, longitude, latitude)
    return easting, northing


# Convert british national grid (OSGB36) to latitude and longitude (WGS84) by calculation
def osgb36_to_wgs84_calc(easting, northing):
    """
    :param easting: [numbers.Number]
    :param northing: [numbers.Number]
    :return: [tuple] (numbers.Number, numbers.Number)

    The code below was copied/modified from:
    http://www.hannahfry.co.uk/blog/2012/02/01/converting-british-national-grid-to-latitude-and-longitude-ii
    """
    # The Airy 180 semi-major and semi-minor axes used for OSGB36 (m)
    a, b = 6377563.396, 6356256.909
    # Scale factor on the central meridian
    f0 = 0.9996012717
    # Latitude of true origin (radians)
    lat0 = 49 * np.pi / 180
    # Longitude of true origin and central meridian (radians):
    lon0 = -2 * np.pi / 180
    # Northing and Easting of true origin (m):
    n0, e0 = -100000, 400000
    e2 = 1 - (b * b) / (a * a)  # eccentricity squared
    n = (a - b) / (a + b)

    # Initialise the iterative variables
    lat, m = lat0, 0

    while northing - n0 - m >= 0.00001:  # Accurate to 0.01mm
        lat += (northing - n0 - m) / (a * f0)
        m1 = (1 + n + (5. / 4) * n ** 2 + (5. / 4) * n ** 3) * (lat - lat0)
        m2 = (3 * n + 3 * n ** 2 + (21. / 8) * n ** 3) * np.sin(lat - lat0) * np.cos(lat + lat0)
        m3 = ((15. / 8) * n ** 2 + (15. / 8) * n ** 3) * np.sin(2 * (lat - lat0)) * np.cos(2 * (lat + lat0))
        m4 = (35. / 24) * n ** 3 * np.sin(3 * (lat - lat0)) * np.cos(3 * (lat + lat0))
        # meridional arc
        m = b * f0 * (m1 - m2 + m3 - m4)

    # transverse radius of curvature
    nu = a * f0 / np.sqrt(1 - e2 * np.sin(lat) ** 2)

    # meridional radius of curvature
    rho = a * f0 * (1 - e2) * (1 - e2 * np.sin(lat) ** 2) ** (-1.5)
    eta2 = nu / rho - 1

    sec_lat = 1. / np.cos(lat)
    vii = np.tan(lat) / (2 * rho * nu)
    viii = np.tan(lat) / (24 * rho * nu ** 3) * (5 + 3 * np.tan(lat) ** 2 + eta2 - 9 * np.tan(lat) ** 2 * eta2)
    ix = np.tan(lat) / (720 * rho * nu ** 5) * (61 + 90 * np.tan(lat) ** 2 + 45 * np.tan(lat) ** 4)
    x = sec_lat / nu
    xi = sec_lat / (6 * nu ** 3) * (nu / rho + 2 * np.tan(lat) ** 2)
    xii = sec_lat / (120 * nu ** 5) * (5 + 28 * np.tan(lat) ** 2 + 24 * np.tan(lat) ** 4)
    xiia = sec_lat / (5040 * nu ** 7) * (61 + 662 * np.tan(lat) ** 2 + 1320 * np.tan(lat) ** 4 + 720 * np.tan(lat) ** 6)
    de = easting - e0

    # These are on the wrong ellipsoid currently: Airy1830. (Denoted by _1)
    lat_1 = lat - vii * de ** 2 + viii * de ** 4 - ix * de ** 6
    lon_1 = lon0 + x * de - xi * de ** 3 + xii * de ** 5 - xiia * de ** 7

    """ Want to convert to the GRS80 ellipsoid. """
    # First convert to cartesian from spherical polar coordinates
    h = 0  # Third spherical coord.
    x_1 = (nu / f0 + h) * np.cos(lat_1) * np.cos(lon_1)
    y_1 = (nu / f0 + h) * np.cos(lat_1) * np.sin(lon_1)
    z_1 = ((1 - e2) * nu / f0 + h) * np.sin(lat_1)

    # Perform Helmut transform (to go between Airy 1830 (_1) and GRS80 (_2))
    s = -20.4894 * 10 ** -6  # The scale factor -1
    # The translations along x,y,z axes respectively
    tx, ty, tz = 446.448, -125.157, + 542.060
    # The rotations along x,y,z respectively, in seconds
    rxs, rys, rzs = 0.1502, 0.2470, 0.8421
    rx, ry, rz = rxs * np.pi / (180 * 3600.), rys * np.pi / (180 * 3600.), rzs * np.pi / (180 * 3600.)  # In radians
    x_2 = tx + (1 + s) * x_1 + (-rz) * y_1 + ry * z_1
    y_2 = ty + rz * x_1 + (1 + s) * y_1 + (-rx) * z_1
    z_2 = tz + (-ry) * x_1 + rx * y_1 + (1 + s) * z_1

    # Back to spherical polar coordinates from cartesian
    # Need some of the characteristics of the new ellipsoid
    # The GSR80 semi-major and semi-minor axes used for WGS84(m)
    a_2, b_2 = 6378137.000, 6356752.3141
    e2_2 = 1 - (b_2 * b_2) / (a_2 * a_2)  # The eccentricity of the GRS80 ellipsoid
    p = np.sqrt(x_2 ** 2 + y_2 ** 2)

    # Lat is obtained by an iterative procedure:
    lat = np.arctan2(z_2, (p * (1 - e2_2)))  # Initial value
    lat_old = 2 * np.pi
    while abs(lat - lat_old) > 10 ** -16:
        lat, lat_old = lat_old, lat
        nu_2 = a_2 / np.sqrt(1 - e2_2 * np.sin(lat_old) ** 2)
        lat = np.arctan2(z_2 + e2_2 * nu_2 * np.sin(lat_old), p)

    # Lon and height are then pretty easy
    long = np.arctan2(y_2, x_2)
    # h = p / cos(lat) - nu_2

    # Print the results
    # print([(lat - lat_1) * 180 / pi, (lon - lon_1) * 180 / pi])

    # Convert to degrees
    long = long * 180 / np.pi
    lat = lat * 180 / np.pi

    return long, lat


# Convert latitude and longitude (WGS84) to British National Grid (OSGB36) by calculation
def wgs84_to_osgb36_calc(latitude, longitude):
    """
    :param longitude: [numbers.Number]
    :param latitude: [numbers.Number]
    :return: [tuple] ([numbers.Number], [numbers.Number])

    The code below was copied/modified from:
    http://www.hannahfry.co.uk/blog/2012/02/01/converting-latitude-and-longitude-to-british-national-grid
    """
    # First convert to radians. These are on the wrong ellipsoid currently: GRS80. (Denoted by _1)
    lon_1, lat_1 = longitude * np.pi / 180, latitude * np.pi / 180

    # Want to convert to the Airy 1830 ellipsoid, which has the following:
    # The GSR80 semi-major and semi-minor axes used for WGS84(m)
    a_1, b_1 = 6378137.000, 6356752.3141
    e2_1 = 1 - (b_1 * b_1) / (a_1 * a_1)  # The eccentricity of the GRS80 ellipsoid
    nu_1 = a_1 / np.sqrt(1 - e2_1 * np.sin(lat_1) ** 2)

    # First convert to cartesian from spherical polar coordinates
    h = 0  # Third spherical coord.
    x_1 = (nu_1 + h) * np.cos(lat_1) * np.cos(lon_1)
    y_1 = (nu_1 + h) * np.cos(lat_1) * np.sin(lon_1)
    z_1 = ((1 - e2_1) * nu_1 + h) * np.sin(lat_1)

    # Perform Helmut transform (to go between GRS80 (_1) and Airy 1830 (_2))
    s = 20.4894 * 10 ** -6  # The scale factor -1
    # The translations along x,y,z axes respectively:
    tx, ty, tz = -446.448, 125.157, -542.060
    # The rotations along x,y,z respectively, in seconds:
    rxs, rys, rzs = -0.1502, -0.2470, -0.8421
    rx, ry, rz = rxs * np.pi / (180 * 3600.), rys * np.pi / (180 * 3600.), rzs * np.pi / (180 * 3600.)  # In radians
    x_2 = tx + (1 + s) * x_1 + (-rz) * y_1 + ry * z_1
    y_2 = ty + rz * x_1 + (1 + s) * y_1 + (-rx) * z_1
    z_2 = tz + (-ry) * x_1 + rx * y_1 + (1 + s) * z_1

    # Back to spherical polar coordinates from cartesian
    # Need some of the characteristics of the new ellipsoid
    # The GSR80 semi-major and semi-minor axes used for WGS84(m)
    a, b = 6377563.396, 6356256.909
    e2 = 1 - (b * b) / (a * a)  # The eccentricity of the Airy 1830 ellipsoid
    p = np.sqrt(x_2 ** 2 + y_2 ** 2)

    # Lat is obtained by an iterative procedure:
    latitude = np.arctan2(z_2, (p * (1 - e2)))  # Initial value
    lat_old = 2 * np.pi
    nu = 0
    while abs(latitude - lat_old) > 10 ** -16:
        latitude, lat_old = lat_old, latitude
        nu = a / np.sqrt(1 - e2 * np.sin(lat_old) ** 2)
        latitude = np.arctan2(z_2 + e2 * nu * np.sin(lat_old), p)

    # Lon and height are then pretty easy
    longitude = np.arctan2(y_2, x_2)
    # h = p / cos(lat) - nu

    # e, n are the British national grid coordinates - easting and northing
    # scale factor on the central meridian
    f0 = 0.9996012717
    # Latitude of true origin (radians)
    lat0 = 49 * np.pi / 180
    # Longitude of true origin and central meridian (radians)
    lon0 = -2 * np.pi / 180
    # Northing & easting of true origin (m)
    n0, e0 = -100000, 400000
    y = (a - b) / (a + b)

    # meridional radius of curvature
    rho = a * f0 * (1 - e2) * (1 - e2 * np.sin(latitude) ** 2) ** (-1.5)
    eta2 = nu * f0 / rho - 1

    m1 = (1 + y + (5 / 4) * y ** 2 + (5 / 4) * y ** 3) * (latitude - lat0)
    m2 = (3 * y + 3 * y ** 2 + (21 / 8) * y ** 3) * np.sin(latitude - lat0) * np.cos(latitude + lat0)
    m3 = ((15 / 8) * y ** 2 + (15 / 8) * y ** 3) * np.sin(2 * (latitude - lat0)) * np.cos(2 * (latitude + lat0))
    m4 = (35 / 24) * y ** 3 * np.sin(3 * (latitude - lat0)) * np.cos(3 * (latitude + lat0))

    # meridional arc
    m = b * f0 * (m1 - m2 + m3 - m4)

    i = m + n0
    ii = nu * f0 * np.sin(latitude) * np.cos(latitude) / 2
    iii = nu * f0 * np.sin(latitude) * np.cos(latitude) ** 3 * (5 - np.tan(latitude) ** 2 + 9 * eta2) / 24
    iii_a = nu * f0 * np.sin(latitude) * np.cos(latitude) ** 5 * (
            61 - 58 * np.tan(latitude) ** 2 + np.tan(latitude) ** 4) / 720
    iv = nu * f0 * np.cos(latitude)
    v = nu * f0 * np.cos(latitude) ** 3 * (nu / rho - np.tan(latitude) ** 2) / 6
    vi = nu * f0 * np.cos(latitude) ** 5 * (
        5 - 18 * np.tan(latitude) ** 2 + np.tan(latitude) ** 4 + 14 * eta2 - 58 * eta2 * np.tan(latitude) ** 2) / 120

    y = i + ii * (longitude - lon0) ** 2 + iii * (longitude - lon0) ** 4 + iii_a * (longitude - lon0) ** 6
    x = e0 + iv * (longitude - lon0) + v * (longitude - lon0) ** 3 + vi * (longitude - lon0) ** 5

    return x, y


# Get the midpoint between <shapely.geometry.point.Point>s
def get_geometric_midpoint(pt_x, pt_y, as_geom=True):
    """
    :param pt_x: [shapely.geometry.point.Point]
    :param pt_y: [shapely.geometry.point.Point]
    :param as_geom: [bool] (default: True)
    :return: [tuple]
    """
    # assert isinstance(x_pt, shapely.geometry.point.Point)
    # assert isinstance(y_pt, shapely.geometry.point.Point)

    midpoint = (pt_x.x + pt_y.x) / 2, (pt_x.y + pt_y.y) / 2

    if as_geom:
        import shapely.geometry
        midpoint = shapely.geometry.Point(midpoint)

    return midpoint


# Get the midpoint between two points
def get_geometric_midpoint_along_earth_surface(pt_x, pt_y, as_geom=False):
    """
    :param pt_x: [shapely.geometry.point.Point]
    :param pt_y: [shapely.geometry.point.Point]
    :param as_geom: [bool] (default: False)
    :return: [tuple]

    References:
    http://code.activestate.com/recipes/577713-midpoint-of-two-gps-points/
    http://www.movable-type.co.uk/scripts/latlong.html
    """
    # Input values as degrees, convert them to radians
    lon_1, lat_1 = math.radians(pt_x.x), math.radians(pt_x.y)
    lon_2, lat_2 = math.radians(pt_y.x), math.radians(pt_y.y)

    b_x, b_y = math.cos(lat_2) * math.cos(lon_2 - lon_1), math.cos(lat_2) * math.sin(lon_2 - lon_1)
    lat_3 = math.atan2(
        math.sin(lat_1) + math.sin(lat_2), math.sqrt((math.cos(lat_1) + b_x) * (math.cos(lat_1) + b_x) + b_y ** 2))
    long_3 = lon_1 + math.atan2(b_y, math.cos(lat_1) + b_x)

    midpoint = math.degrees(long_3), math.degrees(lat_3)

    if as_geom:
        import shapely.geometry
        midpoint = shapely.geometry.Point(midpoint)

    return midpoint


# Calculate distance between two points
def calc_distance_on_unit_sphere(pt_x, pt_y):
    """
    :param pt_x: [shapely.geometry.point.Point]
    :param pt_y: [shapely.geometry.point.Point]
    :return: [float]

    This function was copied/changed from http://www.johndcook.com/blog/python_longitude_latitude/.

    It returns the distance between two locations based on each point's longitude and latitude.
    The distance returned is relative to Earth's radius. To get the distance in miles, multiply by 3960. To get the
    distance in kilometers, multiply by 6373.

    Latitude is measured in degrees north of the equator; southern locations have negative latitude. Similarly,
    longitude is measured in degrees east of the Prime Meridian. A location 10° west of the Prime Meridian,
    for example, could be expressed as either 350° east or as -10° east.

    The function assumes the earth is perfectly spherical. For a discussion of how accurate this assumption is,
    see http://www.johndcook.com/blog/2009/03/02/what-is-the-shape-of-the-earth/

    The algorithm used to calculate distances is described in detail at http://www.johndcook.com/lat_long_details.html

    A web page to calculate the distance between two cities based on longitude and latitude is available at
    http://www.johndcook.com/lat_long_distance.html
    """
    # Convert latitude and longitude to spherical coordinates in radians.
    degrees_to_radians = math.pi / 180.0

    # phi = 90 - latitude
    phi1 = (90.0 - pt_x.y) * degrees_to_radians
    phi2 = (90.0 - pt_y.y) * degrees_to_radians

    # theta = longitude
    theta1 = pt_x.x * degrees_to_radians
    theta2 = pt_y.x * degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) = sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cosine = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) + math.cos(phi1) * math.cos(phi2))
    arc = math.acos(cosine) * 3960  # in miles

    # Remember to multiply arc by the radius of the earth in your favorite set of units to get length.
    return arc


# Find the closest point of the given point to a list of points
def find_closest_point(pt, pts):
    """
    :param pt: [tuple] (lon, lat)
    :param pts: [iterable] a sequence of reference points
    :return: [tuple]
    """
    # Define a function calculating distance between two points
    def distance(o, d):
        """
        math.hypot(x, y) return the Euclidean norm, sqrt(x*x + y*y).
        This is the length of the vector from the origin to point (x, y).
        """
        return math.hypot(o[0] - d[0], o[1] - d[1])

    # Find the min value using the distance function with coord parameter
    return min(pts, key=functools.partial(distance, pt))
