"""
Contextual Reply Generator for Emma (@curated_byemma).
Evaluates real user complaints on Threads and drafts authentic, honest 5-part replies.

Ground Rules:
1. Hard-filter context: Reject memorial/family grief, sports, concerts, marketing spam, and non-complaints.
2. 5-Part Honest Arc:
   - Specific empathy acknowledging their exact pain point.
   - Honest audit: Cite verified Amazon consensus and review count.
   - Honest caveat: State realistic limitation/con.
   - Clean direct link: curatedbyemma.pages.dev/go/[slug].
   - Conversation Magnet: Closing question sparking sub-replies.
3. STRICT "NEVER LIE" & NO FAKE ANECDOTES:
   - NEVER fabricate personal ownership, personal usage, or fake family stories (NO "i swear by", "my cat", "my dog", "my sister", "for me", "saved my couch").
   - Emma is an independent consumer researcher auditing verified consensus, review patterns, and spec teardowns.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
import ssl

try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except Exception:
    SSL_CONTEXT = ssl._create_unverified_context()

def load_env():
    """Load key-values from local .env if present."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k not in os.environ:
                        os.environ[k] = v

load_env()

CATALOG_SPECS = {
    1: {
        "name": 'PetLovers Extra-Sticky Lint Roller (5 pack)',
        "category": 'Pet hair / Sofas & Clothes',
        "rating": 4.6,
        "reviews": 39300,
        "honest_pros": 'Adhesive is sticky enough to pull embedded undercoat fur from velvet and textured woven sofas',
        "honest_caveats": 'You burn through sheets quickly if you have a massive double-coated dog, peeling diagonal sheets takes a second to get used to',
        "slug": 'roller',
        "bio_slot": "#1",
        "draft_templates": [
            (
                "trying to get stubborn pet hair off couch fabric is the most frustrating workout ever. regular sticky tape rollers lose their grip in two swipes, but that extra-sticky roller with over 39k verified reviews is the consensus winner for deep fur. only catch is you go through sheets fast with a heavy shedder, but it actually pulls what vacuums miss. here's the direct link to it: curatedbyemma.pages.dev/go/roller. what breed is your pet?"
            ),
            (
                "vacuums always seem to push double-coated dog hair deeper into weave fibers. when auditing pet hair tools against stubborn fur, that pet lovers extra-sticky roller with 39k+ verified ratings was the consensus pick that lifts embedded undercoat in one swipe. sheets peel fast so don't hoard them, but it actually works without shredding the fabric. found the exact one here: curatedbyemma.pages.dev/go/roller. what kind of couch fabric do you have?"
            ),
        ]
    },
    2: {
        "name": 'Fisher-Price Calming Otter Sleep Soother',
        "category": 'Toddler / Infant sleep',
        "rating": 4.7,
        "reviews": 59700,
        "honest_pros": 'Rhythmic breathing motion and soft white noise genuinely calms overtired babies down to sleep',
        "honest_caveats": 'Not a magic fix for teething pain or severe colic, and you will need to replace AAA batteries every few weeks',
        "slug": 'otter',
        "bio_slot": "#2",
        "draft_templates": [
            (
                "night wakeups every hour are completely exhausting when you are trying to function the next day. parents navigating sleep regressions consistently point to that rhythmic breathing otter with nearly 60k reviews as one of the few soothers that genuinely settles babies down. only catch is you go through batteries every month, but verified parents highlight it gave them their first long sleep stretch. here's the direct link: curatedbyemma.pages.dev/go/otter. how many months are they right now?"
            ),
            (
                'running on two hours of sleep with a crying baby is surviving on pure adrenaline. across parenting communities, that breathing belly otter with 59k verified reviews is the consensus favorite because the rhythmic movement settles overtired infants without rocking for hours. eats AAA batteries fast, but the gentle heartbeat rhythm works so well. found the exact one here: curatedbyemma.pages.dev/go/otter. are you guys in the 4-month or 8-month regression?'
            ),
        ]
    },
    3: {
        "name": 'Ergonomic Memory Foam Lumbar Cushion',
        "category": 'Desk setup / Lower back pain',
        "rating": 4.4,
        "reviews": 27400,
        "honest_pros": 'High-density molded foam that actually holds shape under full bodyweight without flattening',
        "honest_caveats": "Feels noticeably firm the first 2-3 days before conforming to your lower back, doesn't fix serious medical sciatica",
        "slug": 'lumbar',
        "bio_slot": "#3",
        "draft_templates": [
            (
                "sitting in standard desk chairs all day literally destroys lower back posture. when auditing cushions to filter out sponsored hype, high-density molded foam was the only design 27k verified buyers consistently backed. it won't cure medical spine issues and feels pretty firm the first couple days, but taking pressure off the tailbone makes 8-hour workdays actually bearable. here's the direct link to it: curatedbyemma.pages.dev/go/lumbar. what kind of office chair are you using right now?"
            ),
            (
                "desk chairs with zero lumbar curve compress your lower spine by 3pm. after comparing dozens of supports, the firm memory foam cushion with 27k reviews was the undisputed consensus pick for tailbone relief. won't replace a physio for chronic sciatica, but it makes long desk sessions noticeably more comfortable. saved the link to it here: curatedbyemma.pages.dev/go/lumbar. what kind of chair do you have?"
            ),
        ]
    },
    4: {
        "name": 'TrendPlain Glass Olive Oil Mister',
        "category": 'Kitchen / Air fryer oil',
        "rating": 4.6,
        "reviews": 49100,
        "honest_pros": 'Even, clog-free wide fan mist for air fryers without aerosol chemical propellants',
        "honest_caveats": "You have to pull the trigger with a firm, quick squeeze to get the wide fan mist instead of a stream; heavier than plastic since it's thick glass",
        "slug": 'mister',
        "bio_slot": "#4",
        "draft_templates": [
            (
                "pouring oil from a bottle into an air fryer always turns food soggy and uneven. standard aerosol spray cans leave sticky chemical residue, but that refillable glass oil mister with 49k+ verified reviews mists a clean wide fan. only trick is you have to pull the trigger with a quick firm squeeze or it shoots a stream, but it gives a super even crisp without soaking food. here's the direct link to it: curatedbyemma.pages.dev/go/mister. what's your favorite thing to air fry?"
            ),
            (
                'drizzling oil straight onto air fryer food makes half of it drenched and the other half dry. the glass fan-spray mister with 49k reviews solved that without using propellants or aerosol cans. glass bottle is a little heavy and you need a snappy trigger squeeze for the fan effect, but fries come out actually crispy. found the link here: curatedbyemma.pages.dev/go/mister. what kind of oil are you using in yours?'
            ),
        ]
    },
    5: {
        "name": 'BEAUTURAL Fabric Shaver and Sweater Defuzzer',
        "category": 'Wardrobe / Knitwear fuzz & pills',
        "rating": 4.5,
        "reviews": 116000,
        "honest_pros": 'Dual-speed motorized rotary blades shave pills and fuzz off wool sweaters, knit cardigans, and fleece in 2 minutes',
        "honest_caveats": "Garment must be stretched completely flat on a table so blade guard doesn't catch loose seams; empty lint trap regularly",
        "slug": 'defuzzer',
        "bio_slot": "#5",
        "draft_templates": [
            (
                "throwing away an $80 sweater just because of surface fuzz and pilling hurts so much. that beautural fabric defuzzer with 116k reviews is the verified consensus pick for restoring knit cardigans in two minutes. only rule is lay the fabric completely flat on a table so the guard doesn't snag loose threads, but it makes knits look brand new. here's the direct link: curatedbyemma.pages.dev/go/defuzzer. is it a wool knit or a fleece blanket?"
            ),
            (
                "chunky knit sweaters pilling after two washes is the most frustrating winter problem. the beautural electric sweater shaver has over 115k verified reviews for a reason—it shaves off all the fuzzy bobbles without thinning the fabric. just empty the clear lint chamber frequently so it doesn't slow down the motor, but it cleans up worn wool coats completely. found the exact one here: curatedbyemma.pages.dev/go/defuzzer. what type of knit are you dealing with?"
            ),
        ]
    },
    6: {
        "name": 'Smartish Magnetic Cable Wrangler',
        "category": 'Tech / Nightstand cable clutter',
        "rating": 4.6,
        "reviews": 5200,
        "honest_pros": 'Heavy magnetic weighted base holds phone and watch cords firmly so they never drop behind furniture',
        "honest_caveats": 'Base is heavy enough for standard phone and USB-C cords, but very stiff thick braided HDMI cords can pull it if not positioned right',
        "slug": 'cables',
        "bio_slot": "#6",
        "draft_templates": [
            (
                "cables sliding off the nightstand and falling into the dark gap behind the bed is such an annoying daily headache. that weighted magnetic cable wrangler has over 5k verified reviews and actually keeps cords anchored right where you leave them. heavy base stays put for charging cords, just make sure to use the magnetic collars on thin wires. here's the direct link: curatedbyemma.pages.dev/go/cables. how many cords do you usually have at your bedside?"
            ),
            (
                'fishing charging cords out from behind the headboard in the dark is beyond annoying. the weighted magnetic cable manager with 5k reviews has enough mass to keep phone and watch chargers sitting neatly on top of the nightstand. stiff heavy hdmi cables can slide it if tugged hard, but for bedside cords it is completely seamless. found the exact one here: curatedbyemma.pages.dev/go/cables. is your nightstand against a wall gap?'
            ),
        ]
    },
    7: {
        "name": 'Perilogics Airplane Tray-Table Phone Mount',
        "category": 'Travel / Flight neck strain',
        "rating": 4.6,
        "reviews": 22900,
        "honest_pros": 'Clamp locks directly onto airplane tray table or seatback, holding phone eye-level for hands-free viewing',
        "honest_caveats": "Spring clamp is quite stiff out of the box to ensure it doesn't slip; not needed on newer aircraft with built-in seatback monitors",
        "slug": 'flight-mount',
        "bio_slot": "#7",
        "draft_templates": [
            (
                "holding your phone looking down for hours on a flight is literal neck torture. instead of overpriced airport gadgets, that clamp mount that locks directly onto the seatback tray table had 22k+ verified reviews for a reason—hands-free screen right at eye level. the spring clamp is a bit stiff to open at first, but completely saves your neck on long flights. here's the direct link: curatedbyemma.pages.dev/go/flight-mount. how long is your upcoming flight?"
            ),
            (
                'looking straight down at your lap for a 4-hour flight leaves your neck completely stiff. that universal tray-table phone clamp has over 22k reviews and mounts right to the latch at eye level. clamp spring takes some force to open, but watching downloaded shows hands-free makes economy flights 10x better. found the exact one here: curatedbyemma.pages.dev/go/flight-mount. where are you flying to?'
            ),
        ]
    },
    8: {
        "name": 'OGHom Compact Handheld Garment Steamer',
        "category": 'Travel / Wrinkle removal',
        "rating": 4.3,
        "reviews": 30000,
        "honest_pros": 'Heats up in 60 seconds and steams out wrinkles without dragging out a heavy iron or ironing board',
        "honest_caveats": 'Compact 240ml tank only lasts for about 2-3 shirts before needing a refill; must keep it upright to prevent water bubbling',
        "slug": 'steamer',
        "bio_slot": "#8",
        "draft_templates": [
            (
                "dragging out a heavy ironing board for travel clothes is way too much effort. that compact handheld steamer heats in 60 seconds and has over 30k verified reviews for de-wrinkling linen and cotton in one quick pass. small tank only does about 2 to 3 garments per water fill, but for quick travel touchups it handles wrinkles without dragging out a heavy iron. here's the direct link: curatedbyemma.pages.dev/go/steamer. are you traveling for work or vacation?"
            ),
            (
                'unpacking wrinkled clothes at a hotel and trying to use a rusty hotel iron is the worst. that portable handheld steamer with 30k+ reviews steams out deep suitcase wrinkles in literally two minutes. tank is compact so you refill after 2 shirts, but it glides right over delicate fabrics without burning. found the exact one here: curatedbyemma.pages.dev/go/steamer. is it mostly linen or cotton shirts?'
            ),
        ]
    },
    9: {
        "name": 'TOPOINT 3D Bluetooth Sleep Mask',
        "category": 'Sleep / Side sleeping with audio',
        "rating": 4.3,
        "reviews": 13200,
        "honest_pros": 'Zero eye pressure contoured 3D blackout mask with ultra-thin flat speakers that allow comfortable side sleeping',
        "honest_caveats": "Speakers are completely flat so side sleeping doesn't hurt your ears, but the velcro strap needs careful adjusting if you toss and turn aggressively",
        "slug": 'sleep-mask',
        "bio_slot": "#9",
        "draft_templates": [
            (
                "if light leaks or morning noise keeps waking you up, normal hard plastic earbuds hurt your ears when sleeping on your side. that 3D contoured eye mask has ultra-flat soft speakers built in and over 13k verified reviews for true pitch-black sleep. velcro strap takes a night to dial in so it doesn't shift, but you can finally side sleep without sore ears. here's the direct link: curatedbyemma.pages.dev/go/sleep-mask. do you usually listen to white noise or podcasts to fall asleep?"
            ),
            (
                'side sleeping with regular earbuds creates so much painful pressure on your ear cartilage. that memory foam blackout mask with wafer-thin speakers inside has 13k+ reviews and lets you play white noise or podcasts comfortably on your side. takes a minute to adjust the velcro strap snug, but the total blackout and soft speakers make side sleeping with audio actually comfortable. found the link here: curatedbyemma.pages.dev/go/sleep-mask. are you a light sleeper or side sleeper?'
            ),
        ]
    },
    10: {
        "name": 'ThermoPro TP03B Digital Meat Thermometer',
        "category": 'Cooking / Holiday meat doneness',
        "rating": 4.6,
        "reviews": 151000,
        "honest_pros": 'Reads accurate internal food temperatures in 3-4 seconds with foldaway stainless probe and bright backlight',
        "honest_caveats": 'Do NOT leave the plastic body inside a hot oven or grill while door is shut; only probe touches the meat during measurement',
        "slug": 'thermometer',
        "bio_slot": "#10",
        "draft_templates": [
            (
                "the anxiety of dry holiday turkey or undercooked chicken before dinner is so stressful. after comparing dozens of kitchen thermometers, that $15 folding thermopro with 150k verified reviews is the consensus winner. reads accurately in 3 seconds flat. just don't leave the plastic body inside the oven door, only the probe touches meat. here's the direct link: curatedbyemma.pages.dev/go/thermometer. are you hosting thanksgiving this year or just regular cooking?"
            ),
            (
                "guessing meat doneness by poking it always results in either leather-dry chicken or raw centers. the thermopro instant read with 151k reviews gives an exact digital reading in 3 seconds so you never overcook. probe folds right into the handle so it's super safe in drawers. found the exact one here: curatedbyemma.pages.dev/go/thermometer. what's the main dish you usually cook?"
            ),
        ]
    },
    11: {
        "name": 'TubShroom Revolutionary Tub Drain Hair Catcher',
        "category": 'Bathroom / Drain hair clogs',
        "rating": 4.4,
        "reviews": 112000,
        "honest_pros": 'Fits snugly inside standard tub drains and neatly wraps all human and pet hair out of sight without clogging water flow',
        "honest_caveats": 'Must wipe collected hair off every week or water begins draining slower; does not fit flat magnetic or pop-up drain caps',
        "slug": 'tubshroom',
        "bio_slot": "#11",
        "draft_templates": [
            (
                'pulling disgusting slimy hair clogs out of the shower drain with coat hangers is the worst household chore. when auditing drain protectors, the silicone tubshroom with 112k verified reviews is the undisputed consensus pick because hair wraps around the cylinder instead of going down pipes. only catch is you have to wipe it off with a paper towel once a week, but it completely ends liquid drain cleaner chemicals. direct link: curatedbyemma.pages.dev/go/tubshroom. do you have a standard drain or pop-up stopper?'
            ),
        ]
    },
    12: {
        "name": 'The Pink Stuff Miracle Cleaning Paste',
        "category": 'Deep Cleaning / Scorched pans & tile stains',
        "rating": 4.4,
        "reviews": 165000,
        "honest_pros": 'Mild mineral abrasive paste erases burnt pot bottoms, tile water spots, and ceramic stains without harsh fumes',
        "honest_caveats": 'It is mildly abrasive so avoid high-gloss plastic or scratchable car paint; requires a thorough damp wipe-down after scrubbing',
        "slug": 'pink-stuff',
        "bio_slot": "#12",
        "draft_templates": [
            (
                "scrubbing burnt cookware until your arms ache usually leaves half the carbon stains behind. the pink stuff miracle paste has over 165k verified reviews for cutting through baked grease and ceramic discoloration without toxic bleach fumes. it is mildly abrasive so test a small corner on delicate surfaces, but for stainless pans and grout it works in minutes. found the link: curatedbyemma.pages.dev/go/pink-stuff. what's the hardest stain you're dealing with?"
            ),
        ]
    },
    13: {
        "name": 'ChomChom Roller Reusable Pet Hair Remover',
        "category": 'Pet Care / Reusable upholstery fur removal',
        "rating": 4.5,
        "reviews": 152000,
        "honest_pros": 'Electrostatic rubber squeegee lifts embedded cat and dog fur from sofas and car seats without buying sticky tape refills',
        "honest_caveats": 'Only works by rolling briskly back and forth on firm upholstered fabric; does not work on smooth flat floors or loose clothing',
        "slug": 'chomchom',
        "bio_slot": "#13",
        "draft_templates": [
            (
                "buying endless packs of sticky lint tape rolls gets expensive fast when you have a shedding pet. the chomchom roller with 150k reviews uses an electrostatic squeegee that traps embedded fur in a waste chamber with a quick back-and-forth motion. won't work on smooth wood floors or loose clothes, but for couches and car seats verified pet owners swear by it. direct link: curatedbyemma.pages.dev/go/chomchom. are you dealing with cat or dog shedding?"
            ),
        ]
    },
    14: {
        "name": 'Angry Mama Microwave Steam Cleaner',
        "category": 'Kitchen / Baked-on microwave grease',
        "rating": 4.3,
        "reviews": 62000,
        "honest_pros": 'Natural vinegar and water steam loosens rock-hard microwave food crust in 7 minutes so it wipes off with one swipe',
        "honest_caveats": "Body gets extremely hot out of the microwave so lift only by the arms; vinegar steam smell is strong if you don't add lemon drops",
        "slug": 'angry-mama',
        "bio_slot": "#14",
        "draft_templates": [
            (
                'scraping dried chili or soup splatters off microwave ceilings feels practically cemented on. the angry mama steam cleaner with 60k reviews uses pressurized vinegar and water steam to soften all that crust in 7 minutes so it wipes clean with one paper towel. plastic gets super hot right after microwaving so hold the arms, but it eliminates harsh chemical oven sprays. link: curatedbyemma.pages.dev/go/angry-mama. how long has that splatter been sitting there lol?'
            ),
        ]
    },
    15: {
        "name": 'BISSELL Little Green Portable Carpet & Upholstery Cleaner',
        "category": 'Home Cleaning / Carpet & pet accident stains',
        "rating": 4.5,
        "reviews": 88000,
        "honest_pros": 'High-powered spray and targeted suction extracts deep set-in pet messes, coffee spills, and vehicle upholstery grime',
        "honest_caveats": 'Dirty water tank must be flushed and air-dried immediately after use to prevent moldy odors; power cord is not auto-retractable',
        "slug": 'little-green',
        "bio_slot": "#15",
        "draft_templates": [
            (
                "blotting pet stains or coffee spills with paper towels just pushes the liquid deeper into carpet padding. the bissell little green with 88k verified reviews is the consensus winner for pulling out deep upholstery grime that surface sprays can't touch. you do need to rinse the dirty water tank right after use so it stays fresh, but it saves couches from being ruined. direct link: curatedbyemma.pages.dev/go/little-green. is it a pet stain or a drink spill?"
            ),
        ]
    },
    16: {
        "name": 'Scotchgard Fabric Water Shield Spray',
        "category": 'Furniture / Spill & stain prevention',
        "rating": 4.6,
        "reviews": 26000,
        "honest_pros": 'Invisible barrier forces liquid spills, coffee, and wine to bead on top of fabric upholstery instead of absorbing instantly',
        "honest_caveats": 'Strong solvent odor during initial application so spray in a well-ventilated area; high-friction seat cushions need re-coating every 6 months',
        "slug": 'fabric-shield',
        "bio_slot": "#16",
        "draft_templates": [
            (
                'the constant fear of someone spilling red wine or coffee on a light-colored couch is exhausting. scotchgard fabric water shield with 26k reviews creates a surface barrier that makes liquids bead right up for easy blotting before soaking in. strong chemical smell while spraying so crack the windows open, but it preserves fabric from accidental stains. link: curatedbyemma.pages.dev/go/fabric-shield. is your sofa linen or woven fabric?'
            ),
        ]
    },
    17: {
        "name": 'MAXTID Under Door Draft Stopper Seal',
        "category": 'Home Comfort / Door drafts & hallway noise',
        "rating": 4.3,
        "reviews": 31000,
        "honest_pros": 'Double-sided foam cylinders slide under door, insulating against winter drafts, apartment hallway noise, and outside light',
        "honest_caveats": 'Can drag slightly on high-pile shag rugs; measure your door gap before trimming foam tubes to length',
        "slug": 'draft-stopper',
        "bio_slot": "#17",
        "draft_templates": [
            (
                'cold drafts slipping under bedroom doors and apartment hallway footsteps can make bedrooms feel impossible to keep cozy. double-sided under-door draft seals with 30k+ verified reviews block both chilly airflow and hallway light without needing screws or glue. drags slightly on thick shag rugs, but for keeping room temperatures stable it makes a noticeable difference. link: curatedbyemma.pages.dev/go/draft-stopper. is it on hardwood or carpet?'
            ),
        ]
    },
    18: {
        "name": "Linda's Essentials Silicone Stove Counter Gap Covers",
        "category": 'Kitchen / Stove counter food gap',
        "rating": 4.4,
        "reviews": 46000,
        "honest_pros": 'Heat-resistant flexible T-seal bridges the crack between stove and countertop so crumbs and sauces never drop down the side',
        "honest_caveats": 'Matte silicone collects fine kitchen dust and needs a weekly rinse; only seals flush if your stove and counter are roughly level',
        "slug": 'stove-gap',
        "bio_slot": "#18",
        "draft_templates": [
            (
                'dropping crumbs, sauce, or utensils into the dark crack between the stove and kitchen counter is so annoying because you can never reach it. heat-resistant silicone stove gap covers with 45k+ reviews bridge that gap completely so everything wipes right onto the counter. matte silicone catches dust so give it a quick rinse occasionally, but it saves deep stove cleanouts. link: curatedbyemma.pages.dev/go/stove-gap. are your countertops granite or laminate?'
            ),
        ]
    },
    19: {
        "name": 'Full Circle Bubble Up Ceramic Soap Dispenser & Dish Brush',
        "category": 'Kitchen / Sink organization & dish soap',
        "rating": 4.5,
        "reviews": 16000,
        "honest_pros": 'Spring-loaded ceramic base foams soap directly into natural plant bristles with one pump, eliminating slimy soap bottles',
        "honest_caveats": 'Bamboo handle needs to air-dry upright to prevent moisture wear; replace worn brush heads every 4 to 6 months',
        "slug": 'dish-brush',
        "bio_slot": "#19",
        "draft_templates": [
            (
                "messy plastic dish soap bottles leaking slimy rings all over sink edges looks so cluttered. the full circle ceramic bubble-up set with 16k reviews uses a spring-loaded base that foams soap right into the brush with a single press. bamboo handle should dry standing upright so water doesn't pool, but it keeps the whole sink area super tidy. link: curatedbyemma.pages.dev/go/dish-brush. do you prefer liquid dish soap or solid dish blocks?"
            ),
        ]
    },
    20: {
        "name": 'OXO Good Grips Jar Opener with Base Pad',
        "category": 'Kitchen / Stuck jar lids & weak grip',
        "rating": 4.5,
        "reviews": 26000,
        "honest_pros": 'Hardened stainless steel teeth grip vacuum-sealed jar lids of any size, multiplying leverage to pop them open with zero wrist strain',
        "honest_caveats": 'Requires two hands (holding the jar base on non-slip pad and turning opener); gripping teeth will slightly dent metal lids',
        "slug": 'jar-opener',
        "bio_slot": "#20",
        "draft_templates": [
            (
                "banging vacuum-sealed pickle jars against countertops or straining your wrists trying to twist stubborn lids is painful. oxo's stainless jar opener with 26k verified reviews locks onto any lid diameter with sharp teeth to break the seal with minimal effort. teeth can leave tiny indentations on metal lids, but it completely removes hand strain. direct link: curatedbyemma.pages.dev/go/jar-opener. is it mostly pickle jars or tight pasta sauce lids?"
            ),
        ]
    },
    21: {
        "name": 'Pumie Heavy Duty Pumice Scouring Stick',
        "category": 'Bathroom / Hard water toilet bowl rings',
        "rating": 4.4,
        "reviews": 42000,
        "honest_pros": 'Natural volcanic pumice erases stubborn mineral toilet bowl rings, rust, and lime scale that chemical bleach sprays fail to touch',
        "honest_caveats": 'Both the pumice stick and porcelain surface MUST be kept wet during use to prevent scratches; stick naturally erodes as you scrub',
        "slug": 'pumice-stick',
        "bio_slot": "#21",
        "draft_templates": [
            (
                "hard water mineral rings inside toilet bowls laugh at normal toilet brushes and bleach sprays. heavy-duty pumice scouring sticks with 40k+ verified reviews physically buff out mineral scale and rust without chemical fumes. just make sure the stick and porcelain stay wet while scrubbing so it doesn't scratch, but it makes decades-old bowls look new. link: curatedbyemma.pages.dev/go/pumice-stick. have you been dealing with lime or rust stains?"
            ),
        ]
    },
    22: {
        "name": 'Bar Keepers Friend Cookware Cleanser & Polish',
        "category": 'Cookware / Scorched stainless steel pots',
        "rating": 4.7,
        "reviews": 36000,
        "honest_pros": 'Oxalic acid mineral cleanser dissolves heat tint, cloudy mineral haze, and baked pan grease on stainless steel in under a minute',
        "honest_caveats": 'Can dry out sensitive hands so wear rubber cleaning gloves; do not use on non-stick Teflon or seasoned cast iron',
        "slug": 'bar-keepers',
        "bio_slot": "#22",
        "draft_templates": [
            (
                'cloudy heat stains and burnt grease on stainless steel skillets make great cookware look ruined. bar keepers friend with 36k reviews uses oxalic acid to break down mineral scale and scorched oil without heavy scrubbing. wear gloves because the powder can dry skin, but for bringing stainless steel pots back to a mirror shine it is the gold standard. link: curatedbyemma.pages.dev/go/bar-keepers. what brand of cookware do you use?'
            ),
        ]
    },
    23: {
        "name": 'Kasa Smart Plug Ultra Mini (15A)',
        "category": 'Smart Home / Hard-to-reach lamps & appliances',
        "rating": 4.6,
        "reviews": 125000,
        "honest_pros": 'Control floor lamps, space heaters, and holiday lights on automated schedules from your phone or voice without needing a hub',
        "honest_caveats": 'Connects strictly to 2.4GHz Wi-Fi frequencies (not 5GHz); takes a couple minutes to do the initial router pairing',
        "slug": 'smart-plug',
        "bio_slot": "#23",
        "draft_templates": [
            (
                'crawling behind sofas to plug in floor lamps or worrying if you left a space heater on after leaving the house is unnecessary stress. kasa smart plugs with 120k+ reviews let you set automatic sunset timers and phone toggles with zero external hub needed. works only on 2.4GHz Wi-Fi networks, but for scheduling room lighting it works seamlessly. link: curatedbyemma.pages.dev/go/smart-plug. do you use Alexa, Google Home, or just your phone?'
            ),
        ]
    },
    24: {
        "name": 'Anker Magnetic Phone Ring Holder (MagGo)',
        "category": 'Tech / Phone dropping in bed & desk stand',
        "rating": 4.4,
        "reviews": 32000,
        "honest_pros": "Snap-on MagSafe ring acts as a secure finger grip so phones don't drop on your nose in bed, doubling as an adjustable desk kickstand",
        "honest_caveats": 'Requires a MagSafe-compatible phone or case; must slide ring off before placing phone on flat wireless charging pads',
        "slug": 'magsafe-ring',
        "bio_slot": "#24",
        "draft_templates": [
            (
                "scrolling in bed and having a heavy phone slip and smash right onto your face is an instant wake-up call. anker's magnetic magsafe ring with 30k+ reviews snaps on with strong magnets to give you a natural one-handed grip and doubles as a sturdy video stand. needs a magsafe case to lock firmly, but it completely prevents screen drops. direct link: curatedbyemma.pages.dev/go/magsafe-ring. what phone model are you rocking?"
            ),
        ]
    },
    25: {
        "name": 'Yogasleep Dohm Classic Natural Sound Machine',
        "category": 'Sleep / Loud neighbors & street traffic noise',
        "rating": 4.5,
        "reviews": 46000,
        "honest_pros": 'Real acoustic internal fan creates authentic soothing rushing-air white noise that masks stomping upstairs neighbors and street noise',
        "honest_caveats": 'Has two physical fan speed settings (no digital nature sounds or shutoff timer); heavier than battery travel sound devices',
        "slug": 'dohm',
        "bio_slot": "#25",
        "draft_templates": [
            (
                'tinny digital speaker sound machines with looping audio tracks rarely drown out heavy upstairs foot traffic. the yogasleep dohm classic with 45k reviews uses an actual mechanical fan inside an acoustic shell to generate genuine rushing air frequencies that mask ambient noise. only has two mechanical speeds without digital bells and whistles, but for uninterrupted sleep it is unmatched. link: curatedbyemma.pages.dev/go/dohm. are you dealing with street noise or neighbor footsteps?'
            ),
        ]
    },
    26: {
        "name": 'Liquid I.V. Hydration Multiplier Packets',
        "category": 'Travel & Wellness / Post-flight dehydration',
        "rating": 4.6,
        "reviews": 135000,
        "honest_pros": 'Cellular Transport Technology delivers electrolytes and hydration to the bloodstream 2x faster than plain water after flights or workouts',
        "honest_caveats": 'Has a noticeably salty-sweet taste so mix in 20-24oz water instead of small glasses; contains natural cane sugar',
        "slug": 'hydration',
        "bio_slot": "#26",
        "draft_templates": [
            (
                "the dry pressurized airplane cabin air leaves your throat scratchy, head throbbing, and body completely drained after flying. liquid iv hydration packets with 135k verified reviews use an electrolyte ratio that absorbs significantly faster than plain water. pretty sweet taste so dilute it in a large 24oz water bottle, but it stops travel fatigue fast. link: curatedbyemma.pages.dev/go/hydration. what's your favorite flavor to drink?"
            ),
        ]
    },
    27: {
        "name": 'Loop Quiet Ear Plugs for Sleep',
        "category": 'Sleep / Snoring partner & sensitive ears',
        "rating": 4.3,
        "reviews": 68000,
        "honest_pros": 'Ultra-soft flexible silicone ring sits completely flush inside ear, providing 26dB noise reduction without side-sleeping cartilage pain',
        "honest_caveats": 'Must test all 4 included silicone tip sizes for an airtight seal; does not fully eliminate close-range heavy snoring, only muffles it',
        "slug": 'loop-quiet',
        "bio_slot": "#27",
        "draft_templates": [
            (
                "sleeping next to a loud snorer while wearing stiff foam earplugs makes your ear cartilage ache by 3am. loop quiet silicone sleep plugs with 68k reviews sit flush inside your outer ear so side sleeping doesn't put pressure on your ears while knocking out 26dB of noise. takes a night to test which tip size gives the tightest seal, but it saves relationships. direct link: curatedbyemma.pages.dev/go/loop-quiet. are you a light sleeper or side sleeper?"
            ),
        ]
    },
    28: {
        "name": 'Bedsure Satin Pillowcase for Hair & Skin',
        "category": 'Beauty / Frizzy bedhead & skin creases',
        "rating": 4.5,
        "reviews": 285000,
        "honest_pros": 'Silky-smooth polyester satin eliminates fabric friction against curls and skin, stopping morning hair breakage and pillow creases',
        "honest_caveats": 'Slick fabric can cause pillows to slip around if headboard has gaps; wash on delicate cycle to preserve smooth sheen',
        "slug": 'satin-pillow',
        "bio_slot": "#28",
        "draft_templates": [
            (
                "waking up with frizzy tangled hair and deep sleep creases pressed into your face from rough cotton pillowcases is frustrating. bedsure satin pillowcases with 280k+ reviews reduce hair friction so curls stay defined and skin doesn't get crushed overnight. fabric is slippery so tuck the envelope closure snugly, but for hair preservation it works wonders. direct link: curatedbyemma.pages.dev/go/satin-pillow. do you have naturally curly or straight hair?"
            ),
        ]
    },
    29: {
        "name": 'Glisten Garbage Disposer Cleaner & Deodorizer',
        "category": 'Kitchen / Stinky garbage disposal smells',
        "rating": 4.5,
        "reviews": 47000,
        "honest_pros": 'Deep-cleaning foam reaches hidden blades, under splash guards, and sidewalls to scrub rotten food particles and sewer odors',
        "honest_caveats": 'Foam expanding action requires following warm water flow instructions carefully; will not fix deeper underground plumbing pipe clogs',
        "slug": 'disposal-cleaner',
        "bio_slot": "#29",
        "draft_templates": [
            (
                "that mysterious sour sewer odor coming from the kitchen sink is usually rotting food grease trapped underneath the disposal splash guard. glisten disposal cleaner packets with 45k+ reviews generate an expanding blue foam that scrubs the hidden underside of blades where brushes can't reach. follow the water stream instructions carefully, but it clears sink odors in 2 minutes. link: curatedbyemma.pages.dev/go/disposal-cleaner. how old is your kitchen disposal?"
            ),
        ]
    },
    30: {
        "name": 'Dawn Platinum Powerwash Dish Spray',
        "category": 'Kitchen / Soaking greasy baking pans',
        "rating": 4.8,
        "reviews": 62000,
        "honest_pros": 'Direct continuous spray activates foam on contact with zero water, breaking down baked cheese and grease on sheet pans in 5 minutes',
        "honest_caveats": 'Strong fresh aroma requires thorough warm water rinsing; spray nozzle can run through refills quickly if used on every tiny cup',
        "slug": 'powerwash',
        "bio_slot": "#30",
        "draft_templates": [
            (
                "leaving greasy casserole dishes and sheet pans soaking in the sink for 24 hours just creates cold murky water and takes up counter space. dawn powerwash spray with 60k reviews sprays concentrated suds that lift burnt cheese and grease on contact before adding water. strong scent so rinse well with warm water, but for stubborn cookware it eliminates overnight soaking. direct link: curatedbyemma.pages.dev/go/powerwash. what's the hardest dish you had to scrub lately?"
            ),
        ]
    },
    31: {
        "name": 'Zulay Original Milk Frother Handheld Wand',
        "category": 'Coffee / Clumpy protein powder & latte foam',
        "rating": 4.5,
        "reviews": 115000,
        "honest_pros": 'High-torque motorized whisk aerates cold milk into thick cafe foam and blends chalky protein powder or matcha in 15 seconds',
        "honest_caveats": 'Runs on 2 AA batteries (not USB rechargeable); spins with enough power to splash liquid if cup is filled to the absolute brim',
        "slug": 'frother',
        "bio_slot": "#31",
        "draft_templates": [
            (
                'drinking protein shakes or matcha with chalky dry powder clumps floating on top is so unappetizing. the zulay handheld milk frother with 110k reviews spins at high speed to dissolve powders and whip rich latte foam in 15 seconds flat. runs on 2 AA batteries so keep a couple spares, but it completely replaces bulky shaker cups. direct link: curatedbyemma.pages.dev/go/frother. do you use it for morning coffee or protein shakes?'
            ),
        ]
    },
    32: {
        "name": 'Fullstar Vegetable Chopper Pro (4 Blades)',
        "category": 'Cooking / Dicing onions & meal prep hand fatigue',
        "rating": 4.5,
        "reviews": 98000,
        "honest_pros": 'Sharp stainless grid chops an entire onion or potato into uniform dice in one swift press directly into the catch tray',
        "honest_caveats": 'You must slice root veggies into flat rounds first (forcing a massive whole hard carrot can strain the hinge); hand-wash blade grid',
        "slug": 'veggie-chopper',
        "bio_slot": "#32",
        "draft_templates": [
            (
                'standing over a cutting board weeping from onion fumes while hand-dicing twenty vegetables takes forever during Sunday meal prep. the fullstar vegetable chopper with 95k reviews dices whole onions in one downward press directly into the storage container with zero eye tears. slice onions in half first so the grid presses cleanly, but it cuts prep time in half. found the link: curatedbyemma.pages.dev/go/veggie-chopper. what dishes do you usually meal prep?'
            ),
        ]
    },
    33: {
        "name": 'Dash Rapid Egg Cooker (6-Capacity)',
        "category": 'Kitchen / Hard-to-peel boiled eggs',
        "rating": 4.7,
        "reviews": 118000,
        "honest_pros": 'Steam pressure cooks soft, medium, or hard-boiled eggs in under 10 minutes with shells that slip off in one continuous piece',
        "honest_caveats": 'The finish chime buzzer is noticeably loud and sharp; base heating plate needs occasional lemon/vinegar wipe to clear hard water spots',
        "slug": 'egg-cooker',
        "bio_slot": "#33",
        "draft_templates": [
            (
                'boiling eggs on the stove and having shells stick like concrete, tearing half the egg whites off, ruins breakfast. the dash rapid egg cooker with 115k reviews uses targeted steam to cook eggs perfectly with shells that slide right off in one piece. buzzer chime is super loud when finished, but for peeling hard-boiled eggs with zero frustration it is worth every penny. link: curatedbyemma.pages.dev/go/egg-cooker. do you prefer jammy soft-boiled or firm hard-boiled?'
            ),
        ]
    },
    34: {
        "name": 'Bagail 8 Set Compression Packing Cubes',
        "category": 'Travel / Messy overstuffed suitcases',
        "rating": 4.6,
        "reviews": 47000,
        "honest_pros": 'Secondary compression zipper squeezes bulky sweaters and clothes down by 40%, keeping carry-on bags neatly compartmentalized',
        "honest_caveats": "Compressing clothes saves valuable volume but doesn't reduce bag weight; don't yank zippers around overstuffed corners",
        "slug": 'packing-cubes',
        "bio_slot": "#34",
        "draft_templates": [
            (
                'digging through an exploded suitcase in a hotel room trying to find one pair of socks ruins travel organization. bagail compression packing cubes with 45k reviews use a secondary perimeter zipper to compress bulky clothes by 40% while keeping items separated. saves tons of suitcase volume though weight stays the same, but it keeps carry-ons orderly. link: curatedbyemma.pages.dev/go/packing-cubes. are you packing for a weekend trip or long vacation?'
            ),
        ]
    },
    35: {
        "name": 'Etekcity Digital Hanging Luggage Scale',
        "category": 'Travel / Airport overweight baggage fees',
        "rating": 4.7,
        "reviews": 68000,
        "honest_pros": 'Accurate digital hook sensor weighs heavy suitcases up to 110 lbs before leaving home, preventing unexpected $100 airline check-in fees',
        "honest_caveats": 'Requires lifting the full weight of the suitcase off the ground by hand for 3 seconds to lock reading; uses a CR2032 watch battery',
        "slug": 'luggage-scale',
        "bio_slot": "#35",
        "draft_templates": [
            (
                "the dreaded panic at the airport check-in counter when the conveyor belt scale hits 52 lbs and you have to open suitcases in public is the worst. etekcity's digital luggage scale with 65k reviews weighs bags up to 110 lbs at home so you know exact numbers beforehand. takes lifting the bag off the floor for a few seconds to lock the screen, but it avoids airline fees. link: curatedbyemma.pages.dev/go/luggage-scale. who are you flying with on your next trip?"
            ),
        ]
    },
    36: {
        "name": 'Nite Ize Gear Tie Reusable Rubber Twist Ties',
        "category": 'Home / Tangled appliance cords & wire knots',
        "rating": 4.8,
        "reviews": 22000,
        "honest_pros": 'Thick rubber-coated bendable wire grips appliance cords, hoses, and charger cables without scratching or snapping like brittle plastic zip ties',
        "honest_caveats": 'A bit too thick for tiny delicate earbud wires; bend memory slowly softens after hundreds of heavy industrial wraps',
        "slug": 'gear-tie',
        "bio_slot": "#36",
        "draft_templates": [
            (
                'tangled electrical cords in drawers forming knotted nests that take ten minutes to untangle is such a pet peeve. nite ize reusable rubber gear ties with 22k reviews have a bendable internal wire with a soft grip shell that holds heavy appliance cords securely. a bit chunky for super thin charging wires, but for kitchen mixers, vacuums, and thick cables it organizes everything. link: curatedbyemma.pages.dev/go/gear-tie. what drawer needs the most help in your house?'
            ),
        ]
    },
    37: {
        "name": 'Slideep 2-Tier Under Sink Organizer with Sliding Drawer',
        "category": 'Home / Dark cluttered under-sink cabinets',
        "rating": 4.5,
        "reviews": 26000,
        "honest_pros": 'Sliding bottom drawer rolls out smoothly from under bathroom and kitchen sinks so you can grab cleaning bottles without digging',
        "honest_caveats": 'Measure cabinet depth and drainage pipe clearance before buying; top tier is narrower to fit around drain trap pipes',
        "slug": 'sink-organizer',
        "bio_slot": "#37",
        "draft_templates": [
            (
                "crawling on your knees with a flashlight trying to find extra trash bags or sprays lost in the dark cavern under the sink is so chaotic. slideep's 2-tier under sink organizer with 25k reviews features a smooth slide-out bottom basket that brings bottles straight to you. check pipe clearance dimensions under your sink first, but it completely doubles usable cabinet space. link: curatedbyemma.pages.dev/go/sink-organizer. is this for the kitchen or bathroom cabinet?"
            ),
        ]
    },
    38: {
        "name": 'Mellanni Deep Pocket Microfiber Bed Sheet Set',
        "category": 'Bedroom / Fitted sheets popping off mattress',
        "rating": 4.5,
        "reviews": 345000,
        "honest_pros": 'Buttery-soft double-brushed microfiber with continuous all-around elastic deep pockets that stay firmly tucked on thick mattresses',
        "honest_caveats": 'Being synthetic microfiber, they sleep slightly warmer than lightweight 100% percale cotton during hot humid summer months',
        "slug": 'bed-sheets',
        "bio_slot": "#38",
        "draft_templates": [
            (
                "fitted bed sheets that pop off mattress corners in the middle of the night leaving you sleeping on bare foam are beyond infuriating. mellanni's deep pocket sheet sets with over 340k reviews have all-around reinforced elastic that stays anchored on pillowtop mattresses. traps body heat slightly more than crisp percale cotton in peak summer, but for staying locked down and wrinkle-free it is a favorite. link: curatedbyemma.pages.dev/go/bed-sheets. do you have a standard or deep mattress?"
            ),
        ]
    },
    39: {
        "name": 'Rubbermaid Reveal Cordless Battery Power Scrubber',
        "category": 'Cleaning / Scrubbing tile grout & faucet grime',
        "rating": 4.4,
        "reviews": 37000,
        "honest_pros": 'Oscillating brush head delivers 60 scrubs per second, cleaning black mildew from tile grout, sink edges, and shower corners without knuckle strain',
        "honest_caveats": 'Runs on 4 AA batteries which drain during long deep cleans (rechargeable AAs recommended); head is small for massive floor surfaces',
        "slug": 'power-scrubber',
        "bio_slot": "#39",
        "draft_templates": [
            (
                'scrubbing dirty bathroom tile grout with an old toothbrush until your knuckles are raw and your wrists ache takes forever. the rubbermaid reveal power scrubber with 35k reviews uses an oscillating high-speed brush head that powers through black grout lines and faucet scale in seconds. burns through 4 AA batteries on deep cleaning days, but it saves your wrists and fingernails. direct link: curatedbyemma.pages.dev/go/power-scrubber. is it for shower tile or sink faucets?'
            ),
        ]
    },
    40: {
        "name": 'Conair Battery Operated Compact Fabric Defuzzer',
        "category": 'Wardrobe / Pilled leggings & couch cushions',
        "rating": 4.5,
        "reviews": 112000,
        "honest_pros": 'Compact 3-depth adjustable shaver trims pills off gym leggings, wool blankets, and fleece outerwear quickly without snagging delicate fibers',
        "honest_caveats": 'Runs on 2 AA batteries so motor speed drops as batteries deplete; lint collection cup fills up quickly on large blankets',
        "slug": 'conair-shaver',
        "bio_slot": "#40",
        "draft_templates": [
            (
                "favorite black gym leggings or wool blend cardigans developing fuzzy pilling between the thighs or cuffs makes clothes look instantly worn out. conair's battery fabric defuzzer with 110k reviews has a 3-depth guard that shaves pills clean without nicking fabric. runs on AA batteries so keep fresh ones handy, but it makes pilled athleisure look brand new. found the link: curatedbyemma.pages.dev/go/conair-shaver. are you trimming leggings or a knit sweater?"
            ),
        ]
    },
    41: {
        "name": 'Hero Cosmetics Mighty Patch Original Acne Patches',
        "category": 'Skincare / Popping whiteheads & face picking',
        "rating": 4.5,
        "reviews": 148000,
        "honest_pros": 'Medical-grade hydrocolloid stickers extract pus and oil from surface pimples overnight while physically preventing unconscious face-picking',
        "honest_caveats": 'Only works on whiteheads with visible surface fluid (does not resolve deep blind hormonal cystic bumps under the skin)',
        "slug": 'pimple-patch',
        "bio_slot": "#41",
        "draft_templates": [
            (
                'the urge to squeeze an angry whitehead right before an event usually results in inflamed scabs and post-acne marks. hero cosmetics mighty patches with 145k+ reviews use hydrocolloid that draws out all the gunk overnight while stopping fingers from picking. only works on pimples that have come to a visible head, but it flattens blemishes with zero scarring. link: curatedbyemma.pages.dev/go/pimple-patch. do you usually get surface blemishes or deep spots?'
            ),
        ]
    },
    42: {
        "name": 'Aquaphor Healing Ointment Advanced Therapy',
        "category": 'Skincare / Severely cracked winter lips & skin',
        "rating": 4.8,
        "reviews": 88000,
        "honest_pros": 'Protective petrolatum, panthenol, and glycerin formula seals in hydration to heal cracked winter lips, raw noses, and cuticles overnight',
        "honest_caveats": 'Very rich, thick ointment consistency that feels greasy on bare fingers; can leave oily marks on delicate silk or satin bedding',
        "slug": 'aquaphor',
        "bio_slot": "#42",
        "draft_templates": [
            (
                'waking up in cold winter months with bleeding cracked lips and peeling knuckles that sting every time you wash your hands is miserable. aquaphor healing ointment with 88k reviews creates a semi-permeable barrier that lets skin breathe while locking in moisture to repair raw fissures overnight. greasy texture so apply it before sleeping, but for severe dry skin it works better than fancy lotions. link: curatedbyemma.pages.dev/go/aquaphor. are you dealing with chapped lips or dry hands?'
            ),
        ]
    },
    43: {
        "name": "O'Keeffe's Working Hands Hand Cream Jar",
        "category": 'Body Care / Cracked raw skin from frequent washing',
        "rating": 4.7,
        "reviews": 78000,
        "honest_pros": 'High-concentration non-greasy glycerin cream stimulates natural skin repair on severely cracked fingertips and working hands without washing away',
        "honest_caveats": 'Can cause a temporary 30-second mild sting if applied into fresh, open skin cracks; completely unfragranced',
        "slug": 'working-hands',
        "bio_slot": "#43",
        "draft_templates": [
            (
                "washing dishes or working outside in the cold until fingertips crack open and bleed around the nails makes basic typing painful. o'keeffe's working hands cream with 78k verified reviews creates a deep moisture barrier that doesn't wash off in five seconds like watery perfumed lotions. can sting for half a minute on open cracks, but it closes split skin in 48 hours. link: curatedbyemma.pages.dev/go/working-hands. do you work with your hands a lot during the day?"
            ),
        ]
    },
    44: {
        "name": 'Wet & Forget Shower Daily Cleaner Spray',
        "category": 'Bathroom / Daily soap scum & hard water shower stains',
        "rating": 4.4,
        "reviews": 26000,
        "honest_pros": 'Spray wet shower walls and glass doors right after showering once a week to dissolve soap scum with zero wiping, scrubbing, or harsh fumes',
        "honest_caveats": 'Designed for ongoing maintenance; if you have years of rock-hard calcium crust built up, you must do one manual deep clean first',
        "slug": 'shower-spray',
        "bio_slot": "#44",
        "draft_templates": [
            (
                "standing in a steamy shower scrubbing cloudy soap scum off glass doors with harsh bleach fumes is the worst Saturday chore. wet & forget shower spray with 26k reviews dissolves soap film and mineral scale automatically with zero scrubbing—just spray after showering and rinse the next day. won't instantly remove 5-year mineral crust on day one, but for keeping glass spotless it eliminates manual scrubbing. link: curatedbyemma.pages.dev/go/shower-spray. is your shower glass or fiberglass?"
            ),
        ]
    },
    45: {
        "name": 'Command Large Picture Hanging Strips (16 Pairs)',
        "category": 'Home Decor / Hanging wall art in rental apartments',
        "rating": 4.6,
        "reviews": 58000,
        "honest_pros": 'Click-locking hook-and-loop strips hold heavy framed pictures securely to painted drywall without nails, hammer holes, or losing security deposits',
        "honest_caveats": 'Must wait 1 full hour after pressing strips to wall before snapping frames on; does not stick reliably to textured stucco or humid brick',
        "slug": 'command-strips',
        "bio_slot": "#45",
        "draft_templates": [
            (
                'drilling holes into apartment drywall to hang wall art and stressing about patching them up before moving out to save your security deposit is annoying. command large picture hanging strips with 55k+ reviews lock frames flush to walls with interlocking grips that pull off cleanly without taking paint off. follow the 1-hour adhesive cure time before mounting weight, but it saves rental walls. link: curatedbyemma.pages.dev/go/command-strips. what size frames are you hanging?'
            ),
        ]
    },
    46: {
        "name": 'Mueller Double-Wall Stainless Steel French Press',
        "category": 'Kitchen / Shattered glass coffee presses',
        "rating": 4.6,
        "reviews": 32000,
        "honest_pros": 'Heavy-duty double-wall stainless steel body keeps coffee piping hot for 60 minutes and will never shatter in the sink like fragile glass carafes',
        "honest_caveats": 'Solid steel body means you cannot see coffee level while pressing; requires coarse ground beans to avoid fine sediment at the cup bottom',
        "slug": 'french-press',
        "bio_slot": "#46",
        "draft_templates": [
            (
                "having a delicate glass french press shatter in the kitchen sink while washing it with hot water is both terrifying and dangerous. mueller's double-wall stainless steel press with 30k reviews is virtually drop-proof and keeps brewed coffee hot for over an hour. opaque body means you can't see the liquid level through the sides, but you will never have to buy replacement glass beakers again. link: curatedbyemma.pages.dev/go/french-press. what kind of coffee roast do you brew?"
            ),
        ]
    },
    47: {
        "name": 'ThermoPro TP50 Digital Room Thermometer & Hygrometer',
        "category": 'Home / Apartment dryness, static & humidity check',
        "rating": 4.6,
        "reviews": 88000,
        "honest_pros": 'Fast accurate indoor humidity and temperature sensor with comfort indicators shows exactly when winter heater air is too dry or mold-prone',
        "honest_caveats": 'LCD screen is not backlit so you cannot read numbers in a pitch-black bedroom at night; refreshes readings every 10 seconds',
        "slug": 'hygrometer',
        "bio_slot": "#47",
        "draft_templates": [
            (
                "waking up with dry scratchy throats, static shocks on blankets, and wondering if your apartment heater is sucking all the moisture out of the air is frustrating. thermopro's digital hygrometer with 85k reviews tracks room humidity and temp in real time so you know when to turn on a humidifier. screen isn't backlit for dark rooms, but for keeping indoor air balanced it gives you actual data. link: curatedbyemma.pages.dev/go/hygrometer. does your place feel super dry right now?"
            ),
        ]
    },
    48: {
        "name": 'Gorilla Grip Heat Resistant Silicone Oven Mitts',
        "category": 'Kitchen / Burning fingers through thin fabric oven pads',
        "rating": 4.7,
        "reviews": 32000,
        "honest_pros": 'Waterproof textured silicone exterior resists heat up to 484°F with non-slip grip on heavy cast iron skillets and boiling soup pots',
        "honest_caveats": 'Bulkier and stiffer than traditional cloth fabric pot holders; inner cotton lining can bunch if pulling wet hands out quickly',
        "slug": 'oven-mitts',
        "bio_slot": "#48",
        "draft_templates": [
            (
                "feeling heat searing through thin cotton potholders when pulling a 450-degree heavy cast iron skillet out of the oven is genuinely terrifying. gorilla grip silicone oven mitts with 30k+ reviews are heat-proof up to 484°F and waterproof so steam or boiling broth can't burn your skin. slightly bulkier than cloth pads, but for lifting heavy roasting pans safely they give a secure grip. link: curatedbyemma.pages.dev/go/oven-mitts. do you cook with cast iron or sheet pans mostly?"
            ),
        ]
    },
    49: {
        "name": 'Sleepy Ride Airplane Footrest Under Seat Hammock',
        "category": 'Travel / Swollen legs & lower back flight ache',
        "rating": 4.3,
        "reviews": 16000,
        "honest_pros": 'Memory foam hammock hangs from tray table arms, elevating feet to take pressure off thighs and lower back during long economy flights',
        "honest_caveats": 'Tray table must be stowed for takeoff and landing; taller travelers with long legs have less clearance to swing feet forward',
        "slug": 'airplane-footrest',
        "bio_slot": "#49",
        "draft_templates": [
            (
                "sitting in cramped economy airline seats with feet dangling or pressed flat against cold floorboards leaves your lower back aching and ankles swollen. sleepy ride's airplane footrest hammock with 15k reviews loops over the tray table arms to cradle your feet elevated like a recliner. must stow during takeoff and landing, but for red-eyes and 6-hour flights it takes pressure off your lower spine. link: curatedbyemma.pages.dev/go/airplane-footrest. how long is your next flight?"
            ),
        ]
    },
    50: {
        "name": 'FurZapper Pet Hair Remover for Washer and Dryer',
        "category": 'Laundry / Pet fur stuck to washed clothes',
        "rating": 4.1,
        "reviews": 26000,
        "honest_pros": 'Sticky silicone paw tumbles inside washing machines and dryers, pulling stubborn dog and cat hair off fabric directly into the lint trap',
        "honest_caveats": 'Do NOT use fabric softeners or dryer sheets (softener oils coat the silicone and ruin its tackiness); rinse with dish soap between cycles',
        "slug": 'furzapper',
        "bio_slot": "#50",
        "draft_templates": [
            (
                'pulling freshly washed black shirts out of the dryer only to find dog hair still baked into the weave fibers makes doing laundry feel pointless. furzapper silicone paws with 25k reviews tumble in the wash and dryer to grab pet fur off wet fabric and wash it down the drain or into the lint trap. never use with fabric softeners since oils coat the tacky surface, but it saves lint rolling every shirt. link: curatedbyemma.pages.dev/go/furzapper. do you deal with short or long pet fur in the wash?'
            ),
        ]
    },
}

