"""
StoryGift Birthday Magic Theme - Magical Birthday Wish.

Complete 10-page story: "[NAME]'s Magical Birthday Wish"
Premium theme featuring birthday celebration, wish fulfillment, and family love.
Optimized for both photorealistic and 3D cartoon pipelines.
"""

from app.stories.templates import StoryTemplate, PageTemplate


STORYGIFT_BIRTHDAY_MAGIC_THEME = StoryTemplate(
    theme_id="storygift_birthday_magic",
    title_template="{name}'s Magical Birthday Wish",
    cover_display_title="Magical Birthday Wish",
    description="The birthday gift that makes their wildest birthday wishes come true",
    default_costume="wearing a special birthday outfit with a golden birthday crown",
    protagonist_description="bright joyful eyes, expression of pure happiness and wonder",
    # Cover page settings for typography-ready composition
    cover_costume="wearing a golden birthday crown and festive party outfit, hands clasped in wish-making pose",
    cover_header_atmosphere="Magical sparkles and confetti swirling in pink, purple, and gold against a dreamy bokeh background of party lights",
    cover_magical_elements="Close-up portrait framing, face filling upper third of image. Eyes closed in wish-making moment with soft smile. Elaborate multi-tiered birthday cake with lit candles creating warm golden glow illuminating face from below. Swirling magical sparkles and confetti emerging from the candles framing the face. Presents wrapped in shimmering paper softly blurred behind. Face is the absolute focal point, sharply detailed with perfect skin texture.",
    cover_footer_description="Colorful balloons floating with glowing strings, magical golden hour party atmosphere",
    pages=[
        # === PAGE 1 - THE SPECIAL DAY ===
        PageTemplate(
            page_number=1,
            scene_description="Magical birthday morning",
            scene_type="discovery",
            realistic_prompt="""Magical morning awakening, medium close-up portrait. The child named {name} sitting up in bed with big excited smile, face prominently filling the frame, sharp focus on facial features. Sunlight streaming through window creating god rays filled with dancing dust particles that look like tiny sparkles, warm light illuminating face. Room decorated with birthday decorations including banner saying 'Happy Birthday!' and balloons tied to bedpost, presents on a table slightly out of focus in background. Child wearing birthday pajamas, stretching arms up in joy. Through window, the world outside looks especially beautiful with bluebird on windowsill. Calendar on wall has today's date circled with hearts. Magical warm lighting, sense of excitement and specialness. Child's face is the absolute focal point, three-quarter view, clearly visible and detailed with sharp skin texture, showing pure birthday joy. A small playful comic-style speech bubble near the child containing EXACTLY the text "It's my birthday!", subtle and not covering the face.""",
            story_text="Today was the most special day of the year—{name}'s birthday! The sun seemed to shine a little brighter, the birds sang a little sweeter, and even the morning air felt like it was full of magic, just for {name}.",
            costume="wearing birthday pajamas"
        ),

        # === PAGE 2 - BIRTHDAY BREAKFAST ===
        PageTemplate(
            page_number=2,
            scene_description="Birthday breakfast wish",
            scene_type="intimate",
            face_expression="concentrated birthday wish, eyes softly closed, peaceful anticipation, gentle smile",
            realistic_prompt="""Warm birthday breakfast scene. Bright kitchen with morning light through window. The child named {name} sitting alone at breakfast table wearing golden paper birthday crown with gems, hands clasped together, eyes softly closed making a wish, gentle peaceful smile on face. In front of them: stack of fluffy pancakes with strawberries, whipped cream, chocolate chips, single lit candle positioned slightly forward and level with child's face, casting warm frontal candlelight that illuminates the face naturally from the front — not harsh upward shadows. Kitchen decorated with homemade birthday decorations, 'Happy Birthday' banner visible. Golden sparkles beginning to swirl around the candle flame subtly. Cozy love-filled atmosphere, warm golden light. Child's face prominently and naturally lit, expression of concentrated wishing clearly visible and detailed. Only the child at the table, no other people visible.""",
            story_text="At breakfast, {name}'s family had prepared a special birthday surprise—pancakes stacked high with {name}'s favorite toppings, and right on top was a single candle. 'Make a wish before breakfast!' said Mom with a warm smile. {name} closed their eyes and wished with all their heart.",
            costume="wearing birthday crown and party outfit"
        ),

        # === PAGE 3 - THE BIRTHDAY FAIRY ===
        PageTemplate(
            page_number=3,
            scene_description="Twinkle the birthday fairy appears",
            scene_type="revelation",
            realistic_prompt="""Fairy appearance magic. The child named {name} at breakfast table, mouth formed in surprised 'O', looking up at a small adorable fairy hovering above the pancakes where the candle smoke is transforming into the magical being. Twinkle the fairy is made of golden and pink sparkles, tiny with delicate iridescent wings, wearing a dress made of wishes and confetti, carrying a small wand topped with a star. Trails of glitter and magical smoke curl around her. Kitchen lighting now has magical quality with floating sparkles, rainbow light refractions on surfaces. The pancake candle is out, smoke still rising and partially formed into magic. Only child and fairy prominent in frame. Whimsical, joyful energy, beautiful particle effects. Child's amazed face clearly visible and detailed, lit by fairy's magical glow. A small playful comic-style speech bubble near the child containing EXACTLY the text "WOW!", subtle and not covering the face.""",
            story_text="When {name} opened their eyes and blew out the candle, something incredible happened! The wish didn't just vanish—it transformed into a shimmering, giggling fairy made of birthday sparkles! 'Hello {name}! I'm Twinkle, your Birthday Wish Fairy, and today, your wishes REALLY come true!'",
            costume="wearing birthday crown"
        ),

        # === PAGE 4 - HOUSE TRANSFORMATION ===
        PageTemplate(
            page_number=4,
            scene_description="House transforms into party palace",
            scene_type="transformation",
            realistic_prompt="""House transformation spectacle. The child named {name} standing in center of living room mid-magical transformation, arms spread wide, face turned toward camera with joyful expression — not in profile, face clearly front-facing or gentle three-quarter view toward viewer. Twinkle the fairy flying circles around them leaving sparkle trails. Furniture rearranging itself with sparkle trails, walls decorating themselves with streamers and colorful lights. A rainbow bouncy castle visible in the background. Chocolate fountain in corner with chocolate flowing, presents floating gently in the air wrapped in shimmering paper. Wide horizontally-framed scene showing the transformation in action, magical particle effects, vibrant party colors. Child's joyful face is the primary focal point, clearly visible and detailed, expression of pure wonder and excitement as the magic transforms around them.""",
            story_text="Twinkle sprinkled fairy dust everywhere, and suddenly {name}'s house began to transform! The living room turned into a magnificent party palace with floating presents, a chocolate fountain taller than Dad, and a bouncy castle that reached the ceiling!",
            costume="wearing birthday outfit with crown"
        ),

        # === PAGE 5 - FRIENDS APPEAR ===
        PageTemplate(
            page_number=5,
            scene_description="Friends appear and pets can talk",
            scene_type="celebration",
            realistic_prompt="""Party celebration moment. The child named {name} in birthday outfit with crown stands front and center, face significantly closer to camera and noticeably larger in frame than anyone else — the unmistakably dominant face. Friends (2-3) appear slightly behind and to the sides, partially blurred, their faces smaller and less prominent. Friends mid-hug and laughing in arrival burst of colorful confetti and sparkles, but child is the clear primary subject. Twinkle the fairy flying above with wand leaving rainbow sparkle trails. Family dog beside them with subtle magical glow, looking animated. Balloons, streamers, presents create festive background. Vibrant party colors, joyful energy. Child's happy laughing face is the absolute focal point, sharply detailed, clearly visible, showing genuine joy at the celebration. Friends are supporting characters only, never competing with child's face. Small playful comic-style speech bubbles from the friends containing EXACTLY the text "Surprise!" and "Happy Birthday!", subtle and not covering the child's face.""",
            story_text="But Twinkle wasn't done! 'What else did you wish for, {name}?' With a wave of her wand, {name}'s friends appeared in a burst of confetti and laughter, ready to celebrate! And look—the family pets could talk for the day! Even the shy goldfish was telling jokes!",
            costume="wearing birthday outfit surrounded by friends"
        ),

        # === PAGE 6 - THE BEST PARTY EVER ===
        PageTemplate(
            page_number=6,
            scene_description="Dance party peak moment",
            scene_type="celebration",
            realistic_prompt="""Dance party celebration. The child named {name} in birthday outfit with crown in the center of the transformed living room, in joyful dance pose with big smile. Twinkle the fairy above, wand creating rainbow light beams and floating musical sparkles. Party decorations with balloons, confetti falling, streamers swirling magically. Magical birthday cake visible in background showing rainbow layers. Pet dog dancing beside the child. Vibrant party atmosphere with movement and energy. Child's joyful dancing face is the focal point, clearly visible and detailed, expression of pure celebration happiness. A small playful comic-style speech bubble near the child containing EXACTLY the text "Best party ever!", subtle and not covering the face.""",
            story_text="The party was amazing! {name} and friends played every game imaginable. They danced with the fairy, ate magical birthday cake that tasted like every flavor they wished for, and when {name} made one more secret wish... Twinkle smiled knowingly and said, 'This one is extra special. Come with me!'",
            costume="wearing birthday outfit with crown, dancing"
        ),

        # === PAGE 7 - FAMILY MEMORIES ===
        PageTemplate(
            page_number=7,
            scene_description="Magical memory gallery",
            scene_type="intimate",
            realistic_prompt="""Magical memory gallery moment. Intimate scene in a glowing golden corridor of floating picture frames. The child named {name} walking through the corridor with family — parents walking beside the child, a sibling holding the child's hand, all looking up at the floating memories together. Each golden picture frame contains a shimmering memory scene from the past year — learning to ride a bike, blowing out last year's candles, a fun day at the park, reading a favorite book. Each memory glows with warm golden light. Twinkle the fairy flying beside {name}, wand creating new memory frames that materialize from sparkles. Words like 'kind', 'brave', 'creative', 'loved' float in beautiful golden calligraphy script between the frames. Family members in soft focus to the sides, looking at memories and at the child with love and pride. Child's face is the clear PRIMARY FOCAL POINT — front-facing toward camera, expression showing overwhelmed happiness, eyes shining with happy tears, lit by warm golden glow from the memories. Warm soft golden hour lighting, intimate composition. Child's emotional joyful face clearly visible and detailed, this is the heart of the story.""",
            story_text="Twinkle led {name} to a quiet room, and with the gentlest magic, created something no gift could ever buy—a perfect moment. There, {name}'s family stood together, and one by one, they each shared their favorite memory of {name} from the past year. Every word sparkled in the air like stars.",
            costume="wearing birthday outfit, walking through memory gallery"
        ),

        # === PAGE 8 - MAGICAL TAPESTRY ===
        PageTemplate(
            page_number=8,
            scene_description="Memories woven into magical tapestry",
            scene_type="wonder",
            realistic_prompt="""Magical tapestry creation. Living room at twilight, party winding down peacefully. Above, Twinkle is weaving together magical ribbons of light in different colors. Each ribbon contains miniature scenes from the day's celebration — dancing, cake, friends laughing, the fairy's first appearance. The ribbons weave into an elaborate glowing tapestry floating like aurora borealis, casting beautiful multi-colored light across the room. The child named {name} standing alone in center of room looking up with wonder and contentment, arms slightly raised in awe, face illuminated by the magical light from above. Through large windows, stars are appearing in the evening sky, moonlight mixing with the magical glow. Beautiful volumetric lighting, spectacular but peaceful. Child's wonder-filled face clearly visible and detailed, looking up at the magical memories. Only child and fairy in the scene. A small gentle comic-style thought bubble near the child containing tiny glowing stars and a heart symbol, subtle and not covering the face.""",
            story_text="As the day turned to evening, Twinkle gathered all the magical moments from {name}'s birthday and wove them into a beautiful glowing tapestry that floated above. 'This,' she said, 'is made of love, laughter, and wishes. It will keep this day alive in your heart forever, {name}.'",
            costume="wearing birthday outfit, looking up in wonder"
        ),

        # === PAGE 9 - GOODBYE TWINKLE ===
        PageTemplate(
            page_number=9,
            scene_description="Twinkle says farewell",
            scene_type="farewell",
            realistic_prompt="""Perfect bedtime farewell. The child named {name} in pajamas sitting on edge of bed in peaceful bedroom with party decorations still visible. Twinkle the fairy hovering at eye level in front of them, both holding hands, looking into each other's eyes with love. Fairy is beginning to dissolve into golden sparkles from feet upward, creating beautiful particle effect. Soft nightlight glow in room, stars through window. On nightstand: birthday crown and a small glowing keepsake from the day's magic. Room quiet and intimate, only child and fairy present. Child's face expression is peaceful, content, full of gratitude, beautifully lit by fairy's gentle glow. Child's face clearly visible and detailed, showing bittersweet emotion. Emotional, frame-worthy image.""",
            story_text="As {name} got ready for bed that night, Twinkle prepared to leave. 'Will I see you again?' asked {name}. The fairy smiled. 'Every birthday, if you believe. But remember—the real magic isn't the wishes that come true. It's knowing how loved you are.' She kissed {name}'s forehead, and in a puff of sparkles, she was gone. But {name} could still feel the magic... because love IS magic, and {name} had so much of it.",
            costume="wearing pajamas, holding hands with fairy"
        ),

        # === PAGE 10 - THE MAGIC OF LOVE ===
        PageTemplate(
            page_number=10,
            scene_description="Peaceful sleep full of love",
            scene_type="sleeping",
            face_expression="drowsy, heavy-lidded, softly dreaming, peaceful smile",
            realistic_prompt="""Perfect storybook ending. The child named {name} in bed, covers tucked up, eyes heavy-lidded and softly closing — drowsy and drifting into peaceful sleep, a gentle content smile on their face. Eyes are NOT squeezed shut but softly and naturally drooping, lashes resting lightly — enough facial feature visibility for a warm, recognizable expression. Illuminated by gentle moonlight from the window casting soft silver light across the face naturally from the side. On the pillow next to them, a single golden sparkle glows gently, the last trace of Twinkle's magic. The birthday crown on the nightstand, a floating balloon settled in the corner. Through the window, a shooting star crosses the night sky, moonlight creates soft patterns on the bed. Above the bed, barely visible, the magical tapestry of memories has transformed into a gentle dream. Warm, safe, peaceful atmosphere. Child's drowsy peaceful face clearly visible and detailed, soft smile showing happy dreams. A faint dreamy comic-style thought bubble above the child showing a tiny fairy and sparkling stars, subtle and not covering the face.""",
            story_text="That night, {name} slept better than ever before, dreaming of dancing fairies and magical wishes. On the nightstand, a single sparkle glowed softly—Twinkle's promise that the magic of birthdays never really ends. Because the best gift of all isn't something you can unwrap. It's being surrounded by people who love you. And {name} had plenty of that.",
            costume="wearing pajamas, peacefully sleeping"
        ),
    ]
)
