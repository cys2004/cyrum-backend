# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud, security
from database import SessionLocal, engine
from security import create_access_token, get_current_user

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 初始化FastAPI应用
app = FastAPI()

# 获取数据库会话
def get_session_local():
    db = SessionLocal()
    try:
        yield db
    finally:
        # 关闭数据库会话
        db.close()

# 用户注册接口
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_session_local)):
    db_user = crud.get_user_by_email(db, email=user.email)
    # 检查邮箱是否已被注册
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = crud.create_user(db=db, user=user)
    # 创建新用户并返回用户信息
    return created_user

# 用户登录接口
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session_local)):
    # 用户身份验证
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 创建访问令牌
    access_token = create_access_token(data={"sub": user.email})
    # 返回访问令牌
    return {"access_token": access_token, "token_type": "bearer"}

# 当前登录用户信息获取接口
@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

# 用户创建帖子接口
@app.post("/posts/", response_model=schemas.Post)
def create_post_for_user(
    post: schemas.PostCreate, db: Session = Depends(get_session_local), current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_post(db=db, post=post, user_id=current_user.id)

# 获取帖子列表接口
@app.get("/posts/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_session_local)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

# 更新帖子信息接口
@app.patch("/posts/{post_id}", response_model=schemas.Post)
def update_post(
    post_id: int, post: schemas.PostCreate, db: Session = Depends(get_session_local), current_user: schemas.User = Depends(get_current_user)
):
    db_post = crud.get_post(db, post_id=post_id)
    if not db_post or db_post.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.update_post(db=db, post=post, post_id=post_id)

# 删除帖子接口
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_session_local), current_user: schemas.User = Depends(get_current_user)):
    db_post = crud.get_post(db, post_id=post_id)
    if not db_post or db_post.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Post not found")
    crud.delete_post(db, post_id=post_id)
    return {"ok": True}

# 创建回答接口
@app.post("/posts/{post_id}/answers/", response_model=schemas.Answer)
def create_answer_for_post(
    post_id: int, answer: schemas.AnswerCreate, db: Session = Depends(get_session_local), current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_answer(db=db, answer=answer, user_id=current_user.id, post_id=post_id)

# 获取回答接口
@app.get("/posts/{post_id}/answers/", response_model=List[schemas.Answer])
def read_answers_for_post(post_id: int, db: Session = Depends(get_session_local)):
    answers = crud.get_answers_for_post(db=db, post_id=post_id)
    return answers

# 更新回答接口
@app.patch("/answers/{answer_id}", response_model=schemas.Answer)
def update_answer(
    answer_id: int, answer: schemas.AnswerCreate, db: Session = Depends(get_session_local), current_user: schemas.User = Depends(get_current_user)
):
    db_answer = crud.get_answer(db, answer_id=answer_id)
    if not db_answer or db_answer.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Answer not found")
    return crud.update_answer(db=db, answer=answer, answer_id=answer_id)

# 删除回答接口
@app.delete("/answers/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(answer_id: int, db: Session = Depends(get_session_local), current_user: schemas.User = Depends(get_current_user)):
    db_answer = crud.get_answer(db, answer_id=answer_id)
    if not db_answer or db_answer.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Answer not found")
    crud.delete_answer(db, answer_id=answer_id)
    return {"ok": True}
