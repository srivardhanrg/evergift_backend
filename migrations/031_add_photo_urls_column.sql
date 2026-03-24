-- ============================================================================
-- Migration: 031_add_photo_urls_column.sql
-- Description: Add photo_urls JSONB column for multi-face support
-- ============================================================================
-- Stores all uploaded photo URLs (1-3) as a JSON array.
-- Previously only photo_url (single string) was stored, losing additional
-- reference photos needed for multi-face AI generation.
-- ============================================================================

-- Add photo_urls JSONB array column
ALTER TABLE previews
ADD COLUMN IF NOT EXISTS photo_urls JSONB DEFAULT NULL;

-- Backfill existing rows: wrap single photo_url into a JSON array
UPDATE previews
SET photo_urls = jsonb_build_array(photo_url)
WHERE photo_urls IS NULL AND photo_url IS NOT NULL;

-- Add comment
COMMENT ON COLUMN previews.photo_urls IS
'JSON array of all uploaded child photo URLs (1-3) for multi-face AI generation. Sorted by quality score (best first).';

-- Verify migration
DO $$
DECLARE
    backfilled INTEGER;
BEGIN
    SELECT COUNT(*) INTO backfilled FROM previews WHERE photo_urls IS NOT NULL;
    RAISE NOTICE 'Migration 031 complete: Added photo_urls JSONB column, backfilled % rows', backfilled;
END $$;
