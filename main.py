import os
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.routes import products, chatbot, auth  # Carga los routers
from app.routes.chatbot import router as chatbot_router
from app.routes.auth import router as auth_router
from app.routes.products import router as products_router
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Ecommerce Chatbot API",
    description="API para manejar productos de un ecommerce",
    version="1.0"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiar "*" por "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(products_router)
app.include_router(chatbot_router)

app.include_router(auth_router)

app.mount("/uploads", StaticFiles(directory="app/data/images"), name="uploads")

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del Ecommerce Chatbot"}

# Para ejecutar el servidor: uvicorn app.main:app --reload
