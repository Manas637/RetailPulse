-- ============================================================================
-- RetailPulse
-- Transformation: Seller Dimension
-- Grain: One row per seller
-- Source: sellers
-- ============================================================================

DROP VIEW IF EXISTS dim_sellers;

CREATE VIEW dim_sellers AS
SELECT
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
FROM sellers;