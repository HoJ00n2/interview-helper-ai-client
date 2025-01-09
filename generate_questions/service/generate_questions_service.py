from abc import ABC, abstractmethod


class GenerateQuestionsService(ABC):
    @abstractmethod
    def generateQuestions(self, *args, ipcExecutorConditionalCustomExecutorChannel=None, **kwargs):
        pass