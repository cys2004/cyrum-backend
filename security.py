from datetime import datetime, timedelta  # 用于处理日期和时间操作
from typing import Optional  # 用于支持可选类型注释
from jose import JWTError, jwt  # 用于处理JSON Web Token的操作和错误处理
from passlib.context import CryptContext  # 用于密码哈希
from fastapi.security import OAuth2PasswordBearer  # FastAPI的OAuth2密码承载者工具
from fastapi import Depends, HTTPException, status  # FastAPI的依赖注入工具，HTTP异常和状态码
from sqlalchemy.orm import Session  # SQLAlchemy的会话管理
import crud, schemas  # 导入CRUD操作、数据库模型和Pydantic模型
from database import SessionLocal  # 数据库会话本地实例
import os  # 用于读取环境变量

# 从环境变量中获取密钥，设置JWT算法和访问令牌过期时间
SECRET_KEY = os.getenv("SECRET_KEY")  # 密钥用于JWT编码和解码
ALGORITHM = "HS256"  # 使用的JWT算法，默认为HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 设置访问令牌过期时间（分钟）

# 密码上下文实例，用于密码的加密和校验
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2的密码承载者实例，用于获取token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 密码哈希值获取函数
def get_password_hash(password):
    return pwd_context.hash(password)  # 返回密码的哈希值

# 密码验证函数
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)  # 返回密码是否匹配

# 用户认证函数
def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_name(db, username=username)  # 从数据库中获取用户
    if not user:  # 如果用户不存在，返回False
        return False
    if not verify_password(password, user.hashed_password):  # 如果密码不匹配，返回False
        return False
    return user  # 如果用户存在且密码匹配，返回用户对象

# 定义一个函数创建访问令牌
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()  # 复制数据
    if expires_delta:  # 如果设置了过期时间，则计算过期时间点
        expire = datetime.utcnow() + expires_delta
    else:  # 如果没有设置过期时间，使用默认的15分钟后过期
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})  # 添加过期时间到数据中
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # 编码JWT
    return encoded_jwt  # 返回编码后的JWT

# 获取当前用户函数
def get_current_user(db: Session = Depends(SessionLocal), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,  # 未授权的HTTP状态代码
        detail="Could not validate credentials",  # 错误详细信息
        headers={"WWW-Authenticate": "Bearer"},  # 让客户端知道认证信息应该在Bearer Token中提供
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # 解码JWT
        email: str = payload.get("sub")  # 从payload中获取用户标识（主题）
        if email is None:  # 如果没有获取到email，抛出异常
            raise credentials_exception
        token_data = schemas.TokenData(email=email)  # 创建token数据实例
    except JWTError:  # 如果在解码过程中发生错误，抛出异常
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)  # 从数据库中获取用户
    if user is None:  # 如果用户不存在，抛出异常
        raise credentials_exception
    return user  # 返回用户实例
