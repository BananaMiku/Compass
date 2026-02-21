import math

EARTH_RADIUS = 6371000  # in meters


def lat_lng_to_cartesian(coords, radius=EARTH_RADIUS):
    """Convert latitude and longitude to Cartesian coordinates.
    Returns a tuple of `(x, y, z)` in meters.
    `coords` is a dict with the shape `{"lat": float, "lng": float}`.
    `radius` is the radius of the sphere in meters.
    """

    lat_rad = math.radians(coords["lat"])
    lng_rad = math.radians(coords["lng"])

    x = radius * math.cos(lat_rad) * math.cos(lng_rad)
    y = radius * math.cos(lat_rad) * math.sin(lng_rad)
    z = radius * math.sin(lat_rad)

    return (x, y, z)


def get_distance(a, b):
    """Calculate the distance between two points `a` and `b` in meters.
    Note that this calculates the straight-line distance through the Earth, not the surface distance, but this is good enough for nearby locations.
    Returns infinity if either is None.
    `a` and `b` are both dicts with the shape `{"lat": float, "lng": float}`.
    """

    if a is None or b is None:
        return float("inf")

    cartesian_a = lat_lng_to_cartesian(a)
    cartesian_b = lat_lng_to_cartesian(b)

    return math.sqrt(
        (cartesian_b[0] - cartesian_a[0]) ** 2
        + (cartesian_b[1] - cartesian_a[1]) ** 2
        + (cartesian_b[2] - cartesian_a[2]) ** 2
    )


def project(a, b):
    """Project a vector onto another vector.
    Returns the projection of `a` onto `b`, which is the component of `a` that is parallel to `b`.
    Both `a` and `b` are tuples of `(x, y, z)`.
    """

    b_length_squared = b[0] ** 2 + b[1] ** 2 + b[2] ** 2
    if b_length_squared == 0:
        return (0, 0, 0)

    projection_factor = (a[0] * b[0] + a[1] * b[1] + a[2] * b[2]) / b_length_squared

    return (
        projection_factor * b[0],
        projection_factor * b[1],
        projection_factor * b[2],
    )


def project_perp(a, b):
    """Project a vector out of another vector.
    Returns the projection of `a` out of `b`, which is the component of `a` that is perpendicular to `b`.
    Both `a` and `b` are tuples of `(x, y, z)`.
    """

    projection_parallel = project(a, b)
    return (
        a[0] - projection_parallel[0],
        a[1] - projection_parallel[1],
        a[2] - projection_parallel[2],
    )


def normalize(v):
    """Normalize a vector to have length 1.
    Returns the normalized vector, which has the same direction as `v` but a length of 1.
    `v` is a tuple of `(x, y, z)`.
    """

    length = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    if length == 0:
        return (0, 0, 0)

    return (v[0] / length, v[1] / length, v[2] / length)


def get_bearing(a, b):
    """Calculate the bearing from point `a` to point `b` in degrees.
    Returns None if either is None.
    The bearing is the number of degrees clockwise from the north direction to the direction from `a` to `b`.
    `a` and `b` are both dicts with the shape `{"lat": float, "lng": float}`.
    """

    if a is None or b is None:
        return None

    cartesian_a = lat_lng_to_cartesian(a)
    cartesian_b = lat_lng_to_cartesian(b)

    north_tangent = lat_lng_to_cartesian(
        {"lat": a["lat"] + 90, "lng": a["lng"]}, radius=1
    )
    east_tangent = lat_lng_to_cartesian({"lat": 0, "lng": a["lng"] + 90}, radius=1)

    bearing_vector = normalize(
        project_perp(
            (
                cartesian_b[0] - cartesian_a[0],
                cartesian_b[1] - cartesian_a[1],
                cartesian_b[2] - cartesian_a[2],
            ),
            cartesian_a,
        )
    )

    north_component = (
        bearing_vector[0] * north_tangent[0]
        + bearing_vector[1] * north_tangent[1]
        + bearing_vector[2] * north_tangent[2]
    )
    east_component = (
        bearing_vector[0] * east_tangent[0]
        + bearing_vector[1] * east_tangent[1]
        + bearing_vector[2] * east_tangent[2]
    )

    return (math.degrees(math.atan2(east_component, north_component)) + 360) % 360
