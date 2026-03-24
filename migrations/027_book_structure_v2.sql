-- ============================================================================
-- Migration: 027_book_structure_v2.sql
-- Description: Add 26-page book structure support with filler pages
-- ============================================================================
-- This migration adds columns to support the new book structure:
--   - 26 total pages (cover + 24 interior + back cover)
--   - Filler pages from R2 storage with text overlays
--   - Preview/locked page boundary at index 12
-- ============================================================================

-- Add book_structure JSONB to store complete 26-page structure
-- Format: { "0": {"type": "cover", "url": "..."}, "1": {"type": "dedication", "url": "..."}, ... }
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

-- Update page count defaults for 26-page structure
-- preview_page_count: 13 (pages 0-12 visible in preview)
-- total_page_count: 26 (full book)
UPDATE previews
SET preview_page_count = 13, total_page_count = 26
WHERE preview_page_count = 5 AND total_page_count = 10;

-- Update default values for new previews
ALTER TABLE previews
ALTER COLUMN preview_page_count SET DEFAULT 13;

ALTER TABLE previews
ALTER COLUMN total_page_count SET DEFAULT 26;

-- Add generation_progress for granular progress tracking (0-100)
ALTER TABLE previews
ADD COLUMN IF NOT EXISTS generation_progress INTEGER DEFAULT 0;

-- Add current_generating_page to show which page is being generated
ALTER TABLE previews
ADD COLUMN IF NOT EXISTS current_generating_page INTEGER DEFAULT NULL;

-- Add indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_previews_book_structure
ON previews USING GIN (book_structure);

CREATE INDEX IF NOT EXISTS idx_previews_generation_progress
ON previews(generation_progress);

-- Add comments for documentation
COMMENT ON COLUMN previews.book_structure IS
'Complete 26-page structure: {pageIndex: {type, url, isLocked, isGenerated}}';

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

-- Verify migration
DO $$
BEGIN
    RAISE NOTICE 'Migration 027_book_structure_v2 complete: Added 26-page structure support';
END $$;
