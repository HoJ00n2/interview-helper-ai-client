import os
import chromadb
import openai
from chromadb import Settings
from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction
from dotenv import load_dotenv

from chroma_query_engine.repository.chroma_query_engine_repository import ChromaQueryEngineRepository
from template.utility.color_print import ColorPrinter

load_dotenv()

class ChromaQueryEngineRepositoryImpl(ChromaQueryEngineRepository):
    __instance = None
    client = chromadb.HttpClient(
        # host=os.getenv("CHROMA_HOST_ADDR"),
        host='localhost',
        port=int(os.getenv("CHROMA_HOST_PORT")),
        settings=Settings(
            chroma_client_auth_provider=os.getenv("CHROMA_SERVER_AUTH_PROVIDER"),
            chroma_client_auth_credentials=os.getenv("CHROMA_SERVER_AUTHN_CREDENTIALS")
        )
    )
    embeddings = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"))
    collection = client.get_or_create_collection("interview_helper", embedding_function=embeddings,
                                                 metadata={"hnsw:space": "cosine"})


    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    async def save(self, userId, questionIds, questionCategory, questionTexts):
        try:
            for i in range(len(questionIds)):
                self.collection.add(
                    documents=[questionTexts[i]],
                    metadatas=[{
                        "user_id": userId,
                        "category": questionCategory
                    }],
                    ids=[str(questionIds[i])]
                )
            ColorPrinter.print_important_data("Number of question in the collection:", self.collection.count())
            ColorPrinter.print_important_data("Latest added data:",
                                              self.collection.get(limit=len(questionIds), offset=self.collection.count() - len(questionIds)))
            return True

        except Exception as e:
            print(f"ChromaDB에 데이터 저장 중 오류 발생: {e}")
            return False

    async def search(self, userId, query):
        try:
            results = self.collection.query(
                query_texts=[f"주어진 단어와 관련된 문서를 찾아줘.\n주어진 단어: {query}"],
                where={"user_id": {"$eq": userId}},
                n_results=5
            )
            ColorPrinter.print_important_data("search result:", results)

            return results

        except Exception as e:
            print(f"ChromaDB에서 {query}로 검색 중 오류 발생: {e}")
            return None
