from fastapi import FastAPI

app = FastAPI()

from src.auth_routes import auth_router
from src.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)



#uvicorn main:app --reload
