-- ============================================================================
-- RetailPulse
-- Transformation: Order Item Summary
-- Grain: One row per order
-- Source: stg_order_items
-- ============================================================================

DROP VIEW IF EXISTS order_item_summary;

CREATE VIEW order_item_summary AS
SELECT
    order_id,

    -- Item metrics
    COUNT(*) AS item_count,
    COUNT(DISTINCT product_id) AS distinct_product_count,
    COUNT(DISTINCT seller_id) AS distinct_seller_count,

    -- Merchandise value
    ROUND(SUM(price), 2) AS merchandise_value,

    -- Freight
    ROUND(SUM(freight_value), 2) AS freight_value,

    -- Total item value including freight
    ROUND(SUM(item_total_value), 2) AS item_total_value,

    -- Average item price
    ROUND(AVG(price), 2) AS average_item_price

FROM stg_order_items
GROUP BY order_id;