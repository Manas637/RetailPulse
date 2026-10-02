-- ============================================================================
-- RetailPulse
-- Transformation: Order Payment Summary
-- Grain: One row per order
-- Source: stg_payments
-- ============================================================================

DROP VIEW IF EXISTS order_payment_summary;

CREATE VIEW order_payment_summary AS
SELECT
    order_id,

    -- Payment metrics
    COUNT(*) AS payment_count,

    COUNT(DISTINCT payment_type) AS payment_type_count,

    -- Total amount paid
    ROUND(SUM(payment_value), 2) AS total_payment_value,

    -- Average payment
    ROUND(AVG(payment_value), 2) AS average_payment_value,

    -- Installment information
    MAX(payment_installments) AS max_payment_installments,

    -- Number of installment-based payment records
    COUNT(*) FILTER (
        WHERE is_installment_payment = TRUE
    ) AS installment_payment_count,

    -- Payment types used for the order
    STRING_AGG(
        DISTINCT payment_type,
        ', '
        ORDER BY payment_type
    ) AS payment_types

FROM stg_payments
GROUP BY order_id;