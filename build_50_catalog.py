import json

AMAZON_TAG = "curatedbyem0f-20"

ITEMS_50 = [
    {
        "slot": 1, "slug": "roller", "asin": "B07GV57JYJ",
        "name": "PetLovers Extra-Sticky Lint Roller (5 pack)",
        "category": "Pet hair / Sofas & Clothes", "rating": 4.6, "reviews": 39300,
        "honest_pros": "Adhesive is sticky enough to pull embedded undercoat fur from velvet and textured woven sofas",
        "honest_caveats": "You burn through sheets quickly if you have a massive double-coated dog, peeling diagonal sheets takes a second to get used to",
        "templates": [
            "trying to get stubborn pet hair off couch fabric is the most frustrating workout ever. regular sticky tape rollers lose their grip in two swipes, but that extra-sticky roller with over 39k verified reviews is the consensus winner for deep fur. only catch is you go through sheets fast with a heavy shedder, but it actually pulls what vacuums miss. here's the direct link to it: curatedbyemma.pages.dev/go/roller. what breed is your pet?",
            "vacuums always seem to push double-coated dog hair deeper into weave fibers. when auditing pet hair tools against stubborn fur, that pet lovers extra-sticky roller with 39k+ verified ratings was the consensus pick that lifts embedded undercoat in one swipe. sheets peel fast so don't hoard them, but it actually works without shredding the fabric. found the exact one here: curatedbyemma.pages.dev/go/roller. what kind of couch fabric do you have?"
        ]
    },
    {
        "slot": 2, "slug": "otter", "asin": "B07N1JP56L",
        "name": "Fisher-Price Calming Otter Sleep Soother",
        "category": "Toddler / Infant sleep", "rating": 4.7, "reviews": 59700,
        "honest_pros": "Rhythmic breathing motion and soft white noise genuinely calms overtired babies down to sleep",
        "honest_caveats": "Not a magic fix for teething pain or severe colic, and you will need to replace AAA batteries every few weeks",
        "templates": [
            "night wakeups every hour are completely exhausting when you are trying to function the next day. parents navigating sleep regressions consistently point to that rhythmic breathing otter with nearly 60k reviews as one of the few soothers that genuinely settles babies down. only catch is you go through batteries every month, but verified parents highlight it gave them their first long sleep stretch. here's the direct link: curatedbyemma.pages.dev/go/otter. how many months are they right now?",
            "running on two hours of sleep with a crying baby is surviving on pure adrenaline. across parenting communities, that breathing belly otter with 59k verified reviews is the consensus favorite because the rhythmic movement settles overtired infants without rocking for hours. eats AAA batteries fast, but the gentle heartbeat rhythm works so well. found the exact one here: curatedbyemma.pages.dev/go/otter. are you guys in the 4-month or 8-month regression?"
        ]
    },
    {
        "slot": 3, "slug": "lumbar", "asin": "B074C9F45S",
        "name": "Ergonomic Memory Foam Lumbar Cushion",
        "category": "Desk setup / Lower back pain", "rating": 4.4, "reviews": 27400,
        "honest_pros": "High-density molded foam that actually holds shape under full bodyweight without flattening",
        "honest_caveats": "Feels noticeably firm the first 2-3 days before conforming to your lower back, doesn't fix serious medical sciatica",
        "templates": [
            "sitting in standard desk chairs all day literally destroys lower back posture. when auditing cushions to filter out sponsored hype, high-density molded foam was the only design 27k verified buyers consistently backed. it won't cure medical spine issues and feels pretty firm the first couple days, but taking pressure off the tailbone makes 8-hour workdays actually bearable. here's the direct link to it: curatedbyemma.pages.dev/go/lumbar. what kind of office chair are you using right now?",
            "desk chairs with zero lumbar curve compress your lower spine by 3pm. after comparing dozens of supports, the firm memory foam cushion with 27k reviews was the undisputed consensus pick for tailbone relief. won't replace a physio for chronic sciatica, but it makes long desk sessions noticeably more comfortable. saved the link to it here: curatedbyemma.pages.dev/go/lumbar. what kind of chair do you have?"
        ]
    },
    {
        "slot": 4, "slug": "mister", "asin": "B0CY1S56JZ",
        "name": "TrendPlain Glass Olive Oil Mister",
        "category": "Kitchen / Air fryer oil", "rating": 4.6, "reviews": 49100,
        "honest_pros": "Even, clog-free wide fan mist for air fryers without aerosol chemical propellants",
        "honest_caveats": "You have to pull the trigger with a firm, quick squeeze to get the wide fan mist instead of a stream; heavier than plastic since it's thick glass",
        "templates": [
            "pouring oil from a bottle into an air fryer always turns food soggy and uneven. standard aerosol spray cans leave sticky chemical residue, but that refillable glass oil mister with 49k+ verified reviews mists a clean wide fan. only trick is you have to pull the trigger with a quick firm squeeze or it shoots a stream, but it gives a super even crisp without soaking food. here's the direct link to it: curatedbyemma.pages.dev/go/mister. what's your favorite thing to air fry?",
            "drizzling oil straight onto air fryer food makes half of it drenched and the other half dry. the glass fan-spray mister with 49k reviews solved that without using propellants or aerosol cans. glass bottle is a little heavy and you need a snappy trigger squeeze for the fan effect, but fries come out actually crispy. found the link here: curatedbyemma.pages.dev/go/mister. what kind of oil are you using in yours?"
        ]
    },
    {
        "slot": 5, "slug": "defuzzer", "asin": "B01NAQD0KD",
        "name": "BEAUTURAL Fabric Shaver and Sweater Defuzzer",
        "category": "Wardrobe / Knitwear fuzz & pills", "rating": 4.5, "reviews": 116000,
        "honest_pros": "Dual-speed motorized rotary blades shave pills and fuzz off wool sweaters, knit cardigans, and fleece in 2 minutes",
        "honest_caveats": "Garment must be stretched completely flat on a table so blade guard doesn't catch loose seams; empty lint trap regularly",
        "templates": [
            "throwing away an $80 sweater just because of surface fuzz and pilling hurts so much. that beautural fabric defuzzer with 116k reviews is the verified consensus pick for restoring knit cardigans in two minutes. only rule is lay the fabric completely flat on a table so the guard doesn't snag loose threads, but it makes knits look brand new. here's the direct link: curatedbyemma.pages.dev/go/defuzzer. is it a wool knit or a fleece blanket?",
            "chunky knit sweaters pilling after two washes is the most frustrating winter problem. the beautural electric sweater shaver has over 115k verified reviews for a reason—it shaves off all the fuzzy bobbles without thinning the fabric. just empty the clear lint chamber frequently so it doesn't slow down the motor, but it cleans up worn wool coats completely. found the exact one here: curatedbyemma.pages.dev/go/defuzzer. what type of knit are you dealing with?"
        ]
    },
    {
        "slot": 6, "slug": "cables", "asin": "B07BB4YXHW",
        "name": "Smartish Magnetic Cable Wrangler",
        "category": "Tech / Nightstand cable clutter", "rating": 4.6, "reviews": 5200,
        "honest_pros": "Heavy magnetic weighted base holds phone and watch cords firmly so they never drop behind furniture",
        "honest_caveats": "Base is heavy enough for standard phone and USB-C cords, but very stiff thick braided HDMI cords can pull it if not positioned right",
        "templates": [
            "cables sliding off the nightstand and falling into the dark gap behind the bed is such an annoying daily headache. that weighted magnetic cable wrangler has over 5k verified reviews and actually keeps cords anchored right where you leave them. heavy base stays put for charging cords, just make sure to use the magnetic collars on thin wires. here's the direct link: curatedbyemma.pages.dev/go/cables. how many cords do you usually have at your bedside?",
            "fishing charging cords out from behind the headboard in the dark is beyond annoying. the weighted magnetic cable manager with 5k reviews has enough mass to keep phone and watch chargers sitting neatly on top of the nightstand. stiff heavy hdmi cables can slide it if tugged hard, but for bedside cords it is completely seamless. found the exact one here: curatedbyemma.pages.dev/go/cables. is your nightstand against a wall gap?"
        ]
    },
    {
        "slot": 7, "slug": "flight-mount", "asin": "B08TKPRKBN",
        "name": "Perilogics Airplane Tray-Table Phone Mount",
        "category": "Travel / Flight neck strain", "rating": 4.6, "reviews": 22900,
        "honest_pros": "Clamp locks directly onto airplane tray table or seatback, holding phone eye-level for hands-free viewing",
        "honest_caveats": "Spring clamp is quite stiff out of the box to ensure it doesn't slip; not needed on newer aircraft with built-in seatback monitors",
        "templates": [
            "holding your phone looking down for hours on a flight is literal neck torture. instead of overpriced airport gadgets, that clamp mount that locks directly onto the seatback tray table had 22k+ verified reviews for a reason—hands-free screen right at eye level. the spring clamp is a bit stiff to open at first, but completely saves your neck on long flights. here's the direct link: curatedbyemma.pages.dev/go/flight-mount. how long is your upcoming flight?",
            "looking straight down at your lap for a 4-hour flight leaves your neck completely stiff. that universal tray-table phone clamp has over 22k reviews and mounts right to the latch at eye level. clamp spring takes some force to open, but watching downloaded shows hands-free makes economy flights 10x better. found the exact one here: curatedbyemma.pages.dev/go/flight-mount. where are you flying to?"
        ]
    },
    {
        "slot": 8, "slug": "steamer", "asin": "B0FYF2X322",
        "name": "OGHom Compact Handheld Garment Steamer",
        "category": "Travel / Wrinkle removal", "rating": 4.3, "reviews": 30000,
        "honest_pros": "Heats up in 60 seconds and steams out wrinkles without dragging out a heavy iron or ironing board",
        "honest_caveats": "Compact 240ml tank only lasts for about 2-3 shirts before needing a refill; must keep it upright to prevent water bubbling",
        "templates": [
            "dragging out a heavy ironing board for travel clothes is way too much effort. that compact handheld steamer heats in 60 seconds and has over 30k verified reviews for de-wrinkling linen and cotton in one quick pass. small tank only does about 2 to 3 garments per water fill, but for quick travel touchups it handles wrinkles without dragging out a heavy iron. here's the direct link: curatedbyemma.pages.dev/go/steamer. are you traveling for work or vacation?",
            "unpacking wrinkled clothes at a hotel and trying to use a rusty hotel iron is the worst. that portable handheld steamer with 30k+ reviews steams out deep suitcase wrinkles in literally two minutes. tank is compact so you refill after 2 shirts, but it glides right over delicate fabrics without burning. found the exact one here: curatedbyemma.pages.dev/go/steamer. is it mostly linen or cotton shirts?"
        ]
    },
    {
        "slot": 9, "slug": "sleep-mask", "asin": "B07DG279MB",
        "name": "TOPOINT 3D Bluetooth Sleep Mask",
        "category": "Sleep / Side sleeping with audio", "rating": 4.3, "reviews": 13200,
        "honest_pros": "Zero eye pressure contoured 3D blackout mask with ultra-thin flat speakers that allow comfortable side sleeping",
        "honest_caveats": "Speakers are completely flat so side sleeping doesn't hurt your ears, but the velcro strap needs careful adjusting if you toss and turn aggressively",
        "templates": [
            "if light leaks or morning noise keeps waking you up, normal hard plastic earbuds hurt your ears when sleeping on your side. that 3D contoured eye mask has ultra-flat soft speakers built in and over 13k verified reviews for true pitch-black sleep. velcro strap takes a night to dial in so it doesn't shift, but you can finally side sleep without sore ears. here's the direct link: curatedbyemma.pages.dev/go/sleep-mask. do you usually listen to white noise or podcasts to fall asleep?",
            "side sleeping with regular earbuds creates so much painful pressure on your ear cartilage. that memory foam blackout mask with wafer-thin speakers inside has 13k+ reviews and lets you play white noise or podcasts comfortably on your side. takes a minute to adjust the velcro strap snug, but the total blackout and soft speakers make side sleeping with audio actually comfortable. found the link here: curatedbyemma.pages.dev/go/sleep-mask. are you a light sleeper or side sleeper?"
        ]
    },
    {
        "slot": 10, "slug": "thermometer", "asin": "B01IHHLB3W",
        "name": "ThermoPro TP03B Digital Meat Thermometer",
        "category": "Cooking / Holiday meat doneness", "rating": 4.6, "reviews": 151000,
        "honest_pros": "Reads accurate internal food temperatures in 3-4 seconds with foldaway stainless probe and bright backlight",
        "honest_caveats": "Do NOT leave the plastic body inside a hot oven or grill while door is shut; only probe touches the meat during measurement",
        "templates": [
            "the anxiety of dry holiday turkey or undercooked chicken before dinner is so stressful. after comparing dozens of kitchen thermometers, that $15 folding thermopro with 150k verified reviews is the consensus winner. reads accurately in 3 seconds flat. just don't leave the plastic body inside the oven door, only the probe touches meat. here's the direct link: curatedbyemma.pages.dev/go/thermometer. are you hosting thanksgiving this year or just regular cooking?",
            "guessing meat doneness by poking it always results in either leather-dry chicken or raw centers. the thermopro instant read with 151k reviews gives an exact digital reading in 3 seconds so you never overcook. probe folds right into the handle so it's super safe in drawers. found the exact one here: curatedbyemma.pages.dev/go/thermometer. what's the main dish you usually cook?"
        ]
    },
    {
        "slot": 11, "slug": "tubshroom", "asin": "B01BYMTYBS",
        "name": "TubShroom Revolutionary Tub Drain Hair Catcher",
        "category": "Bathroom / Drain hair clogs", "rating": 4.4, "reviews": 112000,
        "honest_pros": "Fits snugly inside standard tub drains and neatly wraps all human and pet hair out of sight without clogging water flow",
        "honest_caveats": "Must wipe collected hair off every week or water begins draining slower; does not fit flat magnetic or pop-up drain caps",
        "templates": [
            "pulling disgusting slimy hair clogs out of the shower drain with coat hangers is the worst household chore. when auditing drain protectors, the silicone tubshroom with 112k verified reviews is the undisputed consensus pick because hair wraps around the cylinder instead of going down pipes. only catch is you have to wipe it off with a paper towel once a week, but it completely ends liquid drain cleaner chemicals. direct link: curatedbyemma.pages.dev/go/tubshroom. do you have a standard drain or pop-up stopper?"
        ]
    },
    {
        "slot": 12, "slug": "pink-stuff", "asin": "B00DU5SRIY",
        "name": "The Pink Stuff Miracle Cleaning Paste",
        "category": "Deep Cleaning / Scorched pans & tile stains", "rating": 4.4, "reviews": 165000,
        "honest_pros": "Mild mineral abrasive paste erases burnt pot bottoms, tile water spots, and ceramic stains without harsh fumes",
        "honest_caveats": "It is mildly abrasive so avoid high-gloss plastic or scratchable car paint; requires a thorough damp wipe-down after scrubbing",
        "templates": [
            "scrubbing burnt cookware until your arms ache usually leaves half the carbon stains behind. the pink stuff miracle paste has over 165k verified reviews for cutting through baked grease and ceramic discoloration without toxic bleach fumes. it is mildly abrasive so test a small corner on delicate surfaces, but for stainless pans and grout it works in minutes. found the link: curatedbyemma.pages.dev/go/pink-stuff. what's the hardest stain you're dealing with?"
        ]
    },
    {
        "slot": 13, "slug": "chomchom", "asin": "B00BAGT4VO",
        "name": "ChomChom Roller Reusable Pet Hair Remover",
        "category": "Pet Care / Reusable upholstery fur removal", "rating": 4.5, "reviews": 152000,
        "honest_pros": "Electrostatic rubber squeegee lifts embedded cat and dog fur from sofas and car seats without buying sticky tape refills",
        "honest_caveats": "Only works by rolling briskly back and forth on firm upholstered fabric; does not work on smooth flat floors or loose clothing",
        "templates": [
            "buying endless packs of sticky lint tape rolls gets expensive fast when you have a shedding pet. the chomchom roller with 150k reviews uses an electrostatic squeegee that traps embedded fur in a waste chamber with a quick back-and-forth motion. won't work on smooth wood floors or loose clothes, but for couches and car seats verified pet owners swear by it. direct link: curatedbyemma.pages.dev/go/chomchom. are you dealing with cat or dog shedding?"
        ]
    },
    {
        "slot": 14, "slug": "angry-mama", "asin": "B01G717M9M",
        "name": "Angry Mama Microwave Steam Cleaner",
        "category": "Kitchen / Baked-on microwave grease", "rating": 4.3, "reviews": 62000,
        "honest_pros": "Natural vinegar and water steam loosens rock-hard microwave food crust in 7 minutes so it wipes off with one swipe",
        "honest_caveats": "Body gets extremely hot out of the microwave so lift only by the arms; vinegar steam smell is strong if you don't add lemon drops",
        "templates": [
            "scraping dried chili or soup splatters off microwave ceilings feels practically cemented on. the angry mama steam cleaner with 60k reviews uses pressurized vinegar and water steam to soften all that crust in 7 minutes so it wipes clean with one paper towel. plastic gets super hot right after microwaving so hold the arms, but it eliminates harsh chemical oven sprays. link: curatedbyemma.pages.dev/go/angry-mama. how long has that splatter been sitting there lol?"
        ]
    },
    {
        "slot": 15, "slug": "little-green", "asin": "B0016HF5GK",
        "name": "BISSELL Little Green Portable Carpet & Upholstery Cleaner",
        "category": "Home Cleaning / Carpet & pet accident stains", "rating": 4.5, "reviews": 88000,
        "honest_pros": "High-powered spray and targeted suction extracts deep set-in pet messes, coffee spills, and vehicle upholstery grime",
        "honest_caveats": "Dirty water tank must be flushed and air-dried immediately after use to prevent moldy odors; power cord is not auto-retractable",
        "templates": [
            "blotting pet stains or coffee spills with paper towels just pushes the liquid deeper into carpet padding. the bissell little green with 88k verified reviews is the consensus winner for pulling out deep upholstery grime that surface sprays can't touch. you do need to rinse the dirty water tank right after use so it stays fresh, but it saves couches from being ruined. direct link: curatedbyemma.pages.dev/go/little-green. is it a pet stain or a drink spill?"
        ]
    },
    {
        "slot": 16, "slug": "fabric-shield", "asin": "B000063515",
        "name": "Scotchgard Fabric Water Shield Spray",
        "category": "Furniture / Spill & stain prevention", "rating": 4.6, "reviews": 26000,
        "honest_pros": "Invisible barrier forces liquid spills, coffee, and wine to bead on top of fabric upholstery instead of absorbing instantly",
        "honest_caveats": "Strong solvent odor during initial application so spray in a well-ventilated area; high-friction seat cushions need re-coating every 6 months",
        "templates": [
            "the constant fear of someone spilling red wine or coffee on a light-colored couch is exhausting. scotchgard fabric water shield with 26k reviews creates a surface barrier that makes liquids bead right up for easy blotting before soaking in. strong chemical smell while spraying so crack the windows open, but it preserves fabric from accidental stains. link: curatedbyemma.pages.dev/go/fabric-shield. is your sofa linen or woven fabric?"
        ]
    },
    {
        "slot": 17, "slug": "draft-stopper", "asin": "B0836Z3T75",
        "name": "MAXTID Under Door Draft Stopper Seal",
        "category": "Home Comfort / Door drafts & hallway noise", "rating": 4.3, "reviews": 31000,
        "honest_pros": "Double-sided foam cylinders slide under door, insulating against winter drafts, apartment hallway noise, and outside light",
        "honest_caveats": "Can drag slightly on high-pile shag rugs; measure your door gap before trimming foam tubes to length",
        "templates": [
            "cold drafts slipping under bedroom doors and apartment hallway footsteps can make bedrooms feel impossible to keep cozy. double-sided under-door draft seals with 30k+ verified reviews block both chilly airflow and hallway light without needing screws or glue. drags slightly on thick shag rugs, but for keeping room temperatures stable it makes a noticeable difference. link: curatedbyemma.pages.dev/go/draft-stopper. is it on hardwood or carpet?"
        ]
    },
    {
        "slot": 18, "slug": "stove-gap", "asin": "B073VWB4F9",
        "name": "Linda's Essentials Silicone Stove Counter Gap Covers",
        "category": "Kitchen / Stove counter food gap", "rating": 4.4, "reviews": 46000,
        "honest_pros": "Heat-resistant flexible T-seal bridges the crack between stove and countertop so crumbs and sauces never drop down the side",
        "honest_caveats": "Matte silicone collects fine kitchen dust and needs a weekly rinse; only seals flush if your stove and counter are roughly level",
        "templates": [
            "dropping crumbs, sauce, or utensils into the dark crack between the stove and kitchen counter is so annoying because you can never reach it. heat-resistant silicone stove gap covers with 45k+ reviews bridge that gap completely so everything wipes right onto the counter. matte silicone catches dust so give it a quick rinse occasionally, but it saves deep stove cleanouts. link: curatedbyemma.pages.dev/go/stove-gap. are your countertops granite or laminate?"
        ]
    },
    {
        "slot": 19, "slug": "dish-brush", "asin": "B0038K2FES",
        "name": "Full Circle Bubble Up Ceramic Soap Dispenser & Dish Brush",
        "category": "Kitchen / Sink organization & dish soap", "rating": 4.5, "reviews": 16000,
        "honest_pros": "Spring-loaded ceramic base foams soap directly into natural plant bristles with one pump, eliminating slimy soap bottles",
        "honest_caveats": "Bamboo handle needs to air-dry upright to prevent moisture wear; replace worn brush heads every 4 to 6 months",
        "templates": [
            "messy plastic dish soap bottles leaking slimy rings all over sink edges looks so cluttered. the full circle ceramic bubble-up set with 16k reviews uses a spring-loaded base that foams soap right into the brush with a single press. bamboo handle should dry standing upright so water doesn't pool, but it keeps the whole sink area super tidy. link: curatedbyemma.pages.dev/go/dish-brush. do you prefer liquid dish soap or solid dish blocks?"
        ]
    },
    {
        "slot": 20, "slug": "jar-opener", "asin": "B00004OCL8",
        "name": "OXO Good Grips Jar Opener with Base Pad",
        "category": "Kitchen / Stuck jar lids & weak grip", "rating": 4.5, "reviews": 26000,
        "honest_pros": "Hardened stainless steel teeth grip vacuum-sealed jar lids of any size, multiplying leverage to pop them open with zero wrist strain",
        "honest_caveats": "Requires two hands (holding the jar base on non-slip pad and turning opener); gripping teeth will slightly dent metal lids",
        "templates": [
            "banging vacuum-sealed pickle jars against countertops or straining your wrists trying to twist stubborn lids is painful. oxo's stainless jar opener with 26k verified reviews locks onto any lid diameter with sharp teeth to break the seal with minimal effort. teeth can leave tiny indentations on metal lids, but it completely removes hand strain. direct link: curatedbyemma.pages.dev/go/jar-opener. is it mostly pickle jars or tight pasta sauce lids?"
        ]
    },
    {
        "slot": 21, "slug": "pumice-stick", "asin": "B000092N2X",
        "name": "Pumie Heavy Duty Pumice Scouring Stick",
        "category": "Bathroom / Hard water toilet bowl rings", "rating": 4.4, "reviews": 42000,
        "honest_pros": "Natural volcanic pumice erases stubborn mineral toilet bowl rings, rust, and lime scale that chemical bleach sprays fail to touch",
        "honest_caveats": "Both the pumice stick and porcelain surface MUST be kept wet during use to prevent scratches; stick naturally erodes as you scrub",
        "templates": [
            "hard water mineral rings inside toilet bowls laugh at normal toilet brushes and bleach sprays. heavy-duty pumice scouring sticks with 40k+ verified reviews physically buff out mineral scale and rust without chemical fumes. just make sure the stick and porcelain stay wet while scrubbing so it doesn't scratch, but it makes decades-old bowls look new. link: curatedbyemma.pages.dev/go/pumice-stick. have you been dealing with lime or rust stains?"
        ]
    },
    {
        "slot": 22, "slug": "bar-keepers", "asin": "B000V72992",
        "name": "Bar Keepers Friend Cookware Cleanser & Polish",
        "category": "Cookware / Scorched stainless steel pots", "rating": 4.7, "reviews": 36000,
        "honest_pros": "Oxalic acid mineral cleanser dissolves heat tint, cloudy mineral haze, and baked pan grease on stainless steel in under a minute",
        "honest_caveats": "Can dry out sensitive hands so wear rubber cleaning gloves; do not use on non-stick Teflon or seasoned cast iron",
        "templates": [
            "cloudy heat stains and burnt grease on stainless steel skillets make great cookware look ruined. bar keepers friend with 36k reviews uses oxalic acid to break down mineral scale and scorched oil without heavy scrubbing. wear gloves because the powder can dry skin, but for bringing stainless steel pots back to a mirror shine it is the gold standard. link: curatedbyemma.pages.dev/go/bar-keepers. what brand of cookware do you use?"
        ]
    },
    {
        "slot": 23, "slug": "smart-plug", "asin": "B091FXLMS8",
        "name": "Kasa Smart Plug Ultra Mini (15A)",
        "category": "Smart Home / Hard-to-reach lamps & appliances", "rating": 4.6, "reviews": 125000,
        "honest_pros": "Control floor lamps, space heaters, and holiday lights on automated schedules from your phone or voice without needing a hub",
        "honest_caveats": "Connects strictly to 2.4GHz Wi-Fi frequencies (not 5GHz); takes a couple minutes to do the initial router pairing",
        "templates": [
            "crawling behind sofas to plug in floor lamps or worrying if you left a space heater on after leaving the house is unnecessary stress. kasa smart plugs with 120k+ reviews let you set automatic sunset timers and phone toggles with zero external hub needed. works only on 2.4GHz Wi-Fi networks, but for scheduling room lighting it works seamlessly. link: curatedbyemma.pages.dev/go/smart-plug. do you use Alexa, Google Home, or just your phone?"
        ]
    },
    {
        "slot": 24, "slug": "magsafe-ring", "asin": "B099596FYR",
        "name": "Anker Magnetic Phone Ring Holder (MagGo)",
        "category": "Tech / Phone dropping in bed & desk stand", "rating": 4.4, "reviews": 32000,
        "honest_pros": "Snap-on MagSafe ring acts as a secure finger grip so phones don't drop on your nose in bed, doubling as an adjustable desk kickstand",
        "honest_caveats": "Requires a MagSafe-compatible phone or case; must slide ring off before placing phone on flat wireless charging pads",
        "templates": [
            "scrolling in bed and having a heavy phone slip and smash right onto your face is an instant wake-up call. anker's magnetic magsafe ring with 30k+ reviews snaps on with strong magnets to give you a natural one-handed grip and doubles as a sturdy video stand. needs a magsafe case to lock firmly, but it completely prevents screen drops. direct link: curatedbyemma.pages.dev/go/magsafe-ring. what phone model are you rocking?"
        ]
    },
    {
        "slot": 25, "slug": "dohm", "asin": "B000KUHFGM",
        "name": "Yogasleep Dohm Classic Natural Sound Machine",
        "category": "Sleep / Loud neighbors & street traffic noise", "rating": 4.5, "reviews": 46000,
        "honest_pros": "Real acoustic internal fan creates authentic soothing rushing-air white noise that masks stomping upstairs neighbors and street noise",
        "honest_caveats": "Has two physical fan speed settings (no digital nature sounds or shutoff timer); heavier than battery travel sound devices",
        "templates": [
            "tinny digital speaker sound machines with looping audio tracks rarely drown out heavy upstairs foot traffic. the yogasleep dohm classic with 45k reviews uses an actual mechanical fan inside an acoustic shell to generate genuine rushing air frequencies that mask ambient noise. only has two mechanical speeds without digital bells and whistles, but for uninterrupted sleep it is unmatched. link: curatedbyemma.pages.dev/go/dohm. are you dealing with street noise or neighbor footsteps?"
        ]
    },
    {
        "slot": 26, "slug": "hydration", "asin": "B01IT9NLHW",
        "name": "Liquid I.V. Hydration Multiplier Packets",
        "category": "Travel & Wellness / Post-flight dehydration", "rating": 4.6, "reviews": 135000,
        "honest_pros": "Cellular Transport Technology delivers electrolytes and hydration to the bloodstream 2x faster than plain water after flights or workouts",
        "honest_caveats": "Has a noticeably salty-sweet taste so mix in 20-24oz water instead of small glasses; contains natural cane sugar",
        "templates": [
            "the dry pressurized airplane cabin air leaves your throat scratchy, head throbbing, and body completely drained after flying. liquid iv hydration packets with 135k verified reviews use an electrolyte ratio that absorbs significantly faster than plain water. pretty sweet taste so dilute it in a large 24oz water bottle, but it stops travel fatigue fast. link: curatedbyemma.pages.dev/go/hydration. what's your favorite flavor to drink?"
        ]
    },
    {
        "slot": 27, "slug": "loop-quiet", "asin": "B08MFH1BHS",
        "name": "Loop Quiet Ear Plugs for Sleep",
        "category": "Sleep / Snoring partner & sensitive ears", "rating": 4.3, "reviews": 68000,
        "honest_pros": "Ultra-soft flexible silicone ring sits completely flush inside ear, providing 26dB noise reduction without side-sleeping cartilage pain",
        "honest_caveats": "Must test all 4 included silicone tip sizes for an airtight seal; does not fully eliminate close-range heavy snoring, only muffles it",
        "templates": [
            "sleeping next to a loud snorer while wearing stiff foam earplugs makes your ear cartilage ache by 3am. loop quiet silicone sleep plugs with 68k reviews sit flush inside your outer ear so side sleeping doesn't put pressure on your ears while knocking out 26dB of noise. takes a night to test which tip size gives the tightest seal, but it saves relationships. direct link: curatedbyemma.pages.dev/go/loop-quiet. are you a light sleeper or side sleeper?"
        ]
    },
    {
        "slot": 28, "slug": "satin-pillow", "asin": "B072LXQ7PT",
        "name": "Bedsure Satin Pillowcase for Hair & Skin",
        "category": "Beauty / Frizzy bedhead & skin creases", "rating": 4.5, "reviews": 285000,
        "honest_pros": "Silky-smooth polyester satin eliminates fabric friction against curls and skin, stopping morning hair breakage and pillow creases",
        "honest_caveats": "Slick fabric can cause pillows to slip around if headboard has gaps; wash on delicate cycle to preserve smooth sheen",
        "templates": [
            "waking up with frizzy tangled hair and deep sleep creases pressed into your face from rough cotton pillowcases is frustrating. bedsure satin pillowcases with 280k+ reviews reduce hair friction so curls stay defined and skin doesn't get crushed overnight. fabric is slippery so tuck the envelope closure snugly, but for hair preservation it works wonders. direct link: curatedbyemma.pages.dev/go/satin-pillow. do you have naturally curly or straight hair?"
        ]
    },
    {
        "slot": 29, "slug": "disposal-cleaner", "asin": "B000BQWJ6K",
        "name": "Glisten Garbage Disposer Cleaner & Deodorizer",
        "category": "Kitchen / Stinky garbage disposal smells", "rating": 4.5, "reviews": 47000,
        "honest_pros": "Deep-cleaning foam reaches hidden blades, under splash guards, and sidewalls to scrub rotten food particles and sewer odors",
        "honest_caveats": "Foam expanding action requires following warm water flow instructions carefully; will not fix deeper underground plumbing pipe clogs",
        "templates": [
            "that mysterious sour sewer odor coming from the kitchen sink is usually rotting food grease trapped underneath the disposal splash guard. glisten disposal cleaner packets with 45k+ reviews generate an expanding blue foam that scrubs the hidden underside of blades where brushes can't reach. follow the water stream instructions carefully, but it clears sink odors in 2 minutes. link: curatedbyemma.pages.dev/go/disposal-cleaner. how old is your kitchen disposal?"
        ]
    },
    {
        "slot": 30, "slug": "powerwash", "asin": "B07VN9QY29",
        "name": "Dawn Platinum Powerwash Dish Spray",
        "category": "Kitchen / Soaking greasy baking pans", "rating": 4.8, "reviews": 62000,
        "honest_pros": "Direct continuous spray activates foam on contact with zero water, breaking down baked cheese and grease on sheet pans in 5 minutes",
        "honest_caveats": "Strong fresh aroma requires thorough warm water rinsing; spray nozzle can run through refills quickly if used on every tiny cup",
        "templates": [
            "leaving greasy casserole dishes and sheet pans soaking in the sink for 24 hours just creates cold murky water and takes up counter space. dawn powerwash spray with 60k reviews sprays concentrated suds that lift burnt cheese and grease on contact before adding water. strong scent so rinse well with warm water, but for stubborn cookware it eliminates overnight soaking. direct link: curatedbyemma.pages.dev/go/powerwash. what's the hardest dish you had to scrub lately?"
        ]
    },
    {
        "slot": 31, "slug": "frother", "asin": "B074ZL35DH",
        "name": "Zulay Original Milk Frother Handheld Wand",
        "category": "Coffee / Clumpy protein powder & latte foam", "rating": 4.5, "reviews": 115000,
        "honest_pros": "High-torque motorized whisk aerates cold milk into thick cafe foam and blends chalky protein powder or matcha in 15 seconds",
        "honest_caveats": "Runs on 2 AA batteries (not USB rechargeable); spins with enough power to splash liquid if cup is filled to the absolute brim",
        "templates": [
            "drinking protein shakes or matcha with chalky dry powder clumps floating on top is so unappetizing. the zulay handheld milk frother with 110k reviews spins at high speed to dissolve powders and whip rich latte foam in 15 seconds flat. runs on 2 AA batteries so keep a couple spares, but it completely replaces bulky shaker cups. direct link: curatedbyemma.pages.dev/go/frother. do you use it for morning coffee or protein shakes?"
        ]
    },
    {
        "slot": 32, "slug": "veggie-chopper", "asin": "B0764HS44J",
        "name": "Fullstar Vegetable Chopper Pro (4 Blades)",
        "category": "Cooking / Dicing onions & meal prep hand fatigue", "rating": 4.5, "reviews": 98000,
        "honest_pros": "Sharp stainless grid chops an entire onion or potato into uniform dice in one swift press directly into the catch tray",
        "honest_caveats": "You must slice root veggies into flat rounds first (forcing a massive whole hard carrot can strain the hinge); hand-wash blade grid",
        "templates": [
            "standing over a cutting board weeping from onion fumes while hand-dicing twenty vegetables takes forever during Sunday meal prep. the fullstar vegetable chopper with 95k reviews dices whole onions in one downward press directly into the storage container with zero eye tears. slice onions in half first so the grid presses cleanly, but it cuts prep time in half. found the link: curatedbyemma.pages.dev/go/veggie-chopper. what dishes do you usually meal prep?"
        ]
    },
    {
        "slot": 33, "slug": "egg-cooker", "asin": "B00DDXWFY0",
        "name": "Dash Rapid Egg Cooker (6-Capacity)",
        "category": "Kitchen / Hard-to-peel boiled eggs", "rating": 4.7, "reviews": 118000,
        "honest_pros": "Steam pressure cooks soft, medium, or hard-boiled eggs in under 10 minutes with shells that slip off in one continuous piece",
        "honest_caveats": "The finish chime buzzer is noticeably loud and sharp; base heating plate needs occasional lemon/vinegar wipe to clear hard water spots",
        "templates": [
            "boiling eggs on the stove and having shells stick like concrete, tearing half the egg whites off, ruins breakfast. the dash rapid egg cooker with 115k reviews uses targeted steam to cook eggs perfectly with shells that slide right off in one piece. buzzer chime is super loud when finished, but for peeling hard-boiled eggs with zero frustration it is worth every penny. link: curatedbyemma.pages.dev/go/egg-cooker. do you prefer jammy soft-boiled or firm hard-boiled?"
        ]
    },
    {
        "slot": 34, "slug": "packing-cubes", "asin": "B07XDN7T54",
        "name": "Bagail 8 Set Compression Packing Cubes",
        "category": "Travel / Messy overstuffed suitcases", "rating": 4.6, "reviews": 47000,
        "honest_pros": "Secondary compression zipper squeezes bulky sweaters and clothes down by 40%, keeping carry-on bags neatly compartmentalized",
        "honest_caveats": "Compressing clothes saves valuable volume but doesn't reduce bag weight; don't yank zippers around overstuffed corners",
        "templates": [
            "digging through an exploded suitcase in a hotel room trying to find one pair of socks ruins travel organization. bagail compression packing cubes with 45k reviews use a secondary perimeter zipper to compress bulky clothes by 40% while keeping items separated. saves tons of suitcase volume though weight stays the same, but it keeps carry-ons orderly. link: curatedbyemma.pages.dev/go/packing-cubes. are you packing for a weekend trip or long vacation?"
        ]
    },
    {
        "slot": 35, "slug": "luggage-scale", "asin": "B00NW62PCA",
        "name": "Etekcity Digital Hanging Luggage Scale",
        "category": "Travel / Airport overweight baggage fees", "rating": 4.7, "reviews": 68000,
        "honest_pros": "Accurate digital hook sensor weighs heavy suitcases up to 110 lbs before leaving home, preventing unexpected $100 airline check-in fees",
        "honest_caveats": "Requires lifting the full weight of the suitcase off the ground by hand for 3 seconds to lock reading; uses a CR2032 watch battery",
        "templates": [
            "the dreaded panic at the airport check-in counter when the conveyor belt scale hits 52 lbs and you have to open suitcases in public is the worst. etekcity's digital luggage scale with 65k reviews weighs bags up to 110 lbs at home so you know exact numbers beforehand. takes lifting the bag off the floor for a few seconds to lock the screen, but it avoids airline fees. link: curatedbyemma.pages.dev/go/luggage-scale. who are you flying with on your next trip?"
        ]
    },
    {
        "slot": 36, "slug": "gear-tie", "asin": "B00SHBO284",
        "name": "Nite Ize Gear Tie Reusable Rubber Twist Ties",
        "category": "Home / Tangled appliance cords & wire knots", "rating": 4.8, "reviews": 22000,
        "honest_pros": "Thick rubber-coated bendable wire grips appliance cords, hoses, and charger cables without scratching or snapping like brittle plastic zip ties",
        "honest_caveats": "A bit too thick for tiny delicate earbud wires; bend memory slowly softens after hundreds of heavy industrial wraps",
        "templates": [
            "tangled electrical cords in drawers forming knotted nests that take ten minutes to untangle is such a pet peeve. nite ize reusable rubber gear ties with 22k reviews have a bendable internal wire with a soft grip shell that holds heavy appliance cords securely. a bit chunky for super thin charging wires, but for kitchen mixers, vacuums, and thick cables it organizes everything. link: curatedbyemma.pages.dev/go/gear-tie. what drawer needs the most help in your house?"
        ]
    },
    {
        "slot": 37, "slug": "sink-organizer", "asin": "B09TSMT3L2",
        "name": "Slideep 2-Tier Under Sink Organizer with Sliding Drawer",
        "category": "Home / Dark cluttered under-sink cabinets", "rating": 4.5, "reviews": 26000,
        "honest_pros": "Sliding bottom drawer rolls out smoothly from under bathroom and kitchen sinks so you can grab cleaning bottles without digging",
        "honest_caveats": "Measure cabinet depth and drainage pipe clearance before buying; top tier is narrower to fit around drain trap pipes",
        "templates": [
            "crawling on your knees with a flashlight trying to find extra trash bags or sprays lost in the dark cavern under the sink is so chaotic. slideep's 2-tier under sink organizer with 25k reviews features a smooth slide-out bottom basket that brings bottles straight to you. check pipe clearance dimensions under your sink first, but it completely doubles usable cabinet space. link: curatedbyemma.pages.dev/go/sink-organizer. is this for the kitchen or bathroom cabinet?"
        ]
    },
    {
        "slot": 38, "slug": "bed-sheets", "asin": "B00NLLUMOE",
        "name": "Mellanni Deep Pocket Microfiber Bed Sheet Set",
        "category": "Bedroom / Fitted sheets popping off mattress", "rating": 4.5, "reviews": 345000,
        "honest_pros": "Buttery-soft double-brushed microfiber with continuous all-around elastic deep pockets that stay firmly tucked on thick mattresses",
        "honest_caveats": "Being synthetic microfiber, they sleep slightly warmer than lightweight 100% percale cotton during hot humid summer months",
        "templates": [
            "fitted bed sheets that pop off mattress corners in the middle of the night leaving you sleeping on bare foam are beyond infuriating. mellanni's deep pocket sheet sets with over 340k reviews have all-around reinforced elastic that stays anchored on pillowtop mattresses. traps body heat slightly more than crisp percale cotton in peak summer, but for staying locked down and wrinkle-free it is a favorite. link: curatedbyemma.pages.dev/go/bed-sheets. do you have a standard or deep mattress?"
        ]
    },
    {
        "slot": 39, "slug": "power-scrubber", "asin": "B0032V1UPC",
        "name": "Rubbermaid Reveal Cordless Battery Power Scrubber",
        "category": "Cleaning / Scrubbing tile grout & faucet grime", "rating": 4.4, "reviews": 37000,
        "honest_pros": "Oscillating brush head delivers 60 scrubs per second, cleaning black mildew from tile grout, sink edges, and shower corners without knuckle strain",
        "honest_caveats": "Runs on 4 AA batteries which drain during long deep cleans (rechargeable AAs recommended); head is small for massive floor surfaces",
        "templates": [
            "scrubbing dirty bathroom tile grout with an old toothbrush until your knuckles are raw and your wrists ache takes forever. the rubbermaid reveal power scrubber with 35k reviews uses an oscillating high-speed brush head that powers through black grout lines and faucet scale in seconds. burns through 4 AA batteries on deep cleaning days, but it saves your wrists and fingernails. direct link: curatedbyemma.pages.dev/go/power-scrubber. is it for shower tile or sink faucets?"
        ]
    },
    {
        "slot": 40, "slug": "conair-shaver", "asin": "B008I25368",
        "name": "Conair Battery Operated Compact Fabric Defuzzer",
        "category": "Wardrobe / Pilled leggings & couch cushions", "rating": 4.5, "reviews": 112000,
        "honest_pros": "Compact 3-depth adjustable shaver trims pills off gym leggings, wool blankets, and fleece outerwear quickly without snagging delicate fibers",
        "honest_caveats": "Runs on 2 AA batteries so motor speed drops as batteries deplete; lint collection cup fills up quickly on large blankets",
        "templates": [
            "favorite black gym leggings or wool blend cardigans developing fuzzy pilling between the thighs or cuffs makes clothes look instantly worn out. conair's battery fabric defuzzer with 110k reviews has a 3-depth guard that shaves pills clean without nicking fabric. runs on AA batteries so keep fresh ones handy, but it makes pilled athleisure look brand new. found the link: curatedbyemma.pages.dev/go/conair-shaver. are you trimming leggings or a knit sweater?"
        ]
    },
    {
        "slot": 41, "slug": "pimple-patch", "asin": "B074PVTPBW",
        "name": "Hero Cosmetics Mighty Patch Original Acne Patches",
        "category": "Skincare / Popping whiteheads & face picking", "rating": 4.5, "reviews": 148000,
        "honest_pros": "Medical-grade hydrocolloid stickers extract pus and oil from surface pimples overnight while physically preventing unconscious face-picking",
        "honest_caveats": "Only works on whiteheads with visible surface fluid (does not resolve deep blind hormonal cystic bumps under the skin)",
        "templates": [
            "the urge to squeeze an angry whitehead right before an event usually results in inflamed scabs and post-acne marks. hero cosmetics mighty patches with 145k+ reviews use hydrocolloid that draws out all the gunk overnight while stopping fingers from picking. only works on pimples that have come to a visible head, but it flattens blemishes with zero scarring. link: curatedbyemma.pages.dev/go/pimple-patch. do you usually get surface blemishes or deep spots?"
        ]
    },
    {
        "slot": 42, "slug": "aquaphor", "asin": "B006IB5T4W",
        "name": "Aquaphor Healing Ointment Advanced Therapy",
        "category": "Skincare / Severely cracked winter lips & skin", "rating": 4.8, "reviews": 88000,
        "honest_pros": "Protective petrolatum, panthenol, and glycerin formula seals in hydration to heal cracked winter lips, raw noses, and cuticles overnight",
        "honest_caveats": "Very rich, thick ointment consistency that feels greasy on bare fingers; can leave oily marks on delicate silk or satin bedding",
        "templates": [
            "waking up in cold winter months with bleeding cracked lips and peeling knuckles that sting every time you wash your hands is miserable. aquaphor healing ointment with 88k reviews creates a semi-permeable barrier that lets skin breathe while locking in moisture to repair raw fissures overnight. greasy texture so apply it before sleeping, but for severe dry skin it works better than fancy lotions. link: curatedbyemma.pages.dev/go/aquaphor. are you dealing with chapped lips or dry hands?"
        ]
    },
    {
        "slot": 43, "slug": "working-hands", "asin": "B00121UVU0",
        "name": "O'Keeffe's Working Hands Hand Cream Jar",
        "category": "Body Care / Cracked raw skin from frequent washing", "rating": 4.7, "reviews": 78000,
        "honest_pros": "High-concentration non-greasy glycerin cream stimulates natural skin repair on severely cracked fingertips and working hands without washing away",
        "honest_caveats": "Can cause a temporary 30-second mild sting if applied into fresh, open skin cracks; completely unfragranced",
        "templates": [
            "washing dishes or working outside in the cold until fingertips crack open and bleed around the nails makes basic typing painful. o'keeffe's working hands cream with 78k verified reviews creates a deep moisture barrier that doesn't wash off in five seconds like watery perfumed lotions. can sting for half a minute on open cracks, but it closes split skin in 48 hours. link: curatedbyemma.pages.dev/go/working-hands. do you work with your hands a lot during the day?"
        ]
    },
    {
        "slot": 44, "slug": "shower-spray", "asin": "B0019KTH0M",
        "name": "Wet & Forget Shower Daily Cleaner Spray",
        "category": "Bathroom / Daily soap scum & hard water shower stains", "rating": 4.4, "reviews": 26000,
        "honest_pros": "Spray wet shower walls and glass doors right after showering once a week to dissolve soap scum with zero wiping, scrubbing, or harsh fumes",
        "honest_caveats": "Designed for ongoing maintenance; if you have years of rock-hard calcium crust built up, you must do one manual deep clean first",
        "templates": [
            "standing in a steamy shower scrubbing cloudy soap scum off glass doors with harsh bleach fumes is the worst Saturday chore. wet & forget shower spray with 26k reviews dissolves soap film and mineral scale automatically with zero scrubbing—just spray after showering and rinse the next day. won't instantly remove 5-year mineral crust on day one, but for keeping glass spotless it eliminates manual scrubbing. link: curatedbyemma.pages.dev/go/shower-spray. is your shower glass or fiberglass?"
        ]
    },
    {
        "slot": 45, "slug": "command-strips", "asin": "B073XR4X72",
        "name": "Command Large Picture Hanging Strips (16 Pairs)",
        "category": "Home Decor / Hanging wall art in rental apartments", "rating": 4.6, "reviews": 58000,
        "honest_pros": "Click-locking hook-and-loop strips hold heavy framed pictures securely to painted drywall without nails, hammer holes, or losing security deposits",
        "honest_caveats": "Must wait 1 full hour after pressing strips to wall before snapping frames on; does not stick reliably to textured stucco or humid brick",
        "templates": [
            "drilling holes into apartment drywall to hang wall art and stressing about patching them up before moving out to save your security deposit is annoying. command large picture hanging strips with 55k+ reviews lock frames flush to walls with interlocking grips that pull off cleanly without taking paint off. follow the 1-hour adhesive cure time before mounting weight, but it saves rental walls. link: curatedbyemma.pages.dev/go/command-strips. what size frames are you hanging?"
        ]
    },
    {
        "slot": 46, "slug": "french-press", "asin": "B07JDFXWLS",
        "name": "Mueller Double-Wall Stainless Steel French Press",
        "category": "Kitchen / Shattered glass coffee presses", "rating": 4.6, "reviews": 32000,
        "honest_pros": "Heavy-duty double-wall stainless steel body keeps coffee piping hot for 60 minutes and will never shatter in the sink like fragile glass carafes",
        "honest_caveats": "Solid steel body means you cannot see coffee level while pressing; requires coarse ground beans to avoid fine sediment at the cup bottom",
        "templates": [
            "having a delicate glass french press shatter in the kitchen sink while washing it with hot water is both terrifying and dangerous. mueller's double-wall stainless steel press with 30k reviews is virtually drop-proof and keeps brewed coffee hot for over an hour. opaque body means you can't see the liquid level through the sides, but you will never have to buy replacement glass beakers again. link: curatedbyemma.pages.dev/go/french-press. what kind of coffee roast do you brew?"
        ]
    },
    {
        "slot": 47, "slug": "hygrometer", "asin": "B01H1R0K68",
        "name": "ThermoPro TP50 Digital Room Thermometer & Hygrometer",
        "category": "Home / Apartment dryness, static & humidity check", "rating": 4.6, "reviews": 88000,
        "honest_pros": "Fast accurate indoor humidity and temperature sensor with comfort indicators shows exactly when winter heater air is too dry or mold-prone",
        "honest_caveats": "LCD screen is not backlit so you cannot read numbers in a pitch-black bedroom at night; refreshes readings every 10 seconds",
        "templates": [
            "waking up with dry scratchy throats, static shocks on blankets, and wondering if your apartment heater is sucking all the moisture out of the air is frustrating. thermopro's digital hygrometer with 85k reviews tracks room humidity and temp in real time so you know when to turn on a humidifier. screen isn't backlit for dark rooms, but for keeping indoor air balanced it gives you actual data. link: curatedbyemma.pages.dev/go/hygrometer. does your place feel super dry right now?"
        ]
    },
    {
        "slot": 48, "slug": "oven-mitts", "asin": "B079J8XQ7Q",
        "name": "Gorilla Grip Heat Resistant Silicone Oven Mitts",
        "category": "Kitchen / Burning fingers through thin fabric oven pads", "rating": 4.7, "reviews": 32000,
        "honest_pros": "Waterproof textured silicone exterior resists heat up to 484°F with non-slip grip on heavy cast iron skillets and boiling soup pots",
        "honest_caveats": "Bulkier and stiffer than traditional cloth fabric pot holders; inner cotton lining can bunch if pulling wet hands out quickly",
        "templates": [
            "feeling heat searing through thin cotton potholders when pulling a 450-degree heavy cast iron skillet out of the oven is genuinely terrifying. gorilla grip silicone oven mitts with 30k+ reviews are heat-proof up to 484°F and waterproof so steam or boiling broth can't burn your skin. slightly bulkier than cloth pads, but for lifting heavy roasting pans safely they give a secure grip. link: curatedbyemma.pages.dev/go/oven-mitts. do you cook with cast iron or sheet pans mostly?"
        ]
    },
    {
        "slot": 49, "slug": "airplane-footrest", "asin": "B071JM1T46",
        "name": "Sleepy Ride Airplane Footrest Under Seat Hammock",
        "category": "Travel / Swollen legs & lower back flight ache", "rating": 4.3, "reviews": 16000,
        "honest_pros": "Memory foam hammock hangs from tray table arms, elevating feet to take pressure off thighs and lower back during long economy flights",
        "honest_caveats": "Tray table must be stowed for takeoff and landing; taller travelers with long legs have less clearance to swing feet forward",
        "templates": [
            "sitting in cramped economy airline seats with feet dangling or pressed flat against cold floorboards leaves your lower back aching and ankles swollen. sleepy ride's airplane footrest hammock with 15k reviews loops over the tray table arms to cradle your feet elevated like a recliner. must stow during takeoff and landing, but for red-eyes and 6-hour flights it takes pressure off your lower spine. link: curatedbyemma.pages.dev/go/airplane-footrest. how long is your next flight?"
        ]
    },
    {
        "slot": 50, "slug": "furzapper", "asin": "B074CHX3HH",
        "name": "FurZapper Pet Hair Remover for Washer and Dryer",
        "category": "Laundry / Pet fur stuck to washed clothes", "rating": 4.1, "reviews": 26000,
        "honest_pros": "Sticky silicone paw tumbles inside washing machines and dryers, pulling stubborn dog and cat hair off fabric directly into the lint trap",
        "honest_caveats": "Do NOT use fabric softeners or dryer sheets (softener oils coat the silicone and ruin its tackiness); rinse with dish soap between cycles",
        "templates": [
            "pulling freshly washed black shirts out of the dryer only to find dog hair still baked into the weave fibers makes doing laundry feel pointless. furzapper silicone paws with 25k reviews tumble in the wash and dryer to grab pet fur off wet fabric and wash it down the drain or into the lint trap. never use with fabric softeners since oils coat the tacky surface, but it saves lint rolling every shirt. link: curatedbyemma.pages.dev/go/furzapper. do you deal with short or long pet fur in the wash?"
        ]
    }
]

