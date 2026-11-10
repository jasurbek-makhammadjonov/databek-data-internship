SELECT
    order_date,
    SUM(amount) AS daily_revenue
FROM {{ ref('stg_orders') }}
GROUP BY order_date