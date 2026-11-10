from datetime import date, timedelta
import psycopg2

def load_yesterday_orders():

    conn = psycopg2.connect(
        host="postgres",
        dbname="analytics",
        user="postgres",
        password="postgres"
    )

    cur = conn.cursor()

    yesterday = date.today() - timedelta(days=1)

    cur.execute(
        """
        INSERT INTO staging_orders (
            order_id,
            customer_id,
            amount,
            order_date
        )
        SELECT
            order_id,
            customer_id,
            amount,
            order_date
        FROM orders
        WHERE order_date = %s

        ON CONFLICT (order_id)
        DO UPDATE
        SET
            customer_id = EXCLUDED.customer_id,
            amount = EXCLUDED.amount,
            order_date = EXCLUDED.order_date;
        """,
        (yesterday,)
    )

    conn.commit()

    cur.close()
    conn.close()