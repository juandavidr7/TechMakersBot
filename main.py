import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routes import products, chatbot  # Carga los routers
from app.routes.chatbot import router as chatbot_router
from app.routes.products import router as products_router

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Ecommerce Chatbot API",
    description="API para manejar productos de un ecommerce",
    version="1.0"
)

# Registrar rutas correctamente
app.include_router(products_router)
app.include_router(chatbot_router)  # YA NO NECESITA prefix="/chatbot"

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del Ecommerce Chatbot"}

# Para ejecutar el servidor: uvicorn app.main:app --reload
