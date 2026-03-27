"""
StoryGift Enchanted Forest Theme - Converted to Magictales format.

Complete 10-page story: "The Enchanted Forest"
Converted from StoryGift's 5 scenes × 2 panels structure
Preserves all original prompts, dialogue, and story narrative
"""

from app.stories.templates import StoryTemplate, PageTemplate


STORYGIFT_ENCHANTED_FOREST_THEME = StoryTemplate(
    theme_id="storygift_enchanted_forest",
    title_template="{name} and the Enchanted Forest",
    cover_display_title="The Enchanted Forest",
    description="A magical journey through whispering woods and singing streams",
    default_costume="wearing comfortable outdoor clothes",
    protagonist_description="bright curious eyes, sense of wonder and adventure",
    # Cover page settings for typography-ready composition
    cover_costume="wearing an elegant forest adventurer outfit with a flowing green cape, leather satchel, and nature-inspired accessories",
    cover_header_atmosphere="Mystical enchanted forest canopy with ancient towering trees, soft golden sunlight filtering through leaves, magical mist and ethereal glow",
    cover_magical_elements="Glowing fireflies, floating leaves, and gentle magical sparkles dance around the child's body (not face). A friendly deer watches from the shadows. Waterfalls shimmer in the background.",
    cover_footer_description="Mossy forest floor with wildflowers, a winding magical path, and soft ferns",
    pages=[
        # === SCENE 1 - THE SECRET MAP ===

        # PAGE 1 (Scene 1 - Left Panel)
        PageTemplate(
            page_number=1,
            scene_description="Finding the secret map",
            scene_type="discovery",
            realistic_prompt="""Warm indoor discovery scene. A sunny bedroom with toys scattered on the floor. The child named {name} sitting on a soft rug holding a large colorful map open, face lit with excited wonder. Sunlight streaming through window illuminating child's amazed expression. A teddy bear nearby. Child's excited face clearly visible and detailed, showing the thrill of discovery. The child is wearing comfortable indoor clothes. A small excited comic-style speech bubble near the child saying "Look what I found!", subtle and not covering the face.""",
            story_text="The morning sunshine danced through the bedroom window as {name} discovered something amazing hidden under a fuzzy rug. 'Look!' {name} shouted with excitement, 'An adventure is waiting!'",
            costume="wearing comfortable indoor clothes"
        ),

        # PAGE 2 (Scene 1 - Right Panel)
        PageTemplate(
            page_number=2,
            scene_description="Examining the magical map",
            scene_type="discovery",
            realistic_prompt="""Magical map discovery scene. The child named {name} holding the colorful hand-drawn map at chest height, head upright and face naturally forward-facing, eyes glancing down at the map with intense curiosity and excitement — head stays mostly upright so face is prominent and clearly visible, only the eyes directed at the treasure spot being pointed at. The map shows a winding path through a forest, a purple stream, pillow mountains and an 'X' mark. Child's eager expression clearly visible and detailed, face well-lit by window light. The child is wearing comfortable indoor clothes. A small curious comic-style speech bubble near the child saying "What’s at the X?", subtle and not covering the face.""",
            story_text="The map was unlike anything {name} had ever seen before. It showed a winding path through an enchanted forest, a purple singing stream, and mountains that looked like soft pillows. There was even an 'X' marking the treasure spot!",
            costume="wearing comfortable indoor clothes"
        ),

        # === SCENE 2 - THE SILVER TRAIL ===

        # PAGE 3 (Scene 2 - Left Panel)
        PageTemplate(
            page_number=3,
            scene_description="Entering the magical forest",
            scene_type="journey",
            realistic_prompt="""Magical forest entrance. Giant trees with heart-shaped sparkling leaves surround a glowing silver dust trail winding through the emerald grass. The child named {name} walking along the path in three-quarter view, face naturally forward-facing and prominent — head gently angled as eyes take in the magical surroundings ahead and to the sides, not a side profile walking shot. Dappled sunlight filtering through the canopy from above illuminates the child's face naturally. Child's wonder-filled expression clearly visible and detailed, face the focal point of the composition. The child is wearing comfortable outdoor clothes. A small soft comic-style speech bubble near the child saying "It’s like a dream…", subtle and not covering the face.""",
            story_text="Stepping into the enchanted forest felt like entering a dream. Giant trees with heart-shaped leaves sparkled in the sunlight, and a shimmering silver trail of magical dust wound through the emerald grass. 'So shiny!' {name} whispered in wonder.",
            costume="wearing comfortable outdoor clothes"
        ),

        # PAGE 4 (Scene 2 - Right Panel)
        PageTemplate(
            page_number=4,
            scene_description="Meeting Pip the squirrel",
            scene_type="encounter",
            realistic_prompt="""Heartwarming encounter scene. Pip - a cute brown squirrel with a fluffy tail - standing on a log gesturing forward with tiny paws. The child named {name} looking at the squirrel with a warm delighted smile, face lit by dancing fireflies around them. Child's happy smiling face clearly visible and detailed, showing joy at meeting new friend. The child is wearing comfortable outdoor clothes. A small surprised comic-style speech bubble near the child saying "You can talk?", subtle and not covering the face.""",
            story_text="Suddenly, a friendly brown squirrel hopped down from a nearby tree. 'Hello there!' squeaked Pip, waving a tiny paw. 'I'm Pip! Follow the silver trail, {name}, and I'll show you the way to the most magical places in the forest!'",
            costume="wearing comfortable outdoor clothes"
        ),

        # === SCENE 3 - THE SINGING STREAM ===

        # PAGE 5 (Scene 3 - Left Panel)
        PageTemplate(
            page_number=5,
            scene_description="Crossing the singing stream",
            scene_type="challenge",
            realistic_prompt="""Action adventure shot. A beautiful blue singing stream flowing through woods with purple round stepping stones perfectly spaced. The child named {name} mid-hop between stones, face naturally forward-facing and prominent — head upright, eyes glancing briefly down at the next stone with playful concentration, only a gentle downward eye movement rather than a steep head drop. Child caught in a joyful moment of leaping, expression of playful joy and focus clearly visible and detailed. Musical notes floating in the air above the magical water. Sunlight from above illuminates the child's face naturally. Child's face is the clear focal point. The child is wearing comfortable outdoor clothes. A small playful comic-style speech bubble near the child saying "Boing!", subtle and not covering the face.""",
            story_text="The silver trail led to the most amazing discovery yet - the Singing Stream! The crystal-clear water bubbled and gurgled in perfect harmony, and purple stepping stones created a path across. 'Hop! Hop!' laughed {name}, dancing from stone to stone.",
            costume="wearing comfortable outdoor clothes"
        ),

        # PAGE 6 (Scene 3 - Right Panel)
        PageTemplate(
            page_number=6,
            scene_description="The magical musical water",
            scene_type="wonder",
            realistic_prompt="""Enchanted forest stream scene. The child named {name} walking along the bank of the singing stream in three-quarter view, one foot stepping forward onto the mossy path beside the glowing purple water. Face naturally forward-facing and prominent at a relaxed 3/4 angle — expression of wonder and delight as magical musical ripples swirl in the stream beside them. Water glowing softly with magical light, musical clef and note patterns forming in the ripples and floating upward into the air. The forest canopy frames the scene with dappled golden sunlight filtering through from above, illuminating the child's face naturally. Purple stones visible in the stream behind the walking child. Child's walking pose shows full body in the enchanted environment, face clearly visible and detailed as the focal point. The child is wearing comfortable outdoor clothes.""",
            story_text="Each time {name} stepped on a stone, the water sang a different note! The ripples formed magical musical symbols that danced across the surface, creating the most beautiful melody the forest had ever heard.",
            costume="wearing comfortable outdoor clothes"
        ),

        # === SCENE 4 - THE WHISPERING MOUNTAINS ===

        # PAGE 7 (Scene 4 - Left Panel)
        PageTemplate(
            page_number=7,
            scene_description="Discovering the pillow mountains",
            scene_type="awe",
            realistic_prompt="""Epic landscape discovery. In the distance, mountains made not of rock but giant soft purple and pink pillows. Sun smiling cheerfully in the sky. The child named {name} looking up at them in complete awe, mouth open in amazement. Magical dreamy atmosphere. Child's awestruck face clearly visible and detailed, showing wonder at the magical sight. The child is wearing comfortable outdoor clothes.""",
            story_text="Beyond the stream rose the most incredible sight - the Whispering Mountains! But these weren't ordinary mountains made of rock and stone. They were enormous, fluffy pillows of purple and pink velvet that reached toward the smiling sun. 'Giant pillows!' gasped {name}.",
            costume="wearing comfortable outdoor clothes"
        ),

        # PAGE 8 (Scene 4 - Right Panel)
        PageTemplate(
            page_number=8,
            scene_description="Climbing the soft mountains",
            scene_type="adventure",
            realistic_prompt="""Whimsical climbing scene. The child named {name} climbing up a soft slope that looks like a giant duvet — face naturally forward-facing and prominent, head upright as eyes glance upward toward the summit above with pure delight and laughter, not in side profile. Three-quarter view with face well-lit by the soft pastel dreamy light from above. Feathers floating around like soft snow. Magical sparkles in the air. Child's joyful laughing expression clearly visible and detailed, face the focal point of the composition. The child is wearing comfortable outdoor clothes. A small joyful comic-style speech bubble near the child saying "It’s so soft!", subtle and not covering the face.""",
            story_text="Climbing the pillow mountains was like bouncing on the world's softest, most magical bed. With each step, feathers danced through the air like gentle snowflakes, and the whole mountainside whispered secrets of ancient adventures.",
            costume="wearing comfortable outdoor clothes"
        ),

        # === SCENE 5 - THE SUMMIT VIEW ===

        # PAGE 9 (Scene 5 - Left Panel)
        PageTemplate(
            page_number=9,
            scene_description="Reaching the summit",
            scene_type="triumph",
            realistic_prompt="""Breathtaking summit moment. The child named {name} in comfortable outdoor adventurer clothes sitting on the soft grassy peak, face turned toward camera with expression of pure wonder and joy, golden sunset light beautifully illuminating their happy features. Pip the adorable squirrel with fluffy tail perched on child's shoulder, both gazing at the spectacular view. Panoramic magical landscape spreads below - the sparkling enchanted forest, the musical flowing stream, and soft valleys filled with wonder. Warm golden sunset casting long shadows. Child's face detailed and clear, showing peaceful triumph and amazement. Dreamy fairytale atmosphere with soft magical sparkles in the air. Portrait composition ensuring child's delighted face is clearly visible. A small soft comic-style speech bubble near the child saying "Best adventure ever", subtle and not covering the face.""",
            story_text="At the summit, the view was breathtaking. The entire enchanted world spread out below like a living fairytale - the sparkling forest, the musical stream, and valleys filled with wonder. 'Best adventure ever,' whispered {name}, sitting beside faithful Pip.",
            costume="wearing comfortable outdoor adventurer clothes"
        ),

        # PAGE 10 (Scene 5 - Right Panel)
        PageTemplate(
            page_number=10,
            scene_description="A magical friendship",
            scene_type="bonding",
            face_expression="warm joyful smile, eyes soft and bright with happiness, radiant contentment",
            realistic_prompt="""Close up portrait. The child named {name} holding Pip the squirrel gently at chest level — face naturally forward-facing, eyes soft and warm with a beaming joyful smile, radiating happiness and contentment. Face fully unobstructed, Pip held at chest height not pressed against the face. Warm golden sunset light illuminating the child's face naturally from the side-front, skin tone preserved beautifully. Soft magical sparkles surrounding them. A feeling of warmth, friendship, and happiness fills the scene. Child's joyful expression is the clear emotional focal point. The child is wearing comfortable outdoor clothes.""",
            story_text="As the golden sun painted the sky in magical colors, {name} knew this was just the beginning of many adventures to come. With a gentle hug, Pip whispered, 'See you next time, brave explorer!' And {name} smiled, knowing the enchanted forest would always be there, waiting for the next magical journey.",
            costume="wearing comfortable outdoor clothes"
        ),
    ]
)