from marketplace.User.model import User
from marketplace.Order.model import Order
from marketplace.Product.model import Product
from marketplace.Payment.model import Payment
from marketplace.Cart.model import Cart
from marketplace.Product_Cart.model import ProductCart
from marketplace.Product_Order.model import ProductOrder
from marketplace.Errors.dto_error import Error


class ObjectsMother:
    def __init__(self):
        self.user = User()
        self.product = Product()
        self.cart = Cart()
        self.payment = Payment()
        self.order = Order()
        self.product_order = ProductCart()
        self.product_cart = ProductOrder()
        self.error = Error()

    def get_user(self):
        return self.cart

    def get_product(self):
        return self.product

    def get_order(self):
        return self.order

    def get_payment(self):
        return self.payment

    def get_cart(self):
        return self.cart

    def get_product_order(self):
        return self.product_order

    def get_product_cart(self):
        return self.product_cart

    def get_error(self):
        return self.error
