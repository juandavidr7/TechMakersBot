from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..services.chatbot_service import ChatbotService
from ..services.products_service import ProductService

router = APIRouter(prefix="", tags=["chatbot"])

chatbot_service = ChatbotService(ProductService())


def get_chatbot_service(products_service: ProductService = Depends(ProductService)):
    return ChatbotService(products_service)


class ChatQuery(BaseModel):
    query: str

@router.post("/chatbot")
async def chat(query: ChatQuery, chatbot_service: ChatbotService = Depends(get_chatbot_service)):
    """Recibe la consulta y devuelve la respuesta del chatbot"""
    try:
        response = chatbot_service.askBasedOnCurrentProducts(query.query)
        return {"response": response}
    except Exception as e:
        print(f"🚨 ERROR en chatbot: {e}")
        raise HTTPException(status_code=500, detail="Error interno del chatbot")

@router.delete("/chatbot/clear-history")
def clear_chat_history():
    """Borra el historial de chat almacenado en chat_memory.json"""
    return chatbot_service.clear_chat_history()
