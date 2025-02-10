from __future__ import annotations

import requests


def menu() -> int:
    print("""
\nMenu:
0) Shut down the work;
1) Working with the user(s);
2) Working with the product(s);
3) Working with payment(s);
4) Working with the order(s);
5) Working with the shopping cart(s);
6) Working with the communication(s) of the product-basket;
7) Work with the product-order communication(s).
          """)
    action = input("Select an action: ")
    return int(action) if action.isdigit() else 0


def user_menu() -> int:
    print("""
\nPossible actions:
1) Log in;
2) Register;
3) Delete the user;
4) Change user data;
5) Get the user by id;
6) Get the user by email;
7) Get all users.
    """)
    action = input("Select an action: ")
    return int(action) if action.isdigit() else 0


def product_menu() -> int:
    print("""
\nPossible actions:
1) Create a product;
2) Delete the product;
3) Change the product information;
4) Get the product by id;
5) Get the product by title;
6) Get all the products.
    """)
    action = input("Select an action: ")
    return int(action) if action.isdigit() else 0


def payment_menu() -> int:
    print("""
\nPossible actions:
1) Create a payment;
2) Delete the payment;
3) Change the payment details;
4) Receive payment by id;
5) Receive all payments.
    """)
    action = input("Select an action: ")
    return int(action) if action.isdigit() else 0


def order_menu() -> int:
    print("""
\nPossible actions:
1) Change the order details;
2) Receive an order by id;
3) Receive all orders.
    """)
    action = input("Select an action: ")
    return int(action) if action.isdigit() else 0


def cart_menu() -> int:
    print("""
\nPossible actions:
1) Change the data about the shopping cart;
2) Get a shopping cart by id;
3) Get all the baskets.
    """)
    action = input("Select an action: ")
    return int(action) if action.isdigit() else 0


def product_cart_menu() -> int:
    print("""
\nPossible actions:
1) Add an item to the cart;
2) Remove an item from the shopping cart;
3) Change the information about the product in the shopping cart;
4) Get all the items in the cart.
    """)
    action = input("Select an action: ")
    return int(action) if action.isdigit() else 0


def product_order_menu() -> int:
    print("""
\nPossible actions:
1) Add the product to the order;
2) Remove the product from the order;
3) Change the product information in the order;
4) Get all the items in the order.
    """)
    action = input("Select an action: ")
    return int(action) if action.isdigit() else 0


action = menu()
user_id = 0
role = ""
url = "http://localhost:5000"

