from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/",response_model=schemas.Product, status_code=201)
async def create_product(product: schemas.ProductCreate,db: AsyncSession = Depends(get_db)):
    db_product =models.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


@router.get("/",response_model=List[schemas.Product])
async def read_products(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession =Depends(get_db)
):
    result = await db.execute(select(models.Product).offset(skip).limit(limit))
    products = result.scalars().all()
    return products


@router.get("/{product_id}", response_model=schemas.Product)
async def read_product(product_id: int, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Product).where(models.Product.id == product_id))
    db_product = result.scalar_one_or_none()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/{product_id}",response_model=schemas.Product)
async def update_product(product_id: int, product: schemas.ProductUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Product).where(models.Product.id == product_id))
    db_product = result.scalar_one_or_none()

    if db_product is None:
        raise HTTPException(status_code=404,detail="Product not found")

    update_data = product.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_product,key,value)

    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id:int,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Product).where(models.Product.id == product_id))
    db_product = result.scalar_one_or_none()

    if db_product is None:
        raise HTTPException(status_code=404,detail="Product not found")

    await db.delete(db_product)
    await db.commit()
    return {"detail": "Product deleted successfully"}
