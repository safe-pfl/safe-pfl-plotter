import os
import numpy as np

def generate_csv(distance_matrix, metric_name, model_type, precision):
    """Save the distance matrix to a CSV file.
    
    Args:
        distance_matrix (NDArray[float64]): distance matrix result
    
        metric_name (str): Form one of the following: "Euclidean", "Cosine", "coordinate-based", "Jensen-Shannon", "Wasserstein"
    
        model_type (str): From one of the following: "cnn", "resnet", "google", "alexnet", "vgg" 
    """
    dir_path = os.path.join(".", "results", model_type)
    os.makedirs(dir_path, exist_ok=True)
    
    file_path = os.path.join(dir_path, f"{metric_name}_distance.csv")
    
    fmt = f'%.{precision}f'
    np.savetxt(file_path, distance_matrix, delimiter=",", fmt=fmt)
    print(f"Distance matrix saved to {file_path}")