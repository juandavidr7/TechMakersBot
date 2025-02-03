from app.services.llm_provider import llm
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

from app.services.products_service import ProductService  # ✅ Importamos ProductService


class ChatbotService:
    def __init__(self, product_service: ProductService):
        """Inicializa la base de datos de embeddings con los productos existentes"""
        print("✅ Inicializando ChatbotService...")
        self.product_service = product_service  # ✅ Usamos ProductService para obtener productos
        try:
            self.embeddings = OpenAIEmbeddings()
            self.vector_db = None
            print("✅ Embeddings inicializados correctamente.")

            # Intentar crear la base de datos de vectores con los productos disponibles
            if not self.createVectorDB():
                print("⚠️ No se pudo inicializar la base de datos de vectores.")
        except Exception as e:
            print(f"🚨 ERROR en la inicialización de ChatbotService: {e}")

    def createVectorDB(self):
        """Crea una base de datos de búsqueda basada en embeddings de productos"""
        print("🔍 Creando base de datos de vectores...")
        try:
            products = self.product_service.get_all_products()  # ✅ Obtenemos productos desde ProductService
            if not products:
                print("⚠️ No se encontraron productos. No se creó la base de datos de embeddings.")
                return False

            docs = [
                Document(
                    page_content=f"{p['brand']} {p['name']} - {p['description']}",
                    metadata={"id": p["id"], "price": p["price"], "stock": p["stock"], "brand": p["brand"]}
                )
                for p in products
            ]
            print(f"✅ Se crearon {len(docs)} documentos para FAISS.")
            self.vector_db = FAISS.from_documents(docs, self.embeddings)
            print("✅ Base de datos de vectores creada correctamente.")
            return True
        except Exception as e:
            print(f"🚨 ERROR en createVectorDB: {e}")
            return False

    def findRelevantProducts(self, query: str, top_k=3):
        """Busca los productos más relevantes basándose en la consulta"""
        print(f"🔍 Buscando productos relevantes para: '{query}'")
        try:
            if not self.vector_db:
                print("⚠️ Base de datos de vectores no encontrada. Intentando crearla...")
                if not self.createVectorDB():
                    return []

            results = self.vector_db.similarity_search(query, k=top_k)
            print(f"✅ Se encontraron {len(results)} productos relevantes.")
            return results
        except Exception as e:
            print(f"🚨 ERROR en findRelevantProducts: {e}")
            return []

    def askBasedOnCurrentProducts(self, query: str) -> str:
        """Genera una respuesta basada en productos relevantes"""
        print(f"🔍 Generando respuesta para la consulta: '{query}'")
        try:
            relevant_products = self.findRelevantProducts(query)
            if not relevant_products:
                print("⚠️ No se encontraron productos relevantes.")
                return "Lo siento, no encontré productos relacionados con tu búsqueda."

            product_info = "\n".join([
                f"Marca: {doc.metadata['brand']}\n"
                f"Modelo: {doc.page_content.split('-')[0].strip()}\n"
                f"Precio: ${doc.metadata['price']}\n"
                f"Stock disponible: {doc.metadata['stock']} unidades\n"
                f"Descripción: {doc.page_content.split('-')[1].strip()}\n"
                for doc in relevant_products
            ])

            template = PromptTemplate(
                input_variables=["query", "product_info"],
                template=(
                    "Eres un asistente virtual de ventas de 'Makers Tech', una tienda especializada en tecnología. "
                    "Tu tarea es ayudar a los clientes a encontrar la mejor computadora según sus necesidades, "
                    "ofreciendo información precisa y en tiempo real sobre el inventario, características y precios de los productos disponibles.\n\n"

                    "Inventario Relevante:\n"
                    "{product_info}\n\n"

                    "Reglas para responder:\n"
                    "- Usa un tono profesional, amigable y personalizado.\n"
                    "- Si el usuario pregunta por disponibilidad, informa cuántas computadoras hay en total y cuántas de cada marca.\n"
                    "- Si el usuario pregunta por un modelo específico, proporciona detalles sobre sus características, precio y stock.\n"
                    "- Si el usuario quiere comparar productos, muestra diferencias clave y sugiere opciones según el uso (gaming, trabajo, etc.).\n"
                    "- No inventes productos ni proporciones información fuera del inventario.\n"
                )
            )

            prompt = template.format(query=query, product_info=product_info)
            print(f"🔹 Enviando consulta a LLM:\n{prompt}")

            response = llm.generateResponseDependsModel(prompt)
            print(f"🤖 Respuesta del chatbot:\n{response}")
            return response

        except Exception as e:
            print(f"🚨 ERROR en askBasedOnCurrentProducts: {e}")
            return "Lo siento, hubo un error al procesar tu consulta."