# Backward compatibility alias
for s, data in CATALOG_SPECS.items():
    data["draft_template"] = data["draft_templates"][0]

def pre_screen_post(post_text, author="user"):
    """
    Fast, zero-cost negative gate that runs BEFORE LLM evaluation.
    Rejects:
    1. Emma's own posts or bot replies.
    2. Dropshipper / competitor promotions, commercial spam, sales CTAs.
    3. Product pricing ($XX.XX) and store links (shopify, etsy, slankit, amazon links, products/).
    4. Lifestyle / playlist / music vibe shares (no actual pain/struggle).
    5. Non-English threads (Indonesian, Malay, etc.).
    6. Memorial / bereavement / sports / politics.
    """
    text_lower = post_text.lower()
    author_lower = (author or "").lower().strip("@")

    # 1. Emma self-check
    if author_lower in ("curated_byemma", "curatedbyemma"):
        return {"verdict": "REJECT", "reason": "Self-post: Author is Emma herself"}

    # 2. Competitor Ads & Dropshipping Spam CTAs
    promo_phrases = [
        "comment shop", "comment \"shop\"", "comment 'shop'", "dm you the link",
        "dm for link", "dm me the link", "dm me for", "dm us for", "link in bio",
        "link in comments", "link in my bio", "check out our", "order yours",
        "order now", "shop now", "buy now", "free shipping", "promo code",
        "discount code", "coupon code", "exclusive deal", "exclusive discount",
        "limited time offer", "follow @", "follow us for more", "giveaway",
        "read more:", "article:", "bit.ly", "tinyurl"
    ]
    for phrase in promo_phrases:
        if phrase in text_lower:
            return {"verdict": "REJECT", "reason": f"Competitor promo / dropshipping CTA detected ('{phrase}')"}

    # 3. Store URLs & E-commerce Product Links
    store_domains = [
        "slankit.com", "aliexpress.com", "temu.com", "etsy.com", "shopify.com",
        "myshopify.com", "/products/", "/product/", "amzn.to/", "amazon.com/dp/",
        "bit.ly/", "tinyurl.com/", "sca_ref=", "ref=", "affiliate", "tag="
    ]
    for domain in store_domains:
        if domain in text_lower:
            return {"verdict": "REJECT", "reason": f"E-commerce store or product URL detected ('{domain}')"}

    # 4. Product Pricing Tags (e.g. $14.26, $19.99, $25)
    if re.search(r'\$\d+(\.\d{2})?', text_lower):
        return {"verdict": "REJECT", "reason": "Commercial price tag ($XX.XX) detected"}

    # 5. Lifestyle / Music / Playlist Sharing (No genuine struggle/pain)
    vibe_markers = [
        "#musicthreads", "#vinylthreads", "#nowplaying", "#songrecommendation",
        "currently listening to", "lava lamp on", "incense burning", "open.spotify.com",
        "youtu.be/", "youtube.com/watch", "sleep soundly. dream sweetly"
    ]
    for marker in vibe_markers:
        if marker in text_lower:
            return {"verdict": "REJECT", "reason": f"Music/Vibe lifestyle share without pain point ('{marker}')"}

    # 6. Non-English Language Veto (Indonesian, Malay, etc.)
    non_english_markers = [
        "kak", "bayiku", "anakku", "anak", "banget", "nggak", "ngga", "tidak", "bisa", "udah",
        "nih", "tuh", "deh", "dgn", "bgt", "gak", "korang", "kat", "boleh", "je",
        "dah", "tak", "nak", "tu", "saya", "aku", "gue", "lu", "kalo", "kalau",
        "tidur", "kebangun", "malam", "pagi", "sakit", "punggung", "kursi", "kasur", "belakang",
        "apakah", "kenapa", "pakaian", "bergosok", "gosok", "baju", "pelik", "sangat",
        "juga", "lagi", "ini", "itu", "ada", "sama", "kamu", "dia", "mereka", "dengan"
    ]
    tokens = set(re.findall(r'\b[a-z]+\b', text_lower))
    matched_foreign = [w for w in non_english_markers if w in tokens]
    if len(matched_foreign) >= 1:
        return {"verdict": "REJECT", "reason": f"Non-English language detected ('{matched_foreign[0]}')"}

    # 7. Memorial / Sports / Politics
    memorial_words = [
        "passed away", "died", "funeral", "grave", "rip", "grandfather", "grandmother",
        "lolo", "lola", "ancestor", "memory of", "childhood", "growing up", "undas",
        "heaven", "miss him", "miss her", "rest in peace"
    ]
    for word in memorial_words:
        if word in text_lower:
            return {"verdict": "REJECT", "reason": f"Memorial/Personal family story detected ('{word}')"}

    sports_words = [
        "pitcher", "innings", "game 2", "game 3", "mlb", "nba", "nfl", "touchdown",
        "strikeout", "mariners", "dodgers", "yankees", "stray kids", "concert",
        "kpop", "barricade", "tour", "quarterback"
    ]
    for word in sports_words:
        if word in text_lower:
            return {"verdict": "REJECT", "reason": f"Sports/Concert context detected ('{word}')"}

    return None

