-- ============================================================================
-- RetailPulse
-- Analysis: Monthly Sales Performance
-- Grain: One row per purchase month
-- Source: fact_orders + dim_customers
-- ============================================================================

DROP VIEW IF EXISTS monthly_sales;

CREATE VIEW monthly_sales AS
SELECT
    fo.order_purchase_month AS sales_month,

    -- Order metrics
    COUNT(*) AS order_count,

    COUNT(DISTINCT dc.customer_unique_id) AS unique_customers,

    -- Revenue metrics
    ROUND(SUM(fo.merchandise_value), 2) AS merchandise_revenue,

    ROUND(SUM(fo.freight_value), 2) AS freight_revenue,

    ROUND(SUM(fo.item_total_value), 2) AS total_order_value,

    -- Average order value
    ROUND(
        SUM(fo.item_total_value)
        / NULLIF(COUNT(*), 0),
        2
    ) AS average_order_value,

    -- Average items per order
    ROUND(
        AVG(fo.item_count),
        2
    ) AS average_items_per_order

FROM fact_orders fo

LEFT JOIN dim_customers dc
    ON fo.customer_id = dc.customer_id

GROUP BY fo.order_purchase_month;