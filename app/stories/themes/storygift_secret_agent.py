"""
StoryGift Secret Agent Theme - Multi-Profession Spy Adventure.

Complete 10-page story: "[NAME] The Secret Agent"
Premium theme featuring undercover missions requiring different professional disguises.
Scene-First composition emphasizing spy environments and professional settings.

KEY PRINCIPLES:
- Wide environmental compositions showcasing varied professional settings
- Natural expressions (curiosity, confidence, determination, triumph, pride)
- Distinct atmosphere for each professional disguise setting
- Child integrated naturally into each environment with action and pose
- Gender-neutral language throughout
"""

from app.stories.templates import StoryTemplate, PageTemplate


STORYGIFT_SECRET_AGENT_THEME = StoryTemplate(
    theme_id="storygift_secret_agent",
    title_template="{name} The Secret Agent",
    description="Go undercover as a doctor, police officer, firefighter, scientist, and more!",
    cover_display_title="The Secret Agent",
    default_costume="wearing a sleek black spy suit with silver accents",
    protagonist_description="confident determined eyes, clever and brave expression",
    cover_costume="wearing a sleek black tactical spy suit with silver utility belt, spy watch with holographic display, and confident heroic stance",
    cover_header_atmosphere="Dramatic city skyline at night with searchlights, sleek skyscrapers with glowing windows, cinematic blue and purple lighting",
    cover_magical_elements="Holographic screens and data streams floating around the body (not face). Spy gadgets visible - grappling hook, communicator watch. Dynamic pose suggesting readiness for action.",
    cover_footer_description="Rooftop edge with city lights twinkling below, high-tech surveillance equipment",
    pages=[
        PageTemplate(
            page_number=1,
            scene_description="Receiving the secret mission",
            scene_type="discovery",
            realistic_prompt="""DRAMATIC SECRET MISSION DISCOVERY SCENE in cozy bedroom at evening. Wide atmospheric composition: A child's bedroom in the evening — soft lamp light on a wooden desk, posters on the wall, the comfortable familiar setting of home. On the desk, a mysterious high-tech device unlike anything ordinary glows with brilliant blue light, projecting a holographic message upward into the dim air above it. The holographic display shimmers with digital effects, displaying "TOP SECRET" in glowing letters alongside mission briefing text and animated diagrams, casting its cool blue glow outward across the desk surface and the surrounding walls and ceiling. The child named {name} in casual home clothes sitting at the bedroom desk, leaning slightly forward toward the holographic display with wide curious excitement and amazement at the unexpected message. Natural engaged pose of someone encountering the extraordinary in a familiar place. Warm ambient room light from the desk lamp and nightlight preserves natural comfortable atmosphere from the sides, the blue holographic glow contained to the display projection and room surfaces. Cinematic spy movie atmosphere entering an ordinary evening.""",
            story_text="It started like any ordinary evening—until a mysterious device appeared with a glowing message. 'Agent {name}, your mission awaits. The city needs you!' This was going to be the adventure of a lifetime!",
            costume="wearing casual home clothes",
            face_expression="curious, wide-eyed excitement, awestruck, eagerly leaning in"
        ),
        PageTemplate(
            page_number=2,
            scene_description="Training at spy headquarters",
            scene_type="preparation",
            realistic_prompt="""FUTURISTIC SPY HEADQUARTERS SCENE in high-tech training room. Wide impressive composition: A remarkable high-tech room filled with the equipment of espionage and preparation — a wall of screens displaying mission data, global maps, and surveillance feeds, all glowing with blue and silver light. Display cases with illuminated spy tools behind glass. Robotic arms and technical equipment visible. A friendly mentor figure in the background reviewing a holographic display. The room has a sleek silver and charcoal aesthetic with dramatic overhead lighting creating pools of warm illumination. The child named {name} in sleek black junior spy suit with silver accents standing confidently in the room's center, holding a cool spy gadget in one raised hand and examining it with a confident curious smile. Natural pose of someone equipped and ready, enjoying the gadgets of their new role. The warm neutral overhead light illuminates the scene comfortably while the blue screens create atmospheric glow on the background elements. Expression of determined readiness and eager excitement for the mission ahead.""",
            story_text="At the secret headquarters, {name} received special training and amazing gadgets—a watch that could do anything, a suit that could become any disguise! 'Your first mission begins now, Agent {name}!'",
            costume="wearing sleek black junior spy suit with silver accents",
            face_expression="confident, determined, ready for action, eager"
        ),
        PageTemplate(
            page_number=3,
            scene_description="Undercover as a doctor",
            scene_type="infiltration",
            realistic_prompt="""HOSPITAL UNDERCOVER SCENE in modern medical corridor. Wide professional composition: A clean modern hospital corridor — white and light grey surfaces, polished floors reflecting the overhead lighting, medical equipment on wheeled carts, directional signs on the walls, professional medical environment. Natural overhead hospital lighting fills the space cleanly. Other medical staff visible as background figures going about their work. The child named {name} dressed as a young doctor in a crisp white medical coat that reaches below the waist, a stethoscope hanging around their neck, a clipboard held in one hand with official-looking documents visible. The other hand casually positioned near a pocket where a small high-tech spy device is barely visible — the secret within the disguise. Standing in the corridor with a clever knowing expression and one eyebrow slightly raised, the private satisfaction of being undercover in plain sight. Natural pose of a confident young professional who carries a secret. A small soft comic-style speech bubble near the child containing EXACTLY the text "Got it...", clever and satisfied, subtle and not covering the face.""",
            story_text="Disguise one: Doctor! At City Hospital, {name} searched for the hidden clue. With stethoscope in hand and spy skills sharp, our agent found the secret code hidden in the medicine cabinet!",
            costume="wearing white doctor coat with stethoscope",
            face_expression="clever knowing smile, one eyebrow slightly raised, alert and playfully confident"
        ),
        PageTemplate(
            page_number=4,
            scene_description="Undercover as a police officer",
            scene_type="investigation",
            realistic_prompt="""POLICE STATION INVESTIGATION SCENE in evidence room. Wide focused composition: A police station evidence room — filing cabinets along the walls, a large cork evidence board covered in connected photographs and strings, case files stacked on shelves, the serious working environment of law enforcement. A dedicated desk area with screens and computer terminal showing case files and data. Warm overhead desk lamps create focused working light throughout the space. The child named {name} dressed as a junior police officer in a smart blue uniform with a shiny badge on the chest, standing at the computer terminal. Natural engaged stance of someone deep in investigation, leaning slightly toward the screen as important case information becomes clear on the display. The screen's glow contained to the display surface, warm desk lamp illuminating the scene overall. Natural expression of focused concentration shifting to the quiet triumph of discovery — a case cracked. A small soft comic-style speech bubble near the child containing EXACTLY the text "There you are...", focused and satisfied, subtle and not covering the face.""",
            story_text="Disguise two: Police Officer! The clue led {name} to the police station. Using clever detective skills, our agent accessed the secret files and discovered where the villain was hiding!",
            costume="wearing blue police officer uniform with badge",
            face_expression="focused, concentrating, analytical, the thrill of cracking the case"
        ),
        PageTemplate(
            page_number=5,
            scene_description="Undercover as a firefighter",
            scene_type="rescue",
            realistic_prompt="""HEROIC FIREFIGHTER RESCUE SCENE at building entrance. Wide dramatic composition: The entrance to a building in a smoke-filled emergency — orange fire glow emanating from the building's upper windows in the background, thick atmospheric smoke creating dramatic light diffusion. A large red fire truck with flashing lights visible to the side, fellow firefighters in the background cheering with raised arms. The building entrance framing the exit point. The child named {name} in full firefighter gear — yellow protective jacket with reflective stripes, a firefighter helmet, sturdy gloves — emerging from the smoky building entrance with purpose, carrying a small rescued puppy cradled protectively against their chest. The puppy clearly safe and unharmed, looking up with relief. Natural heroic action pose of someone who has just completed a brave rescue and is bringing someone to safety. Brave determination and compassion visible in the body language and expression. Orange fire glow from behind creates dramatic rim lighting on the gear. A small soft comic-style speech bubble near the child containing EXACTLY the text "You're safe now.", reassuring and brave, subtle and not covering the face.""",
            story_text="Disguise three: Firefighter! A building was in trouble—and so was a trapped friend with vital information. {name} suited up, rushed in bravely, and saved the day! Another clue discovered!",
            costume="wearing yellow firefighter jacket and helmet",
            face_expression="brave determination and compassion, heroic, caring, resolute"
        ),
        PageTemplate(
            page_number=6,
            scene_description="Undercover as a scientist",
            scene_type="discovery",
            realistic_prompt="""HIGH-TECH LABORATORY UNDERCOVER SCENE. Wide impressive scientific composition: A futuristic research laboratory with a clean science fiction aesthetic — workstations with glowing holographic displays, DNA helix holograms rotating in the air, colorful liquids bubbling in glass apparatus on adjacent benches, laser equipment with precise beams, screens displaying data graphs and molecular diagrams. The laboratory is sleek white and chrome with dramatic overhead scientific lighting. The child named {name} dressed as a young scientist in a white lab coat and safety goggles pushed up on the forehead, standing at a futuristic workstation. One hand raised holding a glowing vial of luminescent liquid at arm's length, examining it with calm focused curiosity and a quiet intense expression of scientific discovery. Natural scientist pose of careful observation. The vial's colorful glow illuminates the vial itself and creates atmospheric color in the surrounding lab equipment, while the overhead lab lighting preserves natural comfortable illumination across the scene. Expression of focused wonder at the discovery within the vial.""",
            story_text="Disguise four: Scientist! In the secret laboratory, {name} discovered the villain's formula. With quick thinking and steady hands, our agent created an antidote to save everyone!",
            costume="wearing white lab coat with safety goggles",
            face_expression="calm focused wonder, quiet intensity, gentle curious smile"
        ),
        PageTemplate(
            page_number=7,
            scene_description="Undercover as a chef",
            scene_type="infiltration",
            realistic_prompt="""LUXURY RESTAURANT KITCHEN UNDERCOVER SCENE. Wide atmospheric composition: A high-end restaurant kitchen in full operation — gleaming stainless steel surfaces everywhere, copper pots hanging above the central work area, flames leaping from professional gas stoves, gourmet food in various stages of elegant preparation. The warmth and energy of a busy professional kitchen fills the space. Other chefs in white coats working at stations in the background, focused on their work. The kitchen has beautiful warm golden light from the overhead professional fixtures. The child named {name} dressed as a professional chef in a pristine white chef's coat and tall chef's hat, positioned at a gleaming prep counter. One hand stirring a pot with professional ease, while the other hand casually but cleverly holds a tiny spy camera pointed toward a corner of the kitchen — the secret mission within the cover of culinary work. Natural pose of someone performing two tasks simultaneously with practiced ease. A cleverly secretive smile playing at the corner of their lips, the private satisfaction of gathering intelligence. A small soft comic-style speech bubble near the child containing EXACTLY the text "Gotcha...", playful and sneaky, subtle and not covering the face.""",
            story_text="Disguise five: Chef! The villain was hosting a fancy dinner. Dressed as a chef, {name} snuck into the kitchen, overheard the evil plan, and gathered the final piece of the puzzle!",
            costume="wearing white chef coat and tall chef hat",
            face_expression="clever secretive smile, mischievous delight, playful alertness"
        ),
        PageTemplate(
            page_number=8,
            scene_description="Undercover as a pilot",
            scene_type="chase",
            realistic_prompt="""EXCITING COCKPIT CHASE SCENE in aircraft. Wide dynamic composition: A futuristic aircraft cockpit with curved walls lined with sophisticated glowing control panels — buttons and switches in multiple colors pulsing with indicator lights, navigation screens displaying real-time data, communication equipment. The large circular cockpit windows dominate one side of the view, showing a spectacular aerial scene outside — dramatic warm sunset sky in gold and amber, billowing white clouds at flight level, the curvature of the earth visible at the horizon. The outside light creates beautiful warm illumination through the cockpit windows. The child named {name} in professional pilot uniform with captain's hat and aviator sunglasses pushed up on the forehead, seated in the pilot's chair with both hands on the control yoke — gripping it with focused intensity and the thrill of pursuit. Natural active pilot pose showing the physical engagement of flight and the mental intensity of the chase. The warm golden sunset light streams in from the cockpit windows, filling the cockpit with warm natural illumination. Action movie energy, cinematic chase quality.""",
            story_text="Disguise six: Pilot! The villain tried to escape by plane, but Agent {name} was ready. Taking the controls like a pro, our hero gave chase through the clouds!",
            costume="wearing pilot uniform with captain's hat",
            face_expression="intense focus and thrill, determined, exhilarated, quick-thinking"
        ),
        PageTemplate(
            page_number=9,
            scene_description="Final showdown and victory",
            scene_type="triumph",
            realistic_prompt="""TRIUMPHANT ROOFTOP VICTORY SCENE at sunset. Wide cinematic composition: A dramatic city rooftop at golden hour — the skyline stretching in every direction, golden sunset light washing over everything in warm amber and orange, long shadows across the rooftop surface. In the background, a cartoonish non-threatening villain is being led away by friendly agents in suits, the situation clearly resolved. Below, city lights are beginning to twinkle as evening approaches. The rooftop railing and the vast cityscape create a spectacular backdrop of achievement. The child named {name} in sleek black spy suit standing on the rooftop in a natural confident victory pose — one hand on hip, the other relaxed at the side. Wind gently lifting their hair slightly. Natural expression of quiet proud satisfaction at a mission accomplished, a genuine smile of triumph. The warm golden sunset from the west illuminates the scene from the side, creating beautiful warm light across the rooftop while the city skyline glitters behind. Cinematic heroic shot with the city as witness to the victory. A small soft comic-style speech bubble near the child containing EXACTLY the text "Mission complete.", calm and confident, subtle and not covering the face.""",
            story_text="Mission complete! On the city rooftop, {name} confronted the villain and saved the day. The city was safe, all thanks to the bravest, cleverest secret agent ever!",
            costume="wearing sleek black spy suit"
        ),
        PageTemplate(
            page_number=10,
            scene_description="Medal ceremony and celebration",
            scene_type="resolution",
            realistic_prompt="""ELEGANT AWARD CEREMONY SCENE at spy headquarters. Wide warm celebratory composition: A sleek awards setting — a podium area with subtle architectural elegance, soft golden spotlight from above creating a warm circle of recognition. In the soft bokeh background, the shapes of celebrating agents are visible — clapping hands, upright proud postures, a sense of community honor. Confetti pieces drifting gently through the warm air, each catching the spotlight light as it falls. The shiny gold medal on its ribbon is being placed carefully around the child's neck in the ceremony moment, its surface catching the warm spotlight in a brilliant gleam. The child named {name} in a formal black suit standing at the award position, beaming with genuine pride and happiness, a warm real smile of fulfillment on their face, eyes sparkling with the joy of recognition. Natural ceremony pose, a moment of honor being received gracefully. Warm golden light from the spotlight above illuminates the scene comfortably. Beautiful bokeh background with the celebrating agents. Emotional, celebratory, frame-worthy portrait of achievement.""",
            story_text="At headquarters, {name} received the Golden Star Medal—the highest honor for a secret agent. But the best reward? Knowing that being brave, clever, and kind can make the whole world better.",
            costume="wearing formal black suit with gold medal",
            face_expression="beaming pride and happiness, radiant joy, warm fulfilled smile, eyes sparkling"
        ),
    ]
)
