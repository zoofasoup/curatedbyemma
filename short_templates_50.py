import json

SHORT_TEMPLATES_50 = {
    1: [
        "woven couches hold onto pet hair like velcro. that extra-sticky pet roller (curatedbyemma.pages.dev/go/roller) has like 39k reviews for pulling embedded undercoat. what breed do you have?",
        "regular lint rollers run out in two swipes on dog fur. that extra-sticky 5-pack (curatedbyemma.pages.dev/go/roller) actually grabs what vacuums miss. what kind of couch fabric is it?"
    ],
    2: [
        "honestly sounds like a classic 4am night terror. that breathing otter plush (curatedbyemma.pages.dev/go/otter) has like 60k reviews for calming those meltdowns. does he have a night light?",
        "running on two hours of sleep with a crying baby is survival mode. that rhythmic breathing otter (curatedbyemma.pages.dev/go/otter) helped 60k parents get sleep stretches. how many months?"
    ],
    3: [
        "standard desk chairs wreck your lower spine by 3pm. that memory foam lumbar cushion (curatedbyemma.pages.dev/go/lumbar) has 27k reviews for tailbone relief. what chair are you using right now?",
        "sitting 8 hours without lower lumbar support causes insane back aches. that molded foam cushion (curatedbyemma.pages.dev/go/lumbar) takes the tailbone pressure off. do you work from home?"
    ],
    4: [
        "pouring oil straight from bottles leaves air fryer food drenched and soggy. that glass oil mister (curatedbyemma.pages.dev/go/mister) with 49k reviews sprays a clean wide fan. what are you frying?",
        "aerosol cooking sprays leave sticky chemical gunk in air fryers. that refillable glass oil mister (curatedbyemma.pages.dev/go/mister) has 49k reviews for even crispy food. what oil do you use?"
    ],
    5: [
        "pilled sweaters look completely ruined after two washes. that electric fabric defuzzer (curatedbyemma.pages.dev/go/defuzzer) with 116k reviews shaves them smooth in 2 mins. is it wool or fleece?",
        "throwing out nice knitwear just from surface bobbles hurts. that handheld fabric shaver (curatedbyemma.pages.dev/go/defuzzer) has 116k reviews and restores sweaters in seconds. what kind of knit?"
    ],
    6: [
        "cables constantly sliding off nightstands behind the bed is so annoying. that magnetic cord organizer (curatedbyemma.pages.dev/go/cables) has 18k reviews and keeps them anchored. how many cords?",
        "fishing charging cords out from behind the bed every night gets old fast. that weighted magnetic cable base (curatedbyemma.pages.dev/go/cables) keeps cords locked in place. is this for a nightstand?"
    ],
    7: [
        "holding your phone for 4 hours on a flight destroys your neck. that airplane seatback clamp (curatedbyemma.pages.dev/go/flight-mount) has 22k reviews and clips right at eye level. where to?",
        "looking down at a phone on airplane tray tables causes brutal neck cramps. that tray clamp mount (curatedbyemma.pages.dev/go/flight-mount) holds screens right at eye level. how long is your flight?"
    ],
    8: [
        "hotel irons always spit rusty brown water and scorch nice shirts. that handheld travel steamer (curatedbyemma.pages.dev/go/steamer) has 30k reviews and heats up in 60s. are you packing linen?",
        "unpacking completely crumpled shirts on a trip is a headache. that compact travel steamer (curatedbyemma.pages.dev/go/steamer) has 30k reviews and knocks out wrinkles fast. heading out for vacation?"
    ],
    9: [
        "side sleeping with regular earbuds digs straight into your ear cartilage. that bluetooth sleep mask (curatedbyemma.pages.dev/go/sleep-mask) has flat thin speakers and 13k reviews. do you side sleep?",
        "trying to sleep with bulky earbuds poking your ears is painful. that 3D contoured sleep mask (curatedbyemma.pages.dev/go/sleep-mask) has ultra-thin built-in speakers. what do you listen to to sleep?"
    ],
    10: [
        "guessing meat doneness always ends in dry chicken or raw center. that instant-read meat thermometer (curatedbyemma.pages.dev/go/thermometer) with 150k reviews reads temps in 3s. are you grilling?",
        "cutting steaks open in the pan lets all the juices leak out. that digital instant meat thermometer (curatedbyemma.pages.dev/go/thermometer) has 150k reviews and gives exact temps. what are you cooking?"
    ],
    11: [
        "snaking disgusting hair clogs out of shower drains is the worst chore. that silicone tubshroom (curatedbyemma.pages.dev/go/tubshroom) with 112k reviews catches hair before pipes. standard drain?",
        "drain clearing chemicals eat away at plumbing over time. that cylinder tubshroom (curatedbyemma.pages.dev/go/tubshroom) has 112k reviews and catches all hair without standing water. is it for a tub?"
    ],
    12: [
        "scrubbing burnt grease off pans until your arms ache is exhausting. the pink stuff paste (curatedbyemma.pages.dev/go/pink-stuff) with 165k reviews cuts burnt carbon with zero bleach fumes. what pan?",
        "water mineral spots and baked grease on ceramic seem impossible to lift. that pink stuff paste (curatedbyemma.pages.dev/go/pink-stuff) has 165k reviews for erasing grime. what are you cleaning?"
    ],
    13: [
        "sticky tape lint rollers run out way too fast on hairy couches. the reusable chomchom roller (curatedbyemma.pages.dev/go/chomchom) has 150k reviews and lifts fur with zero refills. dog or cat?",
        "vacuum attachments just drag pet hair across velvet couches. that chomchom roller (curatedbyemma.pages.dev/go/chomchom) with 150k reviews squeegees deep undercoat fur straight into the trap. cat fur?"
    ],
    14: [
        "scrubbing crusted spaghetti sauce splatters inside microwaves is miserable. that angry mama steam cleaner (curatedbyemma.pages.dev/go/angry-mama) with 62k reviews softens it in 7 mins with vinegar. messy?"
    ],
    15: [
        "pet stains soaked into rugs always leave dark water rings behind. the bissell little green (curatedbyemma.pages.dev/go/little-green) with 88k reviews suctions mud and vomit right out. rug or sofa?"
    ],
    16: [
        "spilling coffee or wine on a brand new light fabric couch is terrifying. that fabric shield spray (curatedbyemma.pages.dev/go/fabric-shield) with 26k reviews makes liquids bead right off. new couch?"
    ],
    17: [
        "cold draft air blowing under doors runs up winter electric bills fast. that under-door draft stopper (curatedbyemma.pages.dev/go/draft-stopper) with 31k reviews blocks drafts and hall noise. front door?"
    ],
    18: [
        "crumbs and cooking oil dripping into the narrow gap between stove and counter is impossible to clean. silicone stove gap covers (curatedbyemma.pages.dev/go/stove-gap) with 46k reviews seal it. gap width?"
    ],
    19: [
        "slimy dish soap bottles pooling soggy scum next to kitchen sinks look chaotic. that spring-loaded ceramic soap dispenser (curatedbyemma.pages.dev/go/dish-brush) with 16k reviews foams on contact. sink tidy?"
    ],
    20: [
        "banging stubborn pickle jars against kitchen counters or hurting wrists is dangerous. that steel-tooth jar opener (curatedbyemma.pages.dev/go/jar-opener) with 26k reviews pops vacuum seals instantly. jars?"
    ],
    21: [
        "yellow mineral calcium rings in toilet bowls that bleach cant remove look terrible. that natural pumice stick (curatedbyemma.pages.dev/go/pumice-stick) with 42k reviews rubs hard water crust off. hard water?"
    ],
    22: [
        "cloudy scorched oil stains make high-end stainless cookware look ruined. bar keepers friend (curatedbyemma.pages.dev/go/bar-keepers) with 36k reviews brings pans back to a mirror shine. stainless steel?"
    ],
    23: [
        "crawling behind sofas to unplug floor lamps or space heaters is unnecessary work. that mini kasa smart plug (curatedbyemma.pages.dev/go/smart-plug) with 125k reviews schedules timers from phones. lamps?"
    ],
    24: [
        "dropping heavy phones on your face while scrolling in bed hurts so bad. that magnetic magsafe ring (curatedbyemma.pages.dev/go/magsafe-ring) with 32k reviews snaps on as a secure finger grip. iphone?"
    ],
    25: [
        "tinny looping sound machines rarely drown out loud neighbor footsteps. the dohm classic sound machine (curatedbyemma.pages.dev/go/dohm) with 46k reviews uses a real rushing air fan to mask noise. footsteps?"
    ],
    26: [
        "dry pressurized cabin air leaves your throat parched and head throbbing after flights. liquid i.v. packets (curatedbyemma.pages.dev/go/hydration) with 135k reviews hydrate 2x faster than water. long flight?"
    ],
    27: [
        "foam earplugs constantly expanding and putting painful pressure on ear canals ruins sleep. loop quiet silicone plugs (curatedbyemma.pages.dev/go/loop-quiet) with 68k reviews sit flush for side sleeping. snorer?"
    ],
    28: [
        "waking up with frizzy tangled bedhead and deep sleep creases on your skin is frustrating. that satin pillowcase (curatedbyemma.pages.dev/go/satin-pillow) with 285k reviews stops hair friction. curly hair?"
    ],
    29: [
        "rotten food odors wafting up from kitchen sink disposal drains are nauseating. that foaming disposal cleaner (curatedbyemma.pages.dev/go/disposal-cleaner) with 47k reviews scrubs hidden grime. sink smell?"
    ],
    30: [
        "leaving greasy sheet pans soaking in the sink for 24 hours just clutters counters. dawn powerwash spray (curatedbyemma.pages.dev/go/powerwash) with 62k reviews dissolves baked grease instantly. dishes?"
    ],
    31: [
        "drinking protein shakes or matcha with chalky dry clumps floating on top is unappetizing. that handheld milk frother (curatedbyemma.pages.dev/go/frother) with 115k reviews blends powders in 15s flat. coffee?"
    ],
    32: [
        "chopping 4 whole onions while crying your eyes out over a cutting board is miserable. that vegetable chopper (curatedbyemma.pages.dev/go/veggie-chopper) with 98k reviews dices onions in 1 snap. meal prep?"
    ],
    33: [
        "boiled eggs with green sulfur rings and shells that refuse to peel cleanly ruin breakfast. that rapid egg cooker (curatedbyemma.pages.dev/go/egg-cooker) with 118k reviews steams eggs that peel effortlessly. eggs?"
    ],
    34: [
        "sitting on overstuffed suitcases trying to force the zipper closed is pure panic. compression packing cubes (curatedbyemma.pages.dev/go/packing-cubes) with 47k reviews squeeze luggage volume by 40%. packing?"
    ],
    35: [
        "getting hit with a $75 overweight baggage fee at airport check-in counters ruins trips. that digital luggage scale (curatedbyemma.pages.dev/go/luggage-scale) with 68k reviews weighs bags accurately at home. flying?"
    ],
    36: [
        "tangled extension cords and garden hoses creating messy piles in closets is chaotic. reusable rubber gear ties (curatedbyemma.pages.dev/go/gear-tie) with 22k reviews twist tight and hold cords neat. cords?"
    ],
    37: [
        "crawling on knees with a flashlight trying to find extra cleaning sprays under the sink is a pain. that 2-tier slide organizer (curatedbyemma.pages.dev/go/sink-organizer) with 26k reviews rolls right out. kitchen?"
    ],
    38: [
        "fitted bed sheets that pop off mattress corners in the middle of the night are infuriating. deep pocket microfiber sheets (curatedbyemma.pages.dev/go/bed-sheets) with 345k reviews stay locked tight. deep bed?"
    ],
    39: [
        "scrubbing tile grout lines around bathtubs with toothbrushes destroys your knuckles. that battery power scrubber (curatedbyemma.pages.dev/go/power-scrubber) with 37k reviews scrubs 60x/sec. bathroom grout?"
    ],
    40: [
        "fuzzy pills all over knit sweaters make nice clothing look cheap and worn. that conair compact fabric shaver (curatedbyemma.pages.dev/go/conair-shaver) with 112k reviews depills cardigans smoothly. wool coat?"
    ],
    41: [
        "popping angry red whitehead pimples leaves scabs and dark acne scars for weeks. hero mighty hydrocolloid patches (curatedbyemma.pages.dev/go/pimple-patch) with 148k reviews flatten bumps overnight. breakout?"
    ],
    42: [
        "painfully cracked dry winter lips and raw skin patches sting every time you smile. aquaphor healing ointment (curatedbyemma.pages.dev/go/aquaphor) with 88k reviews seals moisture and heals in 24h. chapped lips?"
    ],
    43: [
        "working outside in the cold until fingertips crack open and bleed around cuticles hurts so bad. o'keeffe's working hands (curatedbyemma.pages.dev/go/working-hands) with 78k reviews heals splits in 48h. dry hands?"
    ],
    44: [
        "scrubbing cloudy soap scum off glass shower doors with harsh fumes is a miserable chore. wet & forget shower spray (curatedbyemma.pages.dev/go/shower-spray) with 26k reviews dissolves scum with zero scrubbing. glass?"
    ],
    45: [
        "drilling hammer holes in rental apartment drywall risks losing security deposits. command picture hanging strips (curatedbyemma.pages.dev/go/command-strips) with 58k reviews lock frames flush without nails. rental?"
    ],
    46: [
        "having delicate glass french coffee presses shatter in the kitchen sink is dangerous. that stainless double-wall press (curatedbyemma.pages.dev/go/french-press) with 32k reviews is drop-proof and stays hot 1hr. roast?"
    ],
    47: [
        "waking up with dry scratchy throats and static shocks from winter apartment heating is frustrating. that digital room hygrometer (curatedbyemma.pages.dev/go/hygrometer) with 88k reviews tracks air humidity. dry air?"
    ],
    48: [
        "feeling heat sear through thin cloth pot holders when pulling heavy cast iron from ovens is scary. gorilla grip silicone mitts (curatedbyemma.pages.dev/go/oven-mitts) with 32k reviews are waterproof to 484°F. cast iron?"
    ],
    49: [
        "economy airline seats with no legroom leave your lower spine aching and ankles swollen. that airplane footrest hammock (curatedbyemma.pages.dev/go/airplane-footrest) with 16k reviews cradles feet elevated. long red-eye?"
    ],
    50: [
        "pulling freshly washed shirts out of the dryer only to find dog fur still baked into the fabric is so annoying. furzapper silicone paws (curatedbyemma.pages.dev/go/furzapper) with 26k reviews pull hair in wash. pet fur?"
    ]
}

print(f"Loaded {len(SHORT_TEMPLATES_50)} short human templates!")
lengths = [len(t[0]) for t in SHORT_TEMPLATES_50.values()]
print(f"Length range: {min(lengths)} to {max(lengths)} characters!")
print(f"Average length: {sum(lengths)/len(lengths):.1f} characters!")
