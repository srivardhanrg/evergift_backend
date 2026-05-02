"""
StoryGift Birthday Magic Theme - Magical Birthday Wish.

Complete 10-page story: "[NAME]'s Magical Birthday Wish"
Premium theme featuring birthday celebration, wish fulfillment, and family love.
Scene-First composition emphasizing the magic of birthday environments.

KEY PRINCIPLES:
- Wide environmental compositions showcasing birthday wonder
- Natural expressions (joy, surprise, wonder, peace)
- Rich birthday atmosphere with magical lighting
- Child integrated naturally into celebratory environments
- Gender-neutral language throughout
"""

from app.stories.templates import StoryTemplate, PageTemplate


STORYGIFT_BIRTHDAY_MAGIC_THEME = StoryTemplate(
    theme_id="storygift_birthday_magic",
    title_template="{name}'s Magical Birthday Wish",
    cover_display_title="Magical Birthday Wish",
    description="The birthday gift that makes their wildest birthday wishes come true",
    default_costume="wearing a special birthday outfit with a golden birthday crown",
    protagonist_description="bright joyful eyes, expression of pure happiness and wonder",
    cover_costume="wearing a golden birthday crown and festive party outfit, hands clasped in wish-making pose",
    cover_header_atmosphere="Magical sparkles and confetti swirling in pink, purple, and gold against a dreamy bokeh background of party lights",
    cover_magical_elements="Close-up portrait framing, face filling upper third of image. Eyes closed in wish-making moment with soft smile. Elaborate multi-tiered birthday cake with lit candles creating warm golden glow illuminating face from below. Swirling magical sparkles and confetti emerging from the candles framing the face. Presents wrapped in shimmering paper softly blurred behind. Face is the absolute focal point, sharply detailed with perfect skin texture.",
    cover_footer_description="Colorful balloons floating with glowing strings, magical golden hour party atmosphere",
    pages=[
        PageTemplate(
            page_number=1,
            scene_description="Magical birthday morning",
            scene_type="discovery",
            realistic_prompt="""BIRTHDAY MORNING AWAKENING SCENE in sunny decorated bedroom. Wide environmental composition: Cozy bedroom decorated with birthday banners spelling 'Happy Birthday!' in bright colors, balloons tied to the bedpost in pink, gold, and purple, a small stack of wrapped presents visible on a table near the window. Warm morning sunlight streams through the window in golden rays filled with dancing dust particles that shimmer like tiny sparkles, casting long bright beams across the room. Calendar on wall with today's date circled in hearts. A bluebird perches on the windowsill outside. The child named {name} sitting up in bed wearing birthday pajamas, arms stretching upward in joyful morning excitement, taking in the decorated room with a wide happy smile. Natural pose of morning energy and pure delight. Warm golden light fills the scene from the window. Birthday atmosphere of specialness and celebration fills every corner of the room. A small playful comic-style speech bubble near the child containing EXACTLY the text "It's my birthday!", subtle and not covering the face.""",
            story_text="Today was the most special day of the year—{name}'s birthday! The sun seemed to shine a little brighter, the birds sang a little sweeter, and even the morning air felt like it was full of magic, just for {name}.",
            costume="wearing birthday pajamas"
        ),
        PageTemplate(
            page_number=2,
            scene_description="Birthday breakfast wish",
            scene_type="intimate",
            face_expression="concentrated birthday wish, eyes softly closed, peaceful anticipation, gentle smile",
            realistic_prompt="""BIRTHDAY BREAKFAST WISH SCENE in warm family kitchen. Wide environmental composition: Bright cheerful kitchen with morning light pouring through the window, homemade birthday decorations covering the walls — a 'Happy Birthday' banner stretched across the doorway, paper chain garlands in festive colors. A single breakfast setting at the table: stack of golden fluffy pancakes piled high with fresh strawberries, whipped cream swirls, and chocolate chips. A single lit birthday candle stands upright on the top pancake, its flame burning steadily with a small halo of warm golden light spilling forward across the table. The child named {name} sitting alone at the table wearing a golden paper birthday crown with gem stickers, hands clasped together, eyes softly closed in a moment of pure wishing concentration, gentle peaceful smile on their face. Golden sparkles just beginning to swirl gently around the candle flame. Cozy love-filled kitchen atmosphere with only the child at the table.""",
            story_text="At breakfast, {name}'s family had prepared a special birthday surprise—pancakes stacked high with {name}'s favorite toppings, and right on top was a single candle. 'Make a wish before breakfast!' said Mom with a warm smile. {name} closed their eyes and wished with all their heart.",
            costume="wearing birthday crown and party outfit"
        ),
        PageTemplate(
            page_number=3,
            scene_description="Twinkle the birthday fairy appears",
            scene_type="revelation",
            realistic_prompt="""MAGICAL FAIRY APPEARANCE SCENE above birthday breakfast table. Wide dynamic composition: The kitchen breakfast table with pancakes and the just-blown-out birthday candle, a thin thread of smoke curling upward from the wick. The smoke transforms mid-air into swirling golden and pink sparkles that coalesce into Twinkle — a tiny adorable birthday fairy made of light and confetti, wearing a dress fashioned from wishes, with delicate iridescent wings catching the morning light, carrying a small wand topped with a sparkling star. Glitter trails and magical sparkle ribbons spiral outward from her form as she hovers above the pancakes. The kitchen light takes on a warm magical quality with rainbow refractions dancing on the walls and ceiling. The child named {name} wearing birthday crown sitting at the table with mouth forming a wide surprised 'O', chin tilted upward in amazed delight as they discover the fairy materializing from the candle smoke. Whimsical joyful energy, beautiful golden particle effects. Only child and fairy prominent in the frame. A small playful comic-style speech bubble near the child containing EXACTLY the text "WOW!", subtle and not covering the face.""",
            story_text="When {name} opened their eyes and blew out the candle, something incredible happened! The wish didn't just vanish—it transformed into a shimmering, giggling fairy made of birthday sparkles! 'Hello {name}! I'm Twinkle, your Birthday Wish Fairy, and today, your wishes REALLY come true!'",
            costume="wearing birthday crown"
        ),
        PageTemplate(
            page_number=4,
            scene_description="House transforms into party palace",
            scene_type="transformation",
            realistic_prompt="""MAGICAL HOUSE TRANSFORMATION SCENE in living room mid-metamorphosis. Wide environmental composition: The family living room in the midst of spectacular magical change — furniture rearranging itself with sparkle trails, walls adorning themselves with cascading streamers and strings of colorful glowing lights. A rainbow bouncy castle materializes in the background, its colorful pillars reaching toward the ceiling. A tall chocolate fountain bubbles in the corner, rich dark chocolate flowing. Wrapped presents in shimmering iridescent paper drift and float gently through the air. Confetti rains down from above in every color. Twinkle the fairy swooping in arcing loops around the room, wand trailing long ribbons of golden sparkles that leave glowing after-images. The child named {name} standing in the center of it all in birthday outfit with crown, arms spread wide, turning to take in the magical transformation happening all around them with an expression of pure laughing wonder and disbelief. Vibrant party colors fill every surface, magical particle effects and swirling light saturate the atmosphere.""",
            story_text="Twinkle sprinkled fairy dust everywhere, and suddenly {name}'s house began to transform! The living room turned into a magnificent party palace with floating presents, a chocolate fountain taller than Dad, and a bouncy castle that reached the ceiling!",
            costume="wearing birthday outfit with crown"
        ),
        PageTemplate(
            page_number=5,
            scene_description="Friends appear and pets can talk",
            scene_type="celebration",
            realistic_prompt="""JOYFUL FRIENDS ARRIVAL SCENE in transformed party palace living room. Wide celebratory composition: The magically transformed living room decorated with cascading balloons, swirling streamers, and floating presents — a vibrant party scene in full swing. A burst of colorful confetti and sparkles fills the air from a magical entry point as 2-3 friends arrive mid-laugh, arms reaching out for hugs, faces bright with joy. Twinkle the fairy flying above the group, wand leaving rainbow sparkle trails that arc across the ceiling. The family dog stands nearby with a soft magical glow around them, animated and cheerful. The child named {name} in birthday outfit with crown positioned at the center of the welcome scene, laughing with arms open to greet their arriving friends, the natural hub of all the celebration energy. Vibrant party colors and joyful energy in every corner. Small playful comic-style speech bubbles from the friends containing EXACTLY the text "Surprise!" and "Happy Birthday!", subtle and not covering the child's face.""",
            story_text="But Twinkle wasn't done! 'What else did you wish for, {name}?' With a wave of her wand, {name}'s friends appeared in a burst of confetti and laughter, ready to celebrate! And look—the family pets could talk for the day! Even the shy goldfish was telling jokes!",
            costume="wearing birthday outfit surrounded by friends"
        ),
        PageTemplate(
            page_number=6,
            scene_description="Dance party peak moment",
            scene_type="celebration",
            realistic_prompt="""PEAK DANCE PARTY SCENE in magical transformed living room. Wide dynamic composition: The transformed living room at maximum celebration energy — balloons clustered at the ceiling, confetti falling in slow sparkling rain, streamers swirling magically in the air. Twinkle the fairy hovering above the scene, wand creating rainbow light beams that shoot across the room and burst into floating musical sparkles where they land. A magnificent birthday cake visible in the background, its multiple layers striped in rainbow colors. The family dog dancing joyfully beside the child. The child named {name} in birthday outfit with crown at the center of the dance floor in an exuberant dance pose — one arm raised, head back, big smile, full of the moment. Natural expression of pure birthday celebration happiness. The whole scene vibrates with movement, color, and festive energy. A small playful comic-style speech bubble near the child containing EXACTLY the text "Best party ever!", subtle and not covering the face.""",
            story_text="The party was amazing! {name} and friends played every game imaginable. They danced with the fairy, ate magical birthday cake that tasted like every flavor they wished for, and when {name} made one more secret wish... Twinkle smiled knowingly and said, 'This one is extra special. Come with me!'",
            costume="wearing birthday outfit with crown, dancing"
        ),
        PageTemplate(
            page_number=7,
            scene_description="Magical memory gallery",
            scene_type="intimate",
            realistic_prompt="""MAGICAL MEMORY GALLERY SCENE in glowing golden corridor. Wide emotional composition: A luminous corridor lined on both sides with floating golden picture frames, each one radiating warm soft light. Each frame contains a shimmering memory scene brought to life — a child learning to ride a bike, a family birthday with candles glowing, a fun day at the park with laughter, a cozy reading moment. The frames hover at different heights, some tilted gently, creating a living gallery that extends warmly into the distance. Calligraphy words drift between the frames in glowing golden script — 'kind', 'brave', 'creative', 'loved' — each one softly luminous. Twinkle the fairy glides beside the group leaving sparkle trails, her wand materializing new memory frames from thin air. The child named {name} in birthday outfit walking through the corridor surrounded by parents and a sibling who holds their hand, all looking upward at the floating memory frames together. The golden memory glow illuminates their upturned faces. Warm golden light, intimate and deeply emotional composition.""",
            story_text="Twinkle led {name} to a quiet room, and with the gentlest magic, created something no gift could ever buy—a perfect moment. There, {name}'s family stood together, and one by one, they each shared their favorite memory of {name} from the past year. Every word sparkled in the air like stars.",
            costume="wearing birthday outfit, walking through memory gallery"
        ),
        PageTemplate(
            page_number=8,
            scene_description="Memories woven into magical tapestry",
            scene_type="wonder",
            realistic_prompt="""MAGICAL TAPESTRY WEAVING SCENE in transformed living room at twilight. Wide atmospheric composition: The living room at peaceful golden twilight, the party gently winding down. Soft warm interior light mixes with the fading blue of evening through large windows, the first stars appearing outside. Above the room, Twinkle weaves together ribbons of living light in different colors — each ribbon containing a tiny luminous scene from the day: dancing, cake cutting, friends laughing, the fairy's first dramatic appearance. The ribbons spiral and interweave into an elaborate glowing tapestry that floats and shimmers like a personal aurora borealis, casting beautiful multi-colored patterns across the walls, ceiling, and floor of the room. The child named {name} in birthday outfit standing alone in the center of the room, both arms slightly raised and outward in natural awe, looking upward to watch the tapestry form above them. The magical tapestry light washes softly over the entire scene. A small gentle comic-style thought bubble near the child containing tiny glowing stars and a heart symbol, subtle and not covering the face.""",
            story_text="As the day turned to evening, Twinkle gathered all the magical moments from {name}'s birthday and wove them into a beautiful glowing tapestry that floated above. 'This,' she said, 'is made of love, laughter, and wishes. It will keep this day alive in your heart forever, {name}.'",
            costume="wearing birthday outfit, looking up in wonder"
        ),
        PageTemplate(
            page_number=9,
            scene_description="Twinkle says farewell",
            scene_type="farewell",
            realistic_prompt="""TENDER FAREWELL SCENE in quiet peaceful bedroom at night. Wide intimate composition: A child's bedroom at night, soft nightlight casting warm gentle amber glow. Birthday decorations still cheerfully adorning the walls and doorframe. On the nightstand: the golden birthday crown resting beside a small luminous keepsake — the last glowing trace of the day's magic. Stars visible through the window, the world outside quiet and still. The child named {name} in pajamas sitting on the edge of the bed, reaching out toward Twinkle the fairy who hovers at eye level just in front of them, their hands gently clasped together in a farewell hold. Twinkle beginning to dissolve from her feet upward into rising streams of golden sparkles, the dissolution creating a soft upward light show of particles that drift toward the ceiling. Both child and fairy looking at each other with warmth and deep affection. Only the two of them in the intimate frame. The fairy's gentle dissolving glow illuminates the scene with soft golden light. Quiet, emotional, frame-worthy moment.""",
            story_text="As {name} got ready for bed that night, Twinkle prepared to leave. 'Will I see you again?' asked {name}. The fairy smiled. 'Every birthday, if you believe. But remember—the real magic isn't the wishes that come true. It's knowing how loved you are.' She kissed {name}'s forehead, and in a puff of sparkles, she was gone. But {name} could still feel the magic... because love IS magic, and {name} had so much of it.",
            costume="wearing pajamas, holding hands with fairy"
        ),
        PageTemplate(
            page_number=10,
            scene_description="Peaceful sleep full of love",
            scene_type="sleeping",
            face_expression="drowsy, heavy-lidded, softly dreaming, peaceful smile",
            realistic_prompt="""PEACEFUL BIRTHDAY BEDTIME SCENE in cozy bedroom at night. Wide warm composition: A child's bedroom at night, comforting and safe. Soft moonlight streams through the window casting gentle silver patterns across the bedding and floor. A single golden sparkle glows on the pillow — the very last trace of Twinkle's magic, pulsing softly. The birthday crown rests on the nightstand. A drifting balloon has settled gently in the corner. Through the window, a shooting star arcs silently across the night sky. Above the bed, barely visible, the magical memory tapestry has transformed into the softest dream mist, shapes of friends and a tiny fairy visible within it. The child named {name} tucked snugly under the covers in pajamas, head resting on the pillow beside the glowing golden sparkle, eyes heavy-lidded and softly drooping as sleep naturally arrives — lashes resting gently, a soft content smile on their face, drifting toward happy dreams. Moonlight from the window illuminates the scene in soft silver tones. A faint dreamy comic-style thought bubble above the child showing a tiny fairy and sparkling stars, subtle and not covering the face.""",
            story_text="That night, {name} slept better than ever before, dreaming of dancing fairies and magical wishes. On the nightstand, a single sparkle glowed softly—Twinkle's promise that the magic of birthdays never really ends. Because the best gift of all isn't something you can unwrap. It's being surrounded by people who love you. And {name} had plenty of that.",
            costume="wearing pajamas, peacefully sleeping"
        ),
    ]
)
