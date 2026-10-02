-- ============================================================================
-- RetailPulse
-- Reporting View: Customer Dashboard
-- Grain: One row per customer
-- Source: customer_behavior
-- ============================================================================

DROP VIEW IF EXISTS rpt_customer_dashboard;

CREATE VIEW rpt_customer_dashboard AS
SELECT
    customer_unique_id,
    customer_city,
    customer_state,

    order_count,
    first_order_date,
    last_order_date,

    total_customer_value,
    average_order_value,

    total_items,
    average_items_per_order,

    CASE
        WHEN order_count = 1
            THEN 'One-Time Customer'

        WHEN order_count BETWEEN 2 AND 3
            THEN 'Repeat Customer'

        ELSE 'Frequent Customer'
    END AS customer_segment

FROM customer_behavior;