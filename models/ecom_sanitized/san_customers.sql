{{
    config(
        materialized='incremental',
        unique_key='customer_id'
    )
}}

with customer_cte as (
    select
        customer_id,
        customer_name,
        email,
        phone,
        address,
        registration_date,
        created_at
    from {{ ref('stg_customers') }}
    {% if is_incremental() %}
    where created_at > (select MAX(created_at) from {{ this }})
    {% endif %}
    )

select *
from customer_cte
WHERE NOT REGEXP_LIKE(email, '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
