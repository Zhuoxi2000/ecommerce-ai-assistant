from typing import AsyncGenerator
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from app.core.config import settings

# 创建异步引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # 在开发模式中输出SQL语句
    future=True,
)

# 创建异步会话
async_session_factory = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autocommit=False, 
    autoflush=False,
)

# 创建Base类，用于定义模型
Base = declarative_base(metadata=MetaData())

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    依赖函数，用于获取数据库会话
    
    Yields:
        AsyncSession: 异步数据库会话
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()