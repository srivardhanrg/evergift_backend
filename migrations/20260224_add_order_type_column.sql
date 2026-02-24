-- Add order_type column to orders table
-- Stores 'digital' or 'physical' — set by webhook at order creation time
-- Used by frontend to show correct post-payment UI and by backend for Lulu routing

ALTER TABLE orders ADD COLUMN IF NOT EXISTS order_type VARCHAR(20) DEFAULT 'digital';
COMMENT ON COLUMN orders.order_type IS 'Order type: digital (PDF only) or physical (Lulu print). Set by Shopify webhook.';

-- Backfill existing orders that have print_orders as physical
UPDATE orders
SET order_type = 'physical'
WHERE order_id IN (
    SELECT DISTINCT order_id FROM print_orders
)
AND order_type = 'digital';
