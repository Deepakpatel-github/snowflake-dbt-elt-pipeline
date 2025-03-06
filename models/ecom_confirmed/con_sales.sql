{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

WITH orders AS (
    SELECT * FROM {{ ref('san_orders') }}
),
customers AS (
    SELECT * FROM {{ ref('san_customers') }}
)

SELECT
    o.order_id,
    o.customer_id,
    c.customer_name,
    c.email,
    c.phone,
    c.address,
    o.product_name,
    o.quantity,
    o.total_price,
    o.order_status,
    o.order_date,
    c.registration_date,
    o.created_at
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id

{% if is_incremental() %}
WHERE o.created_at > (SELECT MAX(created_at) FROM {{ this }})
{% endif %}+