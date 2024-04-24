# database.py
from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

# 从环境变量中加载数据库URL
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建异步数据库引擎
#engine = create_async_engine(
#    DATABASE_URL, echo=True
#)

# 创建一个异步会话工厂
#SessionLocal = sessionmaker(
#    engine, class_=AsyncSession, expire_on_commit=False
#)

# 使用异步生成器来提供会话
#async def get_db() -> AsyncGenerator:
#    async with SessionLocal() as session:
#        yield session

# 声明基类
Base = declarative_base()
