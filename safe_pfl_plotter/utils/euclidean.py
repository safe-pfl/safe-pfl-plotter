import numpy as np


def euclidean_distance(u, v):
    """
    Calculates the Euclidean distance between two vectors.

    Args:
        u (array-like): The first input vector.
        v (array-like): The second input vector.

    Returns:
        float: The Euclidean distance between u and v.

    Raises:
        TypeError: If inputs are not array-like.
        ValueError: If input vectors have different lengths.

    Example:
        >>> euclidean_distance([0, 0], [3, 4])
        5.0
        >>> euclidean_distance([1, 2, 3], [4, 5, 6])
        5.196152422706632
    """
    try:
        u = np.asarray(u)
        v = np.asarray(v)
        if len(u) != len(v):
            raise ValueError("Input vectors must have the same length.")
        distance = np.linalg.norm(u - v)
        return distance
    except TypeError:
        raise TypeError(
            "Input vectors must be array-like (e.g., list, tuple, numpy array)."
        )
