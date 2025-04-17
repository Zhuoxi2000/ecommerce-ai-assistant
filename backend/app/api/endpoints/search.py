# app/api/endpoints/search.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List, Optional
from app.db.database import get_db
from app.schemas.product import ProductSearchQuery, SearchResults, ProductSearchResponse
from app.services.ai_service import AIService
from app.services.product_service import ProductService, search_products

router = APIRouter()  # 确保这一行存在
ai_service = AIService()

@router.post("/natural", response_model=SearchResults)
async def search_by_natural_language(
    search_query: ProductSearchQuery,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """基于自然语言搜索产品"""
    try:
        # 解析用户意图
        intent_data = await ai_service.parse_search_intent(search_query.query)
        
        # 搜索产品
        product_service = ProductService(db)
        search_results = await product_service.search_products_by_intent(
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
async def get_featured_products(
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取推荐产品"""
    product_service = ProductService(db)
    products = await product_service.get_featured_products(limit=limit)
    
    return {
        "items": products,
        "total": len(products),
        "page": 1,
        "limit": limit,
        "pages": 1
    }

@router.get("/", response_model=List[ProductSearchResponse])
async def search(
    q: str = Query(..., description="搜索查询"),
    categories: Optional[List[str]] = Query(None, description="按类别过滤"),
    min_price: Optional[float] = Query(None, description="最低价格"),
    max_price: Optional[float] = Query(None, description="最高价格"),
    sort_by: Optional[str] = Query(None, description="排序字段"),
    sort_order: Optional[str] = Query("asc", description="排序顺序"),
    page: int = Query(1, description="页码"),
    limit: int = Query(10, description="每页结果数"),
    db: AsyncSession = Depends(get_db)
):
    """
    搜索产品
    """
    try:
        results = await search_products(
            query=q,
            categories=categories,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            limit=limit,
            db=db
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"搜索失败: {str(e)}"
        )

@router.get("/suggest")
async def get_suggestions(
    q: str = Query(..., description="搜索查询"),
    limit: int = Query(5, description="建议数量")
):
    """
    获取搜索建议
    """
    return {
        "suggestions": [
            f"{q} 相关产品",
            f"{q} 流行款",
            f"{q} 热销商品"
        ]
    }