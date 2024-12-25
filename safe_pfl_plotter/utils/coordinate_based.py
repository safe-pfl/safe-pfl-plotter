def coordinate_based_distance(
    index_u, index_v, model_weight_indices, sensitivity_parameter
):
    """
    Calculate the coordinate-based distance between two indices.

    Args:
        index_u (int): The first index.

        index_v (int): The second index.

        model_weight_indices (list of sets): A list where each element is a set of model weight indices.

        sensitivity_parameter (float): A parameter to adjust the sensitivity of the distance calculation.

    Returns:
        float: The calculated distance.
    """

    indices_u = model_weight_indices[index_u]
    indices_v = model_weight_indices[index_v]

    intersection = len(set(indices_u) & set(indices_v))
    similarity = intersection / sensitivity_parameter
    distance = 1 - similarity
    return distance
