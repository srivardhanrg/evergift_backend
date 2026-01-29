"""
StoryGift Safari Adventure Theme - African Savanna Adventure.

Complete 10-page story: "[NAME]'s Wild Safari Adventure"
Premium adventure story featuring different African animals on each page - elephant, giraffe, zebra, lion, cheetah, hippo.
Each page = 1-2 characters max for perfect facial consistency with NanoBana.
Optimized for exciting narrative flow with wow factor moments.

CONVERSION OPTIMIZATION:
- Pages 1-5 (Preview): Thrilling animal encounters, ends with Lion King confrontation cliffhanger
- Pages 6-10 (Paid): Victory, speed racing, underwater adventure, emotional ceremony
"""

from app.stories.templates import StoryTemplate, PageTemplate


STORYGIFT_SAFARI_ADVENTURE_THEME = StoryTemplate(
    theme_id="storygift_safari_adventure",
    title_template="{name}'s Wild Safari Adventure",
    description="Where the wild things know your name - become the chosen Safari Guardian",
    default_costume="wearing khaki safari explorer outfit with adventure vest, boots, and explorer hat",
    protagonist_description="bright adventurous eyes, expression of wonder and courage",
    # Cover page settings for typography-ready composition
    cover_costume="wearing premium khaki safari outfit with golden compass pendant glowing on chest, adventure vest with pockets, sturdy boots, and explorer hat tilted heroically",
    cover_header_atmosphere="Golden African sunset with dramatic orange and purple clouds, acacia tree silhouettes against the sky, birds flying in formation",
    cover_magical_elements="Majestic elephant Zara with colorful Maasai beads standing protectively behind the child. A proud lion with golden mane on one side. Giraffes, zebras, and colorful birds creating a frame. The magical Heartstone Compass glowing golden on child's chest. Warm rim lighting creates epic silhouette.",
    cover_footer_description="Golden savanna grass swaying, dust particles catching sunset light, animal footprints in red earth",
    pages=[
        # === PAGE 1 - THE HEARTSTONE COMPASS === (PREVIEW - Discovery)
        PageTemplate(
            page_number=1,
            scene_description="Discovering the magical Heartstone Compass",
            scene_type="discovery",
            realistic_prompt="""Magical morning discovery scene. Child {name} in pajamas kneeling on bedroom floor, golden morning light streaming through window. Ancient wooden box with African tribal carvings open before them, revealing the magnificent Heartstone Compass (amber and gold) hovering and pulsing with warm golden light. Tiny golden particles floating like fireflies around it. Child's hands reaching toward it with pure wonder and amazement, face illuminated by magical glow. Safari-themed room decorations visible - animal posters, globe on shelf. The compass casts animal-shaped shadows dancing on walls. Dreamy warm lighting with magical golden glow effects. Child's face showing awe and excitement. Detailed textures, soft focus background.""",
            story_text="{name} gasped—a mysterious box glowed at the foot of the bed! Inside, the most beautiful compass floated in golden light. The moment {name}'s fingers touched it, the room exploded in swirling light. \"WHOOOOSH!\" The adventure was beginning!",
            costume="wearing pajamas"
        ),

        # === PAGE 2 - MEETING ZARA IN THE STORM === (PREVIEW - Dramatic Arrival)
        PageTemplate(
            page_number=2,
            scene_description="Arriving in savanna and meeting Zara the elephant",
            scene_type="adventure",
            realistic_prompt="""Epic first meeting scene in African savanna. Child {name} wearing khaki safari outfit standing confidently beside ZARA - a magnificent wise African elephant with colorful Maasai beads draped around her neck. Child looking up at Zara with amazed wonder, one hand gently touching her trunk in greeting. Zara's trunk curved protectively near child, wise gentle eyes looking down at the young guardian. Magical golden dust particles floating in warm sunset light around them both. Heartstone Compass glowing warmly on child's chest. Acacia trees silhouetted against dramatic orange and purple sunset sky. Golden savanna grass, warm atmospheric lighting. Intimate bonding moment between child and elephant. Child's face clearly visible showing wonder and connection, front-facing three-quarter view. BBC Earth documentary quality. Soft focus background, detailed textures.""",
            story_text="{name} tumbled through spinning light and landed in golden grass! \"Welcome, Guardian!\" rumbled a gentle voice. A magnificent elephant with glowing beads stood before {name}. \"I'm Zara. Quick—we must reach the Great Tree before sunset! Hold tight!\" She knelt. The race was on!",
            costume="wearing khaki safari explorer outfit with vest and hat"
        ),

        # === PAGE 3 - RIDING KITO THROUGH THE CANYON === (PREVIEW - Action)
        PageTemplate(
            page_number=3,
            scene_description="Thrilling ride on Kito the wild horse through canyon",
            scene_type="adventure",
            realistic_prompt="""Thrilling action scene in African canyon. Child {name} in safari outfit riding on KITO's back - a powerful wild African horse with golden-brown coat and flowing dark mane, galloping through narrow red rock canyon. Child sitting tall on horse's back, hands gripping mane, leaning slightly forward with excited smile and windswept hair. Child positioned prominently in upper half of frame, face clearly visible and detailed. Rocky canyon walls on either side creating dramatic framing. Warm golden afternoon light streaming through canyon, dust clouds behind horse's hooves. Dynamic motion composition with child as the clear focal point. Child's joyful excited expression front-facing. National Geographic action quality, cinematic lighting, soft focus background.""",
            story_text="\"The shortcut is through the canyon!\" Kito the wild horse said, kneeling. {name} climbed up—and suddenly they were RACING! The canyon walls blurred past as Kito's hooves thundered on the ground. \"This is AMAZING!\" {name} laughed, holding tight!",
            costume="wearing safari outfit, riding on horse's back"
        ),

        # === PAGE 4 - RACING WITH NIA THE ZEBRA === (PREVIEW - Speed Action)
        PageTemplate(
            page_number=4,
            scene_description="Racing across the plains on Nia the zebra",
            scene_type="action",
            realistic_prompt="""Dynamic high-speed action scene. Child {name} in safari outfit riding on NIA's back - beautiful zebra with striking bold stripes, running at full gallop across golden savanna plains. Child leaning forward, both hands holding zebra's mane, expression of thrilling excitement and laughter. Wind dramatically blowing child's hair back. Heartstone Compass streaming golden light trail. Motion blur in background grass, dust cloud behind them. Golden afternoon dramatic light. Only child riding zebra, powerful two-character action composition. Child's face showing pure joy and adrenaline, clearly detailed. National Geographic wildlife action quality, energy and movement, soft focus background.""",
            story_text="\"The Great Tree is far—we need speed!\" Nia the zebra grinned. \"Hang on, Guardian!\" They EXPLODED into a run! The world became a golden blur! {name} whooped with joy—they were flying across the savanna! Nia was faster than the wind!",
            costume="wearing safari outfit, riding on zebra, hair blown by wind"
        ),

        # === PAGE 5 - THE LION KING BLOCKS THE PATH === (PREVIEW - CLIFFHANGER!)
        PageTemplate(
            page_number=5,
            scene_description="Epic confrontation with the Lion King",
            scene_type="triumph",
            realistic_prompt="""National Geographic award-winning wildlife photography. Dramatic standoff moment in African savanna at golden hour. Child {name} in khaki safari outfit standing bravely facing a magnificent adult male African lion with thick golden-brown mane, intense piercing amber eyes locked onto the child. The Heartstone Compass hanging on child's chest glows with soft warm amber light, casting gentle golden illumination on child's determined face. Lion blocking the path, powerful stance, the Great Tree visible as a distant silhouette behind him. Child standing firm with clenched fists and chin raised despite visible nervousness. Realistic natural savanna setting with dry golden grass, acacia trees, dust particles catching warm sunset light. Eye-level camera angle showing both characters at natural proportionate scale. Dramatic golden rim lighting on lion's magnificent mane. Real wildlife documentary quality lighting and composition. Child's face clearly detailed showing brave determination mixed with fear. Soft focus background, sharp focus on both child and lion.""",
            story_text="Suddenly, the ground SHOOK. The mighty Lion King stepped from the shadows, eyes blazing like fire! \"You dare approach the Great Tree?\" he roared. Thunder rumbled. {name}'s heart hammered, but our brave Guardian stood tall anyway. The lion's eyes narrowed. \"Interesting...\"",
            costume="wearing khaki safari outfit with glowing Heartstone Compass pendant"
        ),

        # === PAGE 6 - THE LION KING'S VICTORY === (PAID - Triumph)
        PageTemplate(
            page_number=6,
            scene_description="Earning the Lion King's respect",
            scene_type="triumph",
            realistic_prompt="""Powerful triumphant moment in golden savanna. Child {name} wearing khaki safari explorer outfit with vest and safari hat, standing face-to-face with the magnificent LION KING who has lowered his great head to child's level. Child's small hand placed gently on lion's golden-maned forehead in sacred connection. Lion's wise amber eyes closed in peaceful respect. Heartstone Compass on child's chest glowing with warm golden light, creating soft halo around them both. Dramatic sunset behind them with orange and gold sky. Child's face showing quiet pride and wonder, three-quarter front view, clearly detailed. Intimate powerful composition, eye-level perspective. Golden rim light on lion's majestic mane. BBC Earth documentary quality, emotional connection captured. Soft focus savanna background.""",
            story_text="The Lion King's fierce expression melted into a smile. He lowered his mighty head to {name}'s. \"You didn't run. You didn't cry. You stood your ground.\" His golden mane glowed. \"THAT is what makes a true Guardian, {name}. Welcome to the Great Tree!\"",
            costume="wearing khaki safari explorer outfit with vest, safari hat, and glowing Heartstone Compass"
        ),

        # === PAGE 7 - FLYING WITH JABARI THE CHEETAH === (PAID - Speed Action)
        PageTemplate(
            page_number=7,
            scene_description="Racing at incredible speed with Jabari the cheetah",
            scene_type="action",
            realistic_prompt="""Explosive speed action scene. Child {name} in safari outfit riding low on JABARI's back - sleek powerful spotted cheetah at absolute maximum sprint, muscles rippling, running faster than wind. Child crouched forward aerodynamically, holding cheetah's neck, hair streaming back, face showing pure exhilaration mixed with slight terror. Heartstone Compass blazing golden speed trail behind them. Extreme motion blur on background, savanna becoming streaks of gold. Dust and grass exploding behind. Golden afternoon light. Only child and cheetah, explosive two-character speed composition. Child's thrilled face detailed. Award-winning wildlife action photography quality, incredible energy, soft focus background.""",
            story_text="\"Want to feel REAL speed?\" Jabari the cheetah grinned mischievously. Before {name} could answer—WHOOOOSH! They became a BLUR! Faster than anything {name} had ever felt! The world streaked past! \"THIS IS INCREDIBLE!\" {name} screamed with joy! They were practically flying!",
            costume="wearing safari outfit, riding cheetah, hair streaming back"
        ),

        # === PAGE 8 - SWIMMING WITH MAKENA THE HIPPO === (PAID - Underwater Wonder)
        PageTemplate(
            page_number=8,
            scene_description="Magical underwater adventure with Makena the hippo",
            scene_type="wonder",
            realistic_prompt="""Magical underwater scene at golden hour. Child {name} in safari outfit riding on MAKENA's back - massive gentle hippopotamus swimming gracefully underwater. Child holding hippo's back, surrounded by stream of magical golden bubbles from Heartstone Compass. Shafts of golden sunset light piercing down through water surface above, creating cathedral-like light rays. Fish swimming around them. Child's face visible underwater, eyes wide with wonder and delight. Only child riding hippo, mystical serene two-character composition. Underwater plants swaying. Detailed child's amazed expression. Magical underwater cinematography like BBC Blue Planet, soft focus background.""",
            story_text="\"Trust me,\" Makena the hippo winked. She dove deep! {name} held tight—and gasped! Underwater was a glowing golden world! They glided through cathedral rays of light, fish sparkling everywhere! \"It's like flying underwater!\" {name} thought, heart bursting with wonder. Magic was everywhere!",
            costume="wearing safari outfit, riding hippo underwater"
        ),

        # === PAGE 9 - THE GUARDIAN'S GOLDEN FEATHER === (PAID - Emotional Ceremony)
        PageTemplate(
            page_number=9,
            scene_description="Receiving the sacred golden feather at the Great Tree ceremony",
            scene_type="bonding",
            realistic_prompt="""Magical ceremony at the Great Tree. CHILD {name} IS THE CLEAR FOCAL POINT - wearing khaki safari explorer outfit, standing prominently in foreground at the base of the Great Tree (massive baobab with golden glowing leaves). A golden owl perched on branch above, presenting shimmering golden feather downward to child. Child's face is the PRIMARY FOCUS - well-lit by warm golden magical glow from the feather and compass, three-quarter front view looking up with overwhelming joy and pride, detailed facial features. Background animals (elephant, zebra, cheetah) shown only as DISTANT BLURRED silhouettes far behind, out of focus. Purple-pink twilight sky with first stars. Heartstone Compass glowing on child's chest illuminating face from below. Child takes up 60% of frame height, face large and clearly detailed. Medium close-up composition centered on child. BBC Earth documentary quality, face dramatically lit, very soft blur on everything except child.""",
            story_text="At the Great Tree, all the animals gathered in a circle. The wise Great Owl flew down, holding a golden feather that sparkled like starlight. \"You showed courage, kindness, and a brave heart,\" she hooted softly. She placed the feather in {name}'s hair. \"You ARE the Guardian!\"",
            costume="wearing khaki safari explorer outfit with vest, receiving golden feather from owl"
        ),

        # === PAGE 10 - THE GUARDIAN RETURNS HOME === (PAID - Resolution)
        PageTemplate(
            page_number=10,
            scene_description="Home again with magic forever in heart",
            scene_type="resolution",
            realistic_prompt="""Perfect magical storybook ending. Child {name} in pajamas sitting at bedroom window at night, looking up at spectacular star-filled sky with expression of peaceful joy and wonder. Heartstone Compass on windowsill glowing softly with warm golden light. Magnificent golden feather tucked behind ear, also glowing. Stars in sky arranged into beautiful African animal constellations - lion, elephant, giraffe, zebra, cheetah clearly visible across the Milky Way, subtly glowing. Small stuffed safari animals on bed behind. Child with peaceful knowing smile, one hand touching the glowing feather. Soft cozy nightlight glow, magical starlight streaming through window. Warm emotional satisfying conclusion. Detailed child's content peaceful face, soft focus background.""",
            story_text="The compass glowed one last time—and {name} tumbled back into bed as stars came out! Looking up, {name} gasped with delight—the stars formed all the animal friends, winking! {name} touched the golden feather and smiled. The adventure had just begun!",
            costume="wearing pajamas, golden feather in hair, compass nearby"
        ),
    ]
)
