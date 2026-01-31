-- ============================================================================
-- Migration: Add Secret Agent theme
-- ============================================================================
-- Run this migration to allow the new Secret Agent theme in the database.
-- New theme:
--   - storygift_secret_agent (Multi-profession spy adventure)
-- ============================================================================

-- Drop the old theme check constraint
ALTER TABLE previews DROP CONSTRAINT IF EXISTS previews_theme_check;

-- Add the new constraint with all themes including Secret Agent
ALTER TABLE previews
ADD CONSTRAINT previews_theme_check
CHECK (theme IN (
    -- StoryGift premium themes
    'storygift_magic_castle',
    'storygift_enchanted_forest',
    'storygift_spy_mission',
    'storygift_cosmic_dreamer',
    'storygift_mighty_guardian',
    'storygift_ocean_explorer',
    'storygift_birthday_magic',
    'storygift_safari_adventure',
    'storygift_dream_weaver',
    -- NEW THEME ADDED
    'storygift_secret_agent',
    -- Legacy themes (for backward compatibility)
    'magic_castle',
    'space_adventure',
    'underwater',
    'forest_friends'
));

-- Verify the constraint was applied
DO $$
BEGIN
    RAISE NOTICE 'Migration complete: Added storygift_secret_agent theme';
END $$;
