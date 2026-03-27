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
    cover_display_title="First Day of Magic School",
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
            realistic_prompt="""Dramatic arrival scene. The child wizard named {name} stands prominently in the foreground, face turned naturally toward camera at a relaxed 3/4 angle — expression of awe and nervous excitement, eyes wide, taking in the enormity of the moment. The massive gothic castle gate made of dark iron rises impressively behind and above the child, castle towers disappearing into the mist. Professor Hoot — a giant brown wise owl wearing large round reading glasses and a small black graduation cap — sits on a high stone pedestal to the side. Child's face is the clear PRIMARY FOCAL POINT, well-lit by warm golden morning rays breaking through mist. Child large and clearly detailed in frame, face prominently visible. The child is wearing elegant wizard robes.""",
            story_text="The morning mist clung to the cobblestones as the Grand Academy of Arcane Arts finally came into view. Standing before the massive iron gates was the school's oldest guardian. Professor Hoot was not merely an owl; he was a giant, ancient sentinel wearing thick spectacles.",
            costume="wearing wizard robes",
            face_expression="wide-eyed awe and nervous excitement, eyebrows slightly raised, mouth slightly open in wonder"
        ),

        # PAGE 2 (Scene 1 - Right Panel)
        PageTemplate(
            page_number=2,
            scene_description="Casting the unlock spell",
            scene_type="arrival",
            realistic_prompt="""Magical spell-casting moment. Close-up of the child wizard named {name} with wand extended toward camera, brilliant golden magic sparks erupting from wand tip. Child's face lit dramatically by the magical glow, expression showing fierce concentration and determination. Professor Hoot (giant wise owl with glasses and graduation cap) visible in soft focus background, watching approvingly. The ancient iron gate lock glowing with magical energy. Child positioned at three-quarter angle, face prominently visible and detailed, eyes focused with magical power. Dramatic cinematic lighting from the spell. The child is wearing elegant wizard robes. A small bold comic-style speech bubble near the child saying "Alohomora!", subtle and not covering the face.""",
            story_text="He adjusted his glasses with a wing tip and peered down. The test had begun before the first step was even taken. 'Only the worthy may pass,' hooted Professor Hoot as {name} shouted 'ALOHOMORA!' and magic sparks illuminated the ancient lock.",
            costume="wearing wizard robes",
            face_expression="fierce concentration and determination, eyes focused with intensity, jaw set with resolve"
        ),

        # === SCENE 2 - BEAST TAMING CLASS ===

        # PAGE 3 (Scene 2 - Left Panel)
        PageTemplate(
            page_number=3,
            scene_description="Beast Taming class begins",
            scene_type="action",
            realistic_prompt="""Dramatic courtyard scene. The child wizard named {name} standing confidently in the foreground, facing DIRECTLY toward the camera with a clear front-facing view. Expression of nervous anticipation and curiosity, wand raised at their side. Child's face is the clear PRIMARY FOCAL POINT — large, well-lit, and fully unobstructed. Behind the child in the FAR BACKGROUND: a mysterious reinforced wooden crate shaking violently with purple smoke leaking from cracks, other students backing away. The purple smoke stays in the far background, well away from the child. Stone castle walls framing the scene. Child positioned prominently in center frame, face large and clearly detailed. The child is wearing wizard robes.""",
            story_text="The courtyard was buzzing as the Beast Taming class began. In the center sat a wooden crate that shook violently. Purple smoke leaked from every crack as students backed away nervously. 'It's gonna blow!' someone shouted.",
            costume="wearing wizard robes",
            face_expression="nervous anticipation and cautious curiosity, slightly tensed expression, alert and watchful"
        ),

        # PAGE 4 (Scene 2 - Right Panel)
        PageTemplate(
            page_number=4,
            scene_description="Meeting Sparky the dragon",
            scene_type="bonding",
            realistic_prompt="""Heartwarming bonding scene in stone courtyard. The child named {name} standing upright and facing DIRECTLY toward the camera with a warm gentle smile showing compassion and wonder. Sparky (tiny adorable baby dragon, red with orange wings) perched on the child's shoulder, nuzzling against their neck — the dragon is small and to the SIDE, not blocking the child's face at all. Child's face is the clear PRIMARY FOCAL POINT — large, centered, and fully visible, well-lit by warm afternoon sunlight from the front-side. Castle walls and the open wooden crate visible in the background. Child's gentle smiling face clearly visible and detailed. The child is wearing wizard robes. A small gentle comic-style speech bubble near the child saying "You’re not scary…", subtle and not covering the face.""",
            story_text="With a pop, the lid flew open, revealing Sparky—a baby dragon with the hiccups. Every time he hiccuped, a smoke ring puffed from his nose. He wasn't scary; he was just hungry. '{name} offered a treat, realizing 'You're just hungry, aren't you?'",
            costume="wearing wizard robes",
            face_expression="gentle smile, warm compassion, wide-eyed wonder, affectionate"
        ),

        # === SCENE 3 - ADVANCED FLIGHT ===

        # PAGE 5 (Scene 3 - Left Panel)
        PageTemplate(
            page_number=5,
            scene_description="Learning to fly on broomstick",
            scene_type="action",
            realistic_prompt="""Magical first flight moment. The child named {name} sitting tall and upright on a wooden magical broomstick hovering just above the grass, face turned naturally toward camera at a relaxed 3/4 angle — expression of pure determination and thrilled excitement, chin raised confidently. One hand gripping the broom handle at their side, the other raised slightly in triumphant readiness. Robes and hair gently stirring from the magical levitation energy. Dust swirling softly around the broom beneath them. Child's face is the clear PRIMARY FOCAL POINT, well-lit by warm afternoon sunlight, face large and clearly detailed. School grounds and castle walls in background. Child sitting upright and proud — the pose of a natural flyer. The child is wearing wizard robes. A small confident comic-style speech bubble near the child saying "Up!", subtle and not covering the face.""",
            story_text="By afternoon, the winds picked up for Advanced Flight. The broomstick vibrated in hand, alive with enchantment. While others wobbled, a surge of confidence took hold. 'Time to fly!' {name} declared with determination.",
            costume="wearing wizard robes",
            face_expression="pure determination and thrilled excitement, confident grin, eyes bright with anticipation"
        ),

        # PAGE 6 (Scene 3 - Right Panel)
        PageTemplate(
            page_number=6,
            scene_description="Flying through the castle grounds",
            scene_type="flight",
            realistic_prompt="""Exhilarating flight scene. The child named {name} zooming through a stone ring high in the sky on a broomstick, face naturally forward-facing and prominent — head upright, eyes bright with exhilaration scanning the open sky ahead with pure freedom and joy, gaze engaged with the rushing wind and clouds rather than a stiff posed look. Wind rushing through hair, robes flowing dramatically behind. Castle grounds and clouds visible far below. Golden afternoon sunlight from the side illuminating the child's face warmly and naturally. Child's joyful triumphant expression clearly visible and detailed, face the clear focal point. The child is wearing wizard robes. A small excited comic-style speech bubble near the child saying "I did it!", subtle and not covering the face.""",
            story_text="With a command of 'UP!', the broom shot into the sky. The wind rushed past ears like a roaring river. The ground became a quilt of green and grey. 'I did it!' {name} shouted with pure exhilaration as they soared through stone rings in the sky.",
            costume="wearing wizard robes",
            face_expression="pure exhilaration and joy, windswept happiness, triumphant grin, eyes bright with freedom"
        ),

        # === SCENE 4 - THE ANCIENT LIBRARY ===

        # PAGE 7 (Scene 4 - Left Panel)
        PageTemplate(
            page_number=7,
            scene_description="Exploring the magical library",
            scene_type="mischief",
            realistic_prompt="""Intimate library exploration scene. The child named {name} sitting at an ancient wooden table in the magnificent library, face angled toward camera at three-quarter view, carefully opening a large dusty leather-bound book with golden magical symbols on its cover. Child's face illuminated by soft warm glow emanating from the book's pages (lighting enhances features without changing skin tone), expression showing wonder and mischievous curiosity. Midnight (a sleek black cat with glowing yellow eyes and silver collar) sitting beside them on the table watching intently. Towering magical bookshelves in background, sunbeams filtering through high windows catching dust motes like sparkles. CRITICAL: Maintain accurate skin tone despite magical glow - the golden light should add warmth and highlights without desaturating, lightening, or changing the child's natural complexion and ethnic features. Child's curious fascinated face clearly visible and detailed with authentic skin tone preserved, lit by the magical book's glow with all facial features fully visible. The child is wearing wizard robes. A small mischievous comic-style speech bubble near the child saying "Just one peek…", subtle and not covering the face.""",
            story_text="The Ancient Library was quiet until curiosity took over. Midnight, the library cat, dozed peacefully as {name} reached for an ancient tome. 'Just one peek...' they whispered, not knowing what magic would unfold.",
            costume="wearing wizard robes",
            face_expression="wide-eyed wonder and mischievous curiosity, soft conspiratorial smile, eyebrows raised with intrigue"
        ),

        # PAGE 8 (Scene 4 - Right Panel)
        PageTemplate(
            page_number=8,
            scene_description="Chaos in the magical library",
            scene_type="chaos",
            realistic_prompt="""Magical chaos scene in the library. The child named {name} standing near the table, facing DIRECTLY toward the camera with an expression of surprised delight, laughing joyfully with arms partially raised. Child's face is the clear PRIMARY FOCAL POINT — large, centered, and fully unobstructed, well-lit by warm candlelight from the side. In the BACKGROUND BEHIND the child: hundreds of books flying like a flock of birds across the high-ceilinged room. Midnight (a sleek black cat with glowing yellow eyes and silver collar) leaping mid-air to catch a book in the far background. All flying books stay BEHIND and to the SIDES of the child — nothing flies in front of or toward the child's face. The library chaos creates an exciting backdrop while the child's amused laughing face remains clearly visible and detailed in the foreground. The child is wearing wizard robes. A small playful comic-style speech bubble near the child saying "Okay… maybe more than one!", subtle and not covering the face.""",
            story_text="A sneeze disturbed the dust, and suddenly the books woke up! Leather-bound covers flapped like heavy wings in a paper storm. Midnight sprang into action, treating the flying literature like birds. 'MEOW! Got it!' seemed to say as {name} called 'Down boy!' It was chaos, but fun.",
            costume="wearing wizard robes",
            face_expression="surprised delight, playful alarm, laughing joyfully, amused and excited"
        ),

        # === SCENE 5 - PEACEFUL ENDING ===

        # PAGE 9 (Scene 5 - Left Panel)
        PageTemplate(
            page_number=9,
            scene_description="Peaceful moment on the tower balcony",
            scene_type="peaceful",
            realistic_prompt="""Magical peaceful night scene. The child named {name} in elegant formal wizard robes standing at the stone balcony railing of the Astronomy Tower, face turned naturally at a relaxed 3/4 angle — expression of peaceful wonder and contentment, soft gentle smile, eyes drifting gently toward the village lights and moons below rather than staring straight at camera. Midnight the sleek black cat with glowing yellow eyes and silver collar sitting beside them on the railing, both at ease. The spectacular twin moons rise large and luminous in the dark blue starry sky behind the child. Magical auroras shimmer in the sky behind them. Village lights twinkling far below. Warm golden light from tower windows to the side-front illuminates the child's face naturally — moonlight casting a beautiful soft silver rim glow from behind, outlining the hair and robes. Child's face is the clear PRIMARY FOCAL POINT, primarily lit by warm golden window light with skin tone fully preserved. Intimate portrait composition. Dreamy magical atmosphere. A small soft comic-style speech bubble near the child saying "It’s beautiful…", subtle and not covering the face.""",
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