CREATE OR REPLACE PROCEDURE relocate_items_from_cart_to_order(
    p_user_id INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_cart_id INTEGER;
	v_order_id INTEGER;
    v_all_price FLOAT;
    v_product RECORD;
BEGIN
    SELECT cart_id, all_price INTO v_cart_id, v_all_price
    FROM carts
    WHERE user_id = p_user_id;

    IF v_cart_id IS NULL THEN
        RAISE EXCEPTION 'No cart found for user';
    END IF;
	

    SELECT order_id INTO v_order_id
    FROM orders
    WHERE user_id = p_user_id;

    IF v_order_id IS NULL THEN
        RAISE EXCEPTION 'No order found for user';
    END IF;


    FOR v_product IN
        SELECT product_id, quantity
        FROM products_carts
        WHERE cart_id = v_cart_id
    LOOP
        INSERT INTO products_orders (product_id, order_id, quantity)
        VALUES (v_product.product_id, v_order_id, v_product.quantity);
    END LOOP;


	DELETE FROM products_carts WHERE cart_id = v_cart_id;
	
    UPDATE orders SET all_price = all_price + v_all_price WHERE order_id = v_order_id;
    
	UPDATE carts SET all_price = 0 WHERE cart_id = v_cart_id;
	
	COMMIT;
	
    RAISE EXCEPTION 'Order placed successfully, Order ID: %', v_order_id;
END;
$$;

drop procedure create_order_from_cart;
CALL create_order_from_cart(7);