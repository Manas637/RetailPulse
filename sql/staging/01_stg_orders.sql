-- ============================================================================
-- RetailPulse
-- Staging Layer: Orders
-- Grain: One row per order
-- Source: orders
-- ============================================================================

DROP VIEW IF EXISTS stg_orders;

CREATE VIEW stg_orders AS
SELECT
    order_id,
    customer_id,

    -- Order lifecycle
    order_status,

    -- Timestamps
    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date,

    -- Derived date fields
    DATE(order_purchase_timestamp) AS order_purchase_date,
    DATE_TRUNC('month', order_purchase_timestamp)::DATE
        AS order_purchase_month,

    -- Delivery metrics
    CASE
        WHEN order_delivered_customer_date IS NOT NULL
        THEN (
            order_delivered_customer_date::DATE
            - order_purchase_timestamp::DATE
        )
    END AS delivery_days,

    CASE
        WHEN order_delivered_customer_date IS NOT NULL
             AND order_estimated_delivery_date IS NOT NULL
        THEN (
            order_delivered_customer_date::DATE
            - order_estimated_delivery_date::DATE
        )
    END AS delivery_vs_estimated_days,

    -- Delivery status
    CASE
        WHEN order_delivered_customer_date IS NULL THEN 'Not Delivered'

        WHEN order_delivered_customer_date::DATE
             <= order_estimated_delivery_date::DATE
            THEN 'On Time'

        ELSE 'Late'
    END AS delivery_performance

FROM orders;