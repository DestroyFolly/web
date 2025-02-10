from __future__ import annotations

from dynaconf import Dynaconf
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# You would need to create modules resembling Blueprints as routers in FastAPI
from fastapi import APIRouter

from marketplace.User.handlerNew import user_page
from marketplace.Payment.handlerNew import payment_page
from marketplace.Cart.handlerNew import cart_page
from marketplace.Order.handlerNew import order_page
from marketplace.Product.handlerNew import product_page
from marketplace.Product_Cart.handlerNew import product_cart_page
from marketplace.Product_Order.handlerNew import product_order_page
from marketplace.Connections.my_jwt import jwt_page


class App:
    def __init__(self, config_name: str) -> None:
        self.settings = Dynaconf(settings_files=[config_name])
        self.app = FastAPI()

        origins = ["*"]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],

        )

    def include_routers(self, routers: list[APIRouter]) -> None:
        for router in routers:
            self.app.include_router(router)

    def run_app(self) -> None:
        import uvicorn
        uvicorn.run(
            self.app,
            host=self.settings.app.app_host,
            port=self.settings.app.app_port,
        )


routers = [
    user_page,
    payment_page,
    cart_page,
    order_page,
    product_page,
    product_cart_page,
    product_order_page,
    jwt_page
]



app_instance = App("pyproject.toml")
app_instance.include_routers(routers)
app_instance.run_app()


