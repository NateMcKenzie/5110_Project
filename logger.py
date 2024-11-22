import matplotlib.pyplot as plt
import os
from pathlib import Path


class Logger:
    def __init__(self, log_path):
        self.__log_path = Path(log_path)
        self.__kind_history = []
        self.__mean_history = []

        if not os.path.exists(log_path):
            os.makedirs(log_path)

    def logStep(self, kind, mean):
        self.__kind_history.append(kind)
        self.__mean_history.append(mean)

    def save(self):
        with open(self.__log_path.joinpath("log.txt"), "w") as log:
            for i in range(len(self.__kind_history)):
                print(f"===== Step {i} =====", file=log)
                print(f"Kind: {self.__kind_history[i]}", file=log)
                print(f"Mean: {self.__mean_history[i]}", file=log)

    def plot(self):
        """
        Courtesy of Claude

        Creates two plots:
        1. Line plot showing kind and mean values over time
        2. Scatter plot showing the relationship between kind and mean values
        """

        # Create figure with two subplots side by side
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

        # Plot 1: Time series
        steps = range(len(self.__kind_history))
        ax1.plot(steps, self.__kind_history, "b-", label="Kind")
        ax1.plot(steps, self.__mean_history, "r-", label="Mean")
        ax1.set_xlabel("Step")
        ax1.set_ylabel("Value")
        ax1.set_title("Kind vs Mean")
        ax1.legend()
        ax1.grid(True)
        # Set integer ticks for x-axis
        ax1.set_xticks(steps)
        ax1.set_xticklabels([str(i) for i in steps])

        # Plot 2: Relationship between Kind and Mean
        ax2.scatter(self.__kind_history, self.__mean_history, alpha=0.5)
        ax2.set_xlabel("Kind")
        ax2.set_ylabel("Mean")
        ax2.set_title("Kind vs Mean Scatter")
        ax2.grid(True)

        # Add step numbers as annotations to scatter plot
        for i, (x, y) in enumerate(zip(self.__kind_history, self.__mean_history)):
            ax2.annotate(
                i, (x, y), xytext=(5, 5), textcoords="offset points", fontsize=8
            )

        # Adjust layout and display
        plt.tight_layout()

        # Save the plots
        plt.savefig(self.__log_path.joinpath("plots.png"))
        plt.close()
