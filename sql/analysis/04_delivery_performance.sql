-- ============================================================================
-- RetailPulse
-- Analysis: Delivery Performance
-- Grain: One row per analysis period / delivery status
-- Source: fact_orders
-- ============================================================================

DROP VIEW IF EXISTS delivery_performance;

CREATE VIEW delivery_performance AS
SELECT
    order_status,

    COUNT(*) AS order_count,

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
        AVG(delivery_days)
        FILTER (
            WHERE delivery_days IS NOT NULL
        ),
        2
    ) AS average_delivery_days,

    ROUND(
        AVG(delivery_vs_estimated_days)
        FILTER (
            WHERE delivery_vs_estimated_days IS NOT NULL
        ),
        2
    ) AS average_delivery_vs_estimated_days

FROM fact_orders

GROUP BY order_status;