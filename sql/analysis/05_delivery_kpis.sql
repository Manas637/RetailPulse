-- ============================================================================
-- RetailPulse
-- Analysis: Delivery KPIs
-- Grain: One row
-- Source: fact_orders
-- ============================================================================

DROP VIEW IF EXISTS delivery_kpis;

CREATE VIEW delivery_kpis AS
SELECT
    COUNT(*) AS total_orders,

    COUNT(*) FILTER (
        WHERE delivery_performance <> 'Not Delivered'
    ) AS delivered_orders,

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
    ) AS average_delivery_days,

    ROUND(
        AVG(delivery_vs_estimated_days)
        FILTER (
            WHERE delivery_vs_estimated_days IS NOT NULL
        ),
        2
    ) AS average_delivery_vs_estimated_days

FROM fact_orders;