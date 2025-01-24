import re  # Regular expressions for parsing log files
import distinctipy  # For generating distinct colors for plots
import matplotlib.pyplot as plt  # For plotting
import numpy as np  # For numerical operations


class LogsPlotter:
    """
    A class to parse log files and visualize test accuracy trends for nodes over multiple rounds.

    This class reads a log file, extracts test accuracy data for each node, and generates a plot
    to visualize the trends. It also supports plotting mean and standard deviation of test
    accuracies across all nodes.

    Attributes:
        log_path (str): Path to the log file containing test accuracy data.

        plot_result_path (str): Path to save the generated plot (optional).

        distinct_colors (bool): Whether to use distinct colors for each node's plot.

        all_test_accuracy_mean (bool): Whether to plot the mean test accuracy across all nodes.

        all_test_accuracy_std (bool): Whether to plot the standard deviation of test accuracies.

        colors (list): List of colors for plotting, generated dynamically if distinct_colors is True.

        node_test_acc (dict): Dictionary where keys are node IDs and values are lists of test accuracies.
    """

    def __init__(
        self,
        log_path: str,
        plot_result_path: str = None,
        all_test_accuracy_mean: bool = True,
        all_test_accuracy_std: bool = True,
        distinct_colors: bool = True,
    ):
        """
        Initializes the LogsPlotter with the given parameters.

        Args:
            log_path (str): Path to the log file.

            plot_result_path (str, optional): Path to save the generated plot. Defaults to None.

            all_test_accuracy_mean (bool, optional): Whether to plot the mean test accuracy. Defaults to True.

            all_test_accuracy_std (bool, optional): Whether to plot the standard deviation. Defaults to True.

            distinct_colors (bool, optional): Whether to use distinct colors for each node's plot. Defaults to True.
        """
        self.log_path: str = log_path  # Path to the log file
        self.plot_result_path: str = (
            plot_result_path  # Path to save the plot (optional)
        )
        self.distinct_colors: bool = distinct_colors  # Use distinct colors for nodes
        self.all_test_accuracy_mean: bool = (
            all_test_accuracy_mean  # Plot mean test accuracy
        )
        self.all_test_accuracy_std: bool = (
            all_test_accuracy_std  # Plot standard deviation
        )
        self.colors = None  # List of colors for plotting
        self.node_test_acc = {}  # Dictionary to store node-wise test accuracies

    def read_log_file(self) -> "LogsPlotter":
        """
        Reads the log file and extracts test accuracy data for each node.

        Returns:
            LogsPlotter: The instance itself to allow method chaining.
        """
        # Open the log file for reading
        with open(self.log_path, "r") as log_file:
            # Iterate through each line in the log file
            for line in log_file:
                # Use regex to extract node ID and test accuracy
                match = re.search(
                    r"Node (\d+) - Round \d+: .*?Test Accuracy: ([\d.]+)%", line
                )
                if match:
                    # Extract node ID and test accuracy
                    node_id = int(match.group(1))
                    test_acc = float(match.group(2))
                    # Initialize the list for the node if it doesn't exist
                    if node_id not in self.node_test_acc:
                        self.node_test_acc[node_id] = []
                    # Append the test accuracy to the node's list
                    self.node_test_acc[node_id].append(test_acc)

        return self  # Return the instance for method chaining

    def plot(self) -> "LogsPlotter":
        """
        Generates a plot of test accuracy trends for each node and optionally includes
        mean and standard deviation across all nodes.

        Returns:
            LogsPlotter: The instance itself to allow method chaining.
        """
        # Set up the plot size
        plt.figure(figsize=(12, 6))

        # Determine the number of clients (nodes) based on the extracted data
        number_of_clients = len(self.node_test_acc)

        # Generate distinct colors for each node if enabled
        if self.distinct_colors:
            self.colors = distinctipy.get_colors(number_of_clients)
        else:
            self.colors = [None] * number_of_clients  # Use default matplotlib colors

        # Plot test accuracy trends for each node
        for idx, (node_id, accuracies) in enumerate(self.node_test_acc.items()):
            color = self.colors[idx] if self.distinct_colors else None
            plt.plot(
                range(1, len(accuracies) + 1),  # Rounds (x-axis)
                accuracies,  # Test accuracies (y-axis)
                label=f"Node {node_id}",  # Label for the node
                color=color,  # Use the assigned color
            )

        # Optionally compute and plot mean and standard deviation
        if self.all_test_accuracy_mean or self.all_test_accuracy_std:
            # Determine the maximum number of rounds across all nodes
            max_rounds = max(len(acc) for acc in self.node_test_acc.values())

            # Initialize lists to store mean and standard deviation for each round
            mean_accuracies = []
            std_accuracies = []

            # Compute mean and standard deviation for each round
            for r in range(max_rounds):
                round_accuracies = []
                for accuracies in self.node_test_acc.values():
                    if r < len(accuracies):  # Check if the node has data for this round
                        round_accuracies.append(accuracies[r])
                if round_accuracies:
                    mean_acc = np.mean(round_accuracies)
                    std_acc = np.std(round_accuracies)
                    mean_accuracies.append(mean_acc)
                    std_accuracies.append(std_acc)
                else:
                    # Handle missing data by appending NaN
                    mean_accuracies.append(np.nan)
                    std_accuracies.append(np.nan)

            # Convert mean and std lists to numpy arrays
            rounds = np.arange(1, max_rounds + 1)  # Round numbers
            mean_accuracies = np.array(mean_accuracies)
            std_accuracies = np.array(std_accuracies)

            # Plot the mean test accuracy as a black line
            if self.all_test_accuracy_mean:
                if r == max_rounds - 1:
                    print(f"Mean Test Accuracy: {mean_accuracies}")
                plt.plot(
                    rounds,
                    mean_accuracies,
                    label="Mean Test Accuracy",
                    color="black",
                    linewidth=2,
                )

            # Plot the standard deviation as a shaded region
            if self.all_test_accuracy_std:
                plt.fill_between(
                    rounds,
                    mean_accuracies - std_accuracies,
                    mean_accuracies + std_accuracies,
                    color="gray",
                    alpha=0.3,
                    label="Standard Deviation",
                )

        # Add plot title and labels
        plt.title("Test Accuracy of Each Node Across Rounds")
        plt.xlabel("Round")
        plt.ylabel("Test Accuracy (%)")
        plt.xticks(range(1, max(len(acc) for acc in self.node_test_acc.values()) + 1))
        plt.legend(loc="best")  # Add legend to the best location
        plt.grid(True, linestyle="--", alpha=0.7)  # Add grid lines
        plt.tight_layout()  # Adjust layout to avoid clipping

        # Save the plot to a file if a path is specified, otherwise display it
        if self.plot_result_path:
            plt.savefig(self.plot_result_path)
            plt.close()  # Close the plot to free memory
        else:
            plt.show()  # Display the plot interactively

        return self  # Return the instance for method chaining
