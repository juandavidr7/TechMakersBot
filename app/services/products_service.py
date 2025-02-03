from app.database import load_data, save_data
from app.models import ProductCreate

class ProductService:
    def __init__(self):
        self.products = load_data()

    def get_all_products(self):
        """Retorna todos los productos."""
        return self.products

    def get_product_by_id(self, product_id):
        """Busca un producto por ID."""
        return next((p for p in self.products if p["id"] == product_id), None)

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
        return None  # Retorna None si no encuentra el producto

    def delete_product(self, product_id: int):
        """Elimina un producto por ID."""
        updated_products = [p for p in self.products if p["id"] != product_id]
        if len(self.products) == len(updated_products):
            return False  # Retorna False si no encontró el producto
        self.products = updated_products
        save_data(self.products)
        return True  # Retorna True si eliminó el producto correctamente
