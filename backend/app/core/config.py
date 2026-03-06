"""
应用配置管理 - 个人开发者简化版
使用 pydantic-settings 管理环境变量
"""

from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""

    # 基础配置
    APP_NAME: str = "PetVoyageAI"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"  # development | production

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # 数据库配置（SQLite简化版）
    DATABASE_URL: str = "sqlite:///./data/petvoyage.db"

    # JWT配置
    JWT_SECRET_KEY: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7天

    # AI服务配置 - 硅基流动
    SILICONFLOW_API_KEY: str = ""  # 从环境变量获取
    SILICONFLOW_API_URL: str = "https://api.siliconflow.cn/v1/image/generations"
    AI_DEFAULT_MODEL: str = "stabilityai/stable-diffusion-xl-base-1.0"
    AI_TIMEOUT_SECONDS: int = 60
    AI_MAX_RETRIES: int = 3

    # 文件存储配置（本地存储简化版）
    UPLOAD_DIR: str = "./data/uploads"
    GENERATED_DIR: str = "./data/generated"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    # 限流配置
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_FREE_USER_DAILY: int = 3
    RATE_LIMIT_PREMIUM_USER_DAILY: int = 100

    # CORS配置
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]

    # 日志配置
    LOG_LEVEL: str = "INFO"

    # 短信服务（开发阶段可禁用）
    SMS_ENABLED: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


# 全局配置实例
settings = get_settings()
