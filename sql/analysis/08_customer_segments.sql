-- ============================================================================
-- RetailPulse
-- Analysis: Customer Segmentation
-- Grain: One row per customer segment
-- Source: customer_behavior
-- ============================================================================

DROP VIEW IF EXISTS customer_segments;

CREATE VIEW customer_segments AS
SELECT
    CASE
        WHEN order_count = 1
            THEN 'One-Time Customer'

        WHEN order_count BETWEEN 2 AND 3
            THEN 'Repeat Customer'

        ELSE 'Frequent Customer'
    END AS customer_segment,

    COUNT(*) AS customer_count,

    ROUND(
        AVG(total_customer_value),
        2
    ) AS average_customer_value,

    ROUND(
        SUM(total_customer_value),
        2
    ) AS total_customer_value,

    ROUND(
        AVG(order_count),
        2
    ) AS average_orders_per_customer

FROM customer_behavior

GROUP BY
    CASE
        WHEN order_count = 1
            THEN 'One-Time Customer'

        WHEN order_count BETWEEN 2 AND 3
            THEN 'Repeat Customer'

        ELSE 'Frequent Customer'
    END;