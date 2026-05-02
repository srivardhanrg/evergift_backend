"""
StoryGift Safari Adventure Theme - African Savanna Adventure.

Complete 10-page story: "[NAME]'s Wild Safari Adventure"
Premium adventure story featuring different African animals on each page - elephant, giraffe, zebra, lion, cheetah, hippo.
Each page = 1-2 characters max for perfect facial consistency with NanoBana.
Optimized for exciting narrative flow with wow factor moments.
Scene-First composition emphasizing African savanna environments and animal encounters.

KEY PRINCIPLES:
- Wide environmental compositions showcasing African savanna wonder
- Natural expressions (awe, excitement, determination, pride, peace)
- Natural animal-scale relationships with authentic proportions
- Child integrated naturally into savanna environments
- Gender-neutral language throughout

CONVERSION OPTIMIZATION:
- Pages 1-5 (Preview): Thrilling animal encounters, ends with Lion King confrontation cliffhanger
- Pages 6-10 (Paid): Victory, speed racing, underwater adventure, emotional ceremony
"""

from app.stories.templates import StoryTemplate, PageTemplate


STORYGIFT_SAFARI_ADVENTURE_THEME = StoryTemplate(
    theme_id="storygift_safari_adventure",
    title_template="{name}'s Wild Safari Adventure",
    cover_display_title="Wild Safari Adventure",
    description="Where the wild things know your name - become the chosen Safari Guardian",
    default_costume="wearing khaki safari explorer outfit with adventure vest, boots, and explorer hat",
    protagonist_description="bright adventurous eyes, expression of wonder and courage",
    cover_costume="wearing premium khaki safari outfit with golden compass pendant glowing on chest, adventure vest with pockets, sturdy boots, and explorer hat tilted heroically",
    cover_header_atmosphere="Golden African sunset with dramatic orange and purple clouds, acacia tree silhouettes against the sky, birds flying in formation",
    cover_magical_elements="Majestic elephant Zara with colorful Maasai beads standing protectively behind the child. A proud lion with golden mane on one side. Giraffes, zebras, and colorful birds creating a frame. The magical Heartstone Compass glowing golden on child's chest. Warm rim lighting creates epic silhouette.",
    cover_footer_description="Golden savanna grass swaying, dust particles catching sunset light, animal footprints in red earth",
    pages=[
        PageTemplate(
            page_number=1,
            scene_description="Discovering the magical Heartstone Compass",
            scene_type="discovery",
            realistic_prompt="""MAGICAL COMPASS DISCOVERY SCENE in safari-themed bedroom at golden morning. Wide environmental composition: A child's bedroom decorated with safari adventure love — animal posters on the walls, a globe on a shelf, adventure books, small toy animals arranged on a windowsill. Golden morning light streams through the window in warm rays. On the bedroom floor, an ancient wooden box with intricate African tribal carvings sits open, its lid pushed back on the soft patterned rug. The box's interior lined with aged velvet, and from within it the magnificent Heartstone Compass hovers and pulses — a beautiful amber and gold instrument radiating warm golden light with tiny golden particles floating outward like fireflies. Animal-shaped shadows dance on the walls from the compass's magical light — the silhouettes of elephants, lions, and giraffes moving across the wallpaper. The child named {name} in pajamas kneeling on the bedroom floor beside the open box, both hands reaching forward toward the hovering glowing compass with pure awe and wide-eyed excitement. Natural pose of encountering something entirely magical for the first time. A small soft comic-style speech bubble near the child containing EXACTLY the text "What is this...?", hushed and curious, subtle and not covering the face.""",
            story_text="{name} gasped—a mysterious box glowed at the foot of the bed! Inside, the most beautiful compass floated in golden light. The moment {name}'s fingers touched it, the room exploded in swirling light. \"WHOOOOSH!\" The adventure was beginning!",
            costume="wearing pajamas"
        ),
        PageTemplate(
            page_number=2,
            scene_description="Arriving in savanna and meeting Zara the elephant",
            scene_type="adventure",
            realistic_prompt="""EPIC FIRST SAVANNA MEETING SCENE at golden hour in African landscape. Wide cinematic environmental composition: The vast African savanna at golden hour — golden grass stretching to the horizon, acacia trees silhouetted against a sky in breathtaking oranges and purples. The air is filled with warm golden light and tiny dust particles that catch the sunset like copper glitter. A herd of elephants visible as distant shapes near the horizon. The child named {name} in khaki safari outfit standing in the golden grass, one hand gently reaching out to touch the tip of Zara's magnificent trunk — the greeting moment. Zara is extraordinary and immediately impressive — a wise adult African elephant of great size, her neck and brow adorned with colorful Maasai beads that catch the sunset light in brilliant patterns. Her trunk curves down protectively toward the small figure beside her, her wise gentle eyes regarding the young visitor with ancient knowing. The Heartstone Compass glowing warmly on the child's chest, its amber light complementing the golden savanna sunset. Magical golden dust particles floating around the scene. Intimate bonding moment between young Guardian and animal elder. A small soft comic-style speech bubble near the child containing EXACTLY the text "You can talk!?", amazed and breathless, subtle and not covering the face.""",
            story_text="{name} tumbled through spinning light and landed in golden grass! \"Welcome, Guardian!\" rumbled a gentle voice. A magnificent elephant with glowing beads stood before {name}. \"I'm Zara. Quick—we must reach the Great Tree before sunset! Hold tight!\" She knelt. The race was on!",
            costume="wearing khaki safari explorer outfit with vest and hat"
        ),
        PageTemplate(
            page_number=3,
            scene_description="Thrilling ride on Kito the wild horse through canyon",
            scene_type="adventure",
            realistic_prompt="""HEROIC CANYON RIDE SCENE in dramatic African red rock landscape. Wide cinematic composition: A magnificent red rock canyon — dramatic sandstone walls rise on either side in warm terracotta and amber layers, creating a natural corridor of ancient geology. Afternoon sunlight streams through the canyon from above, creating golden shafts of light that illuminate the canyon floor and the dust particles stirred by movement. The canyon walls' warm colors glow richly in the directional light. Kito is a powerful and beautiful wild African horse — golden-brown coat gleaming in the canyon light, flowing dark mane and tail, strong and alive with energy, standing steady and proud beneath his rider. The child named {name} in khaki safari outfit sitting tall and upright on Kito's back in a natural riding posture, one hand resting on the horse's mane, the other slightly raised at the side. Heartstone Compass glowing on the child's chest. Golden dust particles swirling in the canyon light around them both. Classic hero-on-horseback composition in a spectacular natural setting. A small soft comic-style speech bubble near the child containing EXACTLY the text "This is amazing!", exhilarated and breathless, subtle and not covering the face.""",
            story_text="\"The shortcut is through the canyon!\" Kito the wild horse said, kneeling. {name} climbed up—and suddenly they were RACING! The canyon walls blurred past as Kito's hooves thundered on the ground. \"This is AMAZING!\" {name} laughed, holding tight!",
            costume="wearing safari outfit, sitting upright on horse",
            face_expression="proud adventurous smile, exhilarated joy, eyes bright and looking at camera, face directly forward"
        ),
        PageTemplate(
            page_number=4,
            scene_description="Discovering Nia the zebra's magical stripes up close",
            scene_type="wonder",
            realistic_prompt="""BREATHTAKING ZEBRA WONDER SCENE in golden African savanna. Wide warm composition: The open African savanna in gorgeous afternoon light — golden grass swaying gently in a warm breeze, distant acacia trees creating gentle silhouettes against the warm sky, the horizon wide and beautiful. The child named {name} in khaki safari outfit kneeling in the lush golden grass beside Nia — a strikingly beautiful adult zebra with bold crisp black-and-white stripes that catch and reflect the afternoon sunlight in beautiful contrast, tall and elegant, her neck curved gently toward the kneeling child in a tender gesture of connection. The child has just traced a finger along Nia's stripes and now looks up and outward with an expression of pure wonder and enchantment — the moment of discovering the magical shimmer. The zebra's stripes carry a subtle golden magical sheen that shimmers faintly where touched. Heartstone Compass glowing warmly on the child's chest. Vast open savanna behind them. National Geographic quality light and atmosphere. A small soft comic-style speech bubble near the child containing EXACTLY the text "It's glowing...", quiet wonder and curiosity, subtle and not covering the face.""",
            story_text="A beautiful zebra trotted out of the grass. \"I'm Nia—touch my stripes!\" she said. {name} knelt and traced a finger along the bold black and white lines. They shimmered like magic! Nia leaned close and whispered, \"Every stripe holds a secret. Ready to fly, Guardian?\"",
            costume="wearing safari outfit, kneeling beside zebra in golden grass",
            face_expression="pure wonder and delight, eyes wide open looking directly at camera, enchanted smile, face straight forward"
        ),
        PageTemplate(
            page_number=5,
            scene_description="Epic confrontation with the Lion King",
            scene_type="triumph",
            realistic_prompt="""DRAMATIC LION CONFRONTATION SCENE in African savanna at golden hour. Wide tense composition: The African savanna at the most dramatic moment of golden hour — warm amber light washing across the dry golden grass from a low sun. The Great Tree visible as a solitary majestic silhouette on the horizon behind the scene. Acacia trees frame the sides, their shapes iconic against the sky. Dry golden grass, red earth, dust particles catching the warm light. The magnificent Lion King occupies the path ahead — an adult male African lion of commanding presence, a thick and rich golden-brown mane framing a powerful face, intense piercing amber eyes locked in a measured assessment. His stance blocks the path to the Great Tree with confident authority. Thunder rumbles implied in the heavy atmosphere. The child named {name} in khaki safari outfit standing firm on the path, body language showing someone holding their ground despite the enormity of the moment — fists slightly clenched at sides, chin raised, the Heartstone Compass glowing on their chest. Dust settles around both figures. Eye-level composition showing the honest scale relationship between the two. Real wildlife documentary quality. A small soft comic-style speech bubble near the child containing EXACTLY the text "I won't run...", quiet but determined, subtle and not covering the face.""",
            story_text="Suddenly, the ground SHOOK. The mighty Lion King stepped from the shadows, eyes blazing like fire! \"You dare approach the Great Tree?\" he roared. Thunder rumbled. {name}'s heart hammered, but our brave Guardian stood tall anyway. The lion's eyes narrowed. \"Interesting...\"",
            costume="wearing khaki safari outfit with glowing Heartstone Compass pendant",
            face_expression="brave determination mixed with visible nervousness, chin raised, clenched jaw, courageous despite fear"
        ),
        PageTemplate(
            page_number=6,
            scene_description="Earning the Lion King's respect",
            scene_type="triumph",
            realistic_prompt="""POWERFUL CORONATION MOMENT in golden African savanna. Wide deeply emotional composition: The African savanna in magnificent golden light — vast sky in warm amber and gold, grass glowing in the sunset, the Great Tree's silhouette visible at the horizon. The Lion King has lowered his great head in a gesture of profound reverence, his head and magnificent golden mane positioned beside the child's shoulder — his massive mane cascading like a living golden crown around both figures, framing the child beautifully from the side. The lion's wise amber eyes are closed in peaceful acknowledgment. The child named {name} in khaki safari explorer outfit with vest and safari hat, one hand draped naturally at their side near the lion's mane, the other touching the Heartstone Compass on their chest. Natural pose absorbing the magnitude of being recognized as the Guardian, expression of quiet overwhelm and profound pride. The lion's presence frames and elevates the child in the composition. Warm golden sunset light from the west, long shadows across the grass. BBC Earth documentary quality, deeply emotional resonance.""",
            story_text="The Lion King's fierce expression melted into a smile. He lowered his mighty head to {name}'s. \"You didn't run. You didn't cry. You stood your ground.\" His golden mane glowed. \"THAT is what makes a true Guardian, {name}. Welcome to the Great Tree!\"",
            costume="wearing khaki safari explorer outfit with vest, safari hat, and glowing Heartstone Compass",
            face_expression="quiet overwhelm and profound pride, eyes glistening with emotion, soft awed smile, absorbing the magnitude of the moment"
        ),
        PageTemplate(
            page_number=7,
            scene_description="Racing at incredible speed with Jabari the cheetah",
            scene_type="action",
            realistic_prompt="""EXHILARATING AFTERGLOW SCENE in golden African savanna. Wide dynamic composition: The vast African savanna stretching wide and golden in afternoon light. Behind the stationary pair, a dramatic motion-blur trail extends far across the scene toward the horizon — golden light streaks and dust that mark the incredible distance covered in seconds, the visual echo of impossible speed fading into the distance. Dust still settling gently around them, golden particles hanging in the warm air. Jabari is a magnificent adult cheetah in their prime — the fastest creature on earth — sleek spotted coat gleaming in the afternoon light, standing tall and proud beside the child with a naturally satisfied expression. The child named {name} in safari outfit sitting upright on Jabari's back, hair slightly windswept and tousled from the speed, laughing with breathless disbelief and pure joy at what just happened. Natural after-speed pose of someone still processing the extraordinary. Heartstone Compass glowing warmly. Wide open savanna, acacia trees distant. A small soft comic-style speech bubble near the child containing EXACTLY the text "That was incredible!", breathless and laughing, subtle and not covering the face.""",
            story_text="\"Want to feel REAL speed?\" Jabari the cheetah grinned mischievously. Before {name} could answer—WHOOOOSH! They became a BLUR! Faster than anything {name} had ever felt! The world streaked past! \"THIS IS INCREDIBLE!\" {name} screamed with joy! They were practically flying!",
            costume="wearing safari outfit, sitting upright on cheetah, hair tousled from speed",
            face_expression="breathless disbelief and pure laughter, mouth open mid-laugh, eyes wide and sparkling with pure joy"
        ),
        PageTemplate(
            page_number=8,
            scene_description="Magical underwater adventure with Makena the hippo",
            scene_type="wonder",
            realistic_prompt="""MAGICAL UNDERWATER PORTRAIT at golden river hour. Wide serene composition: Crystal-clear river water at sunset — warm golden light from the surface above sends cathedral-like shafts of amber light down through the water, creating dramatic illuminated pillars in the underwater space. The river floor visible below, soft sand and rounded pebbles. Colorful tropical freshwater fish drift in soft focus around the edges of the scene. A stream of magical golden bubbles rises from the Heartstone Compass on the child's chest, creating a trail of light upward. Makena is a massive gentle hippopotamus — enormous and rounded, with a kind broad face and gentle eyes, her skin a beautiful dark grey-brown that the golden underwater light catches and warms. She moves with surprising grace through the water. The child named {name} in safari outfit floating naturally in the water beside Makena, one hand resting gently on the hippo's broad snout in a moment of connection. Natural expression of absolute wonder at floating weightlessly in this warm golden underwater world. BBC Blue Planet quality light and clarity. A small soft comic-style speech bubble near the child containing EXACTLY the text "It's like flying underwater!", amazed and breathless, subtle and not covering the face.""",
            story_text="\"Trust me,\" Makena the hippo winked. She dove deep! {name} held tight—and gasped! Underwater was a glowing golden world! They glided through cathedral rays of light, fish sparkling everywhere! \"It's like flying underwater!\" {name} thought, heart bursting with wonder. Magic was everywhere!",
            costume="wearing safari outfit, floating beside hippo underwater",
            face_expression="absolute wonder and delight, eyes wide open looking at camera, amazed joyful smile, face directly forward"
        ),
        PageTemplate(
            page_number=9,
            scene_description="Receiving the sacred golden feather at the Great Tree ceremony",
            scene_type="bonding",
            realistic_prompt="""MAGICAL GUARDIAN CEREMONY SCENE at the Great Tree. Wide ceremonial composition: The Great Tree — a massive ancient baobab with an enormous trunk and wide-spreading branches, its magical leaves glowing with golden light as the evening comes on, the tree radiating a sense of ancient power and wisdom. Purple-pink twilight sky above with the first stars appearing, adding to the ceremonial atmosphere. The distant circle of savanna animals shown only as soft blurred silhouettes far in the background — a ring of witnesses keeping respectful distance. The Great Owl hovers majestically to one side at eye level, wings spread wide in a ceremonial blessing gesture, extraordinary feathers detailed and beautiful, wise amber eyes radiating pride and recognition. The golden feather already placed in the child's hair above the ear, glowing with soft magical light. The child named {name} in khaki safari explorer outfit standing proudly at the base of the Great Tree, the Heartstone Compass glowing softly on their chest, absorbing the full weight of the ceremony with a natural expression of overwhelming joy and emotion. Natural ceremonial pose of being honored. A small soft comic-style speech bubble near the owl containing EXACTLY the text "You are the Guardian!", wise and ceremonial, subtle and not covering the child's face.""",
            story_text="At the Great Tree, all the animals gathered in a circle. The wise Great Owl flew down, holding a golden feather that sparkled like starlight. \"You showed courage, kindness, and a brave heart,\" she hooted softly. She placed the feather in {name}'s hair. \"You ARE the Guardian!\"",
            costume="wearing khaki safari explorer outfit with vest, golden feather in hair",
            face_expression="overwhelming joy and pride, eyes glistening with emotion, soft awed smile, face straight forward looking at camera"
        ),
        PageTemplate(
            page_number=10,
            scene_description="Home again with magic forever in heart",
            scene_type="resolution",
            realistic_prompt="""PERFECT MAGICAL STORYBOOK ENDING SCENE in cozy bedroom at night. Wide warm atmospheric composition: A child's bedroom at night, warm and personal. The window frames a spectacular star-filled sky — brilliant stars, the sweep of the Milky Way, and among the constellations, the unmistakable outlines of animal friends glowing softly: a lion's mane, an elephant's silhouette, a giraffe's long neck, a zebra's stripes, a cheetah's spotted form — all traced in stardust and twinkling light. The Heartstone Compass rests on the windowsill, glowing warmly with soft golden amber light. Small stuffed safari animals arranged on the bed and shelf. The golden feather tucked behind the child's ear glows with its own soft magical light. The child named {name} in pajamas sitting at the bedroom window, one hand gently touching the golden feather, looking at the animal constellations in the sky outside with a quiet knowing smile of belonging and peace. The cozy room nightlight provides warm amber illumination from inside, while the constellation light provides soft silver rim from the window. Natural pose of contentment and private joy at remembering the adventure.""",
            story_text="The compass glowed one last time—and {name} tumbled back into bed as stars came out! Looking up, {name} gasped with delight—the stars formed all the animal friends, winking! {name} touched the golden feather and smiled. The adventure had just begun!",
            costume="wearing pajamas, golden feather in hair, compass nearby",
            face_expression="peaceful knowing smile, quiet pride and contentment, soft eyes full of wonder"
        ),
    ]
)
