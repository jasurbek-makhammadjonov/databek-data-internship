CREATE TABLE staging_orders (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT,
    amount NUMERIC(10,2),
    order_date DATE,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);