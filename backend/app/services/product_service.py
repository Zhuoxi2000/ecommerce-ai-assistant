from typing import Dict, List, Optional, Any, Union
from sqlalchemy import select, func, or_, and_, desc, asc
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
        
    async def search_products_by_intent(
        self, 
        intent_data: Dict[str, Any],
        page: int = 1,
        limit: int = 20
    ) -> Dict[str, Any]:
        """基于意图数据搜索产品"""
        query = select(Product)
        
        # 筛选条件
        filters = []
        
        # 产品类型筛选
        if product_type := intent_data.get("product_type"):
            if product_type != "其他":
                filters.append(Product.category.ilike(f"%{product_type}%"))
        
        # 价格范围筛选
        if price_range := intent_data.get("price_range"):
            if price_range.get("min", 0) > 0:
                filters.append(Product.price >= price_range["min"])
            if price_range.get("max", 0) > 0:
                filters.append(Product.price <= price_range["max"])
        
        # 品牌筛选 - 假设品牌信息可能在tags字段中
        if brands := intent_data.get("brands"):
            for brand in brands:
                # 注意：这里需要根据您的实际数据结构调整
                filters.append(Product.tags.contains([brand]))
        
        # 关键词筛选
        if keywords := intent_data.get("keywords"):
            keyword_filters = []
            for keyword in keywords:
                keyword_filters.append(
                    or_(
                        Product.name.ilike(f"%{keyword}%"),
                        Product.description.ilike(f"%{keyword}%")
                    )
                )
            if keyword_filters:
                filters.append(or_(*keyword_filters))
        
        # 应用筛选条件
        if filters:
            query = query.where(and_(*filters))
        
        # 排序处理
        sort_preference = intent_data.get("sort_preference")
        if sort_preference:
            if "价格" in sort_preference and "高到低" in sort_preference:
                query = query.order_by(desc(Product.price))
            elif "价格" in sort_preference:
                query = query.order_by(asc(Product.price))
            else:
                # 默认按创建时间排序
                query = query.order_by(desc(Product.created_at))
        else:
            # 默认排序
            query = query.order_by(desc(Product.created_at))
        
        # 计算总数
        total_query = select(func.count()).select_from(Product)
        if filters:
            total_query = total_query.where(and_(*filters))
        
        total_result = await self.db.execute(total_query)
        total = total_result.scalar_one()
        
        # 分页
        query = query.offset((page - 1) * limit).limit(limit)
        result = await self.db.execute(query)
        products = result.scalars().all()
        
        # 构建响应
        return {
            "items": products,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit if limit > 0 else 0
        }


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