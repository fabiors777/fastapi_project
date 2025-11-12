from fastapi import Depends, HTTPException
from src.models import db
from sqlalchemy.orm import sessionmaker, Session
from src.security import ALGORITHM, SECRET_KEY, oayth2_schema
from src.models import User
from jose import jwt, JWTError

SessionLocal = sessionmaker(bind=db, autocommit=False, autoflush=False)


def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def token_check(token: str = Depends(oayth2_schema), session: Session = Depends(get_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Access denied. Check token validate.")
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Access.")
    return user
