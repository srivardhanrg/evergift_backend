"""
StoryGift Mighty Guardian Theme - Superhero Adventure.

Complete 10-page story: "[NAME] The Mighty Guardian"
Premium theme featuring superhero transformation, heroic deeds, and inner strength.
Scene-First composition emphasizing superhero environments and heroic action.

KEY PRINCIPLES:
- Wide environmental compositions showcasing heroic city and sky settings
- Natural action and emotion (awe, determination, pride, contentment)
- Superhero suit details consistent across every scene
- Child integrated naturally into dynamic superhero environments
- Gender-neutral language throughout
"""

from app.stories.templates import StoryTemplate, PageTemplate


STORYGIFT_MIGHTY_GUARDIAN_THEME = StoryTemplate(
    theme_id="storygift_mighty_guardian",
    title_template="{name} The Mighty Guardian",
    description="Every child is a hero—now they can see it",
    cover_display_title="The Mighty Guardian",
    default_costume="wearing a skin-tight metallic blue and red superhero bodysuit like Superman — form-fitting spandex with visible muscle definition, gold chest emblem, red cape flowing behind, red boots with gold trim",
    protagonist_description="confident heroic expression, bright determined eyes",
    cover_costume="wearing a skin-tight metallic blue and red superhero bodysuit like Superman — form-fitting glossy spandex with visible muscle definition, gold emblem on chest, flowing red cape billowing dramatically behind, red boots with gold trim",
    cover_header_atmosphere="Dramatic city skyline at sunset with lens flare, epic clouds in orange and purple hues",
    cover_magical_elements="Energy auras radiating from the body in gold and blue, motion lines suggesting speed and power. Dynamic flying pose with one fist forward in classic superhero stance.",
    cover_footer_description="City rooftops below with twinkling lights, dynamic perspective looking up at the hero",
    pages=[
        PageTemplate(
            page_number=1,
            scene_description="Discovering the magical crystal",
            scene_type="discovery",
            realistic_prompt="""MAGICAL CRYSTAL DISCOVERY SCENE in sunny park. Wide environmental composition: A bright afternoon park setting with green grass, mature trees, and children playing in the far background unaware of the magic unfolding nearby. Warm golden afternoon sunlight filtering through tree canopy creates dappled light on the grass. A brilliant crystalline object — geometric in shape, pulsing with soft rainbow energy in iridescent blues and purples — descends in a focused beam of golden light from above, hovering just inches above outstretched hands in the moment just before contact. Leaves and grass around the child stir gently in a mystical wind, hair lifting. The crystal's rainbow reflections scatter across the surrounding grass and trees in colorful patterns. The child named {name} in everyday clothes standing in the park, arms raised with hands outstretched, face turned upward with a wide expression of surprise and wonder at the glowing object hovering in the beam. Natural pose of stunned discovery and destiny. Sense of magic arriving into an ordinary day.""",
            story_text="{name} was having an ordinary day—playing, laughing, being amazing—when something extraordinary happened. A mysterious glowing object fell from the sky and landed right in {name}'s hands!",
            costume="wearing everyday clothes, t-shirt and jeans"
        ),
        PageTemplate(
            page_number=2,
            scene_description="Superhero transformation",
            scene_type="transformation",
            realistic_prompt="""EPIC SUPERHERO TRANSFORMATION SCENE in the park. Wide dynamic composition: The park setting transformed by an explosive burst of energy — the crystal in the child's hands has exploded outward into brilliant ribbons of golden and blue light that spiral and wrap around the figure in a vortex of transformation. The lower body already shows the new metallic blue suit with red accents and gold boots materializing from the light, solid and gleaming, while the upper portion is still wreathed in swirling energy ribbons. The child named {name} floating slightly off the grass in the energy vortex, arms outstretched, caught in the mid-transformation moment with an expression of exhilarated surprise. Energy particles and trailing light ribbons spiral outward from the transformation point, the background blurred by the energy burst. Dramatic backlighting creates a powerful silhouette effect at the edges of the figure. Dynamic frozen moment of power awakening. Vibrant colors, sense of destiny being fulfilled. A dynamic comic-style speech bubble near the child containing EXACTLY the text "Whoa—what's happening?!", slightly energetic styling but subtle and not covering the face.""",
            story_text="The moment {name} touched it, the crystal began to glow even brighter! It transformed into a magnificent superhero costume made specially for someone as brave and kind as {name}. It was time to become... THE MIGHTY GUARDIAN!",
            costume="mid-transformation from regular clothes to superhero suit"
        ),
        PageTemplate(
            page_number=3,
            scene_description="First power awakening on rooftop",
            scene_type="action",
            realistic_prompt="""EPIC POWER AWAKENING SCENE on city rooftop at golden hour. Wide cinematic composition: A city rooftop at golden hour, the skyline stretching dramatically in every direction. The sun low on the horizon casts everything in warm amber and gold, long shadows stretching across the rooftop surface. City buildings create a geometric skyline of silhouettes against the luminous sky. The child named {name} in full superhero costume — metallic blue and red suit with gold accents, flowing red cape — standing alone on the rooftop with right fist raised upward, brilliant blue energy crackling and glowing around the raised fist and forearm in a display of awakening power. A massive golden energy shockwave ring expands outward from the child's body, the air itself bending. The red cape billows dramatically behind in the rooftop wind. Natural heroic stance of someone discovering their power for the first time with exhilarated wonder. The golden sunset from the west illuminates the scene warmly. Energy sparks swirl upward around the raised fist. Single child alone on the rooftop, the entire city as their backdrop.""",
            story_text="{name} discovered amazing powers—super strength to lift anything, super speed to run faster than the wind, and the ability to fly through the clouds! But the greatest power of all was {name}'s brave and caring heart.",
            costume="wearing a skin-tight metallic blue and red superhero bodysuit like Superman — form-fitting spandex with visible muscle definition, gold chest emblem, red cape flowing behind, red boots with gold trim"
        ),
        PageTemplate(
            page_number=4,
            scene_description="Spotting a glowing meteor heading toward the park",
            scene_type="heroic",
            realistic_prompt="""EPIC HEROIC SPOTTING SCENE in beautiful town park. Wide dynamic composition: A sunny afternoon park setting with green grass, flower beds, acacia-style shade trees, swing sets and slides visible in the background. Families and children scattered throughout the park in the middle ground, many with heads tilted upward and hands pointing at the sky in wonder and curiosity. High above in the bright blue daytime sky, a large glowing crystal meteor trails a spectacular arc of rainbow sparkles and multi-colored light as it streaks downward toward the park — its glow casting beautiful scattered rainbow light patterns across the grass below. The child named {name} in the superhero costume — skin-tight metallic blue and red bodysuit with gold emblem on chest, red cape suddenly snapping out in a gust of heroic wind — standing in the park foreground in a natural determined stance, fists clenched at sides, chin raised, looking up at the incoming meteor with fierce ready courage. Cape blowing dramatically. A bold comic-style speech bubble near the child containing EXACTLY the text "I'll handle this!", confident and brave, subtle and not covering the face.""",
            story_text="Just then, something streaked across the sky — a giant glowing meteor, sparkling with rainbow light, heading straight for the town park! Everyone looked up in wonder. {name} knew exactly what to do. 'I'll handle this!' said the Mighty Guardian.",
            costume="wearing a skin-tight metallic blue and red superhero bodysuit like Superman — form-fitting spandex with visible muscle definition, gold chest emblem, red cape flowing behind, red boots with gold trim"
        ),
        PageTemplate(
            page_number=5,
            scene_description="Hero catches the meteor and places it as a park monument",
            scene_type="triumph",
            realistic_prompt="""TRIUMPHANT SUPERHERO FEAT OF STRENGTH SCENE in town park. Wide celebratory composition: The town park's central area with green grass, flower beds, and trees creating a natural amphitheater of sorts. A crowd of diverse children and families gathered in a wide half-circle in the background — arms raised, clapping, some children jumping with excitement, faces lit with awe and delight, all in soft focus. The child named {name} in full superhero costume — metallic blue and red suit, gold accents, red cape billowing behind from the energy of the crystal above — hovering just above the ground at the center of the park, holding a massive glowing crystal rock above their head with both hands in a classic power hold. The crystal meteor is magnificent and magical — translucent with swirling rainbow colors of purple, blue, gold, and pink, radiant light streaming outward from it in all directions and casting colorful patterns across the grass and the gathered crowd. Natural triumphant pose of a hero completing a feat of strength with joy and pride. Golden afternoon sunlight, sparkles and gentle energy particles float in the air around the scene. A cheerful comic-style speech bubble near the child containing EXACTLY the text "A gift from the sky!", warm and triumphant, subtle and not covering the face.""",
            story_text="With a mighty WHOOOOSH, {name} rocketed into the sky and caught the giant meteor with both hands! It wasn't scary at all — it was a beautiful, magical crystal from the stars! {name} gently carried it down and placed it right in the middle of the park, where it glowed like a rainbow nightlight for everyone to enjoy.",
            costume="wearing a skin-tight metallic blue and red superhero bodysuit like Superman — form-fitting spandex, gold chest emblem, red cape billowing dramatically, red boots with gold trim"
        ),
        PageTemplate(
            page_number=6,
            scene_description="Epic storm battle",
            scene_type="climax",
            realistic_prompt="""EPIC STORM BATTLE SCENE in dark dramatic sky. Wide action composition: A stormy sky environment — dark purple and grey storm clouds swirling in dramatic formations all around, rain droplets frozen mid-air creating a curtain of crystal beads, lightning visible in the clouds in the distance. The child named {name} in superhero costume flying alone through this turbulent sky, completely alone with no other figures anywhere. The metallic blue and red suit catches what light remains, the red cape whipping dramatically behind in the fierce storm wind. Both arms extended forward with golden energy beams shooting from hands toward the dark purple storm clouds ahead, the golden energy cutting visibly through the rain and mist. Wind-blown hair, rain streaking past. Natural action pose of determined heroic effort against an elemental challenge. The storm clouds create dramatic framing around the lone hero figure. Distant landscape far below through breaks in the clouds, no town visible. Cinematic superhero action atmosphere. A sharp comic-style speech bubble near the child containing EXACTLY the text "Not on my watch!", bold and determined, subtle and not covering the face.""",
            story_text="But the day wasn't over! Dark storm clouds gathered, and {name} heard that a big storm was heading toward the town. Using incredible powers, {name} flew high into the sky and used super strength to gently push the storm clouds away from the town!",
            costume="wearing a skin-tight metallic blue and red superhero bodysuit like Superman — form-fitting spandex, gold chest emblem, red cape whipping dramatically in wind, red boots with gold trim"
        ),
        PageTemplate(
            page_number=7,
            scene_description="Town celebrates the hero",
            scene_type="celebration",
            realistic_prompt="""VICTORY CELEBRATION SCENE in town square. Wide festive composition: A charming town square filling with celebration — colorful confetti raining down from above catching the sunlight in sparkles of every color, banners and flags waving with a child's initial visible, balloons floating upward. Diverse crowds of adults and children filling the square, cheering with raised arms, throwing confetti, some children jumping with excitement. Reporters with cameras, kids eagerly moving forward. A banner stretched between buildings reads 'Thank you Guardian!' A town official in smart attire holding a golden ceremonial key extended in offering. Behind everything, a breathtaking rainbow arcs across the clearing sky, dramatic golden god rays breaking through the dissipating storm clouds and illuminating the entire square in warm golden light. The child named {name} in superhero costume hovering or standing as the focal point of the celebration, waving with a humble smile, slightly embarrassed by the attention but genuinely proud. Cape draped heroically. Warm golden hour light, festive and joyful atmosphere. A cheerful comic-style speech bubble near the child containing EXACTLY the text "We did it!", light and celebratory, subtle and not covering the face.""",
            story_text="The sun broke through the clouds, and a beautiful rainbow appeared. The whole town came out to cheer for {name} THE MIGHTY GUARDIAN! Flags waved, confetti flew, and everyone celebrated their amazing hero!",
            costume="wearing a skin-tight metallic blue and red superhero bodysuit like Superman — form-fitting spandex, gold chest emblem, red cape draped heroically, red boots with gold trim"
        ),
        PageTemplate(
            page_number=8,
            scene_description="Power returning to crystal",
            scene_type="transformation",
            realistic_prompt="""PEACEFUL TRANSFORMATION RETURN SCENE in home backyard at twilight. Wide atmospheric composition: A private home backyard at the magical transition between golden hour and early evening — the sky above painted in soft oranges, purples, and the first deep blues of dusk. The first stars are appearing. Warm lights glow in the windows of the family home behind, parents' silhouettes visible watching with pride from the window. Garden plants and a quiet fence create a safe domestic enclosure. The child named {name} has just landed gently on the grass — the superhero costume is mid-dissolution, the boots and lower cape already transformed into streams of golden light particles flowing and curling upward. Regular clothes becoming visible underneath as the suit fades. One hand raised to touch a small glowing crystal pendant forming at the chest on a delicate chain, the last of the magic gathering into this keepsake. Natural pose of quiet transformation, the child looking down gently at the forming pendant. Golden particle effects drift upward into the twilight. Sense of secret identity and the quiet pride of a hero coming home. A magical, intimate moment.""",
            story_text="As the day ended, {name} flew home. The superhero costume began to glow and transformed back into the crystal, which now hung on a special chain around {name}'s neck. The powers would always be there when needed.",
            costume="mid-transformation from superhero costume back to regular clothes, crystal pendant forming"
        ),
        PageTemplate(
            page_number=9,
            scene_description="Family dinner with a secret",
            scene_type="intimate",
            realistic_prompt="""HEARTWARMING FAMILY DINNER SCENE with a delightful secret. Wide warm composition: A cozy family dining room at evening, overhead warm light creating intimate golden atmosphere. The dinner table set with a meal in progress, dishes and glasses catching the warm light. Parents and siblings occupying the near side and sides of the table, animated in conversation, passing food, sharing laughter, seen from behind or in partial profile. Through the window behind the table, the night sky shows a single particularly bright star twinkling. A small pencil-sketched superhero drawing visible among other artwork on the wall. The child named {name} in regular clothes seated at the far side of the table, directly across the scene, one hand subtly raised to touch the barely-visible glow of the crystal pendant just under their shirt collar — a small knowing smile playing on their lips as they hold their wonderful secret. Normal family dinner scene charged with the private knowledge of the day's extraordinary adventure. Cozy warm atmosphere of family love and belonging. A tiny comic-style speech bubble near the child containing EXACTLY the text "hehe…", playful and secretive, subtle and not covering the face.""",
            story_text="That night at dinner, {name}'s family talked about their day. When they asked what {name} did, our hero just smiled and touched the crystal under their shirt. Being a hero isn't about powers—it's about being brave, kind, and helping others. And {name}? {name} was ALWAYS a hero.",
            costume="wearing regular clothes, crystal pendant hidden under shirt"
        ),
        PageTemplate(
            page_number=10,
            scene_description="Ready for tomorrow's adventures",
            scene_type="resolution",
            realistic_prompt="""PERFECT HOPEFUL ENDING SCENE in cozy bedroom at night. Wide warm composition: A child's bedroom at night, cozy and personal — superhero posters on the wall, toys scattered, a bookshelf with adventure stories. The window frames the peaceful night city skyline, lights twinkling in distant buildings. A shooting star streaks silently across the dark sky through the window glass. Soft warm light from a bedroom nightlight creates gentle ambient illumination throughout the room. The crystal pendant glows softly around the child's neck, its gentle light adding warmth to the scene. The child named {name} in pajamas standing near the bedroom window, the night city visible through the glass beside them. Natural quiet stance of someone looking out at the world they protect, a quiet confident smile on their face and soft gaze taking in the peaceful city outside. Expression of calm readiness and belonging. Magical hopeful atmosphere, the promise of tomorrow's adventures in the air. The city skyline peaceful under the child's quiet watch.""",
            story_text="Before bed, {name} looked out the window at the peaceful town below. Somewhere out there, someone might need help tomorrow. And the Mighty Guardian would be ready. Because true heroes never stop being brave, kind, and ready to help—just like {name}.",
            costume="wearing pajamas, crystal pendant glowing around neck"
        ),
    ]
)
