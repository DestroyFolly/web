ALTER TABLE users
	ALTER fio SET NOT NULL,
	ALTER email SET NOT NULL,
	ALTER password SET NOT NULL,
	ALTER money SET NOT NULL,
	ALTER phone SET NOT NULL,
	ALTER role SET NOT NULL,
	ADD CONSTRAINT check_email UNIQUE (email),
	ADD CONSTRAINT check_money CHECK (money >= 0),
	ADD CONSTRAINT check_role CHECK (role IN ('admin', 'seller', 'user')),
	ADD CONSTRAINT pk_user_id PRIMARY KEY (user_id);


ALTER TABLE orders
	ALTER all_price SET NOT NULL,
	ALTER address SET NOT NULL,
	ADD CONSTRAINT check_all_price CHECK (all_price >= 0),
	ADD CONSTRAINT pk_order_id PRIMARY KEY (order_id),
	ADD FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;


ALTER TABLE products
    ALTER title SET NOT NULL,
	ALTER seller_id SET NOT NULL,
	ALTER price SET NOT NULL,
	ALTER rate SET NOT NULL,
	ADD CONSTRAINT check_price CHECK (price >= 0),
	ADD CONSTRAINT check_rate CHECK (rate >= 0),
	ADD CONSTRAINT pk_product_id PRIMARY KEY (product_id),
	ADD FOREIGN KEY (seller_id) REFERENCES users(user_id) ON DELETE CASCADE;

	
ALTER TABLE payments
	ALTER all_price SET NOT NULL,
	ALTER state SET NOT NULL,
	ADD CONSTRAINT check_all_price CHECK (all_price >= 0),
	ADD CONSTRAINT check_state CHECK (state IN ('passed', 'not_passed')),
	ADD CONSTRAINT pk_payment_id PRIMARY KEY (payment_id),
	ADD FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;


ALTER TABLE carts
	ALTER all_price SET NOT NULL,
	ADD CONSTRAINT check_all_price CHECK (all_price >= 0),
	ADD CONSTRAINT pk_cart_id PRIMARY KEY (cart_id),
	ADD FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;
	

ALTER TABLE products_carts
	ALTER quantity SET NOT NULL,
	ADD CONSTRAINT check_quantity CHECK (quantity > 0),
	ADD FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
	ADD FOREIGN KEY (cart_id) REFERENCES carts(cart_id) ON DELETE CASCADE;
	
	
ALTER TABLE products_orders
	ALTER quantity SET NOT NULL,
	ADD CONSTRAINT check_quantity CHECK (quantity > 0),
	ADD FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
	ADD FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE;
