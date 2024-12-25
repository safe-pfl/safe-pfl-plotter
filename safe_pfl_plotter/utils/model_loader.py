from typing import List
import torch


def load_model(node_id: int, model_type: str, model_path_prefix: str = "./models"):
    """
    Loads a PyTorch model from a specified file path.

    Args:
        node_id (int): Identifier for the specific model node.

        model_type (str): Type of the model (e.g., "classification", "regression").

        model_path_prefix (str, optional): Base directory where model files are stored. Defaults to "./models".

    Returns:
        torch.nn.Module or None: The loaded PyTorch model if successful, otherwise None.

    Raises:
        ValueError: If input parameters are invalid.
    """
    try:
        model_path = f"{model_path_prefix}/{model_type}/node_{node_id}.pth"
        model = torch.load(model_path)
        print(f"Model loaded successfully from {model_path}")
        return model
    except Exception as e:
        print(f"Error loading model at node {node_id}: {e}")
        return None


def load_models(client_ids: List[int], model_type: str, model_path_prefix: str = "./models"):
    models = []
    for cid in client_ids:
        model = load_model(cid, model_type, model_path_prefix)
        if model is not None:
            models.append(model)
        else:
            print(f"Model at node {cid} could not be loaded.")
    return models
