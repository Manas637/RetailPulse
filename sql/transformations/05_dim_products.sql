-- ============================================================================
-- RetailPulse
-- Transformation: Product Dimension
-- Grain: One row per product
-- Sources: products + category_translation
-- ============================================================================

DROP VIEW IF EXISTS dim_products;

CREATE VIEW dim_products AS
SELECT
    p.product_id,
    p.product_category_name AS category_name_portuguese,
    COALESCE(
        t.product_category_name_english,
        'Unknown'
    ) AS category_name_english,

    p.product_name_length,
    p.product_description_length,
    p.product_photos_qty,

    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm,

    -- Product volume in cubic centimeters
    CASE
        WHEN p.product_length_cm IS NOT NULL
         AND p.product_height_cm IS NOT NULL
         AND p.product_width_cm IS NOT NULL
        THEN
            p.product_length_cm
            * p.product_height_cm
            * p.product_width_cm
    END AS product_volume_cm3

FROM products p

LEFT JOIN category_translation t
    ON p.product_category_name = t.product_category_name;