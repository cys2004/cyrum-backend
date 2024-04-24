# crud.py
from sqlalchemy.orm import Session  # 导入SQLAlchemy的Session用于数据库会话管理
import models, schemas  # 导入定义好的数据库模型和pydantic模型
from security import get_password_hash, verify_password  # 导入密码哈希和校验的函数

# 用户相关操作

# 使用邮箱获取用户
def get_user_by_email(db: Session, email: str):
    # 在数据库中查询邮箱对应的用户，返回第一个匹配的结果
    return db.query(models.User).filter(models.User.email == email).first()

# 使用用户名获取用户
def get_user_by_name(db: Session, username: str):
    # 在数据库中查询邮箱对应的用户，返回第一个匹配的结果
    return db.query(models.User).filter(models.User.username == username).first()

# 创建新用户
def create_user(db: Session, user: schemas.UserCreate):
    # 使用密码生成哈希值
    hashed_password = get_password_hash(user.password)
    # 创建一个用户对象，密码为哈希后的密码
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    # 将用户对象添加到数据库会话中
    db.add(db_user)
    # 提交数据库会话中的所有事务
    db.commit()
    # 刷新数据库中的用户对象，同步最新的信息
    db.refresh(db_user)
    # 返回新创建的用户对象
    return db_user

# 获取帖子列表
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    # 查询数据库中的帖子，可以指定跳过(skip)和数量限制(limit)
    return db.query(models.Post).offset(skip).limit(limit).all()

# 创建新帖子
def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    # 创建一个新帖子对象，数据来源于用户提交的数据，同时附加了发帖用户的ID
    db_post = models.Post(**post.dict(), owner_id=user_id)
    # 将新帖子添加到数据库会话中
    db.add(db_post)
    # 提交数据库会话中的所有事务
    db.commit()
    # 刷新数据库中的帖子对象，同步最新的信息
    db.refresh(db_post)
    # 返回新创建的帖子对象
    return db_post

# 帖子相关操作

# 根据帖子ID获取帖子
def get_post(db: Session, post_id: int):
    # 在数据库中查询ID对应的帖子，返回第一个匹配的结果
    return db.query(models.Post).filter(models.Post.id == post_id).first()

# 更新帖子
def update_post(db: Session, post: schemas.PostCreate, post_id: int):
    # 在数据库中查询ID对应的帖子，返回第一个匹配的结果
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        # 如果找到对应的帖子，则更新其标题和内容
        db_post.title = post.title
        db_post.content = post.content
        # 提交数据库会话中的所有事务
        db.commit()
        # 刷新数据库中的帖子对象，同步最新的信息
        db.refresh(db_post)
    # 返回更新后的帖子对象
    return db_post

# 删除帖子
def delete_post(db: Session, post_id: int):
    # 在数据库中查询ID对应的帖子，返回第一个匹配的结果
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        # 如果找到对应的帖子，则从数据库会话中删除该帖子
        db.delete(db_post)
        # 提交数据库会话中的所有事务
        db.commit()
    # 返回被删除的帖子对象
    return db_post

# 回答相关操作

# 根据回答ID获取回答
def get_answer(db: Session, answer_id: int):
    # 在数据库中查询ID对应的回答，返回第一个匹配的结果
    return db.query(models.Answer).filter(models.Answer.id == answer_id).first()

# 创建新回答
def create_answer(db: Session, answer: schemas.AnswerCreate, user_id: int, post_id: int):
    # 创建一个新回答对象，其数据来源于用户提交的数据，同时附加了作者的用户ID和对应的帖子ID
    db_answer = models.Answer(**answer.dict(), author_id=user_id, post_id=post_id)
    # 将新回答添加到数据库会话中
    db.add(db_answer)
    # 提交数据库会话中的所有事务
    db.commit()
    # 刷新数据库中的回答对象，同步最新的信息
    db.refresh(db_answer)
    # 返回新创建的回答对象
    return db_answer

# 获取某个帖子下的所有回答
def get_answers_for_post(db: Session, post_id: int):
    # 在数据库中查询帖子ID对应的所有回答
    return db.query(models.Answer).filter(models.Answer.post_id == post_id).all()

# 更新回答
def update_answer(db: Session, answer: schemas.AnswerCreate, answer_id: int):
    # 在数据库中查询ID对应的回答，返回第一个匹配的结果
    db_answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if db_answer:
        # 如果找到对应的回答，则更新其内容
        db_answer.content = answer.content
        # 提交数据库会话中的所有事务
        db.commit()
        # 刷新数据库中的回答对象，同步最新的信息
        db.refresh(db_answer)
    # 返回更新后的回答对象
    return db_answer

# 删除回答
def delete_answer(db: Session, answer_id: int):
    # 在数据库中查询ID对应的回答，返回第一个匹配的结果
    db_answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if db_answer:
        # 如果找到对应的回答，则从数据库会话中删除该回答
        db.delete(db_answer)
        # 提交数据库会话中的所有事务
        db.commit()
    # 返回被删除的回答对象
    return db_answer

