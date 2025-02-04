from fastapi import APIRouter, HTTPException, Depends
from ..models import ProductCreate, ProductResponse
from ..services.products_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


def get_product_service():
    return ProductService()

@router.get("/", response_model=list[ProductResponse])
def read_products(product_service: ProductService = Depends(get_product_service)):
    """Obtiene todos los productos con su imagen en Base64."""
    return product_service.get_all_products()

@router.get("/{product_id}", response_model=ProductResponse)
def read_product_by_id(product_id: int, product_service: ProductService = Depends(get_product_service)):
    """Obtiene un producto por su ID con la imagen en Base64."""
    product = product_service.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, product_service: ProductService = Depends(get_product_service)):
    """Crea un nuevo producto."""
    return product_service.create_product(product)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, product_service: ProductService = Depends(get_product_service)):
    """Actualiza un producto existente."""
    updated_product = product_service.update_product(product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated_product

@router.delete("/{product_id}")
def delete_product(product_id: int, product_service: ProductService = Depends(get_product_service)):
    """Elimina un producto por ID."""
    if not product_service.delete_product(product_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}
