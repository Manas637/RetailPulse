-- ============================================================================
-- RetailPulse
-- Reporting View: Delivery Dashboard
-- Grain: One row per purchase month
-- Source: monthly_delivery
-- ============================================================================

DROP VIEW IF EXISTS rpt_delivery_dashboard;

CREATE VIEW rpt_delivery_dashboard AS
SELECT
    sales_month,

    total_orders,
    on_time_orders,
    late_orders,
    not_delivered_orders,

    late_delivery_rate,
    average_delivery_days

FROM monthly_delivery;