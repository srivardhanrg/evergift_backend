-- Migration 030: Add cover type support for physical books
-- Date: 2026-03-22
-- Description: Add cover_type column to orders and print_orders tables
--              to support softcover (saddle stitch) and hardcover (perfect bound) options

-- Add cover_type to orders table
ALTER TABLE orders
ADD COLUMN IF NOT EXISTS cover_type VARCHAR(20) DEFAULT 'hardcover';

-- Add cover_type to print_orders table
ALTER TABLE print_orders
ADD COLUMN IF NOT EXISTS cover_type VARCHAR(20) DEFAULT 'hardcover';

-- Add comment to document valid values
COMMENT ON COLUMN orders.cover_type IS 'Cover type for physical books: softcover (saddle stitch) or hardcover (perfect bound)';
COMMENT ON COLUMN print_orders.cover_type IS 'Cover type for physical books: softcover (saddle stitch) or hardcover (perfect bound)';

-- Update existing records to hardcover (default)
UPDATE orders
SET cover_type = 'hardcover'
WHERE cover_type IS NULL AND order_type = 'physical';

UPDATE print_orders
SET cover_type = 'hardcover'
WHERE cover_type IS NULL;
