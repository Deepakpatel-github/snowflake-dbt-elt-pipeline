{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

with orders_cte as (
    select
        order_id,
        customer_id,
        product_name,
        quantity,
        total_price,
        order_status,
        order_date,
        created_at
    from {{ source('ecom_landing', 'orders') }}
    {% if is_incremental() %}
    where created_at > (select MAX(created_at) from {{ this }})
    {% endif %}
    )



select *
from orders_cte

