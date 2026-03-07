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
            realistic_prompt="""Magical morning discovery scene. Child {name} in pajamas kneeling on bedroom floor, golden morning light streaming through window. Ancient wooden box with African tribal carvings open before them, revealing the magnificent Heartstone Compass (amber and gold) hovering and pulsing with warm golden light. Tiny golden particles floating like fireflies around it. Child's hands reaching toward it, face turned naturally toward camera at a relaxed 3/4 angle — expression of pure awe and wide-eyed excitement, illuminated beautifully by the magical golden glow of the compass. Child's face is the clear PRIMARY FOCAL POINT, large and clearly detailed. Safari-themed room decorations visible - animal posters, globe on shelf. The compass casts animal-shaped shadows dancing on walls. Dreamy warm lighting with magical golden glow effects. Detailed textures, soft focus background.""",
            story_text="{name} gasped—a mysterious box glowed at the foot of the bed! Inside, the most beautiful compass floated in golden light. The moment {name}'s fingers touched it, the room exploded in swirling light. \"WHOOOOSH!\" The adventure was beginning!",
            costume="wearing pajamas"
        ),

        # === PAGE 2 - MEETING ZARA IN THE STORM === (PREVIEW - Dramatic Arrival)
        PageTemplate(
            page_number=2,
            scene_description="Arriving in savanna and meeting Zara the elephant",
            scene_type="adventure",
            realistic_prompt="""Epic first meeting scene in African savanna. Child {name} wearing khaki safari outfit standing confidently beside ZARA - a magnificent wise African elephant with colorful Maasai beads draped around her neck. Child's face turned naturally toward camera at a relaxed 3/4 angle, expression of amazed wonder and joy, one hand gently touching Zara's trunk in greeting. Zara's trunk curved protectively down toward the child, wise gentle eyes looking down at the young guardian. Magical golden dust particles floating in warm sunset light around them both. Heartstone Compass glowing warmly on child's chest. Acacia trees silhouetted against dramatic orange and purple sunset sky. Golden savanna grass, warm atmospheric lighting. Intimate bonding moment between child and elephant. Child's face is the clear PRIMARY FOCAL POINT, well-lit by warm golden light, face large and clearly detailed. BBC Earth documentary quality. Soft focus background, detailed textures.""",
            story_text="{name} tumbled through spinning light and landed in golden grass! \"Welcome, Guardian!\" rumbled a gentle voice. A magnificent elephant with glowing beads stood before {name}. \"I'm Zara. Quick—we must reach the Great Tree before sunset! Hold tight!\" She knelt. The race was on!",
            costume="wearing khaki safari explorer outfit with vest and hat"
        ),

        # === PAGE 3 - RIDING KITO THROUGH THE CANYON === (PREVIEW - Action)
        PageTemplate(
            page_number=3,
            scene_description="Thrilling ride on Kito the wild horse through canyon",
            scene_type="adventure",
            realistic_prompt="""Heroic portrait scene in African red rock canyon. MEDIUM CLOSE-UP COMPOSITION - Child {name} in khaki safari outfit sitting tall and upright on KITO's back — a powerful wild African horse with golden-brown coat and flowing dark mane. Horse and child positioned so child DIRECTLY FACES THE CAMERA - head straight, no profile, no looking away. Child's face DIRECTLY FACING CAMERA with proud adventurous smile, chin slightly raised, one hand resting on Kito's mane. Child's face is the clear PRIMARY FOCAL POINT - takes up 25-30% of frame height, well-lit by warm golden afternoon light streaming through the canyon. Dramatic red rock canyon walls rise on either side framing the pair. Kito stands steady and powerful beneath child. Golden dust particles catching the canyon light around them. Heartstone Compass glowing warmly on child's chest. Classic hero-on-horseback composition. BBC Earth documentary quality, cinematic lighting, soft focus canyon background, sharp focus on child's face.""",
            story_text="\"The shortcut is through the canyon!\" Kito the wild horse said, kneeling. {name} climbed up—and suddenly they were RACING! The canyon walls blurred past as Kito's hooves thundered on the ground. \"This is AMAZING!\" {name} laughed, holding tight!",
            costume="wearing safari outfit, sitting upright on horse",
            face_expression="proud adventurous smile, exhilarated joy, eyes bright and looking at camera, face directly forward"
        ),

        # === PAGE 4 - DISCOVERING NIA'S STRIPES === (PREVIEW - Wonder Moment)
        PageTemplate(
            page_number=4,
            scene_description="Discovering Nia the zebra's magical stripes up close",
            scene_type="wonder",
            realistic_prompt="""Breathtaking wonder scene in golden African savanna. PORTRAIT COMPOSITION - Child {name} in khaki safari outfit kneeling in lush golden grass with NIA — a strikingly beautiful adult zebra with bold, crisp black-and-white stripes glowing in afternoon sunlight — standing beside the child. Child has just touched Nia's stripes, now FACING DIRECTLY TOWARD THE CAMERA with expression of pure wonder and delight, eyes wide open looking at viewer, enchanted smile. Child's face DIRECTLY FACING CAMERA - head straight, not turned toward zebra, not in profile. Child's face is the clear PRIMARY FOCAL POINT - takes up 25-30% of frame height, beautifully lit by warm golden afternoon light from front. Nia the zebra positioned to the side of child, her neck curved gently toward child in a tender gesture but NOT blocking child's face. Heartstone Compass glowing warmly on child's chest. Zebra's stripes shimmer with subtle magical golden sheen. Vast open savanna behind them — golden grass swaying, distant acacia silhouettes, warm sky. National Geographic wildlife quality, soft focus savanna background, sharp focus on child's face.""",
            story_text="A beautiful zebra trotted out of the grass. \"I'm Nia—touch my stripes!\" she said. {name} knelt and traced a finger along the bold black and white lines. They shimmered like magic! Nia leaned close and whispered, \"Every stripe holds a secret. Ready to fly, Guardian?\"",
            costume="wearing safari outfit, kneeling beside zebra in golden grass",
            face_expression="pure wonder and delight, eyes wide open looking directly at camera, enchanted smile, face straight forward"
        ),

        # === PAGE 5 - THE LION KING BLOCKS THE PATH === (PREVIEW - CLIFFHANGER!)
        PageTemplate(
            page_number=5,
            scene_description="Epic confrontation with the Lion King",
            scene_type="triumph",
            realistic_prompt="""National Geographic award-winning wildlife photography. Dramatic standoff moment in African savanna at golden hour. Child {name} in khaki safari outfit standing bravely facing a magnificent adult male African lion with thick golden-brown mane, intense piercing amber eyes locked onto the child. The Heartstone Compass hanging on child's chest glows with soft warm amber light — the glow illuminating the chest and vest area only, not casting upward onto the face. Lion blocking the path, powerful stance, the Great Tree visible as a distant silhouette behind him. Child standing firm with clenched fists and chin raised despite visible nervousness. Face lit by warm golden sunset light from the side-front, skin tone preserved naturally. Realistic natural savanna setting with dry golden grass, acacia trees, dust particles catching warm sunset light. Eye-level camera angle showing both characters at natural proportionate scale. Dramatic golden rim lighting on lion's magnificent mane. Real wildlife documentary quality lighting and composition. Child's face clearly detailed showing brave determination mixed with fear. Soft focus background, sharp focus on both child and lion.""",
            story_text="Suddenly, the ground SHOOK. The mighty Lion King stepped from the shadows, eyes blazing like fire! \"You dare approach the Great Tree?\" he roared. Thunder rumbled. {name}'s heart hammered, but our brave Guardian stood tall anyway. The lion's eyes narrowed. \"Interesting...\"",
            costume="wearing khaki safari outfit with glowing Heartstone Compass pendant",
            face_expression="brave determination mixed with visible nervousness, chin raised, clenched jaw, courageous despite fear"
        ),

        # === PAGE 6 - THE LION KING'S VICTORY === (PAID - Triumph)
        PageTemplate(
            page_number=6,
            scene_description="Earning the Lion King's respect",
            scene_type="triumph",
            realistic_prompt="""Powerful coronation moment in golden savanna. Child {name} wearing khaki safari explorer outfit with vest and safari hat, standing tall and proud. The magnificent LION KING has bowed his great head low and rests it gently BESIDE the child's shoulder in a reverent gesture of respect — his massive golden mane cascading around the child like a living crown, framing them beautifully. Child's hand draped naturally over the lion's golden mane at their side, other hand touching the glowing Heartstone Compass on their chest. Child's face turned naturally at a relaxed 3/4 angle toward camera — expression of quiet overwhelm, pride, and wonder, absorbing the magnitude of being chosen as Guardian. Child's face is the clear PRIMARY FOCAL POINT, well-lit by warm golden sunset light from the side. Lion's wise amber eyes closed in peaceful reverence. The lion frames and elevates the child rather than competing. Dramatic orange and gold sunset sky behind them. BBC Earth documentary quality, deeply emotional. Soft focus savanna background, sharp focus on child's face.""",
            story_text="The Lion King's fierce expression melted into a smile. He lowered his mighty head to {name}'s. \"You didn't run. You didn't cry. You stood your ground.\" His golden mane glowed. \"THAT is what makes a true Guardian, {name}. Welcome to the Great Tree!\"",
            costume="wearing khaki safari explorer outfit with vest, safari hat, and glowing Heartstone Compass",
            face_expression="quiet overwhelm and profound pride, eyes glistening with emotion, soft awed smile, absorbing the magnitude of the moment"
        ),

        # === PAGE 7 - FLYING WITH JABARI THE CHEETAH === (PAID - Speed Action)
        PageTemplate(
            page_number=7,
            scene_description="Racing at incredible speed with Jabari the cheetah",
            scene_type="action",
            realistic_prompt="""Exhilarating afterglow moment in golden African savanna. Child {name} in khaki safari outfit sitting upright on JABARI's back — sleek powerful spotted cheetah standing proud and still, having just skidded to a breathless stop. Child's face turned naturally toward camera at a relaxed 3/4 angle — expression of pure breathless disbelief and laughter, mouth open mid-laugh, eyes wide and sparkling with pure joy. Hair slightly windswept and tousled from the incredible speed. Child's face is the clear PRIMARY FOCAL POINT, beautifully lit by warm golden afternoon light. Jabari stands tall and satisfied beside them, spots gleaming in sunlight, looking back at child with a proud grin. Behind them stretching far across the savanna: a dramatic golden motion-blur trail — streaks of light and golden dust marking the incredible distance they just covered in seconds, fading into the horizon. Heartstone Compass glowing warmly on child's chest. Dust still settling gently around them, golden particles catching the light. Vast open savanna, acacia trees in distance. Child sitting tall, face large and clearly detailed, taking up 60% of frame height. National Geographic award-winning quality, cinematic composition, soft focus background, sharp focus on child's radiant laughing face.""",
            story_text="\"Want to feel REAL speed?\" Jabari the cheetah grinned mischievously. Before {name} could answer—WHOOOOSH! They became a BLUR! Faster than anything {name} had ever felt! The world streaked past! \"THIS IS INCREDIBLE!\" {name} screamed with joy! They were practically flying!",
            costume="wearing safari outfit, sitting upright on cheetah, hair tousled from speed",
            face_expression="breathless disbelief and pure laughter, mouth open mid-laugh, eyes wide and sparkling with pure joy"
        ),

        # === PAGE 8 - SWIMMING WITH MAKENA THE HIPPO === (PAID - Underwater Wonder)
        PageTemplate(
            page_number=8,
            scene_description="Magical underwater adventure with Makena the hippo",
            scene_type="wonder",
            realistic_prompt="""Magical underwater portrait at golden hour. MEDIUM CLOSE-UP COMPOSITION - Child {name} in safari outfit floating beside MAKENA - massive gentle hippopotamus - both suspended weightlessly in crystal-clear water, FACING THE CAMERA together in a calm serene moment. Child positioned in front of hippo (hippo's large friendly face visible behind and beside child), one hand resting gently on Makena's snout. Child's face DIRECTLY FACING CAMERA - NOT in profile, NOT looking away - with expression of absolute wonder and delight, eyes wide open looking at viewer, mouth slightly open in amazement. Child's face takes up 25-30% of frame height - LARGE AND PROMINENT, well-lit and clearly detailed. Surrounded by stream of magical golden bubbles from Heartstone Compass on chest. Warm golden sunset light rays piercing down through crystal-clear water surface above, creating cathedral-like light beams that illuminate the child's face brightly and clearly from above-front. Child's face is the bright PRIMARY FOCAL POINT against the darker water background. Colorful tropical fish swimming in soft focus around them. Natural skin tones preserved. BBC Blue Planet cinematography quality, soft focus background, sharp focus on child's face.""",
            story_text="\"Trust me,\" Makena the hippo winked. She dove deep! {name} held tight—and gasped! Underwater was a glowing golden world! They glided through cathedral rays of light, fish sparkling everywhere! \"It's like flying underwater!\" {name} thought, heart bursting with wonder. Magic was everywhere!",
            costume="wearing safari outfit, floating beside hippo underwater",
            face_expression="absolute wonder and delight, eyes wide open looking at camera, amazed joyful smile, face directly forward"
        ),

        # === PAGE 9 - THE GUARDIAN'S GOLDEN FEATHER === (PAID - Emotional Ceremony)
        PageTemplate(
            page_number=9,
            scene_description="Receiving the sacred golden feather at the Great Tree ceremony",
            scene_type="bonding",
            realistic_prompt="""Magical ceremony at the Great Tree. PORTRAIT COMPOSITION - Child {name} wearing khaki safari explorer outfit, standing proudly at the base of the Great Tree (massive baobab with golden glowing leaves). The shimmering golden feather ALREADY PLACED in child's hair above the ear, glowing with soft magical light. The GREAT OWL hovering majestically to the side of the child at eye level, wings spread wide in a blessing gesture, wise amber eyes looking at the child with pride. Child's face DIRECTLY FACING THE CAMERA - head straight, no tilt, no turn - with expression of overwhelming joy and pride, eyes glistening with emotion, absorbing the magnitude of being named Guardian. Child's face is the clear PRIMARY FOCAL POINT - takes up 30% of frame height, beautifully lit by warm golden magical glow from the feather and soft twilight ambient light. Owl positioned to the LEFT side, NOT blocking child's face, creating balanced composition. Heartstone Compass glowing softly on chest. Background animals (elephant, zebra, cheetah) shown only as DISTANT BLURRED silhouettes in a circle far behind. Purple-pink twilight sky with first stars appearing. BBC Earth documentary quality, face sharply detailed, soft blur on everything except child and owl.""",
            story_text="At the Great Tree, all the animals gathered in a circle. The wise Great Owl flew down, holding a golden feather that sparkled like starlight. \"You showed courage, kindness, and a brave heart,\" she hooted softly. She placed the feather in {name}'s hair. \"You ARE the Guardian!\"",
            costume="wearing khaki safari explorer outfit with vest, golden feather in hair",
            face_expression="overwhelming joy and pride, eyes glistening with emotion, soft awed smile, face straight forward looking at camera"
        ),

        # === PAGE 10 - THE GUARDIAN RETURNS HOME === (PAID - Resolution)
        PageTemplate(
            page_number=10,
            scene_description="Home again with magic forever in heart",
            scene_type="resolution",
            realistic_prompt="""Perfect magical storybook ending. Child {name} in pajamas sitting at bedroom window at night, facing camera at a relaxed 3/4 angle with a peaceful knowing smile, one hand touching the magnificent golden feather tucked behind their ear. Spectacular star-filled sky with glowing African animal constellations — lion, elephant, giraffe, zebra, cheetah — shimmering in the Milky Way visible through the window to the side. Heartstone Compass on windowsill glowing softly with warm golden light. Small stuffed safari animals on bed behind. Child's face the clear focal point, lit warmly by the soft cozy room nightlight from the front — starlight from the window providing a beautiful silver rim glow from the side, outlining hair and shoulder without washing over the face. Natural skin tone fully preserved. Warm emotional satisfying conclusion. Detailed child's content peaceful face clearly visible, soft focus background.""",
            story_text="The compass glowed one last time—and {name} tumbled back into bed as stars came out! Looking up, {name} gasped with delight—the stars formed all the animal friends, winking! {name} touched the golden feather and smiled. The adventure had just begun!",
            costume="wearing pajamas, golden feather in hair, compass nearby",
            face_expression="peaceful knowing smile, quiet pride and contentment, soft eyes full of wonder"
        ),
    ]
)
