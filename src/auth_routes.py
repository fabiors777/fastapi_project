from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.models import User
from src.dependencies import get_session, token_check
from src.security import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from src.schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


auth_router = APIRouter(prefix="/auth", tags=["auth"])


def token_create(user_id, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expire_date = datetime.now(timezone.utc) + token_duration
    dic_info = {"sub": str(user_id), "exp": expire_date}
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def user_authentication(email, password, session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user


@auth_router.get("/")
async def home():
    return {"message": "You are on the authentication page."}


@auth_router.post("/create_account")
async def create_account(user_schema: UserSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == user_schema.email).first()
    if user:
        raise HTTPException(
            status_code=400, detail="A user with that email address already exists.")

    hashed = bcrypt_context.hash(user_schema.password)
    new_user = User(name=user_schema.name, email=user_schema.email, password=hashed,
                    active=user_schema.active, admin=user_schema.admin)
    session.add(new_user)
    session.commit()
    return {"message": f"User {user_schema.email} successfully registered."}


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = user_authentication(
        login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(
            status_code=400, detail="User not found or invalid credentials")
    else:
        access_token = token_create(user.id)
        refresh_token = token_create(user.id, token_duration=timedelta(days=7))
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"
                }


@auth_router.post("/login-form")
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = user_authentication(
        form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=400, detail="User not found or invalid credentials")
    else:
        access_token = token_create(user.id)
        return {"access_token": access_token,
                "token_type": "Bearer"
                }


@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(token_check)):
    access_token = token_create(user.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
