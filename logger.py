import matplotlib.pyplot as plt
import os
import math
from pathlib import Path


class Logger:
    def __init__(self, log_path, lean):
        self.__log_path = Path(log_path)
        self.__coop_history = []
        self.__defect_history = []
        self.__total_history = []
        self.__evac_history = []
        self.__lean = lean

        if not os.path.exists(log_path):
            os.makedirs(log_path)

    def logStep(self, coop, defect, evac):
        self.__coop_history.append(coop)
        self.__defect_history.append(defect)
        self.__total_history.append(defect + coop)
        self.__evac_history.append(evac)

    def save(self):
        with open(self.__log_path.joinpath("log.txt"), "w") as log:
            for i in range(len(self.__coop_history)):
                print(f"===== Step {i} =====", file=log)
                print(f"Kind: {self.__coop_history[i]}", file=log)
                print(f"Mean: {self.__defect_history[i]}", file=log)
                print(f"Evacuated: {self.__evac_history[i]}", file=log)
            print(f"Simulation ended in {len(self.__coop_history)} steps", file=log)
        if not self.__lean:
            self.plot()

    def plot(self):
        """
        Modified from Claude

        Creates multiple plots to visualize simulation data:
        """
        print("Plotting may take time")
        # Ensure the log directory exists
        self.__log_path.mkdir(parents=True, exist_ok=True)

        # Plot 0: Time series
        plt.figure(figsize=(20,10))
        steps = range(len(self.__coop_history))
        small_steps = range(0, len(self.__coop_history), math.ceil(len(self.__coop_history)/50))
        plt.plot(steps, self.__coop_history, "b-", label="Cooperate")
        plt.plot(steps, self.__defect_history, "r-", label="Defect")
        plt.xlabel("Step")
        plt.ylabel("Value")
        plt.title("Cooperation vs Defection")
        plt.legend()
        plt.grid(True)
        # Set integer ticks for x-axis
        plt.xticks(small_steps, [str(i) for i in small_steps])
        plt.savefig(self.__log_path.joinpath("coop_vs_defect.png"))
        plt.close()

        # Plot 1: With total
        plt.figure(figsize=(20,10))
        steps = range(len(self.__coop_history))
        small_steps = range(0, len(self.__coop_history), math.ceil(len(self.__coop_history)/50))
        plt.plot(steps, [self.__coop_history[i]/self.__total_history[i] for i in range(len(self.__total_history)-1)] + [0], "b-", label="Cooperate")
        plt.plot(steps, [self.__defect_history[i]/self.__total_history[i] for i in range(len(self.__total_history)-1)] + [0], "r-", label="Defect")
        plt.xlabel("Step")
        plt.ylabel("Value")
        plt.title("Coop vs Defection as Percentage")
        plt.legend()
        plt.grid(True)
        # Set integer ticks for x-axis
        plt.xticks(small_steps, [str(i) for i in small_steps])
        plt.savefig(self.__log_path.joinpath("coop_vs_defect_percentage.png"))
        plt.close()

        # Plot 2: Balance
        plt.figure(figsize=(20,10))
        steps = range(len(self.__coop_history))
        small_steps = range(0, len(self.__coop_history), math.ceil(len(self.__coop_history)/50))
        plt.plot(steps, [self.__coop_history[i] - self.__defect_history[i] for i in range(len(self.__coop_history))], "p-", label="Cooperate Advantage")
        plt.xlabel("Step")
        plt.ylabel("Value")
        plt.title("Coop Advantage Over Time")
        plt.legend()
        plt.grid(True)
        # Set integer ticks for x-axis
        plt.xticks(small_steps, [str(i) for i in small_steps])
        plt.savefig(self.__log_path.joinpath("coop_advantage.png"))
        plt.close()
        
        # Plot 3: Cooperation Time Series
        plt.figure(figsize=(20,10))
        plt.plot(steps, self.__coop_history, "b-", label="Cooperation")
        plt.xlabel("Step")
        plt.ylabel("Coopeartion Value")
        plt.title("Cooperation Over Time")
        plt.legend()
        plt.grid(True)
        plt.xticks(small_steps, [str(i) for i in small_steps])
        plt.tight_layout()
        plt.savefig(self.__log_path.joinpath("coop_timeseries.png"))
        plt.close()
        
        # Plot 4: Evacuation Time Series
        plt.figure(figsize=(20,10))
        plt.plot(steps, self.__evac_history, "g-", label="Evacuation")
        plt.xlabel("Step")
        plt.ylabel("Total Evacuated")
        plt.title("Evacuation Progress")
        plt.legend()
        plt.grid(True)
        plt.xticks(small_steps, [str(i) for i in small_steps])
        plt.tight_layout()
        plt.savefig(self.__log_path.joinpath("evacuation.png"))
        plt.close()
        
        # Plot 4: Defection Time Series
        plt.figure(figsize=(20,10))
        plt.plot(steps, self.__defect_history, "r-", label="Defection")
        plt.xlabel("Step")
        plt.ylabel("Defection Value")
        plt.title("Defection Over Time")
        plt.legend()
        plt.grid(True)
        plt.xticks(small_steps, [str(i) for i in small_steps])
        plt.tight_layout()
        plt.savefig(self.__log_path.joinpath("defection_timeseries.png"))
        plt.close()
