-- ============================================================================
-- Migration: 027_book_structure_v2_reconciled.sql
-- Description: Add 26-page book structure support (reconciled with existing schema)
-- ============================================================================
-- This migration reconciles the V2 26-page structure with existing columns:
--   - Works with existing 'total_pages' column (not total_page_count)
--   - Adds book_structure alongside existing split_page_data
--   - 26 total pages (cover + 24 interior + back cover)
--   - Preview/locked boundary at index 12 (pages 0-12 visible, 13-25 locked)
-- ============================================================================

-- Add book_structure JSONB to store complete 26-page structure
-- This is separate from split_page_data to support both formats
-- Format: { "0": {"type": "cover", "url": "...", "isLocked": false}, ... }
ALTER TABLE previews
ADD COLUMN IF NOT EXISTS book_structure JSONB DEFAULT NULL;

-- Add filler_pages_processed to track which filler pages have text overlays applied
-- Format: { "1": "https://...", "5": "https://...", ... } (page index to processed URL)
ALTER TABLE previews
ADD COLUMN IF NOT EXISTS filler_pages_processed JSONB DEFAULT NULL;

-- Add story_texts to store the 10 story text contents for text pages
-- Format: { "1": "Story text for page 1...", "2": "Story text for page 2...", ... }
ALTER TABLE previews
ADD COLUMN IF NOT EXISTS story_texts JSONB DEFAULT NULL;

-- Add child_photo_url to store the original uploaded photo for post-payment generation
-- This ensures we can generate remaining pages with the same reference photo
ALTER TABLE previews
ADD COLUMN IF NOT EXISTS child_photo_url TEXT;

-- Update existing total_pages column default to 26 (was 24)
-- NOTE: Using existing 'total_pages' column, not creating 'total_page_count'
ALTER TABLE previews
ALTER COLUMN total_pages SET DEFAULT 26;

-- Update preview_page_count default to 13 (pages 0-12 visible)
ALTER TABLE previews
ALTER COLUMN preview_page_count SET DEFAULT 13;

-- Add generation_progress for granular progress tracking (0-100)
ALTER TABLE previews
ADD COLUMN IF NOT EXISTS generation_progress INTEGER DEFAULT 0;

-- Add current_generating_page to show which page is being generated
ALTER TABLE previews
ADD COLUMN IF NOT EXISTS current_generating_page INTEGER DEFAULT NULL;

-- Update existing records with old 10-page structure to new 26-page defaults
-- Only update if they still have old values (5 preview, 10 total)
UPDATE previews
SET preview_page_count = 13, total_pages = 26
WHERE preview_page_count = 5 AND total_pages = 10;

-- Add indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_previews_book_structure
ON previews USING GIN (book_structure);

CREATE INDEX IF NOT EXISTS idx_previews_generation_progress
ON previews(generation_progress);

-- Add comments for documentation
COMMENT ON COLUMN previews.book_structure IS
'V2 26-page structure: {pageIndex: {type, url, isLocked, isGenerated}} - separate from split_page_data';

COMMENT ON COLUMN previews.filler_pages_processed IS
'Processed filler page URLs with text overlays: {pageIndex: processedUrl}';

COMMENT ON COLUMN previews.story_texts IS
'Story text content for text pages: {pageNumber: textContent} where pageNumber is 1-10';

COMMENT ON COLUMN previews.child_photo_url IS
'Original uploaded child photo URL for AI generation consistency';

COMMENT ON COLUMN previews.generation_progress IS
'Generation progress percentage 0-100 for UI display';

COMMENT ON COLUMN previews.current_generating_page IS
'Index of page currently being generated, NULL when not generating';

COMMENT ON COLUMN previews.total_pages IS
'Total page count in the book (default 26 for V2, was 24 for split_page format, 10 for legacy)';

COMMENT ON COLUMN previews.preview_page_count IS
'Number of preview pages visible before purchase (default 13 for V2: pages 0-12)';

-- Verify migration
DO $$
BEGIN
    RAISE NOTICE 'Migration 027_book_structure_v2_reconciled complete: Added 26-page V2 structure support';
    RAISE NOTICE 'Note: Preserves existing book_format, split_page_* columns for backwards compatibility';
END $$;
