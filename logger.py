class Logger:
    def __init__(self, log_path):
        self.__log = open(log_path, "w")
        self.__kind_history = []
        self.__mean_history = []

    def __del__(self):
        self.__log.close()

    def logStep(self, kind, mean):
        self.__kind_history.append(kind)
        self.__mean_history.append(mean)

    def save(self):
        for i in range(len(self.__kind_history)):
            print(f"===== Step {i} =====", file=self.__log)
            print(f"Kind: {self.__kind_history[i]}", file=self.__log)
            print(f"Mean: {self.__mean_history[i]}", file=self.__log)
