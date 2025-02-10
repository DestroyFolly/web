import psycopg2


def main():
    conn = psycopg2.connect(
        dbname="Bd",
        user="postgres",
        password="314151",
        host="127.0.0.1",
        port="5432"
    )

    cur = conn.cursor()
    try:
        id = 14
        res_sum = 0
        cur.execute(f"CALL relocate_items_from_cart_to_order({id})")  # Передаем user_id для тестирования
        cur.execute(f"SELECT all_price FROM carts WHERE cart_id = {id}")
        res_sum += cur.fetchone()[0]
        cur.execute(f"SELECT all_price FROM orders WHERE order_id = {id}")
        res_sum += cur.fetchone()[0]
        cur.execute(f"SELECT all_price FROM orders WHERE order_id = {id}")
        if res_sum == cur.fetchone()[0]:
            print("The test is passed")
        else:
            print("The test was not passed")
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        print("Error executing procedure:", e)

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
