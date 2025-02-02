from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chatbot_service import ChatbotService

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class ChatQuery(BaseModel):
    query: str

chatbot = ChatbotService()

@router.post("/")
def chat(query: ChatQuery):
    response = chatbot.askBasedOnCurrentProducts(query.query)
    return {"response": response}
