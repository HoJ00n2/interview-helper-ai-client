from abc import abstractmethod, ABC


class ChromaQueryEngineService(ABC):
    @abstractmethod
    def save(self, *args, ipcExecutorConditionalCustomExecutorChannel=None, **kwargs):
        pass

    @abstractmethod
    def search(self, *args, ipcExecutorConditionalCustomExecutorChannel=None, **kwargs):
        pass