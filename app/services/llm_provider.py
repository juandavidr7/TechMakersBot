import os
from dotenv import load_dotenv
from langchain_openai import OpenAI

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener configuración de modelo
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Importar modelos según el proveedor configurado en .env
if not OPENAI_API_KEY:
    raise ValueError("ERROR: La variable OPENAI_API_KEY no está definida en el archivo .env")

class LLMProvider:
    def __init__(self):
        """Inicializa el modelo OpenAI"""
        self.model = OpenAI(api_key=OPENAI_API_KEY, temperature=0)

    def generateResponseDependsModel(self, prompt: str) -> str:
        """Genera una respuesta usando OpenAI"""
        return self.model.invoke(prompt, max_tokens=500)  # ✅ Asegura un límite de tokens adecuado


# ✅ Crear instancia global del modelo
llm = LLMProvider()
