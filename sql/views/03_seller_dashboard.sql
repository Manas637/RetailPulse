-- ============================================================================
-- RetailPulse
-- Reporting View: Seller Dashboard
-- Grain: One row per seller with at least one order item
-- Source: seller_sales
-- ============================================================================

DROP VIEW IF EXISTS rpt_seller_dashboard;

CREATE VIEW rpt_seller_dashboard AS
SELECT
    seller_id,
    seller_city,
    seller_state,

    item_count,
    order_count,
    product_count,

    merchandise_revenue,
    freight_value,
    total_item_value,
    average_item_price,

    ROUND(
        100.0 * freight_value
        / NULLIF(merchandise_revenue, 0),
        2
    ) AS freight_to_merchandise_pct

FROM seller_sales;