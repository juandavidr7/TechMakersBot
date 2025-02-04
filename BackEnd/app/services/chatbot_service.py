

import json
import os
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from app.services.products_service import ProductService
from app.services.llm_provider import llm
from langchain_openai import OpenAIEmbeddings
from typing import List, Dict, Optional

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

    def findRelevantProducts(self, query: str, top_k=5) -> List[Dict]:
        """Busca los productos más relevantes basándose en la consulta"""
        if not self.vector_db:
            self.createVectorDB()
        results = self.vector_db.similarity_search(query, k=top_k)
        return [
            {
                "id": doc.metadata["id"],
                "name": doc.page_content.split("-")[0].strip(),
                "brand": doc.metadata["brand"],
                "price": doc.metadata["price"],
                "stock": doc.metadata["stock"],
            }
            for doc in results
        ]

    def askBasedOnCurrentProducts(self, query: str) -> Dict:
        """Genera una respuesta basada en productos relevantes y usa historial de chat"""

        chat_history = self.load_chat_history()
        relevant_products = self.findRelevantProducts(query)

        formatted_chat_history = "\n".join(
            f"{msg['sender']}: {msg['text']}" for msg in chat_history[-5:]
        ) if chat_history else "No hay historial previo."

        product_info = "\n".join(
            f"- {p['brand']} {p['name']} (${p['price']}, {p['stock']} en stock)"
            for p in relevant_products
        )

        prompt = f"""
        Eres un asistente virtual de Makers Tech especializado en tecnología. 
        Tu objetivo es proporcionar respuestas precisas, profesionales y empáticas sobre nuestros productos.  
        Siempre debes basarte en la información de nuestro catálogo y evitar responder con información inventada.

        ### Instrucciones Claves:
        1. Ordena los productos correctamente al responder preguntas sobre precios.
        2. Si el usuario pregunta por los productos más baratos o caros, selecciona los tres con los precios más bajos o altos, respetando el stock disponible.
        3. Si el usuario menciona un producto específico que fue omitido, verifica si debió estar en la lista y justifica la omisión si fue un error.
        4. Evita respuestas repetitivas y usa diferentes maneras de expresar la misma idea para sonar más natural.

        ### Historial de conversación:
        {formatted_chat_history}

        ### Catálogo de Productos Relevantes:
        {product_info if product_info else "No se encontraron productos disponibles."}

        Responde de forma clara y profesional basándote en la información proporcionada.  
        Si no puedes responder, indícalo claramente en lugar de inventar datos.
        """

        response = llm.generateResponseDependsModel(prompt)

        chat_history.extend([
            {"sender": "user", "text": query},
            {"sender": "bot", "text": response}
        ])
        self.save_chat_history(chat_history)

        return {"response": response, "recommended_products": relevant_products}

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
