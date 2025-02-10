CREATE DATABASE test;

CREATE TABLE IF NOT EXISTS users
(
	user_id SERIAL,
	fio TEXT,
	email TEXT,
	password TEXT, 
	money FLOAT,
	address TEXT,
	phone TEXT,
	role VARCHAR(10)
);


CREATE TABLE IF NOT EXISTS orders
(
	order_id SERIAL,
	all_price FLOAT,
	address TEXT,
	user_id INTEGER
);


CREATE TABLE IF NOT EXISTS products
(
	product_id SERIAL,
	seller_id INTEGER,
	title VARCHAR(30),
	price FLOAT,
	rate FLOAT
);


CREATE TABLE IF NOT EXISTS payments
(
	payment_id SERIAL,
	all_price FLOAT,
	state VARCHAR(10),
	user_id INTEGER
);


CREATE TABLE IF NOT EXISTS carts
(
	cart_id SERIAL,
	all_price FLOAT,
	user_id INTEGER
);


CREATE TABLE IF NOT EXISTS products_carts
(
	product_id INTEGER,
	cart_id INTEGER,
	quantity INTEGER
);


CREATE TABLE IF NOT EXISTS products_orders
(
	product_id INTEGER,
	order_id INTEGER,
	quantity INTEGER
);