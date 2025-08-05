from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/stock",
    tags=["Stock"],
)


@router.post("/", response_model=schemas.StockTransaction, status_code=201)
async def create_stock_transaction(transaction:schemas.StockTransactionCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(
            select(models.Product).where(models.Product.id==transaction.product_id).with_for_update()
        )
        db_product = result.scalar_one_or_none()

        if db_product is None:
            raise HTTPException(status_code=404,detail="Product not found")

        if transaction.transaction_type == models.TransactionType.IN:
            db_product.available_quantity += transaction.quantity
        elif transaction.transaction_type == models.TransactionType.OUT:
            if db_product.available_quantity < transaction.quantity:
                raise HTTPException(status_code=400, detail="Insufficient stock")
            db_product.available_quantity -=transaction.quantity

        db_transaction = models.StockTransaction(**transaction.dict())

        db.add(db_product)
        db.add(db_transaction)

    await db.refresh(db_transaction)
    return db_transaction


@router.get("/",response_model=List[schemas.StockTransaction])
async def read_stock_transactions(skip: int =0, limit: int =100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.StockTransaction).order_by(models.StockTransaction.timestamp.desc()).offset(skip).limit(limit))
    transactions = result.scalars().all()
    return transactions


@router.get("/product/{product_id}", response_model=List[schemas.StockTransaction])
async def read_product_stock_transactions(product_id:int, db:AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.StockTransaction)
        .where(models.StockTransaction.product_id==product_id)
        .order_by(models.StockTransaction.timestamp.desc())
    )
    transactions = result.scalars().all()
    if not transactions:
        product_check = await db.execute(select(models.Product).where(models.Product.id==product_id))
        if product_check.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
    return transactions
