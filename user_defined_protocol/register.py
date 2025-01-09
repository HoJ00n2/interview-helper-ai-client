from generate_questions.service.generate_questions_service_impl import GenerateQuestionsServiceImpl
from generate_questions.service.request.generate_questions_request import GenerateQuestionsRequest
from generate_questions.service.response.generate_questions_response import GenerateQuestionsResponse
from template.custom_protocol.service.custom_protocol_service_impl import CustomProtocolServiceImpl
from template.request_generator.request_class_map import RequestClassMap
from template.response_generator.response_class_map import ResponseClassMap
from user_defined_protocol.protocol import UserDefinedProtocolNumber


class UserDefinedProtocolRegister:
    @staticmethod
    def registerGenerateQuestionsProtocol():
        customProtocolService = CustomProtocolServiceImpl.getInstance()
        generateQuestionsService = GenerateQuestionsServiceImpl.getInstance()

        requestClassMapInstance = RequestClassMap.getInstance()
        requestClassMapInstance.addRequestClass(
            UserDefinedProtocolNumber.GENERATE_QUESTIONS_PROTOCOL_NUMBER,
            GenerateQuestionsRequest
        )

        responseClassMapInstance = ResponseClassMap.getInstance()
        responseClassMapInstance.addResponseClass(
            UserDefinedProtocolNumber.GENERATE_QUESTIONS_PROTOCOL_NUMBER,
            GenerateQuestionsResponse
        )

        customProtocolService.registerCustomProtocol(
            UserDefinedProtocolNumber.GENERATE_QUESTIONS_PROTOCOL_NUMBER,
            generateQuestionsService.generate
        )

    @staticmethod
    def registerUserDefinedProtocol():
        UserDefinedProtocolRegister.registerGenerateQuestionsProtocol()
