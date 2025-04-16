# app/api/endpoints/products.py
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from app.db.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取产品列表"""
    product_service = ProductService(db)
    products = product_service.get_products(skip=skip, limit=limit, category=category)
    return products

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """创建新产品"""
    product_service = ProductService(db)
    return product_service.create_product(product=product)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int = Path(..., description="产品ID"),
    db: Session = Depends(get_db)
):
    """根据ID获取产品详情"""
    product_service = ProductService(db)
    product = product_service.get_product(product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    """更新产品信息"""
    product_service = ProductService(db)
    db_product = product_service.get_product(product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="产品不存在")
    return product_service.update_product(product_id=product_id, product=product)

@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """删除产品"""
    product_service = ProductService(db)
    db_product = product_service.get_product(product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="产品不存在")
    product_service.delete_product(product_id=product_id)
    return None