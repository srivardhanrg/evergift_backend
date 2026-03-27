"""
StoryGift Cosmic Dreamer Theme - Journey to the Stars.

Complete 10-page story: "[NAME]'s Cosmic Adventure"
Premium theme featuring a magical museum-to-space journey.
Optimized for maximum face resemblance with portrait-style compositions.

FACE CONSISTENCY RULES:
- Every prompt has child's face as focal point
- Front-facing or gentle three-quarter views only
- Simple, natural expressions (wonder, joy, peace)
- Helmet always off or visor up
- Skin tone preservation in every scene
- No action shots with small figures
- Gender-neutral language throughout

TO REVERT: Replace this file with storygift_cosmic_dreamer_backup.py
"""

from app.stories.templates import StoryTemplate, PageTemplate


STORYGIFT_COSMIC_DREAMER_THEME = StoryTemplate(
    theme_id="storygift_cosmic_dreamer",
    title_template="{name}'s Cosmic Adventure",
    cover_display_title="Cosmic Adventure",
    description="Watch your child reach for the stars on an epic space journey",
    default_costume="wearing a premium white and silver astronaut suit with gold star accents",
    protagonist_description="bright curious eyes, expression of gentle wonder",
    # Cover page settings - UNCHANGED (user said cover is perfect)
    cover_costume="wearing a premium white and silver NASA-style astronaut suit with gold visor reflecting stars and galaxies, heroic stance",
    cover_header_atmosphere="Deep space with vibrant purple and blue nebula clouds, twinkling stars, and a shooting star trail across the cosmic sky",
    cover_magical_elements="Glowing asteroid surface beneath feet, stardust particles floating around the body (not face). A distant Earth glows blue in the background. Golden rim lighting creates an epic silhouette.",
    cover_footer_description="Glowing asteroid surface with crystalline formations and cosmic dust",
    pages=[
# === PAGE 1 - THE SPACE MUSEUM ===
    PageTemplate(
        page_number=1,
        scene_description="Child at Space Museum looking up at rocket",
        scene_type="discovery",
        realistic_prompt="""Space Museum scene. The child named {name} in casual clothes standing in a grand space museum hall, looking up at a large silver rocket display with wonder and amazement. The child is positioned in the foreground, face turned upward with a gentle smile and dreamy eyes, clearly visible and well-lit by warm museum lights. The rocket is in the background, large and impressive. Planets and stars hang from the ceiling as decorations. Simple clean composition with child as the clear focal point. Child's face shows longing and wonder. Child's natural skin tone preserved exactly as in reference photo regardless of scene lighting. Warm cinematic museum atmosphere. A small gentle comic-style speech bubble near the child saying "I wish I could fly...", subtle and not covering the face.""",
        story_text="{name} had always dreamed of flying to the stars. At the Space Museum, standing before the most beautiful rocket, {name} looked up and whispered, 'I wish I could fly in a real rocket, just once.'",
        costume="wearing casual clothes"
    ),

        # === PAGE 2 - THE ROCKET AWAITS ===
        PageTemplate(
            page_number=2,
            scene_description="Child walks toward open spaceship door — camera inside the ship looking out",
            scene_type="wonder",
            realistic_prompt="""Cinematic POV shot from inside the open spaceship doorway looking outward. The camera is positioned just inside the glowing doorway of a magnificent silver and gold spaceship, looking out through the open hatch into a moonlit field at night. The spaceship's interior doorframe surrounds the edges of the frame like a dramatic cinematic border — warm glowing golden light from inside the ship spills outward through the doorway, illuminating the scene ahead. The child named {name} in casual clothes is walking forward across the dewy moonlit grass directly toward us — directly toward the open door — face naturally and fully front-facing toward camera with an expression of amazed, joyful excitement and wonder, bright natural smile, eyes wide. The warm golden glow from inside the ship falls forward beautifully onto the child's face as a perfect key light, fully illuminating their face from the front with no shadows. The starry night sky stretches above and around the child in the background, with the moonlit grassy field around their feet. The child's arms swing forward slightly in their walking motion, leaning in with excitement, heading toward the light and the adventure inside. Composition: child centered, face filling a generous portion of the frame, doorway framing the shot like a classic cinematic reveal. Child's face is the clear emotional focal point, naturally lit by the warm ship interior. Child's natural skin tone preserved exactly as in reference photo. A small curious comic-style speech bubble near the child saying "Is this for me?", subtle and not covering the face.""",
            story_text="Then something magical happened! {name} found a real spaceship waiting in a moonlit field, its door glowing and open wide. A gentle voice whispered, 'We've been waiting for you, {name}. Are you ready for an adventure?'",
            costume="wearing casual clothes"
        ),

        # === PAGE 3 - TRANSFORMATION ===
        PageTemplate(
            page_number=3,
            scene_description="Transforming into a little astronaut",
            scene_type="preparation",
            realistic_prompt="""Magical transformation scene. The child named {name} standing proudly in a beautiful white astronaut suit with silver and gold star accents. The helmet is held under one arm (not on head), showing the child's face clearly. Swirling golden stardust sparkles around the child. Child has a confident, happy expression with a natural smile, looking directly at camera. The suit glows softly with magical light. Starry space visible in background. Child's face is the absolute focal point, well-lit, detailed, front-facing portrait style. Premium cinematic quality. Child's natural skin tone preserved exactly as in reference photo regardless of scene lighting. A small excited comic-style speech bubble near the child saying "I'm really going to space!", subtle and not covering the face.""",
            story_text="With a swirl of stardust, {name} was wrapped in the most amazing astronaut suit—white and silver with golden stars! It fit perfectly, as if it was made just for {name}. The adventure was about to begin!",
            costume="wearing white astronaut suit with gold star accents, helmet held under arm"
        ),

        # === PAGE 4 - BLAST OFF ===
        PageTemplate(
            page_number=4,
            scene_description="Launching into space in the rocket",
            scene_type="wonder",
            realistic_prompt="""Exciting rocket cockpit scene. The child named {name} in astronaut suit (helmet off, resting beside), seated in a colorful rocket ship cockpit with glowing buttons and screens. Child looking out the large circular window with an excited, joyful expression, natural happy smile. Through the window: Earth getting smaller, stars getting brighter, colorful clouds rushing past. Colorful control panel lights illuminate the child's delighted face. Child facing three-quarter angle toward window but face clearly visible to camera. Warm interior lighting mixed with blue starlight from outside. Child's natural skin tone preserved exactly as in reference photo regardless of scene lighting. Pixar-quality cinematic scene. A small playful comic-style sound bubble near the window saying "WHOOSH!", subtle and not covering the face.""",
            story_text="'3... 2... 1... BLAST OFF!' The rocket zoomed up, up, UP through the clouds! {name} looked out the big round window and laughed with pure joy. The Earth grew smaller, and the stars grew closer!",
            costume="wearing astronaut suit, helmet off"
        ),

        # === PAGE 5 - FLOATING IN WONDER ===
        PageTemplate(
            page_number=5,
            scene_description="Floating in zero gravity inside spacecraft",
            scene_type="wonder",
            realistic_prompt="""Magical zero gravity scene inside a spacecraft. The child named {name} in astronaut suit floating gently in the cabin, arms spread out in joy, small glowing stars floating around. Child's face shows pure delight with a bright natural smile, looking toward camera. Soft blue and purple ambient light from windows showing space outside. The child is floating but face is clearly visible, well-lit, front-facing. Dreamy, weightless atmosphere. Small sparkles and stars drift past gently. Child's natural skin tone preserved exactly as in reference photo regardless of scene lighting. Whimsical, magical quality. A small joyful comic-style speech bubble near the child saying "This is the best feeling ever!", subtle and not covering the face.""",
            story_text="Inside the spacecraft, {name} floated like a feather! Spinning slowly, giggling, reaching out to catch floating stars that danced through the cabin. 'This is the best feeling ever!' {name} whispered.",
            costume="wearing astronaut suit"
        ),

        # === PAGE 6 - WALKING ON THE MOON ===
        PageTemplate(
            page_number=6,
            scene_description="First steps on the moon surface",
            scene_type="triumph",
            realistic_prompt="""Epic moon landing scene. The child named {name} in astronaut suit standing on the silvery moon surface, making a small bounce with arms out for balance, enjoying the low gravity. Helmet visor is flipped up, showing the child's excited, wonder-filled face with a joyful expression and natural smile. Earth glows blue and beautiful in the black starry sky behind. Moon dust sparkles like glitter around the child's boots. Child's face is the hero of the shot, clearly visible, well-lit by soft Earthlight. Cinematic, awe-inspiring composition. Child's natural skin tone preserved exactly as in reference photo regardless of scene lighting. A small triumphant comic-style speech bubble near the child saying "I'm really on the Moon!", subtle and not covering the face.""",
            story_text="The rocket landed softly on the Moon with a gentle POOF of silver dust. {name} took one small step onto the glittery surface—and started bouncing! Every jump went higher and higher into the starry sky!",
            costume="wearing astronaut suit with visor flipped up"
        ),

        # === PAGE 7 - THE RAINBOW NEBULA ===
        PageTemplate(
            page_number=7,
            scene_description="Floating in a beautiful colorful nebula",
            scene_type="wonder",
            realistic_prompt="""Breathtaking nebula scene. PORTRAIT COMPOSITION - The child named {name} in astronaut suit with HELMET COMPLETELY OFF (helmet held at side or not visible), standing confidently on a small glowing asteroid platform, surrounded by a magnificent swirling nebula of pink, purple, blue, and gold colors in the background. Child's face DIRECTLY FACING THE CAMERA - head straight, no tilt - with expression of peaceful awe and gentle wonder, soft smile. Child's face is the clear PRIMARY FOCAL POINT - takes up 25-30% of frame height, illuminated by soft warm neutral light from the front. The nebula colors create beautiful rim glow around hair and suit outline but do NOT wash over the face. Child's natural skin tone fully preserved, no color cast. Stars twinkle in the soft-focus background. Child's face large and clearly detailed. Award-winning space photography quality. A small amazed comic-style speech bubble near the child saying "It's like being inside a rainbow!", subtle and not covering the face.""",
            story_text="The rocket carried {name} to the Rainbow Nebula—a magical cloud of colors swirling through space! Pink, purple, blue, and gold danced together like paint in water. 'It's like being inside a rainbow!' {name} gasped.",
            costume="wearing astronaut suit, helmet off",
            face_expression="peaceful awe and gentle wonder, soft amazed smile, eyes looking directly at camera, face straight forward"
        ),

        # === PAGE 8 - CATCHING STARDUST ===
        PageTemplate(
            page_number=8,
            scene_description="Collecting magical stardust in a jar",
            scene_type="bonding",
            realistic_prompt="""Enchanting stardust collection scene. PORTRAIT COMPOSITION - The child named {name} in astronaut suit with HELMET COMPLETELY OFF (no helmet visible), standing and holding a glowing glass jar filled with swirling golden stardust at chest height. Child's face DIRECTLY FACING THE CAMERA - head straight, no tilt, no downward look - with soft peaceful smile and expression of proud wonder, as if showing the treasure to the viewer. Child's face is the clear PRIMARY FOCAL POINT - takes up 25-30% of frame height. The jar's warm golden glow illuminates the child's face from below-front at chest level, creating soft warm lighting on face. Space and stars visible in the soft-focus background. Child's face large and clearly detailed, natural skin tone preserved. Intimate, magical moment. Cinematic warm lighting.""",
            story_text="Floating through the nebula, {name} discovered something magical—real stardust! Holding out a special jar, {name} watched as golden stardust swirled inside, glowing like captured sunshine. A treasure from the stars!",
            costume="wearing astronaut suit, helmet off",
            face_expression="soft peaceful smile, proud wonder, eyes looking directly at camera, face straight forward"
        ),

        # === PAGE 9 - HOMEWARD BOUND ===
        PageTemplate(
            page_number=9,
            scene_description="Looking at Earth from space, heading home",
            scene_type="peaceful",
            realistic_prompt="""Emotional homecoming scene. The child named {name} in astronaut suit, standing at a large spacecraft window, both hands pressed gently against the glass. Child in three-quarter view, face turned toward camera with a warm, peaceful smile of contentment and happiness — face clearly visible and well-lit. Warm interior spacecraft lighting illuminates the child's face naturally from the front, with only subtle cool blue as a gentle rim on the edges of the suit and hair — face preserves full natural skin tone with no blue color cast. The beautiful blue Earth is visible through the window to the side. No reflections in the window glass. Tender, heartwarming moment. Child's natural skin tone preserved exactly as in reference photo regardless of scene lighting. Cinematic, emotional quality. A small gentle comic-style speech bubble near the child saying "That's where everyone I love lives.", subtle and not covering the face.""",
            story_text="As the rocket turned toward home, {name} pressed both hands against the window and gazed at Earth—a beautiful blue marble wrapped in white clouds. 'That's where everyone I love lives,' {name} smiled. 'I can't wait to tell them everything!'",
            costume="wearing astronaut suit"
        ),

        # === PAGE 10 - SWEET DREAMS ===
        PageTemplate(
            page_number=10,
            scene_description="Back in bed with stardust jar glowing",
            scene_type="sleeping",
            face_expression="drowsy, heavy-lidded, softly dreaming, peaceful smile",
            realistic_prompt="""Cozy, heartwarming bedroom scene. The child named {name} tucked into bed in cozy pajamas, hugging a glowing jar of golden stardust close to chest. Child's face resting on the pillow, eyes heavy-lidded and softly drooping — drowsy and drifting into sleep, a gentle content smile on their face. Eyes NOT squeezed shut but naturally and softly closing, lashes resting lightly, enough facial feature visibility for a warm recognizable expression. The stardust jar's warm golden glow illuminates the child's face from the side at pillow level — natural soft sidelight, no harsh upward shadows. Through the window, the bright star twinkles in the night sky as if saying goodnight. Soft bedroom lighting, cozy blankets, stuffed space toys nearby. Child's face is the emotional focal point, clearly visible, peaceful expression. Warm, loving atmosphere. Child's natural skin tone preserved exactly as in reference photo regardless of scene lighting. A faint dreamy comic-style thought bubble above the child containing a tiny glowing rocket surrounded by small sparkling stars, subtle and not covering the face.""",
            story_text="Safe in bed, {name} hugged the jar of stardust close—proof that the adventure was real. The stars twinkled outside the window as if to say goodnight. {name} smiled and whispered, 'Dreams really do come true.' And in sleep that night, {name} danced among the stars once more.",
            costume="wearing cozy pajamas"
        ),
    ]
)
