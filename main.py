import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.routes import products
from app.routes import chatbot

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Ecommerce Chatbot API",
    description="API para manejar productos de un ecommerce",
    version="1.0"
)


app.include_router(products.router)
app.include_router(chatbot.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del Ecommerce Chatbot"}

# Para ejecutar el servidor: uvicorn app.main:app --reload
