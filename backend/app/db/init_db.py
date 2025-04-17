import json
import logging
import os
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import engine, Base, get_db
from app.models.product import Product
from app.services.product_service import ProductService

logger = logging.getLogger(__name__)

async def init_db():
    """
    初始化数据库：创建表和加载初始数据
    """
    try:
        # 创建所有定义的表
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("数据库表创建完成")
        
        # 加载示例产品数据
        await load_sample_data()
    
    except Exception as e:
        logger.error(f"初始化数据库失败: {str(e)}")
        raise

async def load_sample_data():
    """
    从JSON文件加载示例产品数据
    """
    data_file = Path(__file__).parent.parent.parent / "data" / "sample_products.json"
    
    if not os.path.exists(data_file):
        logger.warning(f"示例数据文件不存在: {data_file}")
        return
    
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            products_data = json.load(f)
        
        # 获取数据库会话
        async for db in get_db():
            product_service = ProductService(db)
            
            # 检查数据库是否已有产品
            existing_count = await product_service.count_products()
            
            if existing_count == 0:
                # 只有在数据库为空时才添加示例数据
                for product_data in products_data:
                    await product_service.create_product_from_dict(product_data)
                
                logger.info(f"成功加载 {len(products_data)} 个示例产品")
            else:
                logger.info(f"数据库中已有 {existing_count} 个产品，跳过示例数据加载")
    
    except Exception as e:
        logger.error(f"加载示例数据失败: {str(e)}")
        # 这里我们记录错误但不抛出异常，以允许应用程序继续启动