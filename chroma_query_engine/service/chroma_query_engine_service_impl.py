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
        userToken = args[0]
        userId = args[1]
        questionIds = args[2]
        questionCategory = args[3]
        questionTexts = args[4]
        ColorPrinter.print_important_data("userId", userId)
        ColorPrinter.print_important_data("questionIds", questionTexts)
        ColorPrinter.print_important_data("questionCategory", questionCategory)
        ColorPrinter.print_important_data("questionTexts", questionTexts)

        result = await self.__chromaQueryEngineRepository.save(userId, questionIds, questionCategory, questionTexts)

        return {"userToken": userToken, "message" : result}

    async def search(self, *args, ipcExecutorConditionalCustomExecutorChannel=None, **kwargs):
        ColorPrinter.print_important_message("service -> search() called!")
        userToken = args[0]
        userId = args[1]
        query = args[2]

        ColorPrinter.print_important_data("userToken", userToken)
        ColorPrinter.print_important_data("userId", userId)
        ColorPrinter.print_important_data("query", query)

        results = await self.__chromaQueryEngineRepository.search(userId, query)
        documents = results['documents'][0]
        ids = results['ids'][0]
        distances = results['distances'][0]
        response = [{"id": ids[i], "title": documents[i], "distance": distances[i]} for i in range(len(documents))]

        return {"userToken": userToken, "message": response}