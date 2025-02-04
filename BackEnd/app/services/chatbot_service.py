import json
import os
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from .products_service import ProductService
from .llm_provider import llm
from langchain_openai import OpenAIEmbeddings
from typing import List, Dict, Optional

EMBEDDING_MODEL = OpenAIEmbeddings()
CHAT_MEMORY_FILE = "chat_memory.json"


class ChatbotService:
    def __init__(self, product_service: Optional[ProductService] = None):
        """Inicializa la base de datos de embeddings con los productos existentes"""
        print("✅ Inicializando ChatbotService con OpenAI...")
        self.product_service = product_service or ProductService()
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

    def findRelevantProducts(self, query: str, top_k=3) -> List[Dict]:
        """Busca los productos más relevantes basándose en la consulta"""
        if not self.vector_db:
            if not self.createVectorDB():
                return []

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

        if relevant_products:
            product_info = "\n".join(
                f"- {p['brand']} {p['name']} (${p['price']}, {p['stock']} en stock)"
                for p in relevant_products
            )
        else:
            product_info = "No se encontraron productos que coincidan con la búsqueda."

        # Nueva versión del prompt con más precisión
        prompt = f"""
        Eres un asistente virtual de Makers Tech especializado en tecnología. 
        Siempre responde con precisión sobre los productos disponibles en nuestro catálogo.

         **Reglas de Respuesta:**
        - Si el usuario solo saluda, responde con: "¡Hola! ¿En qué puedo ayudarte hoy?"
        - Si el usuario pregunta por un producto específico, responde con su información si está disponible.
        - Si el producto no está en la lista, responde claramente que no está disponible.
        - No inventes información. Si no puedes responder, dilo claramente.
        - Responde siempre en un máximo de 100 palabras.
        - Usa diferentes maneras de responder para sonar natural y evitar repeticiones.

        ### Historial de conversación:
        {formatted_chat_history}

        ### Consulta del usuario:
        {query}

        ###  Catálogo de Productos Relevantes:
        {product_info if product_info else "No se encontraron productos disponibles."}

         **Genera una respuesta clara y concisa basada en la información proporcionada.**
        """

        if relevant_products:
            prompt += f"\nProductos disponibles:\n{product_info}"
        else:
            prompt += "\nNo se encontraron productos en stock para esta búsqueda."

        response = llm.generateResponseDependsModel(prompt)

        chat_history.extend([
            {"sender": "usuario", "text": query},
            {"sender": "asistente", "text": response}
        ])
        self.save_chat_history(chat_history)

        return {"response": response, "recommended_products": relevant_products}

    def load_chat_history(self):
        """Carga el historial de chat desde un archivo JSON"""
        if os.path.exists(CHAT_MEMORY_FILE):
            try:
                with open(CHAT_MEMORY_FILE, "r", encoding="utf-8") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("⚠️ El archivo chat_memory.json está corrupto. Creando un nuevo historial.")
                return []
        return []

    def save_chat_history(self, history):
        """Guarda el historial de chat en un archivo JSON"""
        try:
            with open(CHAT_MEMORY_FILE, "w", encoding="utf-8") as file:
                json.dump(history, file, indent=4)
        except Exception as e:
            print(f"⚠️ Error al guardar el historial del chat: {e}")

    def clear_chat_history(self):
        """Elimina el historial de chat almacenado en el archivo JSON"""
        try:
            if os.path.exists(CHAT_MEMORY_FILE):
                os.remove(CHAT_MEMORY_FILE)  # 🔥 Elimina el archivo
                print("✅ Historial de chat eliminado correctamente.")
            else:
                print("⚠️ No se encontró un historial de chat para eliminar.")
        except Exception as e:
            print(f"❌ Error al eliminar el historial de chat: {e}")
