from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.dependencies import get_session, token_check
from src.schemas import OrderSchema, OrderItemSchema, ResponseOrderSchema
from src.models import Order, User, OrderItem
from typing import List


order_router = APIRouter(
    prefix="/orders", tags=["orders"], dependencies=[Depends(token_check)])


@order_router.get("/")
async def orders():
    return {"message": "You are on the order page."}


@order_router.post("/order")
async def order_create(orderschema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user_id=orderschema.user_id)
    session.add(new_order)
    session.commit()
    return {"message": f"Order number{new_order.id} successfully registered."}


@order_router.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(token_check)):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    # Role: user.admin = True and user.id = order.user
    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=400, detail="You don't have permission to make this modification.")
    order.status = "CANCELED"
    session.commit()
    return {
        "message": f"Order number {order.id} canceled successfully",
        "order": order
    }


@order_router.get("/list")
async def order_list(session: Session = Depends(get_session), user: User = Depends(token_check)):
    if not user.admin:
        raise HTTPException(
            status_code=401, detail="You don't have permission to make this request.")
    else:
        order = session.query(Order).all()
        return {
            "order": order
        }


@order_router.post("/order/add_item/{order_id}")
async def add_item(order_id: int,
                   order_item_schema: OrderItemSchema,
                   session: Session = Depends(get_session),
                   user: User = Depends(token_check)):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order does not exist.")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=401, detail="You don't have permission to make this operation")
    order_item = OrderItem(order_item_schema.quantity, order_item_schema.flavor,
                           order_item_schema.size, order_item_schema.unit_price, order_id)
    session.add(order_item)
    order.price_calculate()
    session.commit()
    return {
        "message": "Order created successfully",
        "item_id": order.id,
        "order_price": order.price
    }


@order_router.post("/order/remove_item/{order_item_id}")
async def remove_item(order_item_id: int,
                      session: Session = Depends(get_session),
                      user: User = Depends(token_check)):
    order_item = session.query(OrderItem).filter(
        OrderItem.id == order_item_id).first()
    order_number = session.query(Order).filter(
        Order.id == order_item.order_number).first()
    if not order_item:
        raise HTTPException(
            status_code=400, detail="Order item does not exist.")
    if not user.admin and user.id != order_number.user_id:
        raise HTTPException(
            status_code=401, detail="You don't have permission to make this operation")

    session.delete(order_item)
    order_number.price_calculate()
    session.commit()
    return {
        "message": "Item removed successfully",
        "quantity_itens": len(order_number.itens),
        "order": order_number
    }


@order_router.post("/order/finish/{order_id}")
async def finish_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(token_check)):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    # Role: user.admin = True and user.id = order.user
    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=400, detail="You don't have permission to make this modification.")
    order.status = "FINISHED"
    session.commit()
    return {
        "message": f"Order number {order.id} finished successfully",
        "order": order
    }


@order_router.get("/order/{order_id}")
async def show_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(token_check)):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    # Role: user.admin = True and user.id = order.user
    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=400, detail="You don't have permission to make this modification.")
    return {
        "quantity_itens": len(order.itens),
        "order": order
    }


@order_router.get("/list/user", response_model=List[ResponseOrderSchema])
async def order_list(session: Session = Depends(get_session), user: User = Depends(token_check)):
    orders = session.query(Order).filter(Order.user_id == user.id).all()
    return orders
