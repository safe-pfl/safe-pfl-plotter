from scipy.spatial.distance import cosine


def cosine_distance(u, v):
    """
    Calculates the cosine distance between two vectors.

    Args:
        u (array-like): First input vector.

        v (array-like): Second input vector.

    Returns:
        str: The cosine distance between u and v, formatted to two decimal places.
             Returns "1.00" if either input vector is all zeros, as cosine distance is undefined in this case.

    Raises:
        TypeError: If inputs are not array-like.
        ValueError: If input vectors have different lengths.
        Exception: if any other exception occurs during cosine calculation.

    Example:
        >>> cosine_distance([1, 0, 0], [0, 1, 0])
        '1.00'
        >>> cosine_distance([1, 0, 0], [1, 0, 0])
        '0.00'
        >>> cosine_distance([1, 2, 3], [4, 5, 6])
        '0.02'
    """

    try:
        distance = cosine(u, v)
        if distance is not None:
            return distance
        else:
            return "1.00"
    except TypeError as e:
        raise TypeError(f"Input vectors must be array-like: {e}")
    except ValueError as e:
        raise ValueError(f"Input vectors must have the same length: {e}")
    except Exception as e:
        raise Exception(f"An error occurred during cosine distance calculation: {e}")
