-- ============================================================================
-- RetailPulse
-- Analysis: Monthly Delivery Performance
-- Grain: One row per purchase month
-- Source: fact_orders
-- ============================================================================

DROP VIEW IF EXISTS monthly_delivery;

CREATE VIEW monthly_delivery AS
SELECT
    order_purchase_month AS sales_month,

    COUNT(*) AS total_orders,

    COUNT(*) FILTER (
        WHERE delivery_performance = 'On Time'
    ) AS on_time_orders,

    COUNT(*) FILTER (
        WHERE delivery_performance = 'Late'
    ) AS late_orders,

    COUNT(*) FILTER (
        WHERE delivery_performance = 'Not Delivered'
    ) AS not_delivered_orders,

    ROUND(
        100.0
        * COUNT(*) FILTER (
            WHERE delivery_performance = 'Late'
        )
        / NULLIF(
            COUNT(*) FILTER (
                WHERE delivery_performance IN ('On Time', 'Late')
            ),
            0
        ),
        2
    ) AS late_delivery_rate,

    ROUND(
        AVG(delivery_days)
        FILTER (
            WHERE delivery_days IS NOT NULL
        ),
        2
    ) AS average_delivery_days

FROM fact_orders

GROUP BY order_purchase_month;