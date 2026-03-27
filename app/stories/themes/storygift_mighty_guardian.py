"""
StoryGift Mighty Guardian Theme - Superhero Adventure.

Complete 10-page story: "[NAME] The Mighty Guardian"
Premium theme featuring superhero transformation, heroic deeds, and inner strength.
Optimized for both photorealistic and 3D cartoon pipelines.
"""

from app.stories.templates import StoryTemplate, PageTemplate


STORYGIFT_MIGHTY_GUARDIAN_THEME = StoryTemplate(
    theme_id="storygift_mighty_guardian",
    title_template="{name} The Mighty Guardian",
    description="Every child is a hero—now they can see it",
    default_costume="wearing a skin-tight metallic blue and red superhero bodysuit like Superman — form-fitting spandex with visible muscle definition, gold chest emblem, red cape flowing behind, red boots with gold trim",
    protagonist_description="confident heroic expression, bright determined eyes",
    # Cover page settings for typography-ready composition
    cover_costume="wearing a skin-tight metallic blue and red superhero bodysuit like Superman — form-fitting glossy spandex with visible muscle definition, gold emblem on chest, flowing red cape billowing dramatically behind, red boots with gold trim",
    cover_header_atmosphere="Dramatic city skyline at sunset with lens flare, epic clouds in orange and purple hues",
    cover_magical_elements="Energy auras radiating from the body in gold and blue, motion lines suggesting speed and power. Dynamic flying pose with one fist forward in classic superhero stance.",
    cover_footer_description="City rooftops below with twinkling lights, dynamic perspective looking up at the hero",
    pages=[
        # === PAGE 1 - THE DISCOVERY ===
        PageTemplate(
            page_number=1,
            scene_description="Discovering the magical crystal",
            scene_type="discovery",
            realistic_prompt="""Magical discovery moment. The child named {name} in everyday clothes stands in a park or backyard, looking up with surprise and wonder as a glowing crystalline object with geometric shape and pulsing rainbow energy descends from a beam of light and hovers just above their outstretched hands. The moment just before contact. Golden afternoon light, leaves and grass gently blown by mystical wind, child's hair flowing. Other kids playing in far background, unaware of the magic. The object casts colorful reflections on child's amazed face. Sense of destiny and magic, warm atmosphere.""",
            story_text="{name} was having an ordinary day—playing, laughing, being amazing—when something extraordinary happened. A mysterious glowing object fell from the sky and landed right in {name}'s hands!",
            costume="wearing everyday clothes, t-shirt and jeans"
        ),

        # === PAGE 2 - THE TRANSFORMATION ===
        PageTemplate(
            page_number=2,
            scene_description="Superhero transformation",
            scene_type="transformation",
            realistic_prompt="""Epic transformation sequence. The child named {name} surrounded by swirling energy vortex as the crystal in their hands explodes into ribbons of light that wrap around them, forming a superhero costume. Mid-transformation view showing lower body with the new blue and red suit with gold boots materializing, upper body still in regular clothes but surrounded by glowing energy. Child's expression is exhilarated surprise, arms outstretched, floating slightly off the ground. Energy particles, light trails, dynamic movement. Background blurred by the energy burst. Dramatic backlighting, vibrant colors, sense of power awakening. Split-second frozen moment of magical change. A dynamic comic-style speech bubble near the child saying "Whoa—what’s happening?!", slightly energetic styling but subtle and not covering the face.""",
            story_text="The moment {name} touched it, the crystal began to glow even brighter! It transformed into a magnificent superhero costume made specially for someone as brave and kind as {name}. It was time to become... THE MIGHTY GUARDIAN!",
            costume="mid-transformation from regular clothes to superhero suit"
        ),

        # === PAGE 3 - DISCOVERING POWERS ===
        PageTemplate(
            page_number=3,
            scene_description="First power awakening on rooftop",
            scene_type="action",
            realistic_prompt="""Epic power awakening scene. The child named {name} in full superhero costume with metallic blue and red suit, gold accents, and flowing cape, standing alone on a city rooftop at golden hour. Child's right fist raised upward glowing with brilliant blue energy, a massive golden energy shield expanding outward from their body in a shockwave ring. Cape billowing dramatically behind in the wind. Child's face shows exhilarated determination and wonder, mouth slightly open in awe at their own power, looking toward camera. Blue and gold energy crackling around the child's raised fist and arms only, not on face. City skyline behind with warm golden sunset light. Energy particles and sparks swirling upward around the fist. Single child alone on rooftop, single face, front-facing portrait composition with the child filling the center of the frame. Cinematic superhero movie quality. Child's face clearly visible, naturally lit by warm sunset glow, no colored energy lighting on face or eyes.""",
            story_text="{name} discovered amazing powers—super strength to lift anything, super speed to run faster than the wind, and the ability to fly through the clouds! But the greatest power of all was {name}'s brave and caring heart.",
            costume="wearing a skin-tight metallic blue and red superhero bodysuit like Superman — form-fitting spandex with visible muscle definition, gold chest emblem, red cape flowing behind, red boots with gold trim"
        ),

        # === PAGE 4 - THE CALL FOR HELP ===
        PageTemplate(
            page_number=4,
            scene_description="Responding to a call for help",
            scene_type="heroic",
            realistic_prompt="""Urgent rescue moment in a sunlit park. The child named {name} wearing a skin-tight superhero bodysuit in vivid metallic blue with bold red accents on the shoulders, sides, and boots — form-fitting spandex material that hugs the body like Superman’s suit with visible muscle definition underneath, a bold gold emblem on the chest, and a flowing red cape attached at the shoulders. The suit is sleek, shiny, and realistic — not baggy, not a Halloween costume, not armor. The child is captured mid-run toward an enormous oak tree, body leaning forward with momentum, one foot pushing off the ground, cape streaming behind from the speed. Face turned naturally toward camera in a three-quarter running angle — expression of urgent concern and fierce determination, brow slightly furrowed, eyes focused and compassionate, mouth slightly open as if calling out reassurance. High up on the tallest branch of the oak tree, a tiny frightened kitten clings on with wide scared eyes, meowing for help. A worried child who owns the kitten stands in soft focus background, pointing up with tears. Dappled golden afternoon sunlight filtering through the tree’s leaves, dust particles kicked up from the hero’s running feet, cape catching the light. The child hero’s face is the clear focal point — sharply detailed, naturally lit by warm golden light, showing genuine empathy and urgency. Dynamic action composition, not a posed stance.""",
            story_text="Suddenly, {name} heard a call for help! A kitten was stuck at the very top of the tallest tree, too scared to climb down. ‘Don’t worry, little friend,’ called {name}, ‘I’m on my way!’",
            costume="wearing a skin-tight metallic blue and red superhero bodysuit like Superman — form-fitting spandex with visible muscle definition, gold chest emblem, red cape flowing behind, red boots with gold trim"
        ),

        # === PAGE 5 - THE RESCUE ===
        PageTemplate(
            page_number=5,
            scene_description="Triumphant kitten rescue",
            scene_type="bonding",
            realistic_prompt="""Triumphant rescue scene. The child named {name} in superhero costume descending gracefully through the air in protective pose, cradling a small orange kitten against their chest with both arms. The kitten nuzzles warmly into child's neck, tiny paw resting on child's shoulder — face completely unobstructed, no paw or object on cheek or any part of the face. Child's expression is peaceful and warm, face clearly visible and front-facing toward camera. Child's cape billows upward from the descent, golden energy particles trail from boots. Dappled sunlight through tree leaves creates beautiful natural lighting on the child's face from above. Grateful crowd of kids below looking up and cheering with raised arms, soft focus background. Gentle landing moment, dust particles just starting to disturb on ground. Warm, heartwarming atmosphere, emotional connection between hero and rescued animal. Child's face the clear focal point, sharp detailed foreground. A small comic-style speech bubble near the child saying "I've got you, little one!", gentle and reassuring, subtle and not covering the face.""",
            story_text="With a mighty leap, {name} soared up, up, up! Gently cradling the grateful kitten, our hero flew back down, landing softly on the ground. The kitten purred and nuzzled {name}'s cheek. Mission accomplished!",
            costume="wearing a skin-tight metallic blue and red superhero bodysuit like Superman — form-fitting spandex, gold chest emblem, red cape billowing upward from descent, red boots with gold trim"
        ),

        # === PAGE 6 - SAVING THE TOWN ===
        PageTemplate(
            page_number=6,
            scene_description="Epic storm battle",
            scene_type="climax",
            realistic_prompt="""Epic storm battle, medium close-up composition. The child named {name} in superhero costume flying alone through stormy sky, completely alone with no other people visible anywhere. Upper body and face filling one-third of the frame prominently. Both arms extended forward with golden energy beams shooting from hands toward dark purple storm clouds. Child's cape whips dramatically behind, rain droplets frozen mid-air around them. Child's face shows intense concentration and fierce determination, jaw set, eyes focused forward toward camera with natural eye color. Wind-blown hair, rain streaking past. Dark dramatic storm clouds surround the child but do not obscure the face. Empty sky and distant landscape far below, no town or people visible. Cinematic superhero action shot with child as the sole figure in frame. Child's determined face is the absolute focal point, warmly lit by the golden glow from their hands, face naturally lit without colored lighting or glowing effects on eyes or skin. A sharp comic-style speech bubble near the child saying "Not on my watch!", bold and determined, subtle and not covering the face.""",
            story_text="But the day wasn't over! Dark storm clouds gathered, and {name} heard that a big storm was heading toward the town. Using incredible powers, {name} flew high into the sky and used super strength to gently push the storm clouds away from the town!",
            costume="wearing a skin-tight metallic blue and red superhero bodysuit like Superman — form-fitting spandex, gold chest emblem, red cape whipping dramatically in wind, red boots with gold trim"
        ),

        # === PAGE 7 - VICTORY CELEBRATION ===
        PageTemplate(
            page_number=7,
            scene_description="Town celebrates the hero",
            scene_type="celebration",
            realistic_prompt="""Victory celebration. The child named {name} in superhero costume hovering or standing in town square, surrounded by cheering crowd of diverse adults and children throwing confetti, waving banners with child's initial, holding balloons. Enormous vibrant rainbow arcs across clearing sky behind hero. Sun rays breaking through clouds create dramatic god rays. The child is waving with humble smile, slightly embarrassed but proud expression. Mayor offering a golden key to the city. Reporters with cameras, kids asking for autographs. Banner reads 'Thank you Guardian!' Festive, joyful atmosphere, warm golden hour lighting, confetti catching light. Wide celebration shot with hero as focal point. Rich details throughout. A cheerful comic-style speech bubble near the child saying "We did it!", light and celebratory, subtle and not covering the face.""",
            story_text="The sun broke through the clouds, and a beautiful rainbow appeared. The whole town came out to cheer for {name} THE MIGHTY GUARDIAN! Flags waved, confetti flew, and everyone celebrated their amazing hero!",
            costume="wearing a skin-tight metallic blue and red superhero bodysuit like Superman — form-fitting spandex, gold chest emblem, red cape draped heroically, red boots with gold trim"
        ),

        # === PAGE 8 - RETURNING HOME ===
        PageTemplate(
            page_number=8,
            scene_description="Power returning to crystal",
            scene_type="transformation",
            realistic_prompt="""Peaceful transformation return. Twilight scene in home's backyard as the child named {name} lands gently. The superhero costume dissolves into streams of golden light that flow into a crystal pendant on a delicate chain around their neck. Half transformed showing boots and cape already turned to light particles, regular clothes visible underneath the fading costume. Child looking at camera with soft, peaceful smile, one hand touching the glowing crystal at their chest. Family home visible with warm lights in windows, parents' silhouettes watching from window with pride. Purple-orange sunset sky, first stars appearing. Magical atmosphere with particle effects. Sense of secret identity and double life. Quiet emotional moment after action. Child's face clearly visible, front-facing, lit by the warm golden glow of the dissolving costume.""",
            story_text="As the day ended, {name} flew home. The superhero costume began to glow and transformed back into the crystal, which now hung on a special chain around {name}'s neck. The powers would always be there when needed.",
            costume="mid-transformation from superhero costume back to regular clothes, crystal pendant forming"
        ),

        # === PAGE 9 - THE SECRET ===
        PageTemplate(
            page_number=9,
            scene_description="Family dinner with a secret",
            scene_type="intimate",
            realistic_prompt="""Heartwarming family dinner scene. Warm dining room with golden overhead light creating intimate atmosphere. The child named {name} in regular clothes seated at the far side of the dinner table, directly facing the camera across the table. Child's face fully visible and front-facing toward viewer, hand subtly touching the glowing crystal pendant barely visible under their shirt collar, small knowing smile on face looking at camera. Parents and siblings seated on the near side and sides of the table, seen from behind or in profile, talking animatedly, sharing food, laughing warmly. Through window behind the child, night sky shows a single bright star twinkling. On the wall behind the child, drawings include a small superhero sketch. The crystal emits a very subtle glow. Normal family moment but charged with secret knowledge. Cozy, love-filled atmosphere. Sharp focus on child's face and secret smile, family members in soft focus foreground and sides. Child is the clear central focal point facing the viewer. A tiny comic-style speech bubble near the child saying "hehe…", playful and secretive, subtle and not covering the face.""",
            story_text="That night at dinner, {name}'s family talked about their day. When they asked what {name} did, our hero just smiled and touched the crystal under their shirt. Being a hero isn't about powers—it's about being brave, kind, and helping others. And {name}? {name} was ALWAYS a hero.",
            costume="wearing regular clothes, crystal pendant hidden under shirt"
        ),

        # === PAGE 10 - LOOKING TO TOMORROW ===
        PageTemplate(
            page_number=10,
            scene_description="Ready for tomorrow's adventures",
            scene_type="resolution",
            realistic_prompt="""Perfect ending. The child named {name} standing near the bedroom window at night in pajamas, in three-quarter view toward camera — face clearly visible with a quiet, confident smile. A gentle sideways gaze toward the city outside, not a full face-away turn toward the window — face remains mostly front-facing toward the viewer. No reflections in the window glass. The crystal pendant glows softly around their neck, lit warmly by the bedroom nightlight. In the night sky through the window, a shooting star streaks across. Room is cozy with superhero posters on wall, toys scattered. City skyline visible through window to the side. Child's expression shows quiet confidence and readiness for whatever adventure comes next. Magical, hopeful atmosphere. Child's face is the warm, clear focal point of the composition.""",
            story_text="Before bed, {name} looked out the window at the peaceful town below. Somewhere out there, someone might need help tomorrow. And the Mighty Guardian would be ready. Because true heroes never stop being brave, kind, and ready to help—just like {name}.",
            costume="wearing pajamas, crystal pendant glowing around neck"
        ),
    ]
)
