"""
StoryGift Ocean Explorer Theme - Underwater Kingdom.

Complete 10-page story: "[NAME]'s Underwater Kingdom"
Premium theme featuring underwater exploration, sea creature friendships, and ocean magic.
Optimized for both photorealistic and 3D cartoon pipelines.
"""

from app.stories.templates import StoryTemplate, PageTemplate


STORYGIFT_OCEAN_EXPLORER_THEME = StoryTemplate(
    theme_id="storygift_ocean_explorer",
    title_template="{name}'s Underwater Kingdom",
    cover_display_title="Underwater Kingdom",
    description="Dive into a world where imagination runs as deep as the ocean",
    default_costume="wearing a sleek magical diving suit in turquoise and silver with glowing trim and small translucent fins",
    protagonist_description="bright curious eyes, expression of wonder and joy",
    # Cover page settings for typography-ready composition
    cover_costume="wearing a sleek magical diving suit in turquoise and silver with glowing trim, small translucent fins on arms, adventurous swimming pose",
    cover_header_atmosphere="Crystal-clear turquoise water with volumetric god rays piercing down from the surface, creating dramatic light shafts",
    cover_magical_elements="Swirl of colorful tropical fish including clownfish and tangs around the body (not face). A friendly sea turtle beside the child. Glowing jellyfish above creating ambient light. Coral reef with bioluminescent elements in background, treasure chest partially visible.",
    cover_footer_description="Vibrant coral reef with colorful anemones, sea fans, and soft coral formations",
    pages=[
        # === PAGE 1 - THE MAGICAL SHELL ===
        PageTemplate(
            page_number=1,
            scene_description="Finding the magical seashell",
            scene_type="discovery",
            realistic_prompt="""Magical beach discovery. The child named {name} in swimsuit kneeling on golden sandy beach, holding an iridescent conch shell out in front of them at face level, tilted gently as if listening — face fully front-facing toward camera, not turned into profile. Shell held forward and slightly to the side so the child's face remains completely visible and unobstructed. The shell glows with warm golden-white light that illuminates the child's amazed face naturally from the front — soft warm frontal glow, no multi-color light patterns washing over the face. Tiny magical sparkles beginning to swirl around child. Gentle waves in background, turquoise water, clear blue sky. Warm natural beach lighting, soft focus on background ocean, sharp detail on child and shell. Sand particles floating in golden light, seagulls in distance. Beautiful golden hour beach light. Child's face is the clear focal point, well-lit and fully visible. A soft comic-style speech bubble near the child containing EXACTLY the text "I wish I could explore the ocean", subtle and not covering the face.""",
            story_text="One sunny morning at the beach, {name} found a beautiful seashell that shimmered with all the colors of the rainbow. When {name} held it close and whispered, 'I wish I could explore the ocean,' the shell began to glow!",
            costume="wearing swimsuit"
        ),

        # === PAGE 2 - THE TRANSFORMATION ===
        PageTemplate(
            page_number=2,
            scene_description="Magical underwater transformation",
            scene_type="transformation",
            realistic_prompt="""Magical underwater diving scene. The child named {name} swimming horizontally toward camera, arms stretched forward with the child's face looking directly ahead at the viewer — front-facing composition, face clearly visible, well-lit, prominently filling the frame. Wearing a sleek magical diving suit in turquoise and silver with small translucent fins on arms. A swirl of magical golden bubbles and sparkles trails behind the child. Sunlight streams down through the crystal-clear turquoise water from above, creating beautiful god rays that illuminate the child's face naturally from above-front. Colorful tropical fish swimming alongside the child in greeting. Hair gently flowing back in water. Soft coral reef visible in background below. Magical transformation sparkles trailing behind. Child's expression shows pure joy and wonder, eyes open, face the absolute focal point. A small excited comic-style speech bubble near the child containing EXACTLY the text "WOW! I can breathe underwater!", playful and full of wonder, subtle and not covering the face. Beautiful natural underwater lighting, sense of freedom and adventure.""",
            story_text="In a swirl of bubbles and light, {name} transformed! Suddenly able to breathe underwater with magical gills that sparkled like diamonds, and wearing a special outfit that let {name} swim like a fish. With an excited laugh, {name} dove beneath the waves!",
            costume="wearing magical diving suit in turquoise and silver with translucent fins"
        ),

        # === PAGE 3 - OCEAN WELCOME ===
        PageTemplate(
            page_number=3,
            scene_description="Fish welcome dance",
            scene_type="wonder",
            realistic_prompt="""Joyful underwater welcome. The child named {name} in magical aquatic outfit prominently in center-foreground, laughing with delight — face large, clearly visible, sharply detailed, the undisputed focal point of the composition. Medium shot keeping child's face prominent rather than a wide shot. Schools of colorful tropical fish in coordinated spiral patterns swirl behind and around the child — orange clownfish, blue tangs, yellow butterflyfish, purple anthias creating rainbow tunnels in the background. A sleek dolphin beside the child (not in front, not blocking face), both reaching toward each other, dolphin's eye showing intelligence and friendliness. Shafts of sunlight pierce the clear blue water from above, creating god ray lighting that falls naturally on the child's face from above. Coral reef visible in background below. Bubbles from laughter, sense of dance and play, vibrant but natural ocean colors. Child's joyful laughing face is the absolute focal point, well-lit by natural sunlight from above. A small delighted comic-style speech bubble near the child containing EXACTLY the text "Hi! Wow, you're so beautiful!", full of excitement and friendliness, subtle and not covering the face.""",
            story_text="The ocean welcomed {name} with open waves! Schools of colorful fish swam in swirling patterns, performing an underwater dance just for {name}. A playful dolphin appeared and chirped hello, spinning through the water with joy!",
            costume="wearing magical aquatic outfit with fins"
        ),

    # === PAGE 4 - THE SEA TURTLE ===
    PageTemplate(
        page_number=4,
        scene_description="Riding the wise sea turtle",
        scene_type="journey",
        realistic_prompt="""Iconic turtle ride. The child named {name} sitting upright on the broad back of an enormous ancient sea turtle with intricate geometric patterns and coral growth on shell. Child sitting tall and confident, facing toward camera with joyful adventurous expression, face clearly visible and detailed, taking up a prominent portion of the frame. Hair and fins flowing gently from movement. Small colorful fish swimming alongside. Turtle's wise shell visible beneath the child, they're gliding through open crystal-clear blue water with golden sun rays streaming from above, kelp forest passing below, school of fish accompanying them. Sense of graceful movement through water, peaceful companionship. Beautiful underwater lighting with warm light illuminating the child's face, magical atmosphere. Child's face is the absolute focal point of the composition. A small soft comic-style speech bubble near the child containing EXACTLY the text "Let's go!", excited and adventurous, subtle and not covering the face.""",
        story_text="A wise old sea turtle with a shell covered in beautiful patterns glided over. 'Welcome to our kingdom, {name},' she said in a gentle voice. 'Would you like to see something magical? Climb on!' {name} carefully held on as they began an incredible journey.",
        costume="wearing magical aquatic outfit, sitting on turtle"
    ),
        # === PAGE 5 - BIOLUMINESCENT DEPTHS ===
        PageTemplate(
            page_number=5,
            scene_description="Bioluminescent wonderland",
            scene_type="awe",
            realistic_prompt="""Bioluminescent wonderland scene. Deeper water transitioning from blue to purple-indigo. The child named {name} and sea turtle moving through a magical zone filled with glowing creatures. Child's face prominently visible, front-facing toward camera, expression of absolute awe — face illuminated by soft warm ambient light from slightly above the front, preserving natural skin tone completely. The bioluminescent creatures — jellyfish in pink, purple, and blue, glowing plankton, spotted fish — create beautiful colorful rim and edge lighting around the child's suit, hair, and body outline, but do NOT cast colored light directly onto the child's face. Child reaching gently toward a jellyfish to the side (arm extended sideways, not blocking face). Turtle nearby, shell reflecting colorful glows. Soft god rays still filtering from distant surface above. Volumetric lighting through water, particle effects, ethereal and dreamlike atmosphere. Child's face is the warm, clear focal point against the magical glowing background. A small soft comic-style speech bubble near the child containing EXACTLY the text "Wow", gentle and full of wonder, subtle and not covering the face.""",
            story_text="They dove deeper into the ocean where the water glowed with bioluminescent creatures! Jellyfish like floating lanterns lit the way. Tiny fish sparkled like stars. {name} had never seen anything so beautiful!",
            costume="wearing magical aquatic outfit"
        ),

        # === PAGE 6 - THE UNDERWATER PALACE ===
        PageTemplate(
            page_number=6,
            scene_description="Approaching the coral palace entrance with excitement",
            scene_type="revelation",
            realistic_prompt="""Underwater palace arrival — action approaching shot. The child named {name} in the foreground mid-stride moving toward the grand coral palace entrance, body leaning forward with excitement and momentum, arms slightly extended out to the sides in wonder and delight. Face is front-facing toward camera with a huge, breathless smile and wide eyes full of amazement — the absolute focal point of the composition. Well-lit by warm golden sunlight shafts streaming down from above, falling naturally and warmly on the child's face. The towering grand palace carved from living coral in pinks, purples, and whites fills the background — elaborate archways, giant pearls, abalone shells, seaweed gardens and spiral shell towers. The ancient sea turtle gliding beside the child. Colorful sea creatures — seahorses, manta rays, tropical fish — gathered near the palace entrance in the background, smiling and welcoming. Child's entire posture communicates movement, wonder, and joy — they are ENTERING this magical world, not just observing it. Medium-close shot keeping child large and detailed. Grand majestic atmosphere, child is the emotional and physical center of the scene. A small soft comic-style speech bubble near the child containing EXACTLY the text "Whoa...", breathless and excited, subtle and not covering the face.""",
            story_text="They arrived at a magnificent underwater palace made entirely of coral, pearls, and seashells! 'This is the Ocean Kingdom,' explained the turtle. 'And today, {name}, you are our honored guest!' Sea creatures of every kind gathered to meet their special visitor.",
            costume="wearing magical aquatic outfit"
        ),

        # === PAGE 7 - THE TREASURE DISCOVERY ===
        PageTemplate(
            page_number=7,
            scene_description="Child discovers and opens treasure chest in magical grotto",
            scene_type="intimate",
            realistic_prompt="""Treasure grotto discovery — child as the hero. Magical cave grotto interior with walls covered in colorful living anemones, sea fans, and bioluminescent algae casting a soft ambient teal-blue glow on the surrounding walls. The child named {name} is front and center, kneeling forward on both knees with both hands gripping the heavy lid of an enormous ornate treasure chest, having just thrown it OPEN — the lid pushed back at an angle, golden magical light erupting outward from inside the chest directly onto the child's face. The child's face is front-facing toward camera, expression of pure breathless amazement and joy — eyes wide, mouth open in a gasp of delight, face beautifully and warmly illuminated by the treasure's forward golden glow at face level. No harsh upward under-chin shadows — the golden light spills forward and upward at face level naturally. Inside the chest: glowing pearls, a radiant shell necklace, golden coins, and softly pulsing magical orbs of light visible. The child's hands on the chest rim, leaning in to see. No other human characters — this is the child's solo discovery moment. Small curious fish peeking from coral crevices in the background watching. A sea turtle partially visible in the far background. Smaller decorative chests and glowing artifacts scattered around the grotto floor. Warm intimate golden light, the child's amazed face is the clear emotional focal point of the entire composition. Unforgettable discovery scene.""",
            story_text="The Ocean Queen, a beautiful mermaid with a crown of pearls, smiled warmly. 'We've been waiting for someone with a heart as curious and kind as yours, {name}. We have a gift for you.' She led {name} to a secret grotto filled with treasures!",
            costume="wearing magical aquatic outfit"
        ),

        # === PAGE 8 - THE MAGICAL NECKLACE ===
        PageTemplate(
            page_number=8,
            scene_description="Receiving the magical shell necklace from the wise octopus",
            scene_type="looking_down",
            realistic_prompt="""Gift-giving ceremony. Close-up intimate moment. The wise, friendly octopus guardian with shimmering purple-gold tentacles holds the delicate golden chain with glowing shell pendant up at the child named {name}'s eye level, presenting it before placing it around the neck — child looking straight ahead at the necklace being held up at face level, head upright and fully front-facing toward camera, expression of wonder and gratitude clearly visible. Child's hands coming up to gently touch it. Face remains prominently front-facing, no steep downward angle. The shell pendant's warm golden glow emanates forward at face level, illuminating the child's face naturally from the front — no upward under-chin light. The octopus has kind, intelligent eyes, tentacles decorated with tiny pearls and sea gems. Soft focus on background showing palace interior with coral archways, other sea creatures watching with happy expressions. Warm magical atmosphere. No other human-like faces in the scene, only the child and the octopus. Child's face is the clear focal point, beautifully and naturally lit. Touching moment of honor and friendship. A small soft comic-style speech bubble near the child containing EXACTLY the text "Thank you...", quiet and heartfelt, subtle and not covering the face.""",
            story_text="The wise octopus guardian, keeper of the ocean's secrets, placed a special necklace around {name}'s neck with gentle tentacles—a golden shell that would always carry the magic of the ocean. 'Whenever you need courage or wonder, hold this close and remember: you are always welcome in our kingdom, brave explorer {name}.'",
            costume="wearing magical aquatic outfit, receiving golden shell necklace"
        ),

        # === PAGE 9 - RETURNING TO SHORE ===
        PageTemplate(
            page_number=9,
            scene_description="Sunset return to the beach",
            scene_type="farewell",
            realistic_prompt="""Perfect sunset ending. The child named {name} in regular swimsuit walking out of gentle surf onto beach at golden hour, ankle-deep in water with small waves lapping around feet. Child facing three-quarter toward camera with a warm, content smile — face clearly visible and well-lit. The child's gaze drifts gently toward the ocean with just a subtle sideways eye movement and slight head turn, NOT a full over-shoulder profile turn — face remains mostly front-facing toward the viewer throughout. The golden shell necklace clearly visible, glowing softly around their neck. In the water behind them: the silhouette of the sea turtle surfacing to wave goodbye with one flipper, a dolphin's arc above the water, fish jumping in the golden light. The sky is spectacular with orange, pink, and purple sunset reflecting on wet sand and calm water. Warm golden hour light illuminates child's face naturally from the front-side. Seashells scattered on beach in foreground. Child's footprints in sand leading from water. Peaceful, complete feeling. Emotionally satisfying ending with child's face as the warm focal point. A small soft comic-style speech bubble near the child containing EXACTLY the text "Bye...", gentle and content, subtle and not covering the face.""",
            story_text="The turtle brought {name} back to the surface, where the sun was setting in beautiful colors. As {name} waded back to shore, the magical outfit faded away, but the golden shell necklace remained. The ocean would always be {name}'s special place—full of friends, magic, and endless adventures waiting below the waves.",
            costume="wearing regular swimsuit, golden shell necklace around neck"
        ),

        # === PAGE 10 - DREAMING OF THE DEEP ===
        PageTemplate(
            page_number=10,
            scene_description="Bedtime ocean dreams",
            scene_type="sleeping",
            face_expression="drowsy, heavy-lidded, softly dreaming, peaceful smile",
            realistic_prompt="""Peaceful bedtime scene. The child named {name} in pajamas tucked into bed, the golden shell necklace resting on the pillow beside their face, glowing softly. Child's face resting on the pillow, eyes heavy-lidded and softly drooping — drowsy and drifting into sleep, a gentle content smile on their face. Eyes NOT squeezed shut but naturally and softly closing, lashes resting lightly — enough facial feature visibility for a warm, recognizable expression. The shell beside the pillow at face level casts its warm golden glow sideways across the child's cheek — natural side light at face level, no harsh upward under-chin shadows. Above the bed, dream bubbles or a soft magical mist shows glimpses of the underwater kingdom: the sea turtle, the palace, colorful fish, the Ocean Queen waving. Ocean-themed decorations in the bedroom including shells on shelf, fish mobile, ocean painting. Moonlight streams softly through window. Warm, safe, magical atmosphere. Child's drowsy face clearly visible, the warm emotional focal point of the scene. A small soft comic-style speech bubble near the child containing EXACTLY the text "zzz", sleepy and fading, subtle and not covering the face.""",
            story_text="That night, {name} fell asleep holding the magical shell, dreaming of coral palaces and dancing fish. The Ocean Queen had been right—the ocean would always be there, waiting for the next adventure. And somewhere in the deep blue sea, {name}'s friends were waving goodnight.",
            costume="wearing pajamas, holding glowing shell necklace"
        ),
    ]
)
