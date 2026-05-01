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
            realistic_prompt="""MAGICAL MAP DISCOVERY SCENE in sunny bedroom. Wide environmental composition: Toys scattered across wooden floor, colorful building blocks and stuffed animals creating a lived-in space. Warm golden morning sunlight streaming through large window, casting soft shadows and creating bright illuminated patches on the floor. Large colorful hand-drawn treasure map spread open on a soft patterned rug, showing winding forest paths and mysterious markings. The child named {name} sitting cross-legged on the rug, both hands holding the map edges, leaning forward with pure excitement as they discover the adventure ahead. Teddy bear sitting nearby watching. Child's expression of wonder clearly visible in the warm window light. Dreamy morning atmosphere emphasizing the magic of discovery. The child is wearing comfortable indoor clothes. A small excited comic-style speech bubble near the child containing EXACTLY the text "Look what I found!", subtle and not covering the face.""",
            story_text="The morning sunshine danced through the bedroom window as {name} discovered something amazing hidden under a fuzzy rug. 'Look!' {name} shouted with excitement, 'An adventure is waiting!'",
            costume="wearing comfortable indoor clothes"
        ),

        # PAGE 2 (Scene 1 - Right Panel)
        PageTemplate(
            page_number=2,
            scene_description="Examining the magical map",
            scene_type="discovery",
            realistic_prompt="""CLOSE EXAMINATION OF TREASURE MAP in bright bedroom setting. Dynamic scene composition: Large colorful hand-drawn map held at chest level, detailed illustrations visible showing winding forest path through green trees, a purple singing stream with musical notes, soft pillow-shaped mountains in pink and purple, and a bold red 'X' marking the treasure location. The child named {name} studying the map intently, one finger pointing to trace the winding path, other hand holding the map edge. Natural engaged pose showing concentration and curiosity. Warm window light illuminating the map details and creating bright highlights. Bedroom details visible in background - toy shelf, adventure posters on wall, globe. Child's expression of intense curiosity and excitement visible as they discover the route. Wonder-filled moment of planning an adventure. The child is wearing comfortable indoor clothes. A small curious comic-style speech bubble near the child containing EXACTLY the text "What's at the X?", subtle and not covering the face.""",
            story_text="The map was unlike anything {name} had ever seen before. It showed a winding path through an enchanted forest, a purple singing stream, and mountains that looked like soft pillows. There was even an 'X' marking the treasure spot!",
            costume="wearing comfortable indoor clothes"
        ),

        # === SCENE 2 - THE SILVER TRAIL ===

        # PAGE 3 (Scene 2 - Left Panel)
        PageTemplate(
            page_number=3,
            scene_description="Entering the magical forest",
            scene_type="journey",
            realistic_prompt="""ENCHANTED FOREST ENTRANCE with wide environmental composition. Majestic ancient trees with enormous trunks frame the scene, their branches forming a natural archway overhead. Heart-shaped leaves in vibrant greens shimmer with magical sparkles, catching the dappled sunlight filtering through the dense canopy. A shimmering silver dust trail winds through the emerald grass, glowing softly and leading deeper into the mystical woods. Magical particles float in the air like fairy dust. The child named {name} walking along the glowing path, taking in the breathtaking magical surroundings with natural wonder. Soft rays of golden sunlight break through the leaves, creating dramatic light beams in the forest mist. Ferns and wildflowers line the path. Dreamy fairytale atmosphere emphasizing the transition from ordinary world to magical realm. Child's expression of amazement visible as they step into this enchanted world. The child is wearing comfortable outdoor clothes. A small soft comic-style speech bubble near the child containing EXACTLY the text "It's like a dream…", subtle and not covering the face.""",
            story_text="Stepping into the enchanted forest felt like entering a dream. Giant trees with heart-shaped leaves sparkled in the sunlight, and a shimmering silver trail of magical dust wound through the emerald grass. 'So shiny!' {name} whispered in wonder.",
            costume="wearing comfortable outdoor clothes"
        ),

        # PAGE 4 (Scene 2 - Right Panel)
        PageTemplate(
            page_number=4,
            scene_description="Meeting Pip the squirrel",
            scene_type="encounter",
            realistic_prompt="""MAGICAL FIRST ENCOUNTER SCENE in enchanted forest clearing. Wide dynamic composition: Moss-covered fallen log in dappled forest sunlight, surrounded by ferns and small wildflowers. Pip - an adorable brown squirrel with an exceptionally fluffy tail and bright expressive eyes - standing upright on the log, one tiny paw raised in a friendly wave, the other paw gesturing forward along the silver trail. Magical fireflies dancing in the air around the scene, their soft golden light creating a warm glow. The child named {name} stopping on the forest path, body language showing delighted surprise at discovering a talking forest friend. Natural interaction moment capturing the wonder of finding magic in the ordinary. Warm afternoon forest light filtering through leaves creates a cozy, welcoming atmosphere. Child's expression of joyful amazement visible as they connect with their new guide. The child is wearing comfortable outdoor clothes. A small surprised comic-style speech bubble near the child containing EXACTLY the text "You can talk?", subtle and not covering the face.""",
            story_text="Suddenly, a friendly brown squirrel hopped down from a nearby tree. 'Hello there!' squeaked Pip, waving a tiny paw. 'I'm Pip! Follow the silver trail, {name}, and I'll show you the way to the most magical places in the forest!'",
            costume="wearing comfortable outdoor clothes"
        ),

        # === SCENE 3 - THE SINGING STREAM ===

        # PAGE 5 (Scene 3 - Left Panel)
        PageTemplate(
            page_number=5,
            scene_description="Crossing the singing stream",
            scene_type="challenge",
            realistic_prompt="""DYNAMIC STREAM-CROSSING ACTION SCENE with wide environmental composition. Crystal-clear singing stream flowing through enchanted forest, water sparkling with magical blue light and creating gentle musical ripples. Perfectly spaced round purple stepping stones create a whimsical path across the water, each stone glowing softly with inner light. Magical musical notes and clef symbols float in the air above the water's surface, visualizing the stream's melody. The child named {name} captured mid-leap between stones, arms spread for balance, one foot leaving a stone while the other reaches for the next. Dynamic jumping pose showing playful adventure and confident movement. Forest canopy overhead filters golden sunlight, creating dramatic light beams that illuminate the magical water and the leaping child. Moss-covered rocks and ferns line the banks. Joyful moment of play and exploration. Child's expression of delighted concentration visible as they hop across. The child is wearing comfortable outdoor clothes. A small playful comic-style speech bubble near the child containing EXACTLY the text "Boing!", subtle and not covering the face.""",
            story_text="The silver trail led to the most amazing discovery yet - the Singing Stream! The crystal-clear water bubbled and gurgled in perfect harmony, and purple stepping stones created a path across. 'Hop! Hop!' laughed {name}, dancing from stone to stone.",
            costume="wearing comfortable outdoor clothes"
        ),

        # PAGE 6 (Scene 3 - Right Panel)
        PageTemplate(
            page_number=6,
            scene_description="The magical musical water",
            scene_type="wonder",
            realistic_prompt="""MAGICAL MUSICAL STREAM SCENE with wide environmental storytelling. Wide environmental composition: Enchanted stream flowing gently through forest glade, water glowing with soft purple and blue magical light. Intricate musical patterns form in the ripples - treble clefs, quarter notes, and musical staffs swirl in the water and rise into the air like ethereal sheet music. Purple stepping stones visible in the stream, creating a natural bridge. The child named {name} walking along the mossy bank beside the singing water, one foot forward in mid-step, natural walking pose showing engagement with the magical environment. Forest canopy creates a natural frame overhead, golden sunlight filtering through leaves in dramatic beams. Ferns and glowing mushrooms line the bank. Magical atmosphere emphasizing the wonder of nature's music. Dreamlike lighting highlighting the stream's magical properties. Child's expression of wonder and delight visible as they walk beside this enchanted water. The child is wearing comfortable outdoor clothes.""",
            story_text="Each time {name} stepped on a stone, the water sang a different note! The ripples formed magical musical symbols that danced across the surface, creating the most beautiful melody the forest had ever heard.",
            costume="wearing comfortable outdoor clothes"
        ),

        # === SCENE 4 - THE WHISPERING MOUNTAINS ===

        # PAGE 7 (Scene 4 - Left Panel)
        PageTemplate(
            page_number=7,
            scene_description="Discovering the pillow mountains",
            scene_type="awe",
            realistic_prompt="""EPIC LANDSCAPE VISTA DISCOVERY with wide cinematic composition. Breathtaking view: In the distance, extraordinary mountains made entirely of enormous soft pillows in purple, pink, and lavender velvet, stacked impossibly high against the sky. Each pillow mountain catches the light differently, creating depth and texture. Cheerful sun with a gentle smile beams down from bright blue sky, casting warm golden light across the fantastical landscape. Rolling meadows of emerald grass lead to the mountains. The child named {name} standing at the edge of the meadow, body language showing complete awe and wonder, looking up at the impossible magical sight. Small wildflowers dot the grass around them. Whimsical dreamy atmosphere blending reality and imagination. Clouds drift lazily. Magical particles shimmer in the air. Sense of discovery and amazement permeates the scene as the child encounters this surreal wonder. The child is wearing comfortable outdoor clothes.""",
            story_text="Beyond the stream rose the most incredible sight - the Whispering Mountains! But these weren't ordinary mountains made of rock and stone. They were enormous, fluffy pillows of purple and pink velvet that reached toward the smiling sun. 'Giant pillows!' gasped {name}.",
            costume="wearing comfortable outdoor clothes"
        ),

        # PAGE 8 (Scene 4 - Right Panel)
        PageTemplate(
            page_number=8,
            scene_description="Climbing the soft mountains",
            scene_type="adventure",
            realistic_prompt="""WHIMSICAL PILLOW MOUNTAIN CLIMBING SCENE with dynamic environmental composition. Wide scene: Enormous soft slope made of purple and pink velvet pillow fabric, quilted texture creating natural handholds and footholds. The child named {name} climbing upward with playful determination, arms and legs positioned naturally for climbing, body angled against the soft slope. White feathers float through the air like gentle snow, creating dreamy atmosphere. Magical sparkles drift lazily around. Soft pastel light from above illuminates the surreal landscape. More pillow mountains visible in the background, creating fantastical terrain. Clouds pass nearby at mountain height. The slope's quilted pattern creates interesting shadows and depth. Impossible physics made possible through magic - the soft surface somehow supports weight while remaining pillowy. Joyful moment of playful adventure and wonder. Child's expression of pure delight and laughter visible as they climb this impossible terrain. The child is wearing comfortable outdoor clothes. A small joyful comic-style speech bubble near the child containing EXACTLY the text "It's so soft!", subtle and not covering the face.""",
            story_text="Climbing the pillow mountains was like bouncing on the world's softest, most magical bed. With each step, feathers danced through the air like gentle snowflakes, and the whole mountainside whispered secrets of ancient adventures.",
            costume="wearing comfortable outdoor clothes"
        ),

        # === SCENE 5 - THE SUMMIT VIEW ===

        # PAGE 9 (Scene 5 - Left Panel)
        PageTemplate(
            page_number=9,
            scene_description="Reaching the summit",
            scene_type="triumph",
            realistic_prompt="""BREATHTAKING SUMMIT VISTA MOMENT with wide cinematic environmental composition. Expansive scene: Soft grassy mountain peak overlooking an endless magical landscape. Panoramic view spreads below - the sparkling enchanted forest with heart-shaped leaves, the winding musical stream catching sunlight, soft valleys dotted with wonder. Golden sunset paints the sky in oranges, pinks, and purples, casting warm light across the entire vista. Long shadows stretch across the landscape. The child named {name} sitting on the grassy peak in comfortable outdoor adventurer clothes, taking in the spectacular view with wonder. Pip the adorable squirrel with exceptionally fluffy tail perched on child's shoulder, both companions sharing this triumphant moment. Gentle breeze moves the grass. Soft magical sparkles drift in the air. Clouds drift below the peak. Sense of peaceful achievement and awe at the beauty of the magical world. Dreamy fairytale atmosphere celebrating adventure and friendship. Child's expression of pure wonder and joy visible as they share this moment with their faithful companion. A small soft comic-style speech bubble near the child containing EXACTLY the text "Best adventure ever", subtle and not covering the face.""",
            story_text="At the summit, the view was breathtaking. The entire enchanted world spread out below like a living fairytale - the sparkling forest, the musical stream, and valleys filled with wonder. 'Best adventure ever,' whispered {name}, sitting beside faithful Pip.",
            costume="wearing comfortable outdoor adventurer clothes"
        ),

        # PAGE 10 (Scene 5 - Right Panel)
        PageTemplate(
            page_number=10,
            scene_description="A magical friendship",
            scene_type="bonding",
            face_expression="warm joyful smile, eyes soft and bright with happiness, radiant contentment",
            realistic_prompt="""HEARTWARMING FRIENDSHIP MOMENT with environmental storytelling composition. Magical sunset scene on the mountain peak: Sky painted in brilliant golds, soft pinks, and warm oranges as the sun sets over the enchanted landscape. Soft magical sparkles drift through the air, catching the sunset light. The child named {name} holding Pip the squirrel gently at chest level, cradling their small friend with care. Pip's fluffy tail wrapped around the child's arm affectionately. Warm golden sunset light illuminates the scene from the side, creating a beautiful glow. Mountain peak grass sways in gentle evening breeze. Distant forest visible below, glowing in sunset light. Sense of warmth, friendship, and contentment permeates the scene. Natural moment of connection between adventurer and guide, celebrating a successful journey together. Peaceful ending to a magical day. Child's expression of pure happiness and joy visible as they share this tender farewell with their forest friend. The child is wearing comfortable outdoor clothes.""",
            story_text="As the golden sun painted the sky in magical colors, {name} knew this was just the beginning of many adventures to come. With a gentle hug, Pip whispered, 'See you next time, brave explorer!' And {name} smiled, knowing the enchanted forest would always be there, waiting for the next magical journey.",
            costume="wearing comfortable outdoor clothes"
        ),
    ]
)