-- ============================================================================
-- RetailPulse
-- Staging Layer: Order Items
-- Grain: One row per item within an order
-- Source: order_items
-- ============================================================================

DROP VIEW IF EXISTS stg_order_items;

CREATE VIEW stg_order_items AS
SELECT
    order_id,
    order_item_id,
    product_id,
    seller_id,

    -- Monetary fields
    price,
    freight_value,

    -- Item shipping timestamp
    shipping_limit_date,

    -- Derived monetary field
    price + freight_value AS item_total_value,

    -- Freight as percentage of item price
    CASE
        WHEN price > 0
        THEN ROUND(
            (freight_value / price) * 100,
            2
        )
    END AS freight_percentage

FROM order_items;