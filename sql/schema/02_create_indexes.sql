CREATE INDEX idx_orders_customer_id
    ON orders(customer_id);

CREATE INDEX idx_orders_purchase_timestamp
    ON orders(order_purchase_timestamp);

CREATE INDEX idx_orders_status
    ON orders(order_status);


CREATE INDEX idx_order_items_product_id
    ON order_items(product_id);

CREATE INDEX idx_order_items_seller_id
    ON order_items(seller_id);


CREATE INDEX idx_order_payments_order_id
    ON order_payments(order_id);


CREATE INDEX idx_order_reviews_order_id
    ON order_reviews(order_id);


CREATE INDEX idx_customers_unique_id
    ON customers(customer_unique_id);

CREATE INDEX idx_customers_state
    ON customers(customer_state);


CREATE INDEX idx_geolocation_zip_code
    ON geolocation(geolocation_zip_code_prefix);