class Isometry:
    scale_factor = 0.5


def cartesian_to_isometric(coordinate: tuple[float, float]) -> tuple[float, float]:
    """
    Convert 2D Cartesian coordinates (x, y) to isometric coordinates.
    """
    x_iso = coordinate[0] - coordinate[1]
    y_iso = (coordinate[0] + coordinate[1]) * Isometry.scale_factor
    return x_iso, y_iso


def isometric_to_cartesian(coordinate: tuple[float, float]) -> tuple[float, float]:
    """
    Convert isometric coordinates (x_iso, y_iso) back to Cartesian coordinates.
    """
    x = (coordinate[0] / 2) + coordinate[1] / (Isometry.scale_factor * 2)
    y = coordinate[1] / (Isometry.scale_factor * 2) - (coordinate[0] / 2)
    return x, y
