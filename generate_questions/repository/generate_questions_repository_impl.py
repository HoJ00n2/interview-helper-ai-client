import os
import re

import openai
from dotenv import load_dotenv

from generate_questions.repository.generate_questions_repository import GenerateQuestionsRepository

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class GenerateQuestionsRepositoryImpl(GenerateQuestionsRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    async def generate(self, category):
        client = openai.AsyncClient(api_key=OPENAI_API_KEY)
        systemPrompt = "You are a helpful assistant for generating interview questions."
        userPrompt = f"""Generate 5 interview questions for the category in KOREAN: {category}
                      
                      <example>
                      input: Generate 5 interview questions for the category in KOREAN: Technical skills
                      output:
                      1. 첫번째 질문
                      2. 두번째 질문
                      3. 세번째 질문
                      4. 네번째 질문
                      5. 다섯번째 질문
                      </example>
                      
                      OUTPUT:"""

        messages = [
            {
                "role": "system", "content": systemPrompt
            },
            {
                "role": "user", "content": userPrompt
            }
        ]

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )

        result = response.choices[0].message.content.split("\n")
        generatedQuestionList = [re.sub(r'^\d+\.\s+', '', s) for s in result]

        return generatedQuestionList