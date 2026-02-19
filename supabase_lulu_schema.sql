-- ============================================================================
-- Lulu Print Integration Schema
-- Run this AFTER supabase_schema.sql
-- ============================================================================

-- Lulu print job status enum
CREATE TYPE lulu_print_status AS ENUM (
    'pending',          -- Waiting to be sent to Lulu
    'submitted',        -- Sent to Lulu API
    'accepted',         -- Lulu accepted and validated the job
    'rejected',         -- Lulu rejected (file/spec issue)
    'in_production',    -- Being printed
    'shipped',          -- Dispatched by Lulu
    'delivered',        -- Confirmed delivered
    'cancelled',        -- Cancelled before print
    'failed'            -- API error or unrecoverable failure
);

-- ============================================================================
-- print_orders table: tracks every Lulu print job
-- ============================================================================
CREATE TABLE print_orders (
    id SERIAL PRIMARY KEY,
    print_order_id UUID UNIQUE NOT NULL DEFAULT uuid_generate_v4(),

    -- Links
    order_id VARCHAR(100) NOT NULL,       -- FK to orders.order_id
    preview_id UUID NOT NULL,             -- FK to previews.preview_id

    -- Lulu API identifiers
    lulu_print_job_id VARCHAR(100),       -- Lulu's print-job ID (set after submission)
    lulu_status lulu_print_status DEFAULT 'pending',
    lulu_status_raw VARCHAR(100),         -- Raw status string from Lulu API

    -- Files uploaded to Lulu
    interior_pdf_url VARCHAR(500),        -- R2 URL of Lulu-spec interior PDF
    cover_pdf_url VARCHAR(500),           -- R2 URL of Lulu-spec cover wrap PDF

    -- Shipping
    shipping_option VARCHAR(100),         -- e.g. 'MAIL', 'GROUND', 'EXPEDITED'
    shipping_address JSONB,              -- {name, street1, street2, city, state, zip, country}
    tracking_number VARCHAR(100),
    carrier VARCHAR(50),                  -- e.g. 'UPS', 'USPS', 'FedEx'
    estimated_delivery DATE,

    -- Cost
    pod_package_id VARCHAR(100) DEFAULT '0850X0850FCPRESS080CW444GXX',
    print_cost DECIMAL(10,2),
    shipping_cost DECIMAL(10,2),
    total_cost DECIMAL(10,2),
    currency VARCHAR(10) DEFAULT 'USD',

    -- Error handling
    attempts INTEGER DEFAULT 0,
    last_error TEXT,

    -- Raw API response for debugging
    lulu_api_response JSONB,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    submitted_at TIMESTAMP WITH TIME ZONE,
    shipped_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE
);

-- ============================================================================
-- Indexes
-- ============================================================================
CREATE INDEX idx_print_orders_order_id ON print_orders(order_id);
CREATE INDEX idx_print_orders_preview_id ON print_orders(preview_id);
CREATE INDEX idx_print_orders_lulu_print_job_id ON print_orders(lulu_print_job_id);
CREATE INDEX idx_print_orders_lulu_status ON print_orders(lulu_status);
CREATE INDEX idx_print_orders_created_at ON print_orders(created_at);

-- ============================================================================
-- Auto-update updated_at trigger
-- ============================================================================
CREATE TRIGGER update_print_orders_updated_at
    BEFORE UPDATE ON print_orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Foreign key constraints
-- ============================================================================
ALTER TABLE print_orders
    ADD CONSTRAINT print_orders_order_id_fkey
    FOREIGN KEY (order_id) REFERENCES orders(order_id);

ALTER TABLE print_orders
    ADD CONSTRAINT print_orders_preview_id_fkey
    FOREIGN KEY (preview_id) REFERENCES previews(preview_id);

-- ============================================================================
-- Verify
-- ============================================================================
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'print_orders'
    ) THEN
        RAISE NOTICE 'SUCCESS: print_orders table created';
    ELSE
        RAISE WARNING 'FAILED: print_orders table not found';
    END IF;
END $$;
