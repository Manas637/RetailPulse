-- ============================================================================
-- RetailPulse
-- Transformation: Customer Dimension
-- Grain: One row per customer_id
-- Source: customers
-- ============================================================================

DROP VIEW IF EXISTS dim_customers;

CREATE VIEW dim_customers AS
SELECT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
FROM customers;