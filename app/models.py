from typing import Optional

from pydantic import BaseModel

class ProductBase(BaseModel):
    brand: str
    name: str
    price: float
    stock: int
    description: str
    available: bool
    image: Optional[str] = None
    image_base64: Optional[str] = None



class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