while action:
    if action == 1:
        action = user_menu()
        if action == 1:
            data = {"email": input("Enter email: "), "password": input("Enter password: ")}
            response = requests.post(url+"/login", json=data)
            user_id = response.json().get("user_id")
            role = response.json().get("role")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 2:
            data = {"fio": input("Enter your FULL NAME: "), "email": input("Enter email: "),
                    "password": input("Enter password: "), "money": input("Enter the amount to deposit on the site: "),
                    "address": input("Enter the address: "), "phone": input("Enter the phone number: "),
                    "role": input("Enter the role: ")}
            response = requests.post(url + "/register", json=data)
            user_id = response.json().get("user_id")
            role = response.json().get("role")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 3 and role == "admin":
            response = requests.delete(url + f"/delete_user/{input('Enter the user ID: ')}")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 4:
            data = {"fio": input("Enter your FULL NAME: "), "email": input("Enter email: "),
                    "password": input("Enter password: "),
                    "money": input("Enter the amount to deposit on the site: "),
                    "address": input("Enter the address: "), "phone": input("Enter the phone number: ")}
            response = requests.patch(url + f"/update_user/{input('Enter the user ID: ')}", json=data)
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 5 and role == "admin":
            response = requests.get(url + f"/get_user_by_id/{input('Enter the user ID: ')}")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 6 and role == "admin":
            response = requests.get(url + f"/get_user_by_email/{input('Enter the user email: ')}")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 7 and role == "admin":
            response = requests.get(url + "/get_all_users")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        else:
            print("Not enough rights!")
    elif action == 2:
        action = product_menu()
        if action == 1 and role == "admin":
            data = {"title": input("Enter title: "), "price": input("Enter price: "), "rate": input("Enter rate: ")}
            response = requests.post(url+"/create_product", json=data)
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 2 and role == "admin":
            response = requests.delete(url + f"/delete_product/{input('Enter the product ID: ')}")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 3 and role == "admin":
            data = {"title": input("Enter title: "), "price": input("Enter price: "), "rate": input("Enter rate: ")}
            response = requests.patch(url + f"/update_product/{input('Enter the product id: ')}", json=data)
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 4 and role == "admin":
            response = requests.get(url + f"/get_product_by_id/{input('Enter the product ID: ')}")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 5 and role == "admin":
            response = requests.get(url + f"/get_product_by_title/{input('Enter the product title: ')}")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 6 and role == "admin":
            response = requests.get(url + "/get_all_products")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        else:
            print("Not enough rights!")
    elif action == 3:
        action = payment_menu()
        if action == 1:
            data = {"all_price": input("Enter all_price: "), "state": input("Enter state: ")}
            response= requests.post(url+f"/create_payment/{user_id}", json=data)
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 2 and role == "admin":
            response = requests.delete(url + f"/delete_payment/{input('Enter the payment id: ')}")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 3 and role == "admin":
            data = {"all_price": input("Enter all_price: "), "state": input("Enter state: ")}
            response = requests.patch(url + f"/update_payment/{input('Enter the payment id: ')}", json=data)
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 4 and role == "admin":
            response = requests.get(url + f"/get_payment_by_id/{input('Enter the payment id: ')}")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 5 and role == "admin":
            response = requests.get(url + "/get_all_payments")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        else:
            print("Not enough rights!")
    elif action == 4:
        action = order_menu()
        if action == 1:
            data = {"all_price": input("Enter all_price: "), "address": input("Enter address: ")}
            response = requests.patch(url + f"/update_order/{input('Enter the order id: ')}", json=data)
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 2 and role == "admin":
            response = requests.get(url + f"/get_order_by_id/{input('Enter the order ID: ')}")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 3 and role == "admin":
            response = requests.get(url + "/get_all_orders")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        else:
            print("Not enough rights!")
    elif action == 5:
        action = cart_menu()
        if action == 1:
            data = {"all_price": input("Enter all_price: ")}
            response = requests.patch(url + f"/update_cart/{input('Enter the bucket id: ')}", json=data)
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 2 and role == "admin":
            response = requests.get(url + f"/get_cart_by_id/{input('Enter the bucket id: ')}")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 3 and role == "admin":
            response = requests.get(url + "/get_all_carts")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        else:
            print("Not enough rights!")
    elif action == 6:
        action = product_cart_menu()
        if action == 1:
            data = {"product_id": input("Enter product_id: "), "quantity": input("Enter quantity: ")}
            response = requests.post(url + f"/create_product_cart/{user_id}", json=data)
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 2:
            response = requests.delete(url + f"/delete_product_cart/{input('Enter the bucket id: ')}",
                                       json={"product_id": input("Enter product_id: ")})
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 3 and role == "admin":
            data = {"product_id": input("Enter product_id: "), "quantity": input("Enter quantity: ")}
            response = requests.patch(url + f"/update_product_cart/{input('Enter the bucket id: ')}", json=data)
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 4 and role == "admin":
            response = requests.get(url + f"/get_products_cart_by_id/{input('Enter the bucket id: ')}")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        else:
            print("Not enough rights!")
    elif action == 7:
        action = product_order_menu()
        if action == 1:
            data = {"product_id": input("Enter product_id: "), "quantity": input("Enter quantity: ")}
            response = requests.post(url + f"/create_product_order/{user_id}", json=data)
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 2:
            response = requests.delete(url + f"/delete_product_order/{input('Enter the order ID: ')}",
                                       json={"product_id": input("Enter product_id: ")})
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 3 and role == "admin":
            data = {"product_id": input("Enter product_id: "), "quantity": input("Enter quantity: ")}
            response = requests.patch(url + f"/update_product_order/{input('Enter the order id: ')}", json=data)
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        elif action == 4 and role == "admin":
            response = requests.get(url + f"/get_product_order_by_id/{input('Enter the order ID: ')}")
            print(f"Information: {response.json()}\nStatus code: {response.status_code}")
        else:
            print("Not enough rights!")
    else:
        print("Incorrect input!")
    action = menu()
