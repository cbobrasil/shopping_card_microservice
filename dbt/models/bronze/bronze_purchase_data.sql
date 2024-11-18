{{ config(
    materialized='incremental',
    unique_key='buyer_id'
) }}

WITH raw_data AS (
    SELECT
        buyer_id,
        product_id,
        number_of_installments,
        total_amount,
        purchase_date,
        current_timestamp() AS ingestion_time
    FROM {{ source('dynamo_streams', 'purchase_data') }}
)

SELECT *
FROM raw_data
