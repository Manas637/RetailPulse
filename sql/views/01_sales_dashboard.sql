-- ============================================================================
-- RetailPulse
-- Reporting View: Sales Dashboard
-- Grain: One row per purchase month
-- Sources:
--   fact_orders
--   dim_customers
-- ============================================================================

DROP VIEW IF EXISTS rpt_sales_dashboard;

CREATE VIEW rpt_sales_dashboard AS
SELECT
    fo.order_purchase_month AS sales_month,

    -- Volume
    COUNT(*) AS order_count,

    COUNT(DISTINCT dc.customer_unique_id) AS unique_customers,

    -- Revenue
    ROUND(SUM(fo.merchandise_value), 2) AS merchandise_revenue,

    ROUND(SUM(fo.freight_value), 2) AS freight_revenue,

    ROUND(SUM(fo.item_total_value), 2) AS total_revenue,

    -- Average metrics
    ROUND(
        AVG(fo.item_total_value),
        2
    ) AS average_order_value,

    ROUND(
        AVG(fo.item_count),
        2
    ) AS average_items_per_order,

    -- Delivery
    COUNT(*) FILTER (
        WHERE fo.delivery_performance = 'On Time'
    ) AS on_time_orders,

    COUNT(*) FILTER (
        WHERE fo.delivery_performance = 'Late'
    ) AS late_orders,

    COUNT(*) FILTER (
        WHERE fo.delivery_performance = 'Not Delivered'
    ) AS not_delivered_orders,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE fo.delivery_performance = 'Late'
        )
        / NULLIF(
            COUNT(*) FILTER (
                WHERE fo.delivery_performance IN ('On Time', 'Late')
            ),
            0
        ),
        2
    ) AS late_delivery_rate

FROM fact_orders fo

LEFT JOIN dim_customers dc
    ON fo.customer_id = dc.customer_id

GROUP BY fo.order_purchase_month;