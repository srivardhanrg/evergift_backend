"""
StoryGift Secret Agent Theme - Multi-Profession Spy Adventure.

Complete 10-page story: "[NAME] The Secret Agent"
Premium theme featuring undercover missions requiring different professional disguises.
Optimized for both photorealistic and 3D cartoon pipelines with strict face consistency.

FACE CONSISTENCY RULES:
- Every prompt has child's face as focal point
- Three-quarter or front-facing compositions only
- Face clearly lit and detailed in every scene
- No back views, silhouettes, or looking away from camera
"""

from app.stories.templates import StoryTemplate, PageTemplate


STORYGIFT_SECRET_AGENT_THEME = StoryTemplate(
    theme_id="storygift_secret_agent",
    title_template="{name} The Secret Agent",
    description="Go undercover as a doctor, police officer, firefighter, scientist, and more!",
    default_costume="wearing a sleek black spy suit with silver accents",
    protagonist_description="confident determined eyes, clever and brave expression",
    # Cover page settings for typography-ready composition
    cover_costume="wearing a sleek black tactical spy suit with silver utility belt, spy watch with holographic display, and confident heroic stance",
    cover_header_atmosphere="Dramatic city skyline at night with searchlights, sleek skyscrapers with glowing windows, cinematic blue and purple lighting",
    cover_magical_elements="Holographic screens and data streams floating around the body (not face). Spy gadgets visible - grappling hook, communicator watch. Dynamic pose suggesting readiness for action.",
    cover_footer_description="Rooftop edge with city lights twinkling below, high-tech surveillance equipment",
    pages=[
        # === PAGE 1 - THE SECRET MESSAGE ===
        PageTemplate(
            page_number=1,
            scene_description="Receiving the secret mission",
            scene_type="discovery",
            realistic_prompt="""Dramatic discovery scene. The child named {name} in casual home clothes sitting at bedroom desk, face illuminated by glowing blue holographic message projecting from a mysterious high-tech device. Child's expression shows excited surprise and determination, eyes wide with wonder, mouth slightly open. The holographic display shows "TOP SECRET" text and mission briefing. Dim bedroom background with posters on wall, dramatic lighting from the hologram casting blue glow on child's amazed face. Child's face is the focal point, clearly visible and detailed, lit dramatically by the holographic light. Cinematic spy movie atmosphere.""",
            story_text="It started like any ordinary evening—until a mysterious device appeared with a glowing message. 'Agent {name}, your mission awaits. The city needs you!' This was going to be the adventure of a lifetime!",
            costume="wearing casual home clothes"
        ),

        # === PAGE 2 - SPY HEADQUARTERS ===
        PageTemplate(
            page_number=2,
            scene_description="Training at spy headquarters",
            scene_type="preparation",
            realistic_prompt="""Futuristic spy headquarters scene. The child named {name} standing in a high-tech gadget room wearing a sleek black junior spy suit with silver accents. Child facing camera with confident smile, holding a cool spy gadget in one hand. Behind them: wall of high-tech equipment, screens showing mission data, robotic arms, and glowing display cases with spy tools. A friendly mentor figure in background. Blue and silver lighting creates premium atmosphere. Child's determined confident face clearly visible and detailed, showing readiness for the mission. Eyes bright with excitement.""",
            story_text="At the secret headquarters, {name} received special training and amazing gadgets—a watch that could do anything, a suit that could become any disguise! 'Your first mission begins now, Agent {name}!'",
            costume="wearing sleek black junior spy suit with silver accents"
        ),

        # === PAGE 3 - UNDERCOVER: DOCTOR ===
        PageTemplate(
            page_number=3,
            scene_description="Undercover as a doctor",
            scene_type="infiltration",
            realistic_prompt="""Hospital undercover scene. The child named {name} dressed as a young doctor in crisp white medical coat with stethoscope around neck, standing in a modern hospital corridor. Child's face turned toward camera with clever knowing expression, one eyebrow slightly raised, holding a clipboard while secretly checking a high-tech spy device hidden in their pocket. Clean white hospital environment with medical equipment visible. Soft professional lighting illuminating child's focused intelligent face. Child's face clearly visible and detailed, showing the thrill of the secret mission. Professional yet playful atmosphere.""",
            story_text="Disguise one: Doctor! At City Hospital, {name} searched for the hidden clue. With stethoscope in hand and spy skills sharp, our agent found the secret code hidden in the medicine cabinet!",
            costume="wearing white doctor coat with stethoscope"
        ),

        # === PAGE 4 - UNDERCOVER: POLICE OFFICER ===
        PageTemplate(
            page_number=4,
            scene_description="Undercover as a police officer",
            scene_type="investigation",
            realistic_prompt="""Police station scene. The child named {name} dressed as a junior police officer in smart blue uniform with shiny badge, standing at a computer terminal in an evidence room. Child's face lit by the glow of multiple screens showing case files, expression of concentration and discovery as they find important information. Police station background with filing cabinets, evidence boards with connected photos. Child posed at three-quarter angle, face clearly showing the excitement of cracking the case. Child's determined detective face clearly visible and detailed. Dramatic blue screen glow lighting.""",
            story_text="Disguise two: Police Officer! The clue led {name} to the police station. Using clever detective skills, our agent accessed the secret files and discovered where the villain was hiding!",
            costume="wearing blue police officer uniform with badge"
        ),

        # === PAGE 5 - UNDERCOVER: FIREFIGHTER ===
        PageTemplate(
            page_number=5,
            scene_description="Undercover as a firefighter",
            scene_type="rescue",
            realistic_prompt="""Heroic firefighter rescue scene. The child named {name} in full firefighter gear with yellow jacket and helmet, emerging from a smoky building entrance carrying a small puppy to safety. Child's face showing brave determination and compassion, looking toward camera with heroic expression. Orange fire glow in background, smoke effects, fire truck visible with flashing lights. Fellow firefighters cheering in background. Child's courageous face is the focal point, clearly visible and detailed, lit by the dramatic fire glow. Heroic action pose, cape of smoke behind. Cinematic drama.""",
            story_text="Disguise three: Firefighter! A building was in trouble—and so was a trapped friend with vital information. {name} suited up, rushed in bravely, and saved the day! Another clue discovered!",
            costume="wearing yellow firefighter jacket and helmet"
        ),

        # === PAGE 6 - UNDERCOVER: SCIENTIST ===
        PageTemplate(
            page_number=6,
            scene_description="Undercover as a scientist",
            scene_type="discovery",
            realistic_prompt="""High-tech laboratory scene. The child named {name} dressed as a young scientist in white lab coat and safety goggles pushed up on forehead, standing at a futuristic workstation with glowing test tubes and holographic displays. Child holding a glowing vial, face showing amazed discovery expression, eyes wide with scientific wonder. Colorful bubbling liquids, laser equipment, DNA helix holograms in background. Child's fascinated excited face clearly visible and detailed, lit by the colorful glow of the experiments. Premium science fiction laboratory aesthetic.""",
            story_text="Disguise four: Scientist! In the secret laboratory, {name} discovered the villain's formula. With quick thinking and steady hands, our agent created an antidote to save everyone!",
            costume="wearing white lab coat with safety goggles"
        ),

        # === PAGE 7 - UNDERCOVER: CHEF ===
        PageTemplate(
            page_number=7,
            scene_description="Undercover as a chef",
            scene_type="infiltration",
            realistic_prompt="""Luxury restaurant kitchen scene. The child named {name} dressed as a professional chef in pristine white chef's coat and tall chef's hat, positioned at a gleaming stainless steel counter. Child's face turned toward camera with a clever secretive smile, one hand stirring a pot while the other secretly holds a tiny spy camera. Fancy kitchen with copper pots, flames from stove, gourmet food being prepared. Other chefs working in background. Warm golden kitchen lighting illuminating child's mischievous clever face. Child's face clearly visible and detailed, showing the fun of the undercover mission.""",
            story_text="Disguise five: Chef! The villain was hosting a fancy dinner. Dressed as a chef, {name} snuck into the kitchen, overheard the evil plan, and gathered the final piece of the puzzle!",
            costume="wearing white chef coat and tall chef hat"
        ),

        # === PAGE 8 - UNDERCOVER: PILOT ===
        PageTemplate(
            page_number=8,
            scene_description="Undercover as a pilot",
            scene_type="chase",
            realistic_prompt="""Exciting cockpit scene. The child named {name} dressed as an airplane pilot in professional uniform with captain's hat and aviator sunglasses pushed up on their head, seated in an aircraft cockpit. Child gripping the control yoke with both hands, face showing intense focus and excitement, looking toward camera with determined expression. Through cockpit windows: dramatic clouds and sunset sky. Control panels with glowing buttons and screens visible. Child's thrilled focused face is the focal point, clearly visible and detailed, lit by cockpit instrument glow and sunset light. Action movie energy.""",
            story_text="Disguise six: Pilot! The villain tried to escape by plane, but Agent {name} was ready. Taking the controls like a pro, our hero gave chase through the clouds!",
            costume="wearing pilot uniform with captain's hat"
        ),

        # === PAGE 9 - MISSION COMPLETE ===
        PageTemplate(
            page_number=9,
            scene_description="Final showdown and victory",
            scene_type="triumph",
            realistic_prompt="""Triumphant rooftop scene at sunset. The child named {name} in sleek black spy suit standing heroically on a city rooftop, the captured villain (cartoonish, not scary) being led away by friendly agents in background. Child's face turned toward camera with proud victorious smile, one hand on hip in confident pose, wind slightly blowing their hair. Golden sunset light creating beautiful rim lighting around child. City skyline glittering behind. Child's triumphant joyful face is the absolute focal point, clearly visible and detailed, glowing in the warm sunset light. Victory pose, cinematic heroic shot.""",
            story_text="Mission complete! On the city rooftop, {name} confronted the villain and saved the day. The city was safe, all thanks to the bravest, cleverest secret agent ever!",
            costume="wearing sleek black spy suit"
        ),

        # === PAGE 10 - HERO'S HONOR ===
        PageTemplate(
            page_number=10,
            scene_description="Medal ceremony and celebration",
            scene_type="resolution",
            realistic_prompt="""Elegant award ceremony scene. Close-up of the child named {name} in a formal black suit with a shiny gold medal being placed around their neck. Child's face beaming with pride and happiness, warm genuine smile, eyes sparkling with joy. Soft bokeh background showing clapping agents and celebration, but child is the clear focus. Warm golden spotlight illuminating child's proud happy face. Confetti floating gently in the air. Child's radiant smiling face clearly visible and detailed, the medal gleaming against the formal suit. Emotional, celebratory, frame-worthy portrait.""",
            story_text="At headquarters, {name} received the Golden Star Medal—the highest honor for a secret agent. But the best reward? Knowing that being brave, clever, and kind can make the whole world better.",
            costume="wearing formal black suit with gold medal"
        ),
    ]
)
