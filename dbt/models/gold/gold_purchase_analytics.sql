{{ config(
    materialized='table'
) }}

WITH aggregated_data AS (
    SELECT
        buyer_id,
        COUNT(product_id) AS total_purchases,
        SUM(total_amount) AS total_spent,
        MAX(purchase_date) AS last_purchase_date
    FROM {{ ref('silver_purchase_data') }}
    GROUP BY buyer_id
)

SELECT *
FROM aggregated_data
