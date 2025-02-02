from fastapi import FastAPI
from app.routes import products

app = FastAPI(
    title="Ecommerce Chatbot API",
    description="API para manejar productos de un ecommerce",
    version="1.0"
)


app.include_router(products.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del Ecommerce Chatbot"}

# Para ejecutar el servidor: uvicorn app.main:app --reload