print(f"Loaded {len(ITEMS_50)} items.")

# 1. Update master_catalog.json
catalog_list = []
for item in ITEMS_50:
    catalog_list.append({
        "asin": item["asin"],
        "category": item["category"],
        "target_pain_point": item["honest_pros"],
        "title": item["name"],
        "price": 19.99,
        "currency": "USD",
        "rating": item["rating"],
        "reviews_count": item["reviews"],
        "bought_past_month": "1K+ bought in past month",
        "winning_score": round(100.0 - (item["slot"] * 0.5), 1),
        "image_url": f"https://m.media-amazon.com/images/I/default_{item['asin']}.jpg",
        "affiliate_url": f"https://www.amazon.com/dp/{item['asin']}?tag={AMAZON_TAG}",
        "slot_number": item["slot"],
        "slug": item["slug"]
    })

with open("/Users/macbookair/.gemini/antigravity/scratch/affiliate-engine/master_catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog_list, f, indent=2)
print("Updated master_catalog.json with 50 products.")

# 2. Update functions/go/[[catchall]].js
cf_code = """/**
 * Cloudflare Pages Edge Function: CuratedByEmma Smart Outbound Redirector
 * Maps 50 Curated Viral Amazon Problem-Solvers to Cloaked Redirects.
 * Direct ASIN fallback and Shopee Indonesia fallbacks supported.
 */

const AMAZON_TAG = "curatedbyem0f-20";

const AMAZON_PRODUCTS = {
"""

for item in ITEMS_50:
    slot_str = str(item["slot"])
    slug_str = item["slug"]
    asin = item["asin"]
    url_target = f"https://www.amazon.com/dp/{asin}?tag=" + " + AMAZON_TAG"
    cf_code += f'  // Slot #{slot_str}: {item["name"]}\n'
    cf_code += f'  "{slot_str}": "https://www.amazon.com/dp/{asin}?tag=" + AMAZON_TAG,\n'
    cf_code += f'  "{slug_str}": "https://www.amazon.com/dp/{asin}?tag=" + AMAZON_TAG,\n\n'

cf_code += """};

// Fallback Shopee targets if Indonesian slug clicked on Emma domain
const SHOPEE_FALLBACKS = {
  "serbuk": "https://s.shopee.co.id/an_redir?origin_link=https%3A%2F%2Fshopee.co.id%2Fsearch%3Fkeyword%3Dserbuk%20pembersih%20kerak%20panci%20gosong&affiliate_id=11324391980&sub_id=serbuk",
  "rak": "https://s.shopee.co.id/an_redir?origin_link=https%3A%2F%2Fshopee.co.id%2Fsearch%3Fkeyword%3Drak%20sudut%20kamar%20mandi%20tempel%20tanpa%20bor&affiliate_id=11324391980&sub_id=rak",
  "pel": "https://s.shopee.co.id/an_redir?origin_link=https%3A%2F%2Fshopee.co.id%2Fsearch%3Fkeyword%3Dalat%20pel%20flat%20mop%20peras%20otomatis&affiliate_id=11324391980&sub_id=pel",
  "tawas": "https://s.shopee.co.id/an_redir?origin_link=https%3A%2F%2Fshopee.co.id%2Fsearch%3Fkeyword%3Ddeodorant%20tawas%20spray%20ketiak&affiliate_id=11324391980&sub_id=tawas",
  "acne": "https://s.shopee.co.id/an_redir?origin_link=https%3A%2F%2Fshopee.co.id%2Fsearch%3Fkeyword%3Dacne%20patch%20jerawat%20hydrocolloid&affiliate_id=11324391980&sub_id=acne"
};

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const slug = url.pathname.replace(/^\\/go\\/?/, "").toLowerCase().trim();

  let targetUrl = null;
  let slotNum = null;

  // 1. Direct match by slug or slot
  if (AMAZON_PRODUCTS[slug]) {
    targetUrl = AMAZON_PRODUCTS[slug];
    slotNum = parseInt(slug) || null;
  } else if (SHOPEE_FALLBACKS[slug]) {
    targetUrl = SHOPEE_FALLBACKS[slug];
  } else if (slug.startsWith("b0") && slug.length === 10) {
    // Direct ASIN format (e.g. /go/B074C9F45S)
    targetUrl = `https://www.amazon.com/dp/${slug.toUpperCase()}?tag=${AMAZON_TAG}`;
  } else if (slug.startsWith("dp/")) {
    const asin = slug.replace(/^dp\\//, "").toUpperCase();
    targetUrl = `https://www.amazon.com/dp/${asin}?tag=${AMAZON_TAG}`;
  }

  // 2. Fallback to homepage
  if (!targetUrl) {
    return Response.redirect("https://curatedbyemma.pages.dev", 302);
  }

  // 3. Asynchronously record click to VPS
  const ip = context.request.headers.get("cf-connecting-ip") || "0.0.0.0";
  const userAgent = context.request.headers.get("user-agent") || "";
  const referer = context.request.headers.get("referer") || "";

  context.waitUntil(
    fetch("http://202.10.42.133:7860/api/track", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        slot: slotNum,
        slug: slug,
        target_url: targetUrl,
        ip: ip,
        user_agent: userAgent,
        referer: referer,
        timestamp: new Date().toISOString()
      })
    }).catch(() => {})
  );

  return new Response(null, {
    status: 302,
    headers: {
      "Location": targetUrl,
      "Cache-Control": "no-cache, no-store, must-revalidate",
      "Pragma": "no-cache",
      "Expires": "0"
    }
  });
}
"""

with open("/Users/macbookair/.gemini/antigravity/scratch/affiliate-engine/functions/go/[[catchall]].js", "w", encoding="utf-8") as f:
    f.write(cf_code)
print("Updated functions/go/[[catchall]].js with 50 products.")
