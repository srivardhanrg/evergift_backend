"""
StoryGift Cosmic Dreamer Theme - Journey to the Stars.

Complete 10-page story: "[NAME]'s Cosmic Adventure"
Premium theme featuring a magical museum-to-space journey.
Scene-First composition emphasizing cosmic environments and adventure storytelling.

KEY PRINCIPLES:
- Wide environmental compositions showcasing space wonder
- Natural expressions (wonder, joy, peace)
- Helmet always off or visor up for face visibility
- Skin tone preservation in every scene
- Child integrated naturally into cosmic environments
- Gender-neutral language throughout
"""

from app.stories.templates import StoryTemplate, PageTemplate


STORYGIFT_COSMIC_DREAMER_THEME = StoryTemplate(
    theme_id="storygift_cosmic_dreamer",
    title_template="{name}'s Cosmic Adventure",
    cover_display_title="Cosmic Adventure",
    description="Watch your child reach for the stars on an epic space journey",
    default_costume="wearing a premium white and silver astronaut suit with gold star accents",
    protagonist_description="bright curious eyes, expression of gentle wonder",
    # Cover page settings - UNCHANGED (user said cover is perfect)
    cover_costume="wearing a premium white and silver NASA-style astronaut suit with gold visor reflecting stars and galaxies, heroic stance",
    cover_header_atmosphere="Deep space with vibrant purple and blue nebula clouds, twinkling stars, and a shooting star trail across the cosmic sky",
    cover_magical_elements="Glowing asteroid surface beneath feet, stardust particles floating around the body (not face). A distant Earth glows blue in the background. Golden rim lighting creates an epic silhouette.",
    cover_footer_description="Glowing asteroid surface with crystalline formations and cosmic dust",
    pages=[
# === PAGE 1 - THE SPACE MUSEUM ===
    PageTemplate(
        page_number=1,
        scene_description="Child at Space Museum looking up at rocket",
        scene_type="discovery",
        realistic_prompt="""GRAND SPACE MUSEUM DISCOVERY SCENE with wide environmental composition. Impressive museum hall with high vaulted ceilings, dramatic architectural features. Towering silver rocket display dominates the center, reaching toward the ceiling with gleaming metallic surfaces catching spotlights. Hanging planets and stars suspended from ceiling as decorations - Saturn with rings, colorful Jupiter, red Mars. Museum exhibits visible in background - moon rock displays, astronaut suits. The child named {name} in casual clothes standing in the foreground, looking up at the magnificent rocket with wonder and amazement, body language showing awe at the massive scale. Warm museum spotlights create dramatic lighting throughout the hall, illuminating the rocket and casting soft shadows. Professional museum atmosphere blending education and inspiration. Child's expression of longing and wonder clearly visible, face naturally lit by warm museum lighting. Child's natural skin tone preserved exactly as in reference photo regardless of scene lighting. A small gentle comic-style speech bubble near the child containing EXACTLY the text "I wish I could fly...", subtle and not covering the face.""",
        story_text="{name} had always dreamed of flying to the stars. At the Space Museum, standing before the most beautiful rocket, {name} looked up and whispered, 'I wish I could fly in a real rocket, just once.'",
        costume="wearing casual clothes"
    ),

        # === PAGE 2 - THE ROCKET AWAITS ===
        PageTemplate(
            page_number=2,
            scene_description="Child walks toward open spaceship door — camera inside the ship looking out",
            scene_type="wonder",
            realistic_prompt="""MAGICAL SPACESHIP DISCOVERY SCENE in moonlit field at night. Wide cinematic composition: Magnificent silver and gold spaceship resting in dewy grass field, sleek futuristic design with smooth curves and metallic surfaces reflecting moonlight. Open glowing doorway in the ship's side spills warm golden light across the grass, creating a welcoming path of illumination. Vast starry night sky stretches overhead, countless stars twinkling, Milky Way visible as soft band of light. Bright moon casts silver glow across the entire scene. The child named {name} in casual clothes walking through the moonlit grass toward the magical ship, drawn to the warm golden light of the open doorway. Natural walking pose showing excitement and wonder. The ship's warm interior light illuminates the child from ahead, creating beautiful front lighting on the face. Grass around feet sparkles with dew catching moonlight and ship glow. Sense of magical discovery and invitation to adventure. Dreamy cinematic atmosphere blending reality and fantasy. Child's expression of amazed joyful excitement clearly visible in the warm light. Child's natural skin tone preserved exactly as in reference photo. A small curious comic-style speech bubble near the child containing EXACTLY the text "Is this for me?", subtle and not covering the face.""",
            story_text="Then something magical happened! {name} found a real spaceship waiting in a moonlit field, its door glowing and open wide. A gentle voice whispered, 'We've been waiting for you, {name}. Are you ready for an adventure?'",
            costume="wearing casual clothes"
        ),

        # === PAGE 3 - TRANSFORMATION ===
        PageTemplate(
            page_number=3,
            scene_description="Transforming into a little astronaut",
            scene_type="preparation",
            realistic_prompt="""MAGICAL ASTRONAUT TRANSFORMATION SCENE in moonlit field. Wide environmental composition: Vast dramatic night sky dominates the upper portion - deep navy blue filled with thousands of brilliant twinkling stars, Milky Way band visible as soft cosmic glow, bright crescent moon casting silver light across the landscape. Silver-and-gold spaceship parked in the grassy field, its open doorway spilling warm golden light. Dewy grass sparkles with moonlight and ship glow, creating magical atmosphere. The child named {name} standing in the moonlit field next to the ship, wearing beautiful white astronaut suit with silver and gold star accents. Helmet held under one arm showing face clearly. Swirling golden stardust sparkles wrap around the child's body in spiraling ribbons as the suit finishes magically forming, particles of light dancing in the air. The suit glows softly with inner magical light. Natural confident pose showing excitement about the coming adventure. Moonlight from above and warm ship light from the side create beautiful illumination. Sense of wonder at the transformation and anticipation of space exploration. Premium cinematic quality capturing the moment before launch. Child's expression of confident excitement clearly visible, face well-lit by moonlight and ship's warm glow. Child's natural skin tone preserved exactly as in reference photo regardless of scene lighting. A small excited comic-style speech bubble near the child containing EXACTLY the text "I'm really going to space!", subtle and not covering the face.""",
            story_text="With a swirl of stardust, {name} was wrapped in the most amazing astronaut suit—white and silver with golden stars! It fit perfectly, as if it was made just for {name}. The adventure was about to begin!",
            costume="wearing white astronaut suit with gold star accents, helmet held under arm"
        ),

        # === PAGE 4 - BLAST OFF ===
        PageTemplate(
            page_number=4,
            scene_description="Launching into space in the rocket",
            scene_type="wonder",
            realistic_prompt="""EXCITING ROCKET LAUNCH SCENE inside spacecraft cockpit. Wide dynamic composition: Futuristic cockpit interior with curved walls lined with glowing colorful control panels - buttons in reds, blues, greens pulsing with light, screens displaying trajectory data and star maps. Large circular window dominates one wall, showing spectacular view of launch - Earth curving below getting smaller, white clouds rushing past, deep space opening up ahead with stars getting brighter and more numerous. Blue atmosphere giving way to black space. The child named {name} in astronaut suit (helmet off, resting on nearby seat) seated in the pilot's chair, hands gripping armrests, looking out the window with excited joyful expression and natural happy smile. Dynamic moment of acceleration and discovery. Colorful control panel lights create vibrant illumination throughout cockpit, mixing with blue starlight streaming through window. Sense of speed and adventure. Premium Pixar-quality cinematic scene capturing the thrill of blasting into space. Child's delighted expression clearly visible in the colorful cockpit lighting. Child's natural skin tone preserved exactly as in reference photo regardless of scene lighting. A small playful comic-style sound bubble near the window containing EXACTLY the text "WHOOSH!", subtle and not covering the face.""",
            story_text="'3... 2... 1... BLAST OFF!' The rocket zoomed up, up, UP through the clouds! {name} looked out the big round window and laughed with pure joy. The Earth grew smaller, and the stars grew closer!",
            costume="wearing astronaut suit, helmet off"
        ),

        # === PAGE 5 - FLOATING IN WONDER ===
        PageTemplate(
            page_number=5,
            scene_description="Floating in zero gravity inside spacecraft",
            scene_type="wonder",
            realistic_prompt="""MAGICAL ZERO GRAVITY SCENE inside spacecraft cabin. Wide environmental composition: Spacious cabin interior with curved metallic walls, glowing control panels, and large windows showing deep space outside - stars stretching infinitely, distant nebula clouds in soft purples and blues. Small glowing stars and magical sparkles drift weightlessly through the cabin air, floating in all directions creating whimsical atmosphere. Equipment and small objects suspended in mid-air. The child named {name} in astronaut suit floating gracefully in the center of the cabin, arms spread wide in joy, experiencing weightlessness for the first time. Natural floating pose showing pure delight and wonder. Soft blue and purple ambient light from space windows bathes the entire scene, mixing with warm interior cabin lights. Dreamy ethereal atmosphere emphasizing the magic of weightlessness. Stars and sparkles drift past slowly in the zero gravity. Premium cinematic quality capturing the joy of floating among the stars. Child's expression of pure delight clearly visible, face well-lit by ambient space glow. Child's natural skin tone preserved exactly as in reference photo regardless of scene lighting. A small joyful comic-style speech bubble near the child containing EXACTLY the text "This is the best feeling ever!", subtle and not covering the face.""",
            story_text="Inside the spacecraft, {name} floated like a feather! Spinning slowly, giggling, reaching out to catch floating stars that danced through the cabin. 'This is the best feeling ever!' {name} whispered.",
            costume="wearing astronaut suit"
        ),

        # === PAGE 6 - WALKING ON THE MOON ===
        PageTemplate(
            page_number=6,
            scene_description="First steps on the moon surface",
            scene_type="triumph",
            realistic_prompt="""EPIC MOON LANDING SCENE with wide cinematic lunar landscape composition. Vast silvery moon surface stretches out with gentle rolling craters and rocky terrain, fine moon dust covering everything in soft gray shimmer. Beautiful blue Earth glows brilliantly in the black starry sky above, clouds visible on Earth's surface, continents recognizable. Countless stars surround Earth in the deep space background. The child named {name} in astronaut suit with visor flipped up making a joyful bounce on the moon surface, arms spread out for balance enjoying the low gravity. Each bounce kicks up silvery moon dust that sparkles like glitter, floating slowly back down in the low gravity. Spacecraft landed nearby, its landing legs creating small craters. Soft Earthlight from above illuminates the entire lunar landscape with gentle blue glow. Sense of triumph and wonder at walking on another world. Premium cinematic quality capturing the magic of humanity's giant leap. Child's excited wonder-filled expression clearly visible in the soft Earthlight. Child's natural skin tone preserved exactly as in reference photo regardless of scene lighting. A small triumphant comic-style speech bubble near the child containing EXACTLY the text "I'm really on the Moon!", subtle and not covering the face.""",
            story_text="The rocket landed softly on the Moon with a gentle POOF of silver dust. {name} took one small step onto the glittery surface—and started bouncing! Every jump went higher and higher into the starry sky!",
            costume="wearing astronaut suit with visor flipped up"
        ),

        # === PAGE 7 - THE RAINBOW NEBULA ===
        PageTemplate(
            page_number=7,
            scene_description="Floating in a beautiful colorful nebula",
            scene_type="wonder",
            realistic_prompt="""BREATHTAKING RAINBOW NEBULA SCENE with wide cosmic environmental composition. Magnificent swirling nebula dominates the entire scene - vast clouds of cosmic gas in brilliant pink, purple, blue, and gold colors swirl and blend together like paint in water, creating mesmerizing patterns and flows. Nebula stretches infinitely in all directions with depth and dimension. Countless stars twinkle throughout, some bright foreground stars, others embedded deep in the nebula clouds. Small glowing asteroid platform floating in the nebula, crystalline surface catching and reflecting the colorful light. The child named {name} in astronaut suit with helmet completely off (held at side or not visible) standing on the asteroid platform, surrounded by the cosmic wonder. Natural confident pose showing peaceful awe and gentle wonder at being immersed in this cosmic rainbow. The nebula's vibrant colors create beautiful rim lighting around the hair and suit, while soft warm light from nearby stars illuminates the scene. Stars and nebula clouds drift slowly. Sense of floating in an ocean of color and light. Award-winning space photography quality capturing the majesty of deep space. Child's expression of peaceful wonder clearly visible with soft smile, face well-lit by starlight. Child's natural skin tone fully preserved, no color cast on face. A small amazed comic-style speech bubble near the child containing EXACTLY the text "It's like being inside a rainbow!", subtle and not covering the face.""",
            story_text="The rocket carried {name} to the Rainbow Nebula—a magical cloud of colors swirling through space! Pink, purple, blue, and gold danced together like paint in water. 'It's like being inside a rainbow!' {name} gasped.",
            costume="wearing astronaut suit, helmet off",
            face_expression="peaceful awe and gentle wonder, soft amazed smile, eyes looking directly at camera, face straight forward"
        ),

        # === PAGE 8 - CATCHING STARDUST ===
        PageTemplate(
            page_number=8,
            scene_description="Collecting magical stardust in a jar",
            scene_type="bonding",
            realistic_prompt="""ENCHANTING STARDUST COLLECTION SCENE in colorful nebula environment. Wide magical composition: Background continues the beautiful rainbow nebula - swirling clouds of pink, purple, and blue cosmic gas with golden accents, creating ethereal atmosphere. Countless golden stardust particles float through the nebula air like fireflies, drifting in gentle currents. Some particles cluster into streams and ribbons of light. Stars visible in the distance. The child named {name} in astronaut suit with helmet completely off (no helmet visible) standing in the nebula, holding a glowing glass jar at chest height. The jar is filled with swirling captured golden stardust, particles dancing inside creating mesmerizing patterns. More stardust particles drift toward the jar, being drawn in by the magic. Natural pose showing proud wonder at collecting this cosmic treasure. The jar's warm golden glow illuminates upward, creating beautiful warm light that bathes the child's face and creates magical atmosphere. Nebula colors provide soft ambient light from all sides. Intimate moment of discovery and collection. Premium cinematic quality emphasizing the magic of gathering stardust. Child's expression of soft peaceful smile and proud wonder clearly visible, face well-lit by the jar's golden glow. Child's natural skin tone preserved.""",
            story_text="Floating through the nebula, {name} discovered something magical—real stardust! Holding out a special jar, {name} watched as golden stardust swirled inside, glowing like captured sunshine. A treasure from the stars!",
            costume="wearing astronaut suit, helmet off",
            face_expression="soft peaceful smile, proud wonder, eyes looking directly at camera, face straight forward"
        ),

        # === PAGE 9 - HOMEWARD BOUND ===
        PageTemplate(
            page_number=9,
            scene_description="Looking at Earth from space, heading home",
            scene_type="peaceful",
            realistic_prompt="""EMOTIONAL HOMECOMING SCENE inside spacecraft viewing deck. Wide environmental composition: Spacious observation deck with large panoramic window taking up much of one wall, curved spacecraft interior with soft metallic surfaces. Beautiful blue Earth visible through the window - swirling white clouds, blue oceans, green and brown continents clearly visible, looking peaceful and inviting from space. Black space dotted with stars surrounds Earth. The child named {name} in astronaut suit standing at the window, both hands pressed gently against the glass in touching gesture of connection and longing. Natural pose showing tender emotion and contemplation. Warm interior spacecraft lighting fills the cabin from overhead and side panels, creating cozy atmosphere and illuminating the scene naturally. Soft cool blue rim light from Earth's glow provides gentle accent on edges of suit and hair, while face preserves full natural warm skin tone. Window glass is clear with no reflections. Tender heartwarming moment of recognizing home after cosmic adventure. Premium cinematic quality capturing the emotional bond with Earth. Child's expression of warm peaceful smile and contentment clearly visible in the cabin's warm lighting. Child's natural skin tone preserved exactly as in reference photo regardless of scene lighting. A small gentle comic-style speech bubble near the child containing EXACTLY the text "That's where everyone I love lives.", subtle and not covering the face.""",
            story_text="As the rocket turned toward home, {name} pressed both hands against the window and gazed at Earth—a beautiful blue marble wrapped in white clouds. 'That's where everyone I love lives,' {name} smiled. 'I can't wait to tell them everything!'",
            costume="wearing astronaut suit"
        ),

        # === PAGE 10 - SWEET DREAMS ===
        PageTemplate(
            page_number=10,
            scene_description="Back in bed with stardust jar glowing",
            scene_type="sleeping",
            face_expression="drowsy, heavy-lidded, softly dreaming, peaceful smile",
            realistic_prompt="""COZY HEARTWARMING BEDROOM SCENE with warm environmental composition. Peaceful nighttime bedroom with soft ambient lighting creating intimate atmosphere. Cozy bed with fluffy blankets and soft pillows, stuffed space toys scattered nearby - plush rocket ship, astronaut teddy bear, planet pillows. Nighttime window shows beautiful starry sky outside, one particularly bright star twinkling prominently as if saying goodnight. Moonlight streams softly through window curtains. Bedroom details visible - space-themed posters on wall, toy shelf, soft rug. The child named {name} tucked into bed wearing cozy pajamas, hugging glowing jar of golden stardust close to chest. Child's face resting peacefully on pillow, eyes heavy-lidded and softly drooping, naturally closing in drowsy drift toward sleep. Gentle content smile on face. Eyes not squeezed shut but softly closing with lashes resting lightly, maintaining warm recognizable expression. The jar's warm golden glow creates soft sidelight at pillow level, illuminating child's peaceful face naturally without harsh shadows. Warm bedroom lamp provides gentle ambient light. Sense of safety, comfort, and magical dreams. Premium cinematic quality capturing the tender bedtime moment. Child's peaceful sleeping expression clearly visible in the soft golden glow. Child's natural skin tone preserved exactly as in reference photo regardless of scene lighting. A faint dreamy comic-style thought bubble above the child containing a tiny glowing rocket surrounded by small sparkling stars, subtle and not covering the face.""",
            story_text="Safe in bed, {name} hugged the jar of stardust close—proof that the adventure was real. The stars twinkled outside the window as if to say goodnight. {name} smiled and whispered, 'Dreams really do come true.' And in sleep that night, {name} danced among the stars once more.",
            costume="wearing cozy pajamas"
        ),
    ]
)
