from abc import abstractmethod, ABC


class ChromaQueryEngineRepository(ABC):
    @abstractmethod
    def save(self, userId, questionIds, questionCategory, questionTexts):
        pass

    @abstractmethod
    def search(self, userId, query):
        pass