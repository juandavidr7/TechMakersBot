import os
import requests
from dotenv import load_dotenv

# Cargar clave desde las variables de entorno
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if not OPENAI_API_KEY:
    raise ValueError("🚨 ERROR: La variable OPENAI_API_KEY no está definida.")

# URL de la API de OpenAI
API_URL = "https://api.openai.com/v1/chat/completions"

# Datos para la solicitud
payload = {
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "¿Cuáles son las mejores computadoras para trabajo?"}],
    "max_tokens": 100
}

# Headers necesarios
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

def test_openai_api():
    """Prueba la conexión con la API de OpenAI."""
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        print(f"🔹 Status Code: {response.status_code}")
        print(f"🔹 Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 ERROR: No se pudo conectar a la API de OpenAI: {e}")

if __name__ == "__main__":
    print("🔍 Probando conexión con OpenAI...")
    test_openai_api()
