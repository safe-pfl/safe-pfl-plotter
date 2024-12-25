import numpy as np
from scipy.spatial.distance import jensenshannon


def jensen_shannon_distance(u, v):
    """
    Calculates the Jensen-Shannon distance between two probability distributions.

    This function computes the Jensen-Shannon distance between two 1D probability
    distributions. It normalizes the input vectors to ensure they represent
    valid probability distributions and clips values to avoid numerical instability
    (division by zero or log of zero).

    Args:
        u (array-like): First 1D probability distribution.
        v (array-like): Second 1D probability distribution.

    Returns:
        float: The Jensen-Shannon distance between u and v. Returns NaN if either input is all zeros after abs().

    Raises:
        TypeError: If inputs are not array-like.
        ValueError: If input distributions have different shapes.

    Example:
        >>> jensen_shannon_distance([0, 1, 0], [0, 0, 1])
        0.7071067811865476
        >>> jensen_shannon_distance([1, 0, 0], [1, 0, 0])
        0.0
        >>> jensen_shannon_distance([0, 0, 0], [0, 0, 0])
        nan
    """
    try:
        u = np.asarray(u)
        v = np.asarray(v)

        u = np.abs(u)
        v = np.abs(v)

        sum_u = np.sum(u)
        sum_v = np.sum(v)
        if sum_u == 0 or sum_v == 0:
            return np.nan

        u /= sum_u
        v /= sum_v

        epsilon = 1e-12
        u = np.clip(u, epsilon, None)
        v = np.clip(v, epsilon, None)

        distance = jensenshannon(u, v)
        return distance

    except TypeError:
        raise TypeError("Input distributions must be array-like.")
    except ValueError:
        raise ValueError("Input distributions must have the same shape.")
