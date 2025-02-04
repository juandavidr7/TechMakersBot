import os
import base64
from app.database import load_data, save_data
from app.models import ProductCreate

class ProductService:
    def __init__(self):
        self.products = load_data()
        self.image_path = "app/data/images"

    def _get_image_base64(self, product_id):
        """Carga la imagen en Base64 si existe, de lo contrario, devuelve None."""
        image_file = os.path.join(self.image_path, f"{product_id}.png")

        if os.path.exists(image_file):
            with open(image_file, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode("utf-8")
        return None  # Si la imagen no existe

    def get_all_products(self):
        """Retorna todos los productos con su URL e imagen en Base64."""
        products_with_images = []
        for product in self.products:
            product_with_image = product.copy()
            product_with_image["image"] = f"{self.base_url}/{product['id']}.png"
            product_with_image["image_base64"] = self._get_image_base64(product["id"])
            products_with_images.append(product_with_image)
        return products_with_images

    def get_product_by_id(self, product_id):
        """Busca un producto por ID y añade la URL y la imagen en Base64 si existe."""
        product = next((p for p in self.products if p["id"] == product_id), None)
        if product:
            product["image"] = f"{self.base_url}/{product['id']}.png"  # ✅ URL de la imagen
            product["image_base64"] = self._get_image_base64(product_id)
        return product


    def create_product(self, product_data: ProductCreate):
        """Crea un nuevo producto y lo guarda en la base de datos."""
        new_product = product_data.dict()
        new_product["id"] = max([p["id"] for p in self.products], default=0) + 1
        self.products.append(new_product)
        save_data(self.products)
        return new_product

    def update_product(self, product_id: int, product_data: ProductCreate):
        """Actualiza un producto existente."""
        for i, p in enumerate(self.products):
            if p["id"] == product_id:
                self.products[i] = {**product_data.dict(), "id": product_id}
                save_data(self.products)
                return self.products[i]
        return None

    def delete_product(self, product_id: int):
        """Elimina un producto por ID."""
        updated_products = [p for p in self.products if p["id"] != product_id]
        if len(self.products) == len(updated_products):
            return False
        self.products = updated_products
        save_data(self.products)
        return True
