from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .models import TransactionType

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, description="Product name")
    description: Optional[str] = None
    price: float = Field(..., gt=0, description="Price must be greater than zero")

class ProductCreate(ProductBase):
    available_quantity: int = Field(0, ge=0, description="Available quantity must be non-negative")

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)

class Product(ProductBase):
    id: int
    available_quantity: int

    class Config:
        from_attributes = True

class StockTransactionBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Transaction quantity must be positive")
    transaction_type: TransactionType

class StockTransactionCreate(StockTransactionBase):
    pass

class StockTransaction(StockTransactionBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
