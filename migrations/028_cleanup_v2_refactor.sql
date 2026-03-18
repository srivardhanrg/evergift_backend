-- ============================================================================
-- Migration: 028_cleanup_v2_refactor.sql
-- Description: Cleanup for V2 refactor - remove old columns, enforce V2 structure
-- ============================================================================
-- This migration removes old split_page columns and enforces V2 26-page structure.
-- After this migration, the system will ONLY support V2 format.
-- ============================================================================

-- Drop old split-page related columns (no longer needed in V2)
ALTER TABLE previews DROP COLUMN IF EXISTS split_page_data;
ALTER TABLE previews DROP COLUMN IF EXISTS split_page_images;
ALTER TABLE previews DROP COLUMN IF EXISTS background_images;
ALTER TABLE previews DROP COLUMN IF EXISTS book_format;

-- Drop old renamed image storage columns (already migrated to book_structure)
ALTER TABLE previews DROP COLUMN IF EXISTS hires_images_old;
ALTER TABLE previews DROP COLUMN IF EXISTS preview_images_old;
ALTER TABLE previews DROP COLUMN IF EXISTS story_pages_old;

-- Ensure all existing previews have V2 defaults
-- Update any old 10-page or 24-page previews to 26-page structure
UPDATE previews SET total_pages = 26 WHERE total_pages < 26;
UPDATE previews SET preview_page_count = 13 WHERE preview_page_count < 13;

-- Set default values for V2 critical fields
ALTER TABLE previews ALTER COLUMN book_structure SET DEFAULT '{}';
ALTER TABLE previews ALTER COLUMN story_texts SET DEFAULT '{}';
ALTER TABLE previews ALTER COLUMN filler_pages_processed SET DEFAULT '{}';

-- Add check constraint to ensure only V2 format
ALTER TABLE previews ADD CONSTRAINT check_v2_format
CHECK (total_pages >= 26 AND preview_page_count >= 13);

-- Add comment explaining V2-only constraint
COMMENT ON CONSTRAINT check_v2_format ON previews IS
'Enforces V2 26-page structure: total_pages must be 26+, preview_page_count must be 13+';

-- Verify cleanup
DO $$
DECLARE
    old_column_count INTEGER;
    preview_count INTEGER;
    v2_preview_count INTEGER;
BEGIN
    -- Check if old columns still exist (should be 0)
    SELECT COUNT(*) INTO old_column_count
    FROM information_schema.columns
    WHERE table_name = 'previews'
    AND column_name IN ('split_page_data', 'split_page_images', 'background_images', 'book_format');

    -- Count total previews
    SELECT COUNT(*) INTO preview_count FROM previews;

    -- Count V2 previews
    SELECT COUNT(*) INTO v2_preview_count
    FROM previews
    WHERE total_pages >= 26 AND preview_page_count >= 13;

    RAISE NOTICE 'Migration 028 complete: V2 refactor cleanup';
    RAISE NOTICE 'Old columns remaining: % (should be 0)', old_column_count;
    RAISE NOTICE 'Total previews: %', preview_count;
    RAISE NOTICE 'V2-compliant previews: %', v2_preview_count;

    IF old_column_count > 0 THEN
        RAISE WARNING 'Some old columns still exist! Please review.';
    END IF;

    IF preview_count > 0 AND v2_preview_count < preview_count THEN
        RAISE WARNING 'Some previews are not V2-compliant! They may fail to load.';
    END IF;
END $$;
