from src.order_routes import order_router
from src.auth_routes import auth_router
from fastapi import FastAPI
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)


# uvicorn main:app --reload
