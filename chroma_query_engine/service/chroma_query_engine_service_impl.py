from chroma_query_engine.repository.chroma_query_engine_repository_impl import ChromaQueryEngineRepositoryImpl
from chroma_query_engine.service.chroma_query_engine_service import ChromaQueryEngineService
from template.utility.color_print import ColorPrinter


class ChromaQueryEngineServiceImpl(ChromaQueryEngineService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__chromaQueryEngineRepository = ChromaQueryEngineRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    async def save(self, *args, ipcExecutorConditionalCustomExecutorChannel=None, **kwargs):
        ColorPrinter.print_important_message("service -> save() called!")
        userId = args[0]
        questionIds = args[1]
        questionCategory = args[2]
        questionTexts = args[3]
        ColorPrinter.print_important_data("userId", userId)
        ColorPrinter.print_important_data("questionIds", questionTexts)
        ColorPrinter.print_important_data("questionCategory", questionCategory)
        ColorPrinter.print_important_data("questionTexts", questionTexts)

        result = await self.__chromaQueryEngineRepository.save(userId, questionIds, questionCategory, questionTexts)

        return {"message" : result}

    def search(self, *args, ipcExecutorConditionalCustomExecutorChannel=None, **kwargs):
        pass

