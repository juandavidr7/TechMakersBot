from pydantic import BaseModel

class ProductBase(BaseModel):
    brand: str
    name: str
    price: float
    stock: int
    description: str
    available: bool


class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

