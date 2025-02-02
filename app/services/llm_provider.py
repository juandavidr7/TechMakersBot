import os
from dotenv import load_dotenv


env_loaded=load_dotenv()

# Verificar si se cargó correctamente
print(f"DEBUG: `.env` cargado correctamente? {env_loaded}")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Detectar qué modelo usar
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")

# Imprimir la clave (solo los primeros 5 caracteres por seguridad)
print(f"DEBUG: OPENAI_API_KEY = {OPENAI_API_KEY[:5] + '********' if OPENAI_API_KEY else 'No encontrada'}")


if not OPENAI_API_KEY:
    raise ValueError("🚨 ERROR: No se encontró `OPENAI_API_KEY` en las variables de entorno.")


if MODEL_PROVIDER == "openai":
    from langchain_openai import OpenAI
elif MODEL_PROVIDER == "llama":
    """from llama_cpp import Llama"""


class LLMProvider:
    def __init__(self):
        """Inicializa el modelo según el proveedor configurado en .env"""
        if MODEL_PROVIDER == "openai":
            self.model = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif MODEL_PROVIDER == "llama":
            model_path = os.getenv("LLAMA_MODEL_PATH")
            """self.model = Llama(model_path=model_path, n_ctx=2048)"""

    def generateResponseDependsModel(self, prompt: str) -> str:
        """Genera una respuesta según el modelo en uso."""
        if MODEL_PROVIDER == "openai":
            return self.model(prompt)
        elif MODEL_PROVIDER == "llama":
            output = self.model(prompt, max_tokens=200)
            return output["choices"][0]["text"].strip()

# Crear una instancia del modelo
llm = LLMProvider()
