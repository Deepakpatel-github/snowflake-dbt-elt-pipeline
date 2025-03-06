-- tests/test_con_orders_customer_id.sql
SELECT *
FROM {{ ref('con_orders') }} o
WHERE o.customer_id IS NULL
