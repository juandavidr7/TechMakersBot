from app.services.llm_provider import llm
from langchain.prompts import PromptTemplate
import requests

PRODUCTS_API = "http://127.0.0.1:8000/products/"

class ChatbotService:
    def getProducts(self):
        """Obtiene la lista de productos desde la API"""
        response = requests.get(PRODUCTS_API)
        if response.status_code == 200:
            return response.json()
        return []

    def askBasedOnCurrentProducts(self, query: str) -> str:
        """Genera una respuesta basada en productos disponibles"""
        products = self.getProducts()
        product_info = "\n".join([
                f"Marca: {p['marca']}\n"
                f"Modelo: {p['modelo']}\n"
                f"Precio: ${p['precio']}\n"
                f"Stock disponible: {p['stock']} unidades\n"
                f"Descripción: {p['descripcion']}\n" for p in products])

        template = PromptTemplate(
            input_variables=["query", "product_info"],
            template=(
                "Eres un asistente virtual de ventas de 'Makers Tech', una tienda especializada en tecnología. "
                "Tu tarea es ayudar a los clientes a encontrar la mejor computadora según sus necesidades, "
                "ofreciendo información precisa y en tiempo real sobre el inventario, características y precios de los productos disponibles.\n\n"

                "Inventario Actual:\n"
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
        return llm.generate(prompt)
