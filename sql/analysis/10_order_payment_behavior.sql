-- ============================================================================
-- RetailPulse
-- Analysis: Order Payment Behavior
-- Grain: One row per order
-- Source: order_payment_summary
-- ============================================================================

DROP VIEW IF EXISTS order_payment_behavior;

CREATE VIEW order_payment_behavior AS
SELECT
    order_id,
    payment_count,
    payment_type_count,
    total_payment_value,
    average_payment_value,
    max_payment_installments,
    installment_payment_count,
    payment_types,

    CASE
        WHEN payment_type_count > 1
            THEN 'Multiple Payment Types'
        ELSE 'Single Payment Type'
    END AS payment_method_behavior,

    CASE
        WHEN max_payment_installments > 1
            THEN 'Installment'
        ELSE 'Single Payment'
    END AS installment_behavior

FROM order_payment_summary;