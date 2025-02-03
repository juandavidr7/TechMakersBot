from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chatbot_service import ChatbotService

router = APIRouter(prefix="", tags=["chatbot"])

# Inicializar el servicio solo cuando se necesite
chatbot_service = None

class ChatQuery(BaseModel):
    query: str

@router.post("/chatbot")
async def chat(query: ChatQuery):
    """Recibe la consulta y devuelve la respuesta del chatbot"""
    global chatbot_service

    if chatbot_service is None:
        chatbot_service = ChatbotService()

    try:
        response = chatbot_service.askBasedOnCurrentProducts(query.query)
        return {"response": response}
    except Exception as e:
        print(f"🚨 ERROR en chatbot: {e}")
        raise HTTPException(status_code=500, detail="Error interno del chatbot")
