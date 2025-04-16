from fastapi import APIRouter
from app.api.endpoints import products, search

api_router = APIRouter()

api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(products.router, prefix="/products", tags=["products"])