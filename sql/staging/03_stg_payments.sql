-- ============================================================================
-- RetailPulse
-- Staging Layer: Payments
-- Grain: One row per payment record
-- Source: order_payments
-- ============================================================================

DROP VIEW IF EXISTS stg_payments;

CREATE VIEW stg_payments AS
SELECT
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value,

    CASE
        WHEN payment_installments > 1 THEN TRUE
        ELSE FALSE
    END AS is_installment_payment,

    CASE
        WHEN payment_value > 0 THEN TRUE
        ELSE FALSE
    END AS has_payment_value

FROM order_payments;