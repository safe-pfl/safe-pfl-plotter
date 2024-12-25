import sys
import torch
import numpy as np
import matplotlib

from safe_pfl_distance.utils.results import generate_csv

# Use a non-interactive backend
matplotlib.use("Agg")

from safe_pfl_distance.utils.model_loader import load_models
from safe_pfl_distance.utils.coordinate_based import coordinate_based_distance
from safe_pfl_distance.utils.jensen_shannon import jensen_shannon_distance
from safe_pfl_distance.utils.wasserstein import wasserstein_distance
from safe_pfl_distance.utils.euclidean import euclidean_distance
from safe_pfl_distance.utils.cosine import cosine_distance


class ModelDistancesCalculator:
    def __init__(
        self,
        model_type,
        sensitivity_parameter=0.01,
        model_path_prefix: str = "./models",
        precision=5,
    ):
        self.model_type = model_type.lower()
        self.model_path_prefix = model_path_prefix

        self.precision = precision if precision > 0 else 5

        # Validate model_type
        if self.model_type not in ["cnn", "resnet", "google", "alexnet", "vgg"]:
            raise ValueError(
                "Invalid model_type. Please choose from 'cnn', 'resnet', 'google', 'alexnet', or 'vgg'."
            )
        else:
            print(f"Processing model_type: {self.model_type}")

        self.client_ids = list(range(10))
        self.models = []
        self.model_weights = []
        self.model_top_weight_indices = []
        self.p = sensitivity_parameter  # Percentage for top weights (1%)

        self.models = load_models(
            self.client_ids, self.model_type, self.model_path_prefix
        )

    def extract_model_weights(self):
        for idx, model in enumerate(self.models):
            if isinstance(model, dict):
                state_dict = model
            elif isinstance(model, torch.nn.Module):
                state_dict = model.state_dict()
                print("Model state_dict extracted.")
            else:
                print(f"Unrecognized model format at index {idx}. Skipping...")
                continue

            weights = []
            for key, value in state_dict.items():
                # Include all parameters, including biases
                weights.append(value.cpu().numpy().flatten())

            if weights:
                weights_vector = np.concatenate(weights)
                self.model_weights.append(weights_vector)
            else:
                print(f"No weights found for model at index {idx}. Skipping...")

        if len(self.model_weights) < 2:
            print("Not enough models to compute distances.")
            sys.exit(1)
        else:
            self.prepare_top_weight_indices()

    def prepare_top_weight_indices(self):
        N = len(self.model_weights[0])  # Total number of weights
        p = int(self.p * N)
        if p == 0:
            p = 1  # Ensure at least one weight is selected

        self.p = p
        self.model_top_weight_indices = []
        for weights in self.model_weights:
            importance_scores = np.abs(weights)
            top_indices = np.argpartition(-importance_scores, self.p - 1)[: self.p]
            self.model_top_weight_indices.append(set(top_indices))

    def compute_distance_matrix(self, distance_func, is_indices=False):
        num_models = len(self.model_weights)
        distance_matrix = np.zeros((num_models, num_models))
        for i in range(num_models):
            for j in range(num_models):
                if is_indices:
                    distance = distance_func(
                        i, j, self.model_top_weight_indices, self.p
                    )
                else:
                    distance = distance_func(
                        self.model_weights[i], self.model_weights[j]
                    )
                distance_matrix[i, j] = distance
        return distance_matrix

    def compute_distance_matrices(self):
        distance_functions = {
            "Euclidean": euclidean_distance,
            "Cosine": cosine_distance,
            "coordinate-based": coordinate_based_distance,
            "Jensen-Shannon": jensen_shannon_distance,
            "Wasserstein": wasserstein_distance,
        }

        for metric_name, distance_func in distance_functions.items():
            print(f"Computing {metric_name} distance matrix...")

            if metric_name == "coordinate-based":
                distance_matrix = self.compute_distance_matrix(
                    distance_func, is_indices=True
                )
            else:
                distance_matrix = self.compute_distance_matrix(
                    distance_func, is_indices=False
                )

            # Proceed to cluster and generate LaTeX code
            generate_csv(distance_matrix, metric_name, self.model_type, self.precision)
