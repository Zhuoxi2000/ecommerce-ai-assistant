# app/api/endpoints/search.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, Dict
from app.db.database import get_db
from app.schemas.product import ProductSearchQuery, SearchResults  # 修正这里的导入
from app.services.ai_service import AIService
from app.services.product_service import ProductService

router = APIRouter()  # 确保这一行存在
ai_service = AIService()

@router.post("/natural", response_model=SearchResults)
async def search_by_natural_language(
    search_query: ProductSearchQuery,
    db: Session = Depends(get_db)
) -> Any:
    """基于自然语言搜索产品"""
    try:
        # 解析用户意图
        intent_data = await ai_service.parse_search_intent(search_query.query)
        
        # 搜索产品
        product_service = ProductService(db)
        search_results = product_service.search_products(
            intent_data=intent_data,
            page=search_query.page,
            limit=search_query.limit
        )
        
        return search_results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"搜索失败: {str(e)}"
        )

@router.get("/featured", response_model=SearchResults)
def get_featured_products(
    limit: int = 10,
    db: Session = Depends(get_db)
) -> Any:
    """获取推荐产品"""
    product_service = ProductService(db)
    products = product_service.get_featured_products(limit=limit)
    
    return {
        "items": products,
        "total": len(products),
        "page": 1,
        "limit": limit,
        "pages": 1
    }