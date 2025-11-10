from fastapi import APIRouter, Depends, HTTPException
from src.models import User
from src.dependencies import get_session
from src.security import bcrypt_context
from src.schemas import UserSchema
from sqlalchemy.orm import Session


auth_router = APIRouter(prefix="/auth", tags=["auth"])


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
