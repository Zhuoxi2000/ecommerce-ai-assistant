from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.config import settings
from app.db.init_db import init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI驱动的电商助手API",
    version="0.1.0",
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix=settings.API_PREFIX)

@app.on_event("startup")
async def startup_event():
    # 初始化数据库
    await init_db()

@app.get("/")
async def root():
    return {"message": "欢迎使用AI电商助手API"}