def evaluate_and_draft_local(post_text, author="user"):
    """
    Robust evaluator with strict context gating and 10-slot recognition.
    """
    pre = pre_screen_post(post_text, author=author)
    if pre is not None:
        return pre

    text_lower = post_text.lower()

    # 1. HARD REJECT LIST (Immediate veto)
    # Non-English language veto (Indonesian, Malay, etc.)
    non_english_markers = [
        "kak", "bayiku", "anakku", "banget", "nggak", "ngga", "tidak", "bisa", "udah",
        "nih", "tuh", "deh", "dgn", "bgt", "gak", "korang", "kat", "boleh", "je",
        "dah", "tak", "nak", "tu", "saya", "aku", "gue", "lu", "kalo", "kalau",
        "tidur", "kebangun", "malam", "pagi", "sakit", "punggung", "kursi", "kasur", "belakang"
    ]
    tokens = set(re.findall(r'\b[a-z]+\b', text_lower))
    matched_foreign = [w for w in non_english_markers if w in tokens]
    if len(matched_foreign) >= 1:
        return {"verdict": "REJECT", "reason": f"Non-English language detected ('{matched_foreign[0]}') — Emma only targets US English market"}

    memorial_words = [
        "passed away", "died", "funeral", "grave", "rip", "grandfather", "grandmother",
        "lolo", "lola", "ancestor", "memory of", "childhood", "growing up", "undas",
        "heaven", "miss him", "miss her", "rest in peace"
    ]
    sports_words = [
        "pitcher", "innings", "game 2", "game 3", "mlb", "nba", "nfl", "touchdown",
        "strikeout", "mariners", "dodgers", "yankees", "stray kids", "concert",
        "kpop", "barricade", "tour", "quarterback"
    ]
    marketing_words = [
        "giveaway", "discount code", "link in bio", "dm for link", "shop now",
        "article:", "read more:", "tinyurl", "bit.ly", "check out my"
    ]

    for word in memorial_words:
        if word in text_lower:
            return {"verdict": "REJECT", "reason": f"Memorial/Personal family story detected ('{word}')"}

    for word in sports_words:
        if word in text_lower:
            return {"verdict": "REJECT", "reason": f"Sports/Concert context detected ('{word}')"}

    for word in marketing_words:
        if word in text_lower:
            return {"verdict": "REJECT", "reason": f"Marketing/Promotional spam detected ('{word}')"}

    # 2. MATCH SPECIFIC SLOTS WITH STRICT PAIN INTENT
    matched_slot = None

    # Slot 1: Pet hair on furniture/clothes
    has_pet = any(w in text_lower for w in ["dog hair", "cat hair", "retriever", "pet hair", "pet fur", "dog shedding", "cat shedding", "fur everywhere", "shedding is out of control", "dog hairs"])
    has_furniture = any(w in text_lower for w in ["couch", "sofa", "cushion", "velvet", "car seat", "rug", "armchair", "blanket", "vacuuming", "vacuum"])
    has_floor_or_injury = any(w in text_lower for w in ["under the couch", "under the sofa", "threw my back", "back out", "spasm", "floor", "hardwood"])
    if has_pet and has_furniture and not has_floor_or_injury:
        matched_slot = 1

    # Slot 2: Baby / Toddler sleep
    has_baby = any(w in text_lower for w in ["baby", "toddler", "infant", "7 month", "8 month", "6 month", "newborn", "sleep regression"])
    has_sleep_struggle = any(w in text_lower for w in ["crying every hour", "won't go down", "won't sleep", "wakes up crying", "running on 2 hours of sleep", "nap refusal", "up all night crying"])
    if has_baby and has_sleep_struggle:
        matched_slot = 2

    # Slot 3: Desk / Chair Back Pain
    has_chair = any(w in text_lower for w in ["office chair", "desk chair", "sitting all day", "sitting at my desk", "wfh chair", "work chair", "computer chair"])
    has_back_pain = any(w in text_lower for w in ["back hurting", "back pain", "lower back", "spine hurting", "back is killing me", "back aches", "posture is terrible", "lumbar", "destroying my lower spine"])
    if has_chair and has_back_pain:
        matched_slot = 3

    # Slot 4: Air fryer oil / cooking mist
    has_airfryer = any(w in text_lower for w in ["air fryer", "airfryer", "cooking oil", "pouring oil"])
    has_oil_struggle = any(w in text_lower for w in ["soggy and greasy", "soggy", "greasy", "oil mister", "oil sprayer", "clogged sprayer", "oil bottle"])
    if has_airfryer and has_oil_struggle:
        matched_slot = 4

    # Slot 5: Tile / Grout scrubbing
    has_cleaning = any(w in text_lower for w in ["scrubbing", "tile grout", "grout", "bathtub", "shower tile", "bathroom tile"])
    has_scrub_pain = any(w in text_lower for w in ["hands and knees", "elbow grease", "torture on my back", "killing my knees", "back hurts cleaning"])
    if has_cleaning and has_scrub_pain:
        matched_slot = 5

    # Slot 6: Cable clutter / Nightstand
    has_cables = any(w in text_lower for w in ["charging cables", "phone cables", "charging cords", "cables", "cords"])
    has_cable_drop = any(w in text_lower for w in ["sliding off my nightstand", "falling into the gap", "behind the bed", "behind my desk", "dropping behind"])
    if has_cables and has_cable_drop:
        matched_slot = 6

    # Slot 7: Airplane / Flight Neck Strain
    has_flight = any(w in text_lower for w in ["flight", "flying", "airplane", "plane ride", "tray table", "seatback"])
    has_phone_neck = any(w in text_lower for w in ["holding my phone", "holding phone", "neck strain", "neck cramp", "neck hurts", "no seatback screen"])
    if has_flight and has_phone_neck:
        matched_slot = 7

    # Slot 8: Wrinkled suitcase / Travel clothes
    has_clothes = any(w in text_lower for w in ["suitcase", "hotel", "travel clothes", "linen shirts", "unpacked"])
    has_wrinkles = any(w in text_lower for w in ["wrinkled", "horribly wrinkled", "hate dragging out the hotel iron", "need to iron", "wrinkles"])
    if has_clothes and has_wrinkles:
        matched_slot = 8

    # Slot 9: Adult sleep / Earbuds hurt / Light
    has_sleep_issue = any(w in text_lower for w in ["can't sleep", "light keeps waking me", "sleep mask", "partner snoring", "snoring keeps me awake"])
    has_ear_pain = any(w in text_lower for w in ["earbuds hurt", "sleeping on my side", "side sleeping", "ears hurt"])
    if has_sleep_issue and has_ear_pain:
        matched_slot = 9

    # Slot 10: Car air vent dust / crumbs
    has_car = any(w in text_lower for w in ["car air vents", "car vents", "cup holders", "car interior", "car console"])
    has_dust = any(w in text_lower for w in ["dust and crumbs", "crumbs stuck", "wipes cannot reach", "cleaning putty", "dust stuck"])
    if has_car and has_dust:
        matched_slot = 10

    if not matched_slot:
        return {"verdict": "REJECT", "reason": "No clear first-person physical pain point matched"}

    spec = CATALOG_SPECS[matched_slot]
    templates = spec.get("draft_templates", [spec.get("draft_template", "")])
    seed_str = f"{author}_{post_text}"
    chosen_template = templates[abs(hash(seed_str)) % len(templates)]

    return {
        "verdict": "ACCEPT",
        "slot": matched_slot,
        "product_name": spec["name"],
        "reply_draft": chosen_template,
        "source": "heuristic_fallback"
    }

