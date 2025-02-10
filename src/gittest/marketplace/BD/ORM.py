from __future__ import annotations

from typing import Any

from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

from marketplace.Cart.model import Cart
from marketplace.Order.model import Order
from marketplace.Payment.model import Payment
from marketplace.Product.model import Product
from marketplace.Product_Cart.model import ProductCart
from marketplace.Product_Order.model import ProductOrder
from marketplace.User.model import User


Base: Any = declarative_base()


class UserDB(Base):
    def __init__(self, user: User):
        self.user_id = user.user_id
        self.fio = user.fio
        self.email = user.email
        self.password = user.password
        self.money = user.money
        self.address = user.address
        self.phone = user.phone
        self.role = user.role

    def update(self, new_data: User) -> None:
        self.fio = new_data.fio if new_data.fio else self.fio
        self.email = new_data.email if new_data.email else self.email
        self.password = new_data.password if new_data.password else self.password
        self.money = new_data.money if new_data.money else self.money
        self.address = new_data.address if new_data.address else self.address
        self.phone = new_data.phone if new_data.phone else self.phone
        self.role = new_data.role if new_data.role else self.role

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    fio = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    money = Column(Float, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    role = Column(String(10), CheckConstraint("role IN ('admin', 'seller', 'user')"), nullable=False)

    def __eq__(self, other: Any) -> bool:
        return self.user_id == other.user_id

    def __repr__(self) -> str:
        return f"User_id={self.user_id}; email={self.email}; Password={self.password}; Role={self.role}."


class OrderDB(Base):
    def __init__(self, order: Order):
        self.order_id = order.order_id
        self.all_price = order.all_price
        self.address = order.address
        self.user_id = order.user_id

    def update(self, new_data: Order) -> None:
        self.all_price = new_data.all_price if new_data.all_price else self.all_price
        self.address = new_data.address if new_data.address else self.address

    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    all_price = Column(Float, nullable=False)
    address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))

    def __eq__(self, other: Any) -> bool:
        return self.order_id == other.order_id

    def __repr__(self) -> str:
        return f"Order_d={self.order_id}; All_price={self.all_price}; User_id={self.user_id}."


class ProductDB(Base):
    def __init__(self, product: Product):
        self.product_id = product.product_id
        self.seller_id = product.seller_id
        self.title = product.title
        self.price = product.price
        self.rate = product.rate

    def update(self, new_data: Product) -> None:
        self.title = new_data.title if new_data.title else self.title
        self.price = new_data.price if new_data.price else self.price
        self.rate = new_data.rate if new_data.rate else self.rate

    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    rate = Column(Float, CheckConstraint("rate > 0"), nullable=False)

    def __eq__(self, other: Any) -> bool:
        return self.product_id == other.product_id

    def __repr__(self) -> str:
        return f"Order_d={self.product_id}; Price={self.price}; Rate={self.rate}."


class PaymentDB(Base):
    def __init__(self, payment: Payment):
        self.payment_id = payment.payment_id
        self.all_price = payment.all_price
        self.state = payment.state
        self.user_id = payment.user_id

    def update(self, new_data: Payment) -> None:
        self.all_price = new_data.all_price if new_data.all_price else self.all_price
        self.state = new_data.state if new_data.state else self.state

    __tablename__ = 'payments'

    payment_id = Column(Integer, primary_key=True)
    all_price = Column(Float, nullable=False)
    state = Column(String(10), CheckConstraint("state IN ('passed', 'not_passed')"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))

    def __eq__(self, other: Any) -> bool:
        return self.payment_id == other.payment_id

    def __repr__(self) -> str:
        return f"Payment_id={self.payment_id}; All_price={self.all_price}; " \
               f"State={self.state}; User_id={self.user_id}."


class CartDB(Base):
    def __init__(self, cart: Cart):
        self.cart_id = cart.cart_id
        self.all_price = cart.all_price
        self.user_id = cart.user_id

    def update(self, new_data: Cart) -> None:
        self.all_price = new_data.all_price if new_data.all_price else self.all_price

    __tablename__ = 'carts'

    cart_id = Column(Integer, primary_key=True)
    all_price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))

    def __eq__(self, other: Any) -> bool:
        return self.cart_id == other.cart_id

    def __repr__(self) -> str:
        return f"Cart_id={self.cart_id}; All_price={self.all_price}; User_id={self.user_id}."


class ProductCartDB(Base):
    def __init__(self, product_cart: ProductCart):
        self.product_id = product_cart.product_id
        self.quantity = product_cart.quantity
        self.cart_id = product_cart.cart_id

    def update(self, new_data: ProductCart) -> None:
        self.quantity = new_data.quantity if new_data.quantity else self.quantity

    __tablename__ = 'products_carts'

    product_id = Column(Integer, ForeignKey('products.product_id', ondelete='CASCADE'), primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.cart_id', ondelete='CASCADE'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    def __eq__(self, other: Any) -> bool:
        return self.product_id == other.product_id and self.cart_id == other.cart_id

    def __repr__(self) -> str:
        return f"Product_id={self.product_id}; Quantuty={self.quantity}; Cart_id={self.cart_id}."


class ProductOrderDB(Base):
    def __init__(self, product_order: ProductOrder):
        self.product_id = product_order.product_id
        self.quantity = product_order.quantity
        self.order_id = product_order.order_id

    def update(self, new_data: ProductOrder) -> None:
        self.quantity = new_data.quantity if new_data.quantity else self.quantity

    __tablename__ = 'products_orders'

    product_id = Column(Integer, ForeignKey('products.product_id', ondelete='CASCADE'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id', ondelete='CASCADE'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    def __eq__(self, other: Any) -> bool:
        return self.product_id == other.product_id and self.order_id == other.order_id

    def __repr__(self) -> str:
        return f"Product_id={self.product_id}; Quantuty={self.quantity}; Order_id={self.order_id}."
