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
    from {{ source('ecom_landing', 'customers') }}
    {% if is_incremental() %}
    where created_at > (select MAX(created_at) from {{ this }})
    {% endif %}
    )

select *
from customer_cte
