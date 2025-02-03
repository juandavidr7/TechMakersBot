from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.chatbot_service import ChatbotService
from app.services.products_service import ProductService

router = APIRouter(prefix="", tags=["chatbot"])


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
