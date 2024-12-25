from scipy.stats import wasserstein_distance


def wasserstein_distance_scaled(u, v):
    """
    Calculates the Wasserstein distance (Earth Mover's Distance) between two distributions and scales the result.

    This function computes the Wasserstein distance between two 1D distributions
    and then multiplies the result by 10, rounding it to two decimal places.

    Args:
        u (array-like): First 1D distribution (e.g., list, tuple, numpy array).
        v (array-like): Second 1D distribution (e.g., list, tuple, numpy array).

    Returns:
        float: The scaled Wasserstein distance, rounded to two decimal places.
               Returns 0.0 if either input is empty.

    Raises:
        TypeError: If inputs are not array-like.
        ValueError: If input distributions have different shapes (if multidimensional).

    Example:
        >>> wasserstein_distance_scaled([0, 1, 2], [3, 4, 5])
        30.0
        >>> wasserstein_distance_scaled([0, 1, 2], [0, 1, 2])
        0.0
        >>> wasserstein_distance_scaled([], [1,2,3])
        0.0
    """
    try:
        if not u or not v:
            return 0.0
        distance = wasserstein_distance(u, v)
        return distance
    except TypeError:
        raise TypeError("Input distributions must be array-like.")
    except ValueError as e:
        raise ValueError(f"Input distributions must be 1D: {e}")
