from abc import ABC, abstractmethod


class AbstractModel(ABC):
    def __init__(self):
        # self.value = value
        super().__init__()

    @abstractmethod
    def fit(self):
        pass

    def evaluate(self):
        pass


