import asyncio

from generate_questions.repository.generate_questions_repository_impl import GenerateQuestionsRepositoryImpl
from generate_questions.service.generate_questions_service import GenerateQuestionsService
from template.utility.color_print import ColorPrinter


class GenerateQuestionsServiceImpl(GenerateQuestionsService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__generateQuestionsRepository = GenerateQuestionsRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    async def generateQuestions(self, *args, ipcExecutorConditionalCustomExecutorChannel=None, **kwargs):
        loop = asyncio.get_running_loop()
        ColorPrinter.print_important_data("args", args)
        ColorPrinter.print_important_data("userToken", args[0])
        ColorPrinter.print_important_data("category", args[1])
        ColorPrinter.print_important_data("ipcExecutorConditionalCustomExecutorChannel", args[2])

        generatedQuestions = await self.__generateQuestionsRepository.generate(args[1])
        ColorPrinter.print_important_data("generatedQuestions", generatedQuestions)

        return { "userToken": args[0], "message": generatedQuestions }
