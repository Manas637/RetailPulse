-- ============================================================================
-- RetailPulse
-- Transformation: Order Fact
-- Grain: One row per order
-- Sources:
--   stg_orders
--   order_item_summary
--   order_payment_summary
-- ============================================================================

DROP VIEW IF EXISTS fact_orders;

CREATE VIEW fact_orders AS
SELECT
    o.order_id,
    o.customer_id,

    -- Order information
    o.order_status,
    o.order_purchase_timestamp,
    o.order_purchase_date,
    o.order_purchase_month,

    -- Delivery information
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    o.delivery_days,
    o.delivery_vs_estimated_days,
    o.delivery_performance,

    -- Item metrics
    i.item_count,
    i.distinct_product_count,
    i.distinct_seller_count,
    i.merchandise_value,
    i.freight_value,
    i.item_total_value,
    i.average_item_price,

    -- Payment metrics
    p.payment_count,
    p.payment_type_count,
    p.total_payment_value,
    p.average_payment_value,
    p.max_payment_installments,
    p.installment_payment_count,
    p.payment_types

FROM stg_orders o

LEFT JOIN order_item_summary i
    ON o.order_id = i.order_id

LEFT JOIN order_payment_summary p
    ON o.order_id = p.order_id;