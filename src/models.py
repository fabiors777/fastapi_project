from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ChoiceType  # <- pode importar assim
# from sqlalchemy_utils.types import ChoiceType  # também funciona

# Create database connection
db = create_engine("sqlite:///database/database.db", echo=False, future=True)

# Base
Base = declarative_base()


# Models
class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(255), nullable=False)
    email = Column("email", String(255))
    # corrige "passord" -> "password"
    password = Column("password", String(10))
    active = Column("active", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin


class Order(Base):
    __tablename__ = "orders"

    # ORDER_STATUS = (
    #     ("PENDING", "PENDING"),
    #     ("CANCELED", "CANCELED"),
    #     ("FINISHED", "FINISHED"),
    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    # status = Column(ChoiceType(choices=ORDER_STATUS)) >> da pau no sqlachemy
    status = Column("status", String(50))
    user_id = Column("user_id", Integer, ForeignKey("users.id"),
                     nullable=False)  # era "username"
    price = Column("price", Float, default=0)

    def __init__(self, user_id, status="PENDING", price=0):
        self.user_id = user_id
        self.status = status
        self.price = price


class OrderItem(Base):
    __tablename__ = "order_items"  # corrige "order_itens"

    # PIZZA_SIZES = (
    #     ("SMALL", "SMALL"),
    #     ("MEDIUM", "MEDIUM"),
    #     ("LARGE", "LARGE"),
    #     ("GIANT", "GIANT"),
    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer, nullable=False)
    flavor = Column("flavor", String(255), nullable=False)
    size = Column("size", String(10), nullable=False)
    unit_price = Column("unit_price", Float, nullable=False)
    order_number = Column("order_number", Integer,
                          ForeignKey("orders.id"), nullable=False)

    def __init__(self, quantity, flavor, size, unit_price, order_number):
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.unit_price = unit_price
        self.order_number = order_number
