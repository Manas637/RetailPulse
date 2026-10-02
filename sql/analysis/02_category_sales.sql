-- ============================================================================
-- RetailPulse
-- Analysis: Product Category Sales
-- Grain: One row per English product category
-- Sources: fact_orders + stg_order_items + dim_products
-- ============================================================================

DROP VIEW IF EXISTS category_sales;

CREATE VIEW category_sales AS
SELECT
    dp.category_name_english,

    COUNT(*) AS item_count,

    COUNT(DISTINCT oi.order_id) AS order_count,

    COUNT(DISTINCT oi.product_id) AS product_count,

    ROUND(SUM(oi.price), 2) AS merchandise_revenue,

    ROUND(SUM(oi.freight_value), 2) AS freight_value,

    ROUND(SUM(oi.item_total_value), 2) AS total_item_value,

    ROUND(AVG(oi.price), 2) AS average_item_price

FROM stg_order_items oi

LEFT JOIN dim_products dp
    ON oi.product_id = dp.product_id

GROUP BY dp.category_name_english;