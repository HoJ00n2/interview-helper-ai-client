from abc import ABC, abstractmethod


class GenerateQuestionsRepository(ABC):
    @abstractmethod
    def generate(self, category):
        pass