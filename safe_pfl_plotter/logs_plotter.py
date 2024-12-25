import re

import distinctipy
import matplotlib.pyplot as plt
import numpy as np


class LogsPlotter:
    def __init__(
        self,
        log_path: str,
        plot_result_path: str = None,
        all_test_accuracy_mean: bool = True,
        all_test_accuracy_std: bool = True,
        distinct_colors: bool = True,
    ):
        self.log_path: str = log_path
        self.plot_result_path: str = plot_result_path
        self.distinct_colors: bool = distinct_colors
        self.all_test_accuracy_mean: bool = all_test_accuracy_mean
        self.all_test_accuracy_std: bool = all_test_accuracy_std
        self.colors = None

        self.node_test_acc = {}

    def read_log_file(self) -> "LogsPlotter":
        with open(self.log_path, "r") as log_file:
            for line in log_file:
                match = re.search(
                    r"Node (\d+) - Round \d+: .*?Test Accuracy: ([\d.]+)%", line
                )
                if match:
                    node_id = int(match.group(1))
                    test_acc = float(match.group(2))
                    if node_id not in self.node_test_acc:
                        self.node_test_acc[node_id] = []
                    self.node_test_acc[node_id].append(test_acc)

        return self

    def plot(self) -> "LogsPlotter":
        plt.figure(figsize=(12, 6))

        number_of_clients = len(self.node_test_acc)

        if self.distinct_colors:
            self.colors = distinctipy.get_colors(number_of_clients)
        else:
            self.colors = [None] * number_of_clients

        for idx, (node_id, accuracies) in enumerate(self.node_test_acc.items()):
            color = self.colors[idx] if self.distinct_colors else None
            plt.plot(
                range(1, len(accuracies) + 1),
                accuracies,
                label=f"Node {node_id}",
                color=color,
            )

        if self.all_test_accuracy_mean or self.all_test_accuracy_std:
            max_rounds = max(len(acc) for acc in self.node_test_acc.values())

            mean_accuracies = []
            std_accuracies = []

            for r in range(max_rounds):
                round_accuracies = []
                for accuracies in self.node_test_acc.values():
                    if r < len(accuracies):
                        round_accuracies.append(accuracies[r])
                    else:
                        pass
                if round_accuracies:
                    mean_acc = np.mean(round_accuracies)
                    std_acc = np.std(round_accuracies)
                    mean_accuracies.append(mean_acc)
                    std_accuracies.append(std_acc)
                else:
                    mean_accuracies.append(np.nan)
                    std_accuracies.append(np.nan)

            rounds = np.arange(1, max_rounds + 1)
            mean_accuracies = np.array(mean_accuracies)
            std_accuracies = np.array(std_accuracies)

            if self.all_test_accuracy_mean:
                plt.plot(
                    rounds,
                    mean_accuracies,
                    label="Mean Test Accuracy",
                    color="black",
                    linewidth=2,
                )

            if self.all_test_accuracy_std:
                plt.fill_between(
                    rounds,
                    mean_accuracies - std_accuracies,
                    mean_accuracies + std_accuracies,
                    color="gray",
                    alpha=0.3,
                    label="Standard Deviation",
                )

        plt.title("Test Accuracy of Each Node Across Rounds")
        plt.xlabel("Round")
        plt.ylabel("Test Accuracy (%)")
        plt.xticks(range(1, max(len(acc) for acc in self.node_test_acc.values()) + 1))
        plt.legend(loc="best")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()

        if self.plot_result_path:
            plt.savefig(self.plot_result_path)
            plt.close()
        else:
            plt.show()

        return self
