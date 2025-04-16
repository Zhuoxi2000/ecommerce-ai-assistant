from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Dict, List, Any, Optional

from app.db.database import Base

class Product(Base):
    """产品数据库模型"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    currency = Column(String(3), default="CNY")
    category = Column(String(100), nullable=False, index=True)
    stock = Column(Integer, default=0)
    image_url = Column(String(512), nullable=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    tags = Column(JSON, default=list)
    attributes = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def to_dict(self) -> Dict[str, Any]:
        """将模型转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "currency": self.currency,
            "category": self.category,
            "stock": self.stock,
            "image_url": self.image_url,
            "sku": self.sku,
            "tags": self.tags or [],
            "attributes": self.attributes or {},
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        """从字典创建模型实例"""
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            price=data.get("price"),
            currency=data.get("currency", "CNY"),
            category=data.get("category"),
            stock=data.get("stock", 0),
            image_url=data.get("image_url"),
            sku=data.get("sku"),
            tags=data.get("tags", []),
            attributes=data.get("attributes", {})
        )