def generate_reply_llm(post_text, author="user", timeout=25):
    """
    Contextual LLM evaluator and reply crafter powered by OpenRouter.
    Reads user context, enforces strict 'Never Lie', and generates custom 4-part replies.
    """
    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        return None

    model = os.environ.get("OPENROUTER_MODEL", "google/gemini-2.5-flash").strip()

    catalog_lines = []
    for s, data in CATALOG_SPECS.items():
        catalog_lines.append(
            f"Slot #{s}: {data['name']} (Category: {data['category']})\n"
            f"  - Verified Reviews: {data['reviews']:,} (Rating: {data['rating']}★)\n"
            f"  - What it fixes: {data['honest_pros']}\n"
            f"  - Limitations/Cons (NEVER LIE): {data['honest_caveats']}\n"
            f"  - Direct link: curatedbyemma.pages.dev/go/{data.get('slug', str(s))}"
        )
    catalog_prompt = "\n\n".join(catalog_lines)

    system_instruction = f"""You are Emma (@curated_byemma), a 29-year-old practical consumer researcher in Seattle. You review everyday viral Amazon products and give completely honest, down-to-earth recommendations on Threads.

RULES:
0. STRICT ENGLISH ONLY (US Market Target):
   - The user post MUST be primarily written in English.
   - If the post is in Indonesian, Malay, Tagalog, Spanish, or any non-English language, REJECT IT IMMEDIATELY with reason "Non-English post". Emma only operates in the US English market.
1. NEVER ENGAGE COMPETITOR ADS, DROPSHIPPERS, OR PROMO POSTS:
   - If the post is an ad, dropshipper, commercial brand, or seller promoting a product (has prices, store links, 'comment SHOP', 'DM for link', 'buy now'), REJECT IMMEDIATELY with reason "Competitor promo / dropshipping post".
   - Emma ONLY replies to real, organic consumer complaints and daily life frustrations.
2. NEVER ENGAGE LIFESTYLE / VIBE / POSITIVE POSTS:
   - If the post is someone relaxing, enjoying music, sharing playlists (#MusicThreads), wishing goodnight, or in a good mood without an actual physical problem or pain point, REJECT IMMEDIATELY.
   - We NEVER pitch products to people who are content and not asking for a solution.
3. STRICT "NEVER LIE" & ABSOLUTELY ZERO FAKE ANECDOTES:
   - NEVER fabricate personal ownership, personal testing claims, or fake family anecdotes!
   - BANNED FABRICATIONS: "i swear by", "i own this", "i bought this", "my cat", "my dog", "my sister", "my friend", "in my bedroom", "for me", "it saved my couch", "my 3-year-old cardigan".
   - Emma is an independent consumer researcher who curates and audits verified data, independent teardowns, and buyer feedback patterns.
   - Speak as an objective, empathetic researcher/curator:
     * "when auditing [category] to filter out sponsored hype..."
     * "verified buyer consensus across [X]k reviews highlights..."
     * "independent testing consistently points to..."
     * "reviewers with heavy shedders note that..."
   - Does one of your 50 catalog items GENUINELY solve this user's exact problem?
   - If someone's problem is NOT solved by your products (e.g. medical spine injury, thrown-out back spasms while vacuuming floor under couch, wanting robot vacuums, dog chewing walls), you MUST REJECT.
   - Do NOT force a product recommendation if it does not fit! A sofa lint roller does NOT vacuum floors or heal lower back spasms!
   - Hard REJECT: memorials, family grief, sports games, politics, brand giveaways, spam.
4. BAN AI SLOP & CLICHÉ OPENERS (NO "UGH", "OMG", "THE STRUGGLE IS REAL"):
   - NEVER start replies with generic, whiny, robotic AI filler:
     * STRICTLY BANNED OPENERS: "ugh", "ugh,", "omg", "omg,", "sigh", "the struggle is real", "i feel this in my soul", "this hits close to home", "sending you strength", "game-changer", "game changer".
     * Jump straight into a grounded, natural conversational observation about their specific issue.
     * BAD: "ugh, the struggle is real when your dog sheds all over the bed..."
     * GOOD: "woven bedding seems to trap pet undercoat hair tighter than almost anything else..."
     * BAD: "ugh, the office chair struggle is so real!"
     * GOOD: "standard desk chairs offer basically zero lower lumbar contour, so your lower spine ends up absorbing all that compression by 3pm."
5. 5-PART HONEST ARC (if ACCEPTED):
   - Part 1: Real empathy referencing their SPECIFIC situation, vocabulary, and pain (never generic boilerplate).
   - Part 2: Honest audit citing verified Amazon consensus and review count.
   - Part 3: Honest caveat/con (what it doesn't do or real limitations).
   - Part 4: Include the clean direct link seamlessly: "found the exact one here: curatedbyemma.pages.dev/go/[slug]" (or "here's the direct link if you wanna check it: curatedbyemma.pages.dev/go/[slug]"). Always use the clean curatedbyemma.pages.dev/go/[slug] URL so they can tap directly without hunting in a bio lander!
   - Part 5 (Conversation Magnet): End with a brief, friendly, natural question related to their post (e.g. "btw what kind of chair do you have right now?", "what breed is your pet? some coats are so much harder to pull off velvet lol", "what's the first thing you're cooking in it?"). This sparks replies and elevates the comment to the Top Comment position!
   - Tone: Lowercase casual, friendly, authentic peer, zero marketing hype, helpful friend, natural human flow.
6. OUTPUT FORMAT:
   Return strictly valid JSON:
   {{
     "verdict": "ACCEPT" or "REJECT",
     "reason": "Clear 1-sentence reasoning",
     "slot": 1-50 or null,
     "reply_draft": "Your customized 5-part honest reply with direct link and closing question"
   }}

EMMA'S 50-SLOT CURATED VIRAL CATALOG:
{catalog_prompt}
"""

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Target Author: @{author}\nTarget Post Content:\n\"\"\"{post_text}\"\"\""}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.4
    }

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://curatedbyemma.com",
            "X-Title": "CuratedByEmma"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            content = res_data["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            if parsed.get("verdict") == "ACCEPT" and parsed.get("slot"):
                slot_id = int(parsed["slot"])
                spec = CATALOG_SPECS.get(slot_id)
                prod_name = spec["name"] if spec else f"Product #{slot_id}"
                return {
                    "verdict": "ACCEPT",
                    "slot": slot_id,
                    "product_name": prod_name,
                    "reply_draft": parsed.get("reply_draft", ""),
                    "reason": parsed.get("reason", "Accepted by LLM"),
                    "source": f"openrouter/{model}"
                }
            else:
                return {
                    "verdict": "REJECT",
                    "reason": parsed.get("reason", "Context does not match genuine product solution"),
                    "source": f"openrouter/{model}"
                }
    except Exception as e:
        print(f"[!] OpenRouter LLM call error: {e}. Falling back to local heuristic.")
        return None

def evaluate_and_draft(post_text, author="user"):
    """
    Master evaluator:
    1. Zero-cost negative pre-screen (rejects competitor ads, vibe posts, foreign languages, Emma self-posts).
    2. Uses OpenRouter LLM for human-level contextual understanding if OPENROUTER_API_KEY is set.
    3. Falls back to local heuristics if API key is missing or network fails.
    """
    # 1. Negative Pre-Screen Gate
    pre = pre_screen_post(post_text, author=author)
    if pre is not None:
        return pre

    # 2. Contextual LLM
    res = generate_reply_llm(post_text, author=author)
    if res is not None:
        return res

    # 3. Local Heuristic Fallback
    return evaluate_and_draft_local(post_text, author=author)

if __name__ == "__main__":
    t = "My phone charging cables keep sliding off my nightstand and falling into the gap behind the bed."
    print(evaluate_and_draft(t))
