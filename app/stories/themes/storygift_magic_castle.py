"""
StoryGift Magic Castle Theme - Converted to Magictales format.

Complete 10-page story: "The First Day of Magic School"
Converted from StoryGift's 5 scenes × 2 panels structure
Preserves all original prompts, dialogue, and story narrative
"""

from app.stories.templates import StoryTemplate, PageTemplate


STORYGIFT_MAGIC_CASTLE_THEME = StoryTemplate(
    theme_id="storygift_magic_castle",
    title_template="{name}'s First Day of Magic School",
    description="A detailed magical academy adventure",
    default_costume="wearing wizard robes",
    protagonist_description="bright expressive eyes, curious and brave expression",
    # Cover page settings for typography-ready composition
    cover_costume="wearing elegant purple and gold wizard robes with magical embroidered patterns, a flowing cape, and holding a glowing wand",
    cover_header_atmosphere="Majestic magical castle towers rising into a mystical purple twilight sky with stars and magical aurora, castle spires fading into elegant mist",
    cover_magical_elements="Glowing magical orbs float gently around the child's body (not face). Professor Hoot the wise owl perches on a nearby pillar. Sparky the baby dragon peeks from behind. Magical sparkles and wisps dance in the air.",
    cover_footer_description="Polished marble castle courtyard floor with magical glowing runes, ancient stone steps leading to grand doors",
    pages=[
        # === SCENE 1 - THE ARRIVAL ===

        # PAGE 1 (Scene 1 - Left Panel)
        PageTemplate(
            page_number=1,
            scene_description="Arrival at the magic school gates",
            scene_type="arrival",
            realistic_prompt="""Wide establishing shot. The child wizard named {name} stands in the foreground looking up at a massive gothic castle gate made of dark iron, castle towers disappearing into the mist. To the right of the gate, sitting on a high stone pedestal, is Professor Hoot - a giant brown wise owl wearing large round reading glasses and a small black graduation cap. Cinematic lighting with golden morning rays breaking through mist. Child's face showing awe and nervous excitement, clearly visible and detailed in the dramatic lighting. The child is wearing elegant wizard robes.""",
            story_text="The morning mist clung to the cobblestones as the Grand Academy of Arcane Arts finally came into view. Standing before the massive iron gates was the school's oldest guardian. Professor Hoot was not merely an owl; he was a giant, ancient sentinel wearing thick spectacles.",
            costume="wearing wizard robes"
        ),

        # PAGE 2 (Scene 1 - Right Panel)
        PageTemplate(
            page_number=2,
            scene_description="Casting the unlock spell",
            scene_type="arrival",
            realistic_prompt="""Magical spell-casting moment. Close-up of the child wizard named {name} with wand extended toward camera, brilliant golden magic sparks erupting from wand tip. Child's face lit dramatically by the magical glow, expression showing fierce concentration and determination. Professor Hoot (giant wise owl with glasses and graduation cap) visible in soft focus background, watching approvingly. The ancient iron gate lock glowing with magical energy. Child positioned at three-quarter angle, face prominently visible and detailed, eyes focused with magical power. Dramatic cinematic lighting from the spell. The child is wearing elegant wizard robes.""",
            story_text="He adjusted his glasses with a wing tip and peered down. The test had begun before the first step was even taken. 'Only the worthy may pass,' hooted Professor Hoot as {name} shouted 'ALOHOMORA!' and magic sparks illuminated the ancient lock.",
            costume="wearing wizard robes"
        ),

        # === SCENE 2 - BEAST TAMING CLASS ===

        # PAGE 3 (Scene 2 - Left Panel)
        PageTemplate(
            page_number=3,
            scene_description="Beast Taming class begins",
            scene_type="action",
            realistic_prompt="""Dramatic courtyard scene. A reinforced wooden crate in the center of a stone courtyard is shaking violently with purple smoke leaking from cracks. The child wizard named {name} standing cautiously, holding wand at the ready, watching the mysterious crate with mix of fear and curiosity. Stone castle walls in background. Dramatic lighting from purple smoke glow. Child's face showing nervous anticipation, expression clearly visible and detailed. The child is wearing wizard robes.""",
            story_text="The courtyard was buzzing as the Beast Taming class began. In the center sat a wooden crate that shook violently. Purple smoke leaked from every crack as students backed away nervously. 'It's gonna blow!' someone shouted.",
            costume="wearing wizard robes"
        ),

        # PAGE 4 (Scene 2 - Right Panel)
        PageTemplate(
            page_number=4,
            scene_description="Meeting Sparky the dragon",
            scene_type="bonding",
            realistic_prompt="""Heartwarming bonding scene in stone courtyard. The child named {name} kneeling while facing toward camera at three-quarter angle, body positioned to show full face clearly to viewer. The child is looking down affectionately at Sparky (tiny adorable baby dragon, red with orange wings) in the open wooden crate beside them. Child's face lit with gentle smile showing compassion and wonder, offering a treat to the baby dragon who is breathing a tiny puff of harmless smoke. CRITICAL: Child's face must be clearly visible to camera showing frontal or three-quarter view, NOT profile view. Castle walls in background. Warm afternoon sunlight illuminating the child's face from the side without washing out natural skin tone. Child's gentle smiling face clearly visible and detailed with authentic skin tone, showing emotional connection with the baby dragon. The child is wearing wizard robes.""",
            story_text="With a pop, the lid flew open, revealing Sparky—a baby dragon with the hiccups. Every time he hiccuped, a smoke ring puffed from his nose. He wasn't scary; he was just hungry. '{name} offered a treat, realizing 'You're just hungry, aren't you?'",
            costume="wearing wizard robes"
        ),

        # === SCENE 3 - ADVANCED FLIGHT ===

        # PAGE 5 (Scene 3 - Left Panel)
        PageTemplate(
            page_number=5,
            scene_description="Learning to fly on broomstick",
            scene_type="action",
            realistic_prompt="""Dynamic action shot. The child named {name} straddling a wooden magical broomstick, hovering just above the grass, feet kicking off the ground to launch. Dust swirling around them dramatically. Child gripping broom handle tight with both hands, expression of pure determination and excitement on their face. Wind beginning to blow their hair and robes. Child's determined excited face clearly visible and detailed showing the thrill of first flight. The child is wearing wizard robes.""",
            story_text="By afternoon, the winds picked up for Advanced Flight. The broomstick vibrated in hand, alive with enchantment. While others wobbled, a surge of confidence took hold. 'Time to fly!' {name} declared with determination.",
            costume="wearing wizard robes"
        ),

        # PAGE 6 (Scene 3 - Right Panel)
        PageTemplate(
            page_number=6,
            scene_description="Flying through the castle grounds",
            scene_type="flight",
            realistic_prompt="""Exhilarating flight scene. The child named {name} zooming through a stone ring high in the sky on a broomstick, face turned toward camera showing pure joy and accomplishment. Wind rushing through hair, robes flowing dramatically behind. Castle grounds and clouds visible far below. Golden afternoon sunlight catching child's triumphant expression. Child's joyful face clearly visible and detailed, showing the thrill of successful flight. The child is wearing wizard robes.""",
            story_text="With a command of 'UP!', the broom shot into the sky. The wind rushed past ears like a roaring river. The ground became a quilt of green and grey. 'I did it!' {name} shouted with pure exhilaration as they soared through stone rings in the sky.",
            costume="wearing wizard robes"
        ),

        # === SCENE 4 - THE ANCIENT LIBRARY ===

        # PAGE 7 (Scene 4 - Left Panel)
        PageTemplate(
            page_number=7,
            scene_description="Exploring the magical library",
            scene_type="mischief",
            realistic_prompt="""Intimate library exploration scene. The child named {name} sitting at an ancient wooden table in the magnificent library, face angled toward camera at three-quarter view, carefully opening a large dusty leather-bound book with golden magical symbols on its cover. Child's face illuminated by soft warm glow emanating from the book's pages (lighting enhances features without changing skin tone), expression showing wonder and mischievous curiosity. Midnight (a sleek black cat with glowing yellow eyes and silver collar) sitting beside them on the table watching intently. Towering magical bookshelves in background, sunbeams filtering through high windows catching dust motes like sparkles. CRITICAL: Maintain accurate skin tone despite magical glow - the golden light should add warmth and highlights without desaturating, lightening, or changing the child's natural complexion and ethnic features. Child's curious fascinated face clearly visible and detailed with authentic skin tone preserved, lit by the magical book's glow with all facial features fully visible. The child is wearing wizard robes.""",
            story_text="The Ancient Library was quiet until curiosity took over. Midnight, the library cat, dozed peacefully as {name} reached for an ancient tome. 'Just one peek...' they whispered, not knowing what magic would unfold.",
            costume="wearing wizard robes"
        ),

        # PAGE 8 (Scene 4 - Right Panel)
        PageTemplate(
            page_number=8,
            scene_description="Chaos in the magical library",
            scene_type="chaos",
            realistic_prompt="""Magical chaos scene in the library. Hundreds of books flying like a flock of birds across the high-ceilinged room. Midnight (a sleek black cat with glowing yellow eyes and silver collar) leaping mid-air to catch one. The child named {name} near a table with expression of surprised delight and playful alarm, trying to catch flying books. Dramatic lighting from stained glass windows. Child's amused surprised face clearly visible and detailed, showing fun amidst the chaos. The child is wearing wizard robes.""",
            story_text="A sneeze disturbed the dust, and suddenly the books woke up! Leather-bound covers flapped like heavy wings in a paper storm. Midnight sprang into action, treating the flying literature like birds. 'MEOW! Got it!' seemed to say as {name} called 'Down boy!' It was chaos, but fun.",
            costume="wearing wizard robes"
        ),

        # === SCENE 5 - PEACEFUL ENDING ===

        # PAGE 9 (Scene 5 - Left Panel)
        PageTemplate(
            page_number=9,
            scene_description="Peaceful moment on the tower balcony",
            scene_type="peaceful",
            realistic_prompt="""Magical peaceful night scene. The child named {name} in elegant formal wizard robes leaning against a stone balcony railing of the Astronomy Tower, face turned slightly toward camera showing peaceful contemplative expression illuminated by soft silver moonlight. Midnight the sleek black cat with glowing yellow eyes and silver collar sits beside them, both gazing at the spectacular twin moons rising over the castle. Child's face shows wonder and contentment, detailed features visible in the beautiful moonlight. Village lights twinkle far below. Dark blue starry sky with magical auroras. Warm golden light from tower windows behind. Intimate portrait composition, child's serene face clearly visible and detailed. Dreamy magical atmosphere.""",
            story_text="As the twin moons rose, the castle quieted down. Standing on the balcony of the Astronomy Tower, looking out over the glittering lights of the village, everything felt magical. Midnight purred contentedly, a faithful companion in this new adventure.",
            costume="wearing elegant formal wizard robes"
        ),

        # PAGE 10 (Scene 5 - Right Panel)
        PageTemplate(
            page_number=10,
            scene_description="Finding home at magic school",
            scene_type="peaceful",
            realistic_prompt="""Perfect storybook ending. The child named {name} in elegant formal wizard robes sitting on the edge of the Astronomy Tower balcony, Midnight the black cat curled up in their lap. Child's face turned toward camera with warm peaceful smile, soft moonlight beautifully illuminating their happy expression while preserving natural skin tone and ethnic features. Giant twin moons glow warmly in the starry night sky. Village lights twinkle like stars far below. Child gently petting the purring cat, expression of belonging and joy. Magical atmosphere with subtle sparkles in the air. Portrait composition with child's content smiling face clearly visible and detailed. CRITICAL: Moonlight should create gentle highlights and depth without desaturating, cooling, or lightening the child's natural warm skin tone - maintain authentic complexion in nighttime lighting. Warm, safe, hopeful feeling of finding home.""",
            story_text="This wasn't just a school; it was home. With Midnight by their side and a world of magic to explore, {name} smiled and whispered, 'I'm ready for tomorrow.' The moon smiled back, casting silver light on a perfect first day.",
            costume="wearing elegant formal wizard robes"
        )
    ]
)