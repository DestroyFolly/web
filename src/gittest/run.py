from __future__ import annotations

from flask import Blueprint
from flask import Flask


from marketplace.Cart.handler import cart_page
from marketplace.Order.handler import order_page
from marketplace.Payment.handler import payment_page
from marketplace.Product.handler import product_page
from marketplace.Product_Cart.handler import product_cart_page
from marketplace.Product_Order.handler import product_order_page
from marketplace.User.handler import user_page


class App:
    def __init__(self, pages: list[Blueprint]) -> None:
        self.pages = pages

    def run_app(self) -> None:
        app = Flask(__name__)
        for page in self.pages:
            app.register_blueprint(page)
        app.run("127.0.0.1", 5001)


app = App([cart_page, order_page, payment_page, product_cart_page,
            product_order_page, product_page, user_page])
app.run_app()
