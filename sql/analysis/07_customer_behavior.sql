-- ============================================================================
-- RetailPulse
-- Analysis: Customer Purchase Behavior
-- Grain: One row per customer
-- Sources: fact_orders + dim_customers
-- ============================================================================

DROP VIEW IF EXISTS customer_behavior;

CREATE VIEW customer_behavior AS
SELECT
    dc.customer_unique_id,

    -- Customer geography
    MIN(dc.customer_city) AS customer_city,
    MIN(dc.customer_state) AS customer_state,

    -- Purchase behavior
    COUNT(DISTINCT fo.order_id) AS order_count,

    MIN(fo.order_purchase_date) AS first_order_date,
    MAX(fo.order_purchase_date) AS last_order_date,

    -- Customer value
    ROUND(
        SUM(fo.item_total_value),
        2
    ) AS total_customer_value,

    ROUND(
        AVG(fo.item_total_value),
        2
    ) AS average_order_value,

    -- Items
    SUM(fo.item_count) AS total_items,

    ROUND(
        AVG(fo.item_count),
        2
    ) AS average_items_per_order

FROM fact_orders fo

INNER JOIN dim_customers dc
    ON fo.customer_id = dc.customer_id

GROUP BY dc.customer_unique_id;