import os
from dotenv import load_dotenv
from langchain_openai import OpenAI


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if not OPENAI_API_KEY:
    raise ValueError("ERROR: La variable OPENAI_API_KEY no está definida en el archivo .env")

class LLMProvider:
    def __init__(self):
        """Inicializa el modelo OpenAI"""
        self.model = OpenAI(api_key=OPENAI_API_KEY, temperature=0)

    def generateResponseDependsModel(self, prompt: str) -> str:
        """Genera una respuesta usando OpenAI"""
        return self.model.invoke(prompt, max_tokens=500)



llm = LLMProvider()
