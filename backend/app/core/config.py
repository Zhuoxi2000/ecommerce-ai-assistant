import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import List

# 加载 .env 文件
dotenv_path = Path(__file__).parent.parent.parent / ".env"
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Settings(BaseSettings):
    """应用配置"""
    
    # 基本信息
    PROJECT_NAME: str = "AI电商助手"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    VERSION: str = "0.1.0"
    
    # 数据库配置
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite+aiosqlite:///./ecommerce.db"
    )
    
    # 安全配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-for-dev-only")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    
    # 跨域设置 - 修改这里，将字符串解析改为直接使用列表
    # 避免从环境变量解析 JSON 列表
    ALLOWED_HOSTS: List[str] = ["*"]  # 在生产环境中应限制为特定域名
    
    # AI服务配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DEFAULT_AI_MODEL: str = "gpt-3.5-turbo"
    
    # 文件路径
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    MEDIA_DIR: Path = BASE_DIR / "media"
    
    class Config:
        case_sensitive = True
        env_file = dotenv_path

# 创建设置实例
settings = Settings()

# 确保必要的目录存在
os.makedirs(settings.MEDIA_DIR, exist_ok=True)