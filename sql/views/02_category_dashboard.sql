-- ============================================================================
-- RetailPulse
-- Reporting View: Category Dashboard
-- Grain: One row per product category
-- Source: category_sales
-- ============================================================================

DROP VIEW IF EXISTS rpt_category_dashboard;

CREATE VIEW rpt_category_dashboard AS
SELECT
    category_name_english AS product_category,

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

FROM category_sales;