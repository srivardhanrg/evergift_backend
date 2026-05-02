"""
StoryGift Magic Castle Theme - Converted to Magictales format.

Complete 10-page story: "The First Day of Magic School"
Converted from StoryGift's 5 scenes × 2 panels structure
Preserves all original prompts, dialogue, and story narrative
"""

from app.stories.templates import StoryTemplate, PageTemplate


STORYGIFT_MAGIC_CASTLE_THEME = StoryTemplate(
    theme_id="storygift_magic_castle",
    title_template="{name}'s First Day of Magic School",
    cover_display_title="First Day of Magic School",
    description="A detailed magical academy adventure",
    default_costume="wearing wizard robes",
    protagonist_description="bright expressive eyes, curious and brave expression",
    cover_costume="wearing elegant purple and gold wizard robes with magical embroidered patterns, a flowing cape, and holding a glowing wand",
    cover_header_atmosphere="Majestic magical castle towers rising into a mystical purple twilight sky with stars and magical aurora, castle spires fading into elegant mist",
    cover_magical_elements="Glowing magical orbs float gently around the child's body (not face). Professor Hoot the wise owl perches on a nearby pillar. Sparky the baby dragon peeks from behind. Magical sparkles and wisps dance in the air.",
    cover_footer_description="Polished marble castle courtyard floor with magical glowing runes, ancient stone steps leading to grand doors",
    pages=[
        PageTemplate(
            page_number=1,
            scene_description="Arrival at the magic school gates",
            scene_type="arrival",
            realistic_prompt="""DRAMATIC MAGIC SCHOOL ARRIVAL SCENE at gothic castle gates. Wide cinematic environmental composition: The Grand Academy of Arcane Arts looms impressively in morning mist — massive iron gates crafted from dark twisted metal rise to an imposing height, castle towers disappearing into swirling mist above. Ancient stone walls covered in climbing ivy, magical runes faintly glowing on the gateposts. Morning mist clings to the cobblestone path leading to the entrance, golden rays of morning sunlight breaking through from behind the castle, creating dramatic god rays through the haze. Professor Hoot — a giant ancient brown owl wearing large round reading glasses and a small black graduation cap — sits on a high stone pedestal to one side, watching the entrance with wise calm eyes. The child named {name} standing in the foreground in elegant wizard robes, taking in the full enormity of the castle gate above and around them, expression of awe and nervous excitement at arriving at this magnificent place. Natural first-day pose of wonder and anticipation.""",
            story_text="The morning mist clung to the cobblestones as the Grand Academy of Arcane Arts finally came into view. Standing before the massive iron gates was the school's oldest guardian. Professor Hoot was not merely an owl; he was a giant, ancient sentinel wearing thick spectacles.",
            costume="wearing wizard robes",
            face_expression="wide-eyed awe and nervous excitement, eyebrows slightly raised, mouth slightly open in wonder"
        ),
        PageTemplate(
            page_number=2,
            scene_description="Casting the unlock spell",
            scene_type="arrival",
            realistic_prompt="""MAGICAL SPELL-CASTING SCENE at the ancient iron gates. Wide dynamic composition: The massive ancient iron gate lock dominates the scene — ornate and heavily aged metal, glowing with pulsing golden magical energy as a spell takes hold. Brilliant golden sparks and magical light burst outward from the lock mechanism, illuminating the surrounding stone and the misty morning air. Professor Hoot visible as a large wise presence in the background, adjusting his thick round glasses with a wing tip and watching the moment with quiet approval, graduation cap tilted slightly. The child named {name} in elegant wizard robes standing before the gates with wand extended forward, sparks erupting dramatically from the wand tip in a cascade of golden light. Natural spell-casting stance with arm extended and body leaning slightly forward in concentration and determination. The golden magical glow from the exploding lock lights the scene dramatically. Morning mist swirls around the stone pillars. A small bold comic-style speech bubble near the child containing EXACTLY the text "Alohomora!", subtle and not covering the face.""",
            story_text="He adjusted his glasses with a wing tip and peered down. The test had begun before the first step was even taken. 'Only the worthy may pass,' hooted Professor Hoot as {name} shouted 'ALOHOMORA!' and magic sparks illuminated the ancient lock.",
            costume="wearing wizard robes",
            face_expression="fierce concentration and determination, eyes focused with intensity, jaw set with resolve"
        ),
        PageTemplate(
            page_number=3,
            scene_description="Beast Taming class begins",
            scene_type="action",
            realistic_prompt="""BEAST TAMING CLASS SCENE in castle courtyard. Wide environmental composition: A stone castle courtyard with ancient walls and arched passageways surrounding the scene, morning light angling down between the towers. In the center background, a large reinforced wooden crate shakes violently — the wooden slats rattling and straining, purple smoke leaking dramatically from every crack and gap, spilling across the cobblestone ground. Other students visible in the middle ground, backing away with expressions of alarm and curiosity, their wizard robes swirling as they step back. The air is thick with magical tension and the faint scent of whatever is inside the crate. The child named {name} standing in the foreground in wizard robes, wand at their side, facing the scene with natural nervous anticipation and curious watchfulness. Stone castle walls frame the scene on all sides, a stone fountain or archway providing architectural detail. Atmospheric misty morning quality in the courtyard light.""",
            story_text="The courtyard was buzzing as the Beast Taming class began. In the center sat a wooden crate that shook violently. Purple smoke leaked from every crack as students backed away nervously. 'It's gonna blow!' someone shouted.",
            costume="wearing wizard robes",
            face_expression="nervous anticipation and cautious curiosity, slightly tensed expression, alert and watchful"
        ),
        PageTemplate(
            page_number=4,
            scene_description="Meeting Sparky the dragon",
            scene_type="bonding",
            realistic_prompt="""HEARTWARMING DRAGON BONDING SCENE in stone castle courtyard. Wide warm composition: The cobblestone courtyard in afternoon light, the opened wooden crate visible in the background with its lid flung aside. Warm sunlight filtering between the castle towers creates a golden glow across the courtyard. Sparky — a tiny adorable baby dragon in vibrant red with small bright orange wings and a round friendly face — perched on the child's shoulder with one small claw holding gently to the shoulder, nuzzling their neck with affectionate curiosity, each small hiccup producing a charming puff of smoke ring that drifts upward. The dragon is small and positioned entirely to the side, creating a natural companion pose without obstructing anything. The child named {name} in wizard robes standing in the courtyard with a warm gentle smile, one hand raised slightly toward the dragon in a tender greeting gesture. Natural moment of unexpected connection between child and dragon. Warm afternoon castle light. A small gentle comic-style speech bubble near the child containing EXACTLY the text "You're not scary…", subtle and not covering the face.""",
            story_text="With a pop, the lid flew open, revealing Sparky—a baby dragon with the hiccups. Every time he hiccuped, a smoke ring puffed from his nose. He wasn't scary; he was just hungry. '{name} offered a treat, realizing 'You're just hungry, aren't you?'",
            costume="wearing wizard robes",
            face_expression="gentle smile, warm compassion, wide-eyed wonder, affectionate"
        ),
        PageTemplate(
            page_number=5,
            scene_description="Learning to fly on broomstick",
            scene_type="action",
            realistic_prompt="""MAGICAL FIRST FLIGHT SCENE on the school grounds. Wide dynamic composition: The open grassy school grounds in afternoon light, castle walls framing the background. A wooden broomstick — smooth polished wood with a bound bundle of twigs at the end — hovers about a foot above the green grass, vibrating with living magical energy, small motes of golden magical light swirling around the stick's length. Dust and grass blades swirl gently beneath it in the levitation field. The child named {name} sitting tall and upright on the hovering broomstick in wizard robes, one hand gripping the handle at their side, the other raised slightly in triumphant readiness, chin tilted with confidence. Natural riding pose of someone finding their balance and preparing to soar. Robes and hair stirring gently from the magical energy below. Other students visible in the far background, some wobbling, others watching. The warm afternoon school grounds light creates a golden atmosphere. A small confident comic-style speech bubble near the child containing EXACTLY the text "Up!", subtle and not covering the face.""",
            story_text="By afternoon, the winds picked up for Advanced Flight. The broomstick vibrated in hand, alive with enchantment. While others wobbled, a surge of confidence took hold. 'Time to fly!' {name} declared with determination.",
            costume="wearing wizard robes",
            face_expression="pure determination and thrilled excitement, confident grin, eyes bright with anticipation"
        ),
        PageTemplate(
            page_number=6,
            scene_description="Flying through the castle grounds",
            scene_type="flight",
            realistic_prompt="""EXHILARATING BROOMSTICK FLIGHT SCENE high above castle grounds. Wide cinematic composition: Vast sky stretching in all directions — deep blue with scattered white clouds at eye level and below. The magnificent castle grounds far below reduced to a green and grey patchwork, towers and courtyards miniaturized by altitude. Stone rings and archways built for flight practice visible as targets in the middle distance. Golden afternoon sunlight from the west side creates dramatic warm lighting across the entire aerial scene. The child named {name} on their wooden broomstick soaring through one of the stone rings at speed — hair streaming back, wizard robes flowing dramatically behind in a long trailing wake, face forward into the rushing air with pure exhilaration and joy. Natural high-speed flight pose capturing the freedom of first true flight. Wind effects visible in the movement of the robes. The castle and landscape create a spectacular backdrop far below. A small excited comic-style speech bubble near the child containing EXACTLY the text "I did it!", subtle and not covering the face.""",
            story_text="With a command of 'UP!', the broom shot into the sky. The wind rushed past ears like a roaring river. The ground became a quilt of green and grey. 'I did it!' {name} shouted with pure exhilaration as they soared through stone rings in the sky.",
            costume="wearing wizard robes",
            face_expression="pure exhilaration and joy, windswept happiness, triumphant grin, eyes bright with freedom"
        ),
        PageTemplate(
            page_number=7,
            scene_description="Exploring the magical library",
            scene_type="mischief",
            realistic_prompt="""MAGICAL LIBRARY EXPLORATION SCENE in the ancient academy library. Wide atmospheric composition: A magnificent library with towering shelves reaching impossibly high, carved dark wood packed with thousands of leather-bound books in every color. High arched windows allow shafts of warm afternoon sunlight to slice through the air, catching floating dust motes like tiny sparkles. Ancient reading tables of polished wood, candelabras, and brass reading lamps create warm pools of light throughout the space. The quiet hush of the library is palpable. Midnight — a sleek elegant black cat with luminous glowing yellow eyes and a silver collar — sits on the table beside a large ancient tome, watching intently with her tail curled neatly. The child named {name} in wizard robes seated at the ancient wooden table, carefully opening a large dusty leather-bound book with golden magical symbols embossed on its cover, pages beginning to glow with soft warm inner light as the book stirs to life. Natural pose of curious exploration and scholarly wonder. A small mischievous comic-style speech bubble near the child containing EXACTLY the text "Just one peek…", subtle and not covering the face.""",
            story_text="The Ancient Library was quiet until curiosity took over. Midnight, the library cat, dozed peacefully as {name} reached for an ancient tome. 'Just one peek...' they whispered, not knowing what magic would unfold.",
            costume="wearing wizard robes",
            face_expression="wide-eyed wonder and mischievous curiosity, soft conspiratorial smile, eyebrows raised with intrigue"
        ),
        PageTemplate(
            page_number=8,
            scene_description="Chaos in the magical library",
            scene_type="chaos",
            realistic_prompt="""MAGICAL LIBRARY CHAOS SCENE with books taking flight. Wide dynamic composition: The magnificent library interior transformed into beautiful chaos — hundreds of leather-bound books of all sizes have awakened and taken flight, filling the vast high-ceilinged room like a flock of birds, their covers flapping like heavy wings, pages fluttering as they swoop and soar through the golden candlelight. Some books spiral in formation, others dart between the shelves, some hover near the ceiling. Warm candlelight and afternoon sun create dramatic light through all the moving pages. Midnight the sleek black cat with glowing yellow eyes and silver collar leaping mid-air in the far background with athletic grace, batting at a passing book. The child named {name} in wizard robes standing near the table in the foreground, arms partially raised and laughing joyfully at the spectacular accidental chaos they have created, the books flying all around and behind them in an impressive living storm. A small playful comic-style speech bubble near the child containing EXACTLY the text "Okay… maybe more than one!", subtle and not covering the face.""",
            story_text="A sneeze disturbed the dust, and suddenly the books woke up! Leather-bound covers flapped like heavy wings in a paper storm. Midnight sprang into action, treating the flying literature like birds. 'MEOW! Got it!' seemed to say as {name} called 'Down boy!' It was chaos, but fun.",
            costume="wearing wizard robes",
            face_expression="surprised delight, playful alarm, laughing joyfully, amused and excited"
        ),
        PageTemplate(
            page_number=9,
            scene_description="Peaceful moment on the tower balcony",
            scene_type="peaceful",
            realistic_prompt="""MAGICAL NIGHT SCENE on the Astronomy Tower balcony. Wide atmospheric composition: The Astronomy Tower balcony at night, ancient stone railing warm with torchlight from the tower windows. Above and behind, a spectacular sky — deep navy blue filled with thousands of bright twinkling stars, two large luminous moons rising side by side creating soft twin moon shadows. Magical auroras shimmer in ribbons of green and purple across the sky behind the moons. Far below, the lights of the surrounding village twinkle warmly like earthbound stars. The view is breathtaking and vast. Warm golden light from the tower's windows spills out onto the balcony from the side, creating cozy illumination that mingles with the soft silver of twin moonlight. Midnight the sleek black cat with glowing yellow eyes and silver collar sits contentedly on the stone railing beside the child. The child named {name} in elegant formal wizard robes standing at the railing, both hands resting gently on the stone, looking out at the twin moons and the landscape below in peaceful wonder. Natural contemplative pose sharing a quiet moment with a faithful companion. A small soft comic-style speech bubble near the child containing EXACTLY the text "It's beautiful…", subtle and not covering the face.""",
            story_text="As the twin moons rose, the castle quieted down. Standing on the balcony of the Astronomy Tower, looking out over the glittering lights of the village, everything felt magical. Midnight purred contentedly, a faithful companion in this new adventure.",
            costume="wearing elegant formal wizard robes"
        ),
        PageTemplate(
            page_number=10,
            scene_description="Finding home at magic school",
            scene_type="peaceful",
            realistic_prompt="""PERFECT STORYBOOK ENDING SCENE on the Astronomy Tower balcony at night. Wide warm composition: The tower balcony under the light of the twin glowing moons, their warm golden light bathing the stone in soft radiance. The magnificent starry sky stretches above with thousands of brilliant stars. Village lights twinkle like scattered gems far below in the valley. The balcony stone is warm and inviting, torchlight from the window casting a comfortable glow. Midnight the sleek black cat with glowing yellow eyes and silver collar curled up peacefully in the child's lap, purring visibly, tail wrapped around themselves in contentment. The child named {name} in elegant formal wizard robes sitting comfortably on the balcony edge, gently petting the purring cat with one hand, taking in the peaceful night view with a warm, belonging smile — the quiet happiness of having found home. Natural restful pose of complete comfort and contentment. Subtle magical sparkles drift gently in the night air. Warm, safe, hopeful atmosphere of a perfect first day's end.""",
            story_text="This wasn't just a school; it was home. With Midnight by their side and a world of magic to explore, {name} smiled and whispered, 'I'm ready for tomorrow.' The moon smiled back, casting silver light on a perfect first day.",
            costume="wearing elegant formal wizard robes"
        )
    ]
)
