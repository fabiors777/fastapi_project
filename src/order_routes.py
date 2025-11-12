from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.dependencies import get_session
from src.schemas import OrderSchema
from src.models import Order


order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.get("/")
async def orders():
    return {"message": "You are on the order page."}


@order_router.post("/order")
async def order_create(orderschema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user_id=orderschema.user_id)
    session.add(new_order)
    session.commit()
    return {"message": f"Order number{new_order.id} successfully registered."}
