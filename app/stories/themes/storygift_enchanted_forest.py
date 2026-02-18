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
            realistic_prompt="""Warm indoor discovery scene. A sunny bedroom with toys scattered on the floor. The child named {name} sitting on a soft rug holding a large colorful map open, face lit with excited wonder. Sunlight streaming through window illuminating child's amazed expression. A teddy bear nearby. Child's excited face clearly visible and detailed, showing the thrill of discovery. The child is wearing comfortable indoor clothes.""",
            story_text="The morning sunshine danced through the bedroom window as {name} discovered something amazing hidden under a fuzzy rug. 'Look!' {name} shouted with excitement, 'An adventure is waiting!'",
            costume="wearing comfortable indoor clothes"
        ),

        # PAGE 2 (Scene 1 - Right Panel)
        PageTemplate(
            page_number=2,
            scene_description="Examining the magical map",
            scene_type="discovery",
            realistic_prompt="""Close up detail shot. The magical map showing a winding path through a forest, a purple stream, and pillow mountains with an 'X' mark. The child named {name} pointing at the treasure spot, face showing intense curiosity and excitement about the adventure ahead. Map looks hand-drawn and magical. Child's eager focused face clearly visible and detailed. The child is wearing comfortable indoor clothes.""",
            story_text="The map was unlike anything {name} had ever seen before. It showed a winding path through an enchanted forest, a purple singing stream, and mountains that looked like soft pillows. There was even an 'X' marking the treasure spot!",
            costume="wearing comfortable indoor clothes"
        ),

        # === SCENE 2 - THE SILVER TRAIL ===

        # PAGE 3 (Scene 2 - Left Panel)
        PageTemplate(
            page_number=3,
            scene_description="Entering the magical forest",
            scene_type="journey",
            realistic_prompt="""Magical forest entrance. Giant trees with heart-shaped sparkling leaves. A glowing silver dust trail winding through the grass. The child named {name} walking along the path, face showing pure amazement at the magical surroundings. Dappled sunlight creating beautiful atmosphere. Child's wonder-filled face clearly visible and detailed. The child is wearing comfortable outdoor clothes.""",
            story_text="Stepping into the enchanted forest felt like entering a dream. Giant trees with heart-shaped leaves sparkled in the sunlight, and a shimmering silver trail of magical dust wound through the emerald grass. 'So shiny!' {name} whispered in wonder.",
            costume="wearing comfortable outdoor clothes"
        ),

        # PAGE 4 (Scene 2 - Right Panel)
        PageTemplate(
            page_number=4,
            scene_description="Meeting Pip the squirrel",
            scene_type="encounter",
            realistic_prompt="""Heartwarming encounter scene. Pip - a cute brown squirrel with a fluffy tail - standing on a log gesturing forward with tiny paws. The child named {name} looking at the squirrel with a warm delighted smile, face lit by dancing fireflies around them. Child's happy smiling face clearly visible and detailed, showing joy at meeting new friend. The child is wearing comfortable outdoor clothes.""",
            story_text="Suddenly, a friendly brown squirrel hopped down from a nearby tree. 'Hello there!' squeaked Pip, waving a tiny paw. 'I'm Pip! Follow the silver trail, {name}, and I'll show you the way to the most magical places in the forest!'",
            costume="wearing comfortable outdoor clothes"
        ),

        # === SCENE 3 - THE SINGING STREAM ===

        # PAGE 5 (Scene 3 - Left Panel)
        PageTemplate(
            page_number=5,
            scene_description="Crossing the singing stream",
            scene_type="challenge",
            realistic_prompt="""Action adventure shot. A beautiful blue singing stream flowing through woods with purple round stepping stones perfectly spaced. The child named {name} carefully stepping from one stone to another, face showing concentration and playful joy. Musical notes floating in the air above the magical water. Child's joyful focused face clearly visible and detailed. The child is wearing comfortable outdoor clothes.""",
            story_text="The silver trail led to the most amazing discovery yet - the Singing Stream! The crystal-clear water bubbled and gurgled in perfect harmony, and purple stepping stones created a path across. 'Hop! Hop!' laughed {name}, dancing from stone to stone.",
            costume="wearing comfortable outdoor clothes"
        ),

        # PAGE 6 (Scene 3 - Right Panel)
        PageTemplate(
            page_number=6,
            scene_description="The magical musical water",
            scene_type="wonder",
            realistic_prompt="""Magical moment close-up. The child named {name} balanced on a purple stone, face looking down at the water with wonder and delight as ripples form musical clefs and notes. Water glowing softly with magical light. Musical sparkles dancing in the air. Child's amazed face reflected in the magical water, expression clearly visible and detailed. The child is wearing comfortable outdoor clothes.""",
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
            realistic_prompt="""Whimsical climbing scene. The child named {name} climbing up a soft slope that looks like a giant duvet, face showing pure delight and laughter. Feathers floating around like soft snow. Pastel dreamy lighting with magical sparkles. Child's joyful laughing face clearly visible and detailed, showing the fun of this magical adventure. The child is wearing comfortable outdoor clothes.""",
            story_text="Climbing the pillow mountains was like bouncing on the world's softest, most magical bed. With each step, feathers danced through the air like gentle snowflakes, and the whole mountainside whispered secrets of ancient adventures.",
            costume="wearing comfortable outdoor clothes"
        ),

        # === SCENE 5 - THE SUMMIT VIEW ===

        # PAGE 9 (Scene 5 - Left Panel)
        PageTemplate(
            page_number=9,
            scene_description="Reaching the summit",
            scene_type="triumph",
            realistic_prompt="""Breathtaking summit moment. The child named {name} in comfortable outdoor adventurer clothes sitting on the soft grassy peak, face turned toward camera with expression of pure wonder and joy, golden sunset light beautifully illuminating their happy features. Pip the adorable squirrel with fluffy tail perched on child's shoulder, both gazing at the spectacular view. Panoramic magical landscape spreads below - the sparkling enchanted forest, the musical flowing stream, and soft valleys filled with wonder. Warm golden sunset casting long shadows. Child's face detailed and clear, showing peaceful triumph and amazement. Dreamy fairytale atmosphere with soft magical sparkles in the air. Portrait composition ensuring child's delighted face is clearly visible.""",
            story_text="At the summit, the view was breathtaking. The entire enchanted world spread out below like a living fairytale - the sparkling forest, the musical stream, and valleys filled with wonder. 'Best adventure ever,' whispered {name}, sitting beside faithful Pip.",
            costume="wearing comfortable outdoor adventurer clothes"
        ),

        # PAGE 10 (Scene 5 - Right Panel)
        PageTemplate(
            page_number=10,
            scene_description="A magical friendship",
            scene_type="sleeping",
            realistic_prompt="""Close up portrait. The child named {name} is smiling with eyes closed, gently hugging Pip the squirrel with a fluffy tail. Soft magical sparkles surround them in the golden sunset light. A feeling of warmth, friendship, and happiness fills the scene. The child is wearing comfortable outdoor clothes.""",
            story_text="As the golden sun painted the sky in magical colors, {name} knew this was just the beginning of many adventures to come. With a gentle hug, Pip whispered, 'See you next time, brave explorer!' And {name} smiled, knowing the enchanted forest would always be there, waiting for the next magical journey.",
            costume="wearing comfortable outdoor clothes"
        ),
    ]
)