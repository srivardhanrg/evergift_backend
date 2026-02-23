-- ============================================================================
-- Migration: Add tracking_url column to print_orders table
-- Date: 2026-02-23
-- Purpose: Store direct carrier tracking URLs from Lulu API (UPS/FedEx/DHL)
-- ============================================================================

-- Add tracking_url column for storing direct carrier tracking URLs
-- Lulu provides these in the SHIPPED webhook response
ALTER TABLE print_orders
ADD COLUMN IF NOT EXISTS tracking_url VARCHAR(500);

-- Add comment for documentation
COMMENT ON COLUMN print_orders.tracking_url IS
    'Direct carrier tracking URL from Lulu API (e.g., https://www.ups.com/track?tracknum=...)';

-- Create index for faster lookups when filtering by tracking_number
CREATE INDEX IF NOT EXISTS idx_print_orders_tracking_number
    ON print_orders(tracking_number)
    WHERE tracking_number IS NOT NULL;

-- Create index for faster status-based queries (for Ordered tab)
CREATE INDEX IF NOT EXISTS idx_print_orders_lulu_status
    ON print_orders(lulu_status);

-- ============================================================================
-- Verification
-- ============================================================================
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'print_orders'
        AND column_name = 'tracking_url'
    ) THEN
        RAISE NOTICE 'SUCCESS: tracking_url column added to print_orders';
    ELSE
        RAISE WARNING 'FAILED: tracking_url column not found in print_orders';
    END IF;
END $$;

-- ============================================================================
-- Rollback Script (run manually if needed):
-- ALTER TABLE print_orders DROP COLUMN IF EXISTS tracking_url;
-- DROP INDEX IF EXISTS idx_print_orders_tracking_number;
-- ============================================================================
