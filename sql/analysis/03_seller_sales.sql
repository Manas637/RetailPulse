-- ============================================================================
-- RetailPulse
-- Analysis: Seller Performance
-- Grain: One row per seller
-- Sources: stg_order_items + dim_sellers
-- ============================================================================

DROP VIEW IF EXISTS seller_sales;

CREATE VIEW seller_sales AS
SELECT
    ds.seller_id,
    ds.seller_city,
    ds.seller_state,

    COUNT(*) AS item_count,

    COUNT(DISTINCT oi.order_id) AS order_count,

    COUNT(DISTINCT oi.product_id) AS product_count,

    ROUND(SUM(oi.price), 2) AS merchandise_revenue,

    ROUND(SUM(oi.freight_value), 2) AS freight_value,

    ROUND(SUM(oi.item_total_value), 2) AS total_item_value,

    ROUND(AVG(oi.price), 2) AS average_item_price

FROM stg_order_items oi

LEFT JOIN dim_sellers ds
    ON oi.seller_id = ds.seller_id

GROUP BY
    ds.seller_id,
    ds.seller_city,
    ds.seller_state;