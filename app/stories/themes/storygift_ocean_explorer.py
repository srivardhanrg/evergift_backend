"""
StoryGift Ocean Explorer Theme - Underwater Kingdom.

Complete 10-page story: "[NAME]'s Underwater Kingdom"
Premium theme featuring underwater exploration, sea creature friendships, and ocean magic.
Scene-First composition emphasizing underwater environments and ocean wonder.

KEY PRINCIPLES:
- Wide environmental compositions showcasing ocean wonder
- Natural expressions (delight, awe, wonder, contentment)
- Underwater lighting preserves natural skin tone throughout
- Child integrated naturally into oceanic environments
- Gender-neutral language throughout
"""

from app.stories.templates import StoryTemplate, PageTemplate


STORYGIFT_OCEAN_EXPLORER_THEME = StoryTemplate(
    theme_id="storygift_ocean_explorer",
    title_template="{name}'s Underwater Kingdom",
    cover_display_title="Underwater Kingdom",
    description="Dive into a world where imagination runs as deep as the ocean",
    default_costume="wearing a sleek magical diving suit in turquoise and silver with glowing trim and small translucent fins",
    protagonist_description="bright curious eyes, expression of wonder and joy",
    cover_costume="wearing a sleek magical diving suit in turquoise and silver with glowing trim, small translucent fins on arms, adventurous swimming pose",
    cover_header_atmosphere="Crystal-clear turquoise water with volumetric god rays piercing down from the surface, creating dramatic light shafts",
    cover_magical_elements="Swirl of colorful tropical fish including clownfish and tangs around the body (not face). A friendly sea turtle beside the child. Glowing jellyfish above creating ambient light. Coral reef with bioluminescent elements in background, treasure chest partially visible.",
    cover_footer_description="Vibrant coral reef with colorful anemones, sea fans, and soft coral formations",
    pages=[
        PageTemplate(
            page_number=1,
            scene_description="Finding the magical seashell",
            scene_type="discovery",
            realistic_prompt="""MAGICAL BEACH DISCOVERY SCENE on golden sandy shore. Wide environmental composition: A beautiful beach at warm golden hour — soft golden sand stretching along the shore, gentle turquoise waves rolling in and receding with a peaceful rhythm, clear blue sky with soft clouds above. Seagulls visible in the distance over the water. Scattered seashells and smooth pebbles on the sand in the foreground, catching the warm afternoon light. The child named {name} in swimsuit kneeling on the golden sand, holding a remarkable iridescent conch shell out in both hands at chest level, examining it closely with amazed curiosity. The shell glows with a warm golden-white inner light that spills outward across the surrounding sand in a soft halo. Tiny magical sparkles beginning to swirl and dance around the child and the glowing shell. Warm golden hour beach light envelops the entire scene. The ocean stretches out behind in beautiful soft focus. Natural discovery pose of a child who has found something extraordinary. A soft comic-style speech bubble near the child containing EXACTLY the text "I wish I could explore the ocean", subtle and not covering the face.""",
            story_text="One sunny morning at the beach, {name} found a beautiful seashell that shimmered with all the colors of the rainbow. When {name} held it close and whispered, 'I wish I could explore the ocean,' the shell began to glow!",
            costume="wearing swimsuit"
        ),
        PageTemplate(
            page_number=2,
            scene_description="Magical underwater transformation",
            scene_type="transformation",
            realistic_prompt="""MAGICAL UNDERWATER SWIMMING SCENE in crystal-clear tropical water. Wide dynamic composition: Crystal-clear turquoise water stretching in every direction, sunlight streaming down from the surface above in spectacular volumetric god rays that pierce the water in columns of golden light, illuminating the underwater world. Colorful tropical fish in oranges, blues, and yellows swimming in greeting alongside the swimmer, their scales catching the filtered sunlight. Soft coral reef formations visible in the background below, vibrant and detailed. A swirl of golden magical bubbles and sparkles trails behind the swimmer as they move through the water. The child named {name} in the magical diving suit — sleek turquoise and silver with glowing trim and small translucent fins on the arms — swimming forward through the water in a natural swimming pose, arms reaching ahead, legs gently trailing. Hair flowing back softly in the water. The suit's glowing trim catches the god ray light beautifully. Natural expression of pure joy and wonder at breathing underwater. A small excited comic-style speech bubble near the child containing EXACTLY the text "WOW! I can breathe underwater!", playful and full of wonder, subtle and not covering the face.""",
            story_text="In a swirl of bubbles and light, {name} transformed! Suddenly able to breathe underwater with magical gills that sparkled like diamonds, and wearing a special outfit that let {name} swim like a fish. With an excited laugh, {name} dove beneath the waves!",
            costume="wearing magical diving suit in turquoise and silver with translucent fins"
        ),
        PageTemplate(
            page_number=3,
            scene_description="Fish welcome dance",
            scene_type="wonder",
            realistic_prompt="""JOYFUL UNDERWATER WELCOME SCENE in vibrant tropical ocean. Wide celebratory composition: Clear bright blue-green water filled with spectacular color — schools of coordinated tropical fish performing a swirling welcome dance. Orange clownfish, vivid blue tangs, bright yellow butterflyfish, and purple anthias spiral in coordinated rainbow tunnels and arching formations that fill the water from surface to reef below, creating a living kaleidoscope. Sunlight pierces down from the surface in multiple god rays, illuminating the fish in flashes of color. A sleek friendly dolphin moves alongside the scene, intelligent eye showing warmth and curiosity, both reaching toward each other in a natural greeting moment, the dolphin positioned entirely to the side. Coral reef visible in background below, lush and colorful. The child named {name} in magical aquatic outfit positioned in the center of this joyful display, laughing with delight — a natural reaction to being surrounded by this spectacular welcome. Bubbles from laughter rising upward. Sense of dance and play permeating every element of the scene. A small delighted comic-style speech bubble near the child containing EXACTLY the text "Hi! Wow, you're so beautiful!", full of excitement and friendliness, subtle and not covering the face.""",
            story_text="The ocean welcomed {name} with open waves! Schools of colorful fish swam in swirling patterns, performing an underwater dance just for {name}. A playful dolphin appeared and chirped hello, spinning through the water with joy!",
            costume="wearing magical aquatic outfit with fins"
        ),
        PageTemplate(
            page_number=4,
            scene_description="Riding the wise sea turtle",
            scene_type="journey",
            realistic_prompt="""ICONIC SEA TURTLE RIDE SCENE through open crystal water. Wide graceful composition: Open crystal-clear blue ocean water stretching in all directions with warmth and light. Golden sunlight rays streaming down from the distant surface above create dramatic vertical columns of warm light that illuminate the journey. A school of colorful small fish swims alongside in a friendly escort. Kelp forest passing gently in the background below, green ribbons swaying in the current. The wise ancient sea turtle glides magnificently through the water — enormous shell covered in beautiful intricate geometric patterns, ancient textures, with small coral formations that have grown on the shell over centuries of wandering. The child named {name} in magical aquatic outfit seated upright and naturally on the turtle's broad back, one hand resting lightly on the shell's edge for balance, the other reaching forward in joyful anticipation of the journey ahead. Hair and translucent fins flowing gently from the movement through the water. Natural riding pose of confident adventure and happy companionship. A small soft comic-style speech bubble near the child containing EXACTLY the text "Let's go!", excited and adventurous, subtle and not covering the face.""",
            story_text="A wise old sea turtle with a shell covered in beautiful patterns glided over. 'Welcome to our kingdom, {name},' she said in a gentle voice. 'Would you like to see something magical? Climb on!' {name} carefully held on as they began an incredible journey.",
            costume="wearing magical aquatic outfit, sitting on turtle"
        ),
        PageTemplate(
            page_number=5,
            scene_description="Bioluminescent wonderland",
            scene_type="awe",
            realistic_prompt="""BIOLUMINESCENT WONDERLAND SCENE in deep magical ocean. Wide ethereal composition: The water transitions from blue to a rich purple-indigo as they go deeper, the surface light fading and replaced by magical living light from below and around. Glowing jellyfish in soft pink, lavender, and electric blue drift through the water in graceful silence, their trailing tendrils creating flowing ribbons of light. Tiny bioluminescent plankton fill the water like scattered stars, some clustering into softly pulsing clouds. Spotted fish with bioluminescent patterns weave between the jellyfish. The sea turtle's ancient shell reflects the glowing colors across its geometric patterns. The child named {name} in magical aquatic outfit seated on the turtle's back, one arm gently extended to the side toward a passing jellyfish in natural wonder. The bioluminescent creatures create beautiful colorful rim and ambient lighting throughout the scene, their glow surrounding the scene with soft color. Natural expression of complete awe at the otherworldly beauty. Volumetric lighting through the deep water, particle effects, ethereal and dreamlike atmosphere. A small soft comic-style speech bubble near the child containing EXACTLY the text "Wow", gentle and full of wonder, subtle and not covering the face.""",
            story_text="They dove deeper into the ocean where the water glowed with bioluminescent creatures! Jellyfish like floating lanterns lit the way. Tiny fish sparkled like stars. {name} had never seen anything so beautiful!",
            costume="wearing magical aquatic outfit"
        ),
        PageTemplate(
            page_number=6,
            scene_description="Approaching the coral palace entrance with excitement",
            scene_type="revelation",
            realistic_prompt="""UNDERWATER PALACE ARRIVAL SCENE at grand coral kingdom entrance. Wide breathtaking composition: The grand coral palace fills the background in magnificent scale — a towering structure carved from living coral in vibrant pinks, creamy purples, and brilliant whites. Elaborate archways rise to impressive heights, their surfaces studded with giant lustrous pearls and panels of abalone shell that shimmer with iridescent color. Spiral towers made of enormous whelk shells rise above the main structure. Seaweed gardens flow gently in the current on either side of the grand entrance archway. Seahorses hovering in pairs near the entrance columns, colorful manta rays gliding overhead, tropical fish in organized welcoming patterns near the doorway. The ancient sea turtle gliding alongside. Golden sunlight rays still reaching down from above, illuminating the palace facade in warm underwater light. The child named {name} in magical aquatic outfit in the foreground, body leaning forward with momentum toward the palace, arms slightly extended outward to the sides in natural delight and wonder at the scale and beauty of what they're approaching. Natural approaching pose radiating excitement and forward motion. A small soft comic-style speech bubble near the child containing EXACTLY the text "Whoa...", breathless and excited, subtle and not covering the face.""",
            story_text="They arrived at a magnificent underwater palace made entirely of coral, pearls, and seashells! 'This is the Ocean Kingdom,' explained the turtle. 'And today, {name}, you are our honored guest!' Sea creatures of every kind gathered to meet their special visitor.",
            costume="wearing magical aquatic outfit"
        ),
        PageTemplate(
            page_number=7,
            scene_description="Child discovers and opens treasure chest in magical grotto",
            scene_type="intimate",
            realistic_prompt="""TREASURE GROTTO DISCOVERY SCENE deep beneath the coral palace. Wide intimate composition: A magical cave grotto interior — walls covered in layers of colorful living anemones in oranges, purples, and greens, delicate sea fans in pink and cream, soft bioluminescent algae casting a gentle ambient teal-blue glow across the cave walls and ceiling. Smaller decorative chests and glowing artifacts scattered across the grotto floor, their surfaces encrusted with barnacles and sea jewels. Curious small fish peering from crevices in the coral walls, watching from above and below. The sea turtle partially visible in the far background of the grotto. At center stage: an enormous ornate treasure chest, its lid just thrown open in the exact moment of discovery — the massive lid pushed back at an angle, and from inside erupts a brilliant flood of golden magical light upward and outward, illuminating the entire grotto in warm radiance. Inside the chest visible: luminous pearls, a radiant glowing shell necklace, golden coins, and softly pulsing magical orbs of light. The child named {name} in magical aquatic outfit kneeling forward on both knees, both hands on the chest's rim having just opened it, body leaning in toward the light with a gasp of pure breathless amazement. Natural discovery pose capturing the solo triumphant moment of finding the treasure.""",
            story_text="The sea turtle led {name} to a hidden grotto deep beneath the palace. 'This place has been waiting for someone with a heart as curious and kind as yours,' she whispered. Inside, {name} found an ancient treasure chest glowing with golden light — and threw it open!",
            costume="wearing magical aquatic outfit"
        ),
        PageTemplate(
            page_number=8,
            scene_description="Receiving the magical shell necklace from the wise octopus",
            scene_type="looking_down",
            realistic_prompt="""GIFT-GIVING CEREMONY SCENE in the coral palace interior. Wide intimate composition: The interior of the coral palace — arched coral ceilings above, natural light filtering through the water from high windows in the palace walls, other sea creatures gathered at a respectful distance in the background watching with happy expressions. The wise guardian octopus is remarkable — enormous but gentle, with shimmering purple-gold tentacles that catch the palace light, each arm decorated with tiny lustrous pearls and sea gems at their tips, kind and deeply intelligent eyes reflecting genuine warmth. One of the octopus's beautifully decorated tentacles holds the delicate golden chain with its glowing shell pendant raised carefully at eye level in a ceremonial offering. The child named {name} in magical aquatic outfit standing before the octopus, both hands coming up gently to receive or touch the glowing necklace being presented, natural expression of wonder and deep gratitude at receiving this honor. The shell pendant's warm golden glow emanates forward, filling the space between them with warmth. Touching moment of honor and cross-species friendship. No other human-like faces in the scene. A small soft comic-style speech bubble near the child containing EXACTLY the text "Thank you...", quiet and heartfelt, subtle and not covering the face.""",
            story_text="The wise octopus guardian, keeper of the ocean's secrets, placed a special necklace around {name}'s neck with gentle tentacles—a golden shell that would always carry the magic of the ocean. 'Whenever you need courage or wonder, hold this close and remember: you are always welcome in our kingdom, brave explorer {name}.'",
            costume="wearing magical aquatic outfit, receiving golden shell necklace"
        ),
        PageTemplate(
            page_number=9,
            scene_description="Sunset return to the beach",
            scene_type="farewell",
            realistic_prompt="""PERFECT SUNSET BEACH FAREWELL SCENE at golden hour. Wide emotional composition: A breathtaking beach at golden hour — the sky transformed into a spectacular canvas of deep oranges, soft pinks, and warm purples that reflect across the calm water surface and the wet sand below, creating a mirror image of the beautiful sky. Wet sand near the water's edge sparkles with reflected sunset colors. Seashells scattered across the beach foreground catch the golden light. The child's footprints in the wet sand lead from the water toward the dry beach. In the ocean water behind, the silhouette of the wise sea turtle has surfaced, one flipper raised in a gentle goodbye wave. A dolphin arcs above the water catching the last golden light. Small fish leap in the shallows. The child named {name} in regular swimsuit wading ankle-deep in the gentle surf, the water around their feet catching the sunset in orange and gold ripples. The golden shell necklace clearly visible around their neck, glowing softly in the warm light. Natural pose of someone pausing to take in the beauty and say goodbye to a world they are leaving, a warm content smile on their face. A small soft comic-style speech bubble near the child containing EXACTLY the text "Bye...", gentle and content, subtle and not covering the face.""",
            story_text="The turtle brought {name} back to the surface, where the sun was setting in beautiful colors. As {name} waded back to shore, the magical outfit faded away, but the golden shell necklace remained. The ocean would always be {name}'s special place—full of friends, magic, and endless adventures waiting below the waves.",
            costume="wearing regular swimsuit, golden shell necklace around neck"
        ),
        PageTemplate(
            page_number=10,
            scene_description="Bedtime ocean dreams",
            scene_type="sleeping",
            face_expression="drowsy, heavy-lidded, softly dreaming, peaceful smile",
            realistic_prompt="""PEACEFUL OCEAN-THEMED BEDTIME SCENE in cozy bedroom at night. Wide warm composition: A child's bedroom decorated with ocean love — shells arranged on a shelf, a colorful fish mobile hanging above, an ocean landscape painting on the wall, stuffed sea animal toys. Moonlight streams softly through window curtains, casting gentle silver light across the room. Above the bed, soft magical dream mist shows gentle glimpses of the day's underwater adventures — the sea turtle, the coral palace archway, colorful fish, the octopus guardian's kind eyes. The golden shell necklace rests on the pillow beside the child's head, glowing with a soft warm pulsing light at pillow level, its glow casting gentle golden sidelight across the pillow and bedding. The child named {name} in pajamas tucked into bed, head resting on the pillow, eyes heavy-lidded and softly drooping as sleep naturally arrives — not squeezed shut but gently closing, lashes resting lightly, a peaceful content smile on their face. The warm golden glow from the shell beside the pillow creates soft natural illumination at face level. A small soft comic-style speech bubble near the child containing EXACTLY the text "zzz", sleepy and fading, subtle and not covering the face.""",
            story_text="That night, {name} fell asleep holding the magical shell, dreaming of coral palaces and dancing fish. The Ocean Queen had been right—the ocean would always be there, waiting for the next adventure. And somewhere in the deep blue sea, {name}'s friends were waving goodnight.",
            costume="wearing pajamas, holding glowing shell necklace"
        ),
    ]
)
