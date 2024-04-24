# models.py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# 定义User模型，表示用户表
class User(Base):
    __tablename__ = "users"  # 数据库中的表名

    id = Column(Integer, primary_key=True, index=True)  # 用户ID，主键，建立索引
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)  # 用户邮箱，唯一，建立索引
    hashed_password = Column(String)  # 用户密码的散列值

    # 建立与Post模型的关系，表示用户可以拥有多个帖子
    posts = relationship("Post", back_populates="owner")
    # 建立与Answer模型的关系，表示用户可以拥有多个回答
    answers = relationship("Answer", back_populates="author")

# 定义Post模型，表示帖子表
class Post(Base):
    __tablename__ = "posts"  # 数据库中的表名

    id = Column(Integer, primary_key=True, index=True)  # 帖子ID，主键，建立索引
    title = Column(String, index=True)  # 帖子标题，建立索引
    content = Column(Text)  # 帖子内容
    owner_id = Column(Integer, ForeignKey("users.id"))  # 帖子所有者的用户ID，外键关联到用户表的ID字段

    # 建立与User模型的关系，表示帖子属于一个用户
    owner = relationship("User", back_populates="posts")
    # 建立与Answer模型的关系，表示帖子可以有多个回答
    answers = relationship("Answer", back_populates="post")

# 定义Answer模型，表示回答表
class Answer(Base):
    __tablename__ = "answers"  # 数据库中的表名

    id = Column(Integer, primary_key=True, index=True)  # 回答ID，主键，建立索引
    content = Column(Text)  # 回答内容
    created_at = Column(DateTime, default=datetime.utcnow)  # 回答创建的时间，默认为当前UTC时间
    author_id = Column(Integer, ForeignKey("users.id"))  # 回答作者的用户ID，外键关联到用户表的ID字段
    post_id = Column(Integer, ForeignKey("posts.id"))  # 回答所属的帖子ID，外键关联到帖子表的ID字段

    # 建立与User模型的关系，表示回答属于一个用户
    author = relationship("User", back_populates="answers")
    # 建立与Post模型的关系，表示回答属于一个帖子
    post = relationship("Post", back_populates="answers")