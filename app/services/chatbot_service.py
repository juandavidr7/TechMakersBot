import json
import os
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from app.services.products_service import ProductService
from app.services.llm_provider import llm
from langchain_openai import OpenAIEmbeddings

EMBEDDING_MODEL = OpenAIEmbeddings()
CHAT_MEMORY_FILE = "chat_memory.json"


class ChatbotService:
    def __init__(self, product_service: ProductService):
        """Inicializa la base de datos de embeddings con los productos existentes"""
        print("✅ Inicializando ChatbotService con OpenAI...")
        self.product_service = product_service
        self.embeddings = EMBEDDING_MODEL
        self.vector_db = None
        self.createVectorDB()

    def createVectorDB(self):
        """Crea una base de datos de búsqueda basada en embeddings de productos"""
        print("🔍 Creando base de datos de vectores...")
        products = self.product_service.get_all_products()
        if not products:
            print("⚠️ No se encontraron productos.")
            return False

        docs = [
            Document(
                page_content=f"{p['brand']} {p['name']} - {p['description']}",
                metadata={"id": p["id"], "price": p["price"], "stock": p["stock"], "brand": p["brand"]}
            )
            for p in products
        ]

        self.vector_db = FAISS.from_documents(docs, self.embeddings)
        print("✅ Base de datos de vectores creada correctamente.")
        return True

    def findRelevantProducts(self, query: str, top_k=10):
        """Busca los productos más relevantes basándose en la consulta"""
        if not self.vector_db:
            self.createVectorDB()
        results = self.vector_db.similarity_search(query, k=top_k)
        return results

    def load_chat_history(self):
        """Carga el historial de chat desde un archivo JSON"""
        if os.path.exists(CHAT_MEMORY_FILE):
            with open(CHAT_MEMORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        return []

    def save_chat_history(self, history):
        """Guarda el historial de chat en un archivo JSON"""
        with open(CHAT_MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4)

    def askBasedOnCurrentProducts(self, query: str) -> str:
        """Genera una respuesta basada en productos relevantes y usa historial de chat"""


        chat_history = self.load_chat_history()


        relevant_products = self.findRelevantProducts(query)
        if not relevant_products:
            return "Lo siento, no encontré productos relacionados con tu búsqueda."


        formatted_chat_history = "\n".join(
            f"{msg['sender']}: {msg['text']}" for msg in chat_history[-5:]
        ) if chat_history else "No hay historial previo."


        product_info = "\n".join(
            f"- {doc.metadata['brand']} {doc.page_content.split('-')[0].strip()} "
            f"(${doc.metadata['price']}, {doc.metadata['stock']} en stock)"
            for doc in relevant_products
        )

        prompt = f"""
    Saluda, eres un asistente virtual de Makers Tech. Responde de manera profesional, empatica, clara y concisa.

     Historial de conversación:
    {formatted_chat_history}

     Pregunta del cliente:
    "{query}"

     Productos relevantes:
    {product_info}

    Responde solo con información relevante. Si no puedes responder, indícalo claramente.
    """
        # 6️⃣ Enviar el prompt al LLM
        response = llm.generateResponseDependsModel(prompt)

        # 7️⃣ Guardar conversación en JSON
        chat_history.extend([
            {"sender": "user", "text": query},
            {"sender": "bot", "text": response}
        ])
        self.save_chat_history(chat_history)

        return response


