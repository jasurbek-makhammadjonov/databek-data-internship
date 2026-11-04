
import random
import sqlite3
from datetime import date, timedelta

import pandas as pd

random.seed(42)

SCHEMA = """
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    email       TEXT,
    city        TEXT,
    created_at  TEXT
);
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    category   TEXT,
    price      REAL NOT NULL
);
CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date  TEXT NOT NULL,            
    status      TEXT NOT NULL             
);
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL REFERENCES orders(order_id),
    product_id    INTEGER NOT NULL REFERENCES products(product_id),
    quantity      INTEGER NOT NULL,
    unit_price    REAL NOT NULL
);
"""


FIRST = ["Ali", "Vali", "Jasur", "Dilnoza", "Madina", "Sardor", "Aziza", "Bekzod",
         "Nodira", "Otabek", "Malika", "Rustam", "Zarina", "Timur", "Shahlo"]
LAST = ["Karimov", "Aliyev", "Rahimov", "Tursunov", "Yusupov", "Ergashev", "Saidov"]
CITIES = ["Tashkent", "Samarkand", "Bukhara", "Fergana", "Namangan", "Andijan"]
CATEGORIES = {
    "Electronics": [("Headphones", 45), ("Smartwatch", 120), ("Power bank", 30)],
    "Books": [("SQL Handbook", 25), ("Python Basics", 20), ("Data Science 101", 35)],
    "Home": [("Desk lamp", 18), ("Mug set", 12), ("Backpack", 40)],
}


def fill_fake_data(con: sqlite3.Connection, n_customers=40, n_orders=400):
    cur = con.cursor()
    start = date(2025, 1, 1)
    end = date(2025, 6, 30)
    span = (end - start).days


    for cid in range(1, n_customers + 1):
        name = f"{random.choice(FIRST)} {random.choice(LAST)}"
        cur.execute(
            "INSERT INTO customers VALUES (?,?,?,?,?)",
            (cid, name, f"user{cid}@mail.uz", random.choice(CITIES),
             (start - timedelta(days=random.randint(1, 300))).isoformat()),
        )


    pid = 1
    prices = {}
    for cat, items in CATEGORIES.items():
        for pname, price in items:
            cur.execute("INSERT INTO products VALUES (?,?,?,?)", (pid, pname, cat, price))
            prices[pid] = price
            pid += 1

    active_customers = list(range(1, n_customers - 5))

    item_id = 1
    for oid in range(1, n_orders + 1):
        cid = random.choice(active_customers)
        d = start + timedelta(days=random.randint(0, span))
        status = random.choices(["completed", "shipped", "cancelled"], [70, 20, 10])[0]
        cur.execute("INSERT INTO orders VALUES (?,?,?,?)", (oid, cid, d.isoformat(), status))
        for _ in range(random.randint(1, 4)):
            p = random.choice(list(prices))
            cur.execute(
                "INSERT INTO order_items VALUES (?,?,?,?,?)",
                (item_id, oid, p, random.randint(1, 3), prices[p]),
            )
            item_id += 1
    con.commit()


Q1_REVENUE_PER_MONTH = """
SELECT strftime('%Y-%m', o.order_date)          AS month,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status <> 'cancelled'
GROUP BY month
ORDER BY month;
"""


Q2_TOP3_CUSTOMERS_PER_MONTH = """
WITH monthly AS (
    SELECT strftime('%Y-%m', o.order_date) AS month,
           c.customer_id,
           c.name,
           SUM(oi.quantity * oi.unit_price) AS revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    JOIN customers  c  ON c.customer_id = o.customer_id
    WHERE o.status <> 'cancelled'
    GROUP BY month, c.customer_id, c.name
),
ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY month
                              ORDER BY revenue DESC, customer_id) AS rn
    FROM monthly
)
SELECT month, rn AS rank, name, ROUND(revenue, 2) AS revenue
FROM ranked
WHERE rn <= 3
ORDER BY month, rn;
"""


Q3_ROLLING_7D_REVENUE = """
WITH RECURSIVE calendar(day) AS (
    SELECT MIN(order_date) FROM orders
    UNION ALL
    SELECT date(day, '+1 day') FROM calendar
    WHERE day < (SELECT MAX(order_date) FROM orders)
),
daily AS (
    SELECT cal.day,
           COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS revenue
    FROM calendar cal
    LEFT JOIN orders o
           ON o.order_date = cal.day AND o.status <> 'cancelled'
    LEFT JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY cal.day
)
SELECT day,
       ROUND(revenue, 2) AS daily_revenue,
       ROUND(SUM(revenue) OVER (ORDER BY day
                                ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS rolling_7d_revenue
FROM daily
ORDER BY day;
"""


Q4_CUSTOMERS_WITHOUT_ORDERS = """
SELECT c.customer_id, c.name, c.city
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL
ORDER BY c.customer_id;
"""

QUERIES = [
    ("1) Oylik daromad", Q1_REVENUE_PER_MONTH),
    ("2) Har oy top-3 mijoz", Q2_TOP3_CUSTOMERS_PER_MONTH),
    ("3) 7 kunlik rolling daromad (oxirgi 10 qator)", Q3_ROLLING_7D_REVENUE),
    ("4) Buyurtmasiz mijozlar", Q4_CUSTOMERS_WITHOUT_ORDERS),
]



def main():
    con = sqlite3.connect("shop.db")
    con.executescript(SCHEMA)
    fill_fake_data(con)

    pd.set_option("display.width", 120)
    for title, sql in QUERIES:
        df = pd.read_sql_query(sql, con)
        print(f"\n=== {title} ===")
        print(df.tail(10).to_string(index=False) if title.startswith("3") else df.to_string(index=False))
    con.close()
    print("\nBaza 'shop.db' faylida saqlandi.")


if __name__ == "__main__":
    main()