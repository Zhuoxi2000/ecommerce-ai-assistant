from typing import Dict, List, Optional, Any, Union
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductSearchResponse

class ProductService:
    """产品服务，处理产品相关的业务逻辑"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_products(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None
    ) -> List[Product]:
        """获取产品列表"""
        query = select(Product)
        if category:
            query = query.where(Product.category == category)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_product(self, product_id: int) -> Optional[Product]:
        """根据ID获取产品"""
        query = select(Product).where(Product.id == product_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def create_product(self, product: ProductCreate) -> Product:
        """创建新产品"""
        db_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            currency=product.currency,
            category=product.category,
            stock=product.stock,
            image_url=product.image_url,
            sku=product.sku,
            tags=product.tags,
            attributes=product.attributes
        )
        self.db.add(db_product)
        await self.db.commit()
        await self.db.refresh(db_product)
        return db_product
    
    async def create_product_from_dict(self, product_data: Dict[str, Any]) -> Product:
        """从字典创建产品"""
        db_product = Product.from_dict(product_data)
        self.db.add(db_product)
        await self.db.commit()
        await self.db.refresh(db_product)
        return db_product
    
    async def update_product(self, product_id: int, product: ProductUpdate) -> Product:
        """更新产品信息"""
        db_product = await self.get_product(product_id)
        
        # 仅更新非None字段
        update_data = product.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        
        await self.db.commit()
        await self.db.refresh(db_product)
        return db_product
    
    async def delete_product(self, product_id: int) -> None:
        """删除产品"""
        db_product = await self.get_product(product_id)
        await self.db.delete(db_product)
        await self.db.commit()
    
    async def count_products(self) -> int:
        """获取产品总数"""
        query = select(func.count()).select_from(Product)
        result = await self.db.execute(query)
        return result.scalar_one()
    
    async def get_featured_products(self, limit: int = 10) -> List[Product]:
        """获取推荐产品"""
        # 这里可以实现自定义逻辑，例如按照销量、评分等获取推荐产品
        # 这里简化为获取最新产品
        query = select(Product).order_by(Product.created_at.desc()).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()


async def search_products(
    query: str,
    categories: Optional[List[str]] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
    page: int = 1,
    limit: int = 10,
    db: Optional[AsyncSession] = None
) -> List[ProductSearchResponse]:
    """
    搜索产品的函数
    
    注意：这是一个独立函数，不在ProductService类中，主要用于搜索端点
    通常情况下，你会使用数据库会话并自己构建复杂的查询
    这里简化为返回假数据
    """
    # 这是模拟数据，实际应用中会从数据库查询
    demo_products = [
        ProductSearchResponse(
            id=1,
            name="高品质T恤",
            description="舒适透气的纯棉T恤",
            price=99.0,
            category="服装",
            image_url="https://example.com/tshirt.jpg",
            relevance_score=0.95
        ),
        ProductSearchResponse(
            id=2,
            name="时尚牛仔裤",
            description="经典蓝色牛仔裤，适合日常穿着",
            price=199.0,
            category="服装",
            image_url="https://example.com/jeans.jpg",
            relevance_score=0.85
        )
    ]
    
    return demo_products