# app/schemas/product.py
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl, validator
from datetime import datetime

# 基础产品模型
class ProductBase(BaseModel):
    """产品基础信息"""
    name: str = Field(..., description="产品名称")
    description: Optional[str] = Field(None, description="产品描述")
    price: float = Field(..., description="产品价格")
    currency: str = Field("CNY", description="货币单位")
    category: str = Field(..., description="产品类别")
    stock: int = Field(..., description="库存数量")
    image_url: Optional[HttpUrl] = Field(None, description="产品图片URL")

class ProductCreate(ProductBase):
    """创建产品时的输入模型"""
    sku: str = Field(..., description="库存单位")
    tags: List[str] = Field(default=[], description="产品标签")
    attributes: Dict[str, Any] = Field(default={}, description="产品属性")

class ProductUpdate(BaseModel):
    """更新产品的输入模型"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    category: Optional[str] = None
    stock: Optional[int] = None
    image_url: Optional[HttpUrl] = None
    sku: Optional[str] = None
    tags: Optional[List[str]] = None
    attributes: Optional[Dict[str, Any]] = None

class ProductResponse(ProductBase):
    """产品响应模型"""
    id: int
    sku: str
    tags: List[str] = []
    attributes: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 搜索相关模型
class ProductSearchQuery(BaseModel):
    """产品搜索查询"""
    query: str = Field(..., description="搜索查询文本")
    page: int = Field(1, description="页码")
    limit: int = Field(10, description="每页结果数")

class ProductSearchResponse(BaseModel):
    """产品搜索结果项"""
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category: str
    image_url: Optional[HttpUrl] = None
    relevance_score: Optional[float] = None

    class Config:
        orm_mode = True

class SearchResults(BaseModel):
    """搜索结果集合"""
    items: List[ProductSearchResponse]
    total: int
    page: int
    limit: int
    pages: int