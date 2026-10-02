-- ============================================================================
-- RetailPulse
-- Analysis: Payment Behavior
-- Grain: One row per payment type
-- Source: stg_payments
-- ============================================================================

DROP VIEW IF EXISTS payment_analysis;

CREATE VIEW payment_analysis AS
SELECT
    payment_type,

    COUNT(*) AS payment_record_count,

    COUNT(DISTINCT order_id) AS order_count,

    ROUND(SUM(payment_value), 2) AS total_payment_value,

    ROUND(AVG(payment_value), 2) AS average_payment_value,

    ROUND(AVG(payment_installments), 2) AS average_installments,

    COUNT(*) FILTER (
        WHERE payment_installments > 1
    ) AS installment_payment_records,

    COUNT(*) FILTER (
        WHERE payment_value = 0
    ) AS zero_value_payment_records

FROM stg_payments

GROUP BY payment_type;