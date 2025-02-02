from fastapi import APIRouter, HTTPException
from app.database import load_data, save_data
from app.models import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[ProductResponse])
def read_products():
    return load_data()

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int):
    products = load_data()
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate):
    products = load_data()
    new_product = product.dict()
    new_product["id"] = max([p["id"] for p in products], default=0) + 1
    products.append(new_product)
    save_data(products)
    return new_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate):
    products = load_data()
    for i, p in enumerate(products):
        if p["id"] == product_id:
            products[i] = {**product.dict(), "id": product_id}
            save_data(products)
            return products[i]
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@router.delete("/{product_id}")
def delete_product(product_id: int):
    products = load_data()
    updated_products = [p for p in products if p["id"] != product_id]
    if len(products) == len(updated_products):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    save_data(updated_products)
    return {"message": "Producto eliminado correctamente"}
