from abc import ABC, abstractmethod


class AbstractVectorizer(ABC):
    def __init__(self):
        # self.value = value
        super().__init__()

    @abstractmethod
    def fit(self, train_input):
        pass

    def evaluate(self):
        pass


