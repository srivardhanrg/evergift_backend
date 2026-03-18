-- ============================================================================
-- Migration: 029_drop_v1_image_columns.sql
-- Description: Drop old V1 image storage columns (hires_images, preview_images, story_pages)
-- ============================================================================
-- These columns were used in V1 to store arrays of image URLs.
-- V2 uses book_structure JSONB exclusively for all page data.
-- ============================================================================

-- Drop old V1 image storage columns
ALTER TABLE previews DROP COLUMN IF EXISTS hires_images;
ALTER TABLE previews DROP COLUMN IF EXISTS preview_images;
ALTER TABLE previews DROP COLUMN IF EXISTS story_pages;

-- Verify cleanup
DO $$
DECLARE
    old_column_count INTEGER;
BEGIN
    -- Check if old columns still exist (should be 0)
    SELECT COUNT(*) INTO old_column_count
    FROM information_schema.columns
    WHERE table_name = 'previews'
    AND column_name IN ('hires_images', 'preview_images', 'story_pages');

    RAISE NOTICE 'Migration 029 complete: Dropped V1 image columns';
    RAISE NOTICE 'Old V1 columns remaining: % (should be 0)', old_column_count;

    IF old_column_count > 0 THEN
        RAISE WARNING 'Some old V1 columns still exist! Database may have schema issues.';
    END IF;
END $$;

-- Add comment explaining V2-only approach
COMMENT ON TABLE previews IS
'V2 26-page storybook previews. Uses book_structure JSONB for all page data.';
