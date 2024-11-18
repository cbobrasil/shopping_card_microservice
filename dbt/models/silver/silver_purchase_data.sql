{{ config(
    materialized='incremental',
    unique_key='buyer_id'
) }}

WITH cleaned_data AS (
    SELECT
        buyer_id,
        product_id,
        number_of_installments,
        CAST(total_amount AS FLOAT) AS total_amount,
        TO_DATE(purchase_date, 'YYYY-MM-DD') AS purchase_date,
        ingestion_time
    FROM {{ ref('bronze_purchase_data') }}
    WHERE buyer_id IS NOT NULL
      AND product_id IS NOT NULL
      AND total_amount > 0
)

SELECT *
FROM cleaned_data
