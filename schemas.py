# schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# 用户模型的基类
class UserBase(BaseModel):
    email: EmailStr  # 使用EmailStr确保email字段符合电子邮件格式

# 用户创建模型，用于用户注册时的数据传输
class UserCreate(UserBase):
    password: str  # 用户密码
    username: str

# 用户模型，继承自UserBase
class User(UserBase):
    id: int  # 用户ID
    username: str
    posts: List['Post'] = []  # 用户的帖子列表，使用字符串注释以避免循环引用
    answers: List['Answer'] = []  # 用户的回答列表，使用字符串注释以避免循环引用

    class Config:
        orm_mode = True  # 允许ORM模型作为输入

# 帖子模型的基类
class PostBase(BaseModel):
    title: str  # 帖子标题
    content: str  # 帖子内容

# 帖子创建模型
class PostCreate(PostBase):
    pass

# 完整帖子模型
class Post(PostBase):
    id: int  # 帖子ID
    owner_id: int  # 发帖用户的ID
    answers: List['Answer'] = []  # 帖子的回答列表，使用字符串注释以避免循环引用

    class Config:
        orm_mode = True  # 允许ORM模型作为输入

# 回答模型基类
class AnswerBase(BaseModel):
    content: str  # 回答内容

# 回答创建模型
class AnswerCreate(AnswerBase):
    pass

# 完整回答模型
class Answer(AnswerBase):
    id: int  # 回答ID
    created_at: datetime  # 回答创建时间
    author_id: int  # 回答作者的用户ID
    post_id: int  # 回答所属的帖子ID

    class Config:
        orm_mode = True  # 允许ORM模型作为输入

# 令牌模型
class Token(BaseModel):
    access_token: str  # 访问令牌
    token_type: str  # 令牌类型

# 令牌数据模型
class TokenData(BaseModel):
    email: Optional[str] = None  # 可选字段，用于存储电子邮件

# 通过字符串注释来延迟类型评估，解决模型之间的循环引用问题
User.model_rebuild()
Post.model_rebuild()
Answer.model_rebuild()
