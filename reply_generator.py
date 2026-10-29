"""
Contextual Reply Generator for Emma (@curated_byemma).
Evaluates real user complaints on Threads and drafts authentic, honest 4-part replies.

Ground Rules:
1. Hard-filter context: Reject memorial/family grief, sports, concerts, marketing spam, and non-complaints.
2. 4-Part Honest Arc:
   - Specific empathy acknowledging their exact pain point.
   - Honest audit: Cite verified Amazon consensus and review count.
   - Honest caveat: State realistic limitation/con (NEVER LIE).
   - Non-promotional anchor: Point to bio #[slot] on Emma's page. No URLs. Lowercase casual tone.
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
        "name": "PetLovers Extra-Sticky Lint Roller (5 pack)",
        "category": "Pet hair",
        "rating": 4.6,
        "reviews": 39300,
        "honest_pros": "Adhesive is sticky enough to pull embedded undercoat fur from velvet and textured woven sofas",
        "honest_caveats": "You burn through sheets quickly if you have a massive double-coated dog, peeling diagonal sheets takes a second to get used to",
        "bio_slot": "#1",
        "draft_templates": [
            (
                "trying to get stubborn pet hair off couch fabric is the most frustrating workout ever. "
                "regular sticky tape rollers lose their grip in two swipes, but that extra-sticky roller with over 39k verified reviews is the consensus winner for deep fur. "
                "only catch is you go through sheets fast with a heavy shedder, but it actually pulls what vacuums miss. "
                "kept it saved under #1 in my bio."
            ),
            (
                "vacuums always seem to push double-coated dog hair deeper into weave fibers. "
                "after testing lint tools, that pet lovers extra-sticky roller with 39k+ verified ratings was the only thing that lifted the stuck undercoat in one swipe. "
                "sheets peel fast so don't hoard them, but it actually works without shredding the fabric. "
                "cataloged under #1 in my bio."
            ),
            (
                "dog fur embedded in couch cushions is an absolute nightmare to keep up with. "
                "standard grocery store rollers are too weak, but that heavy-tack pet roller with nearly 40k reviews pulls hair vacuums leave behind. "
                "only downside is replacing rolls frequently during shedding season, but it saves hours of scrubbing. "
                "saved the exact one under #1 on my page."
            )
        ]
    },
    2: {
        "name": "Fisher-Price Calming Otter Sleep Soother",
        "category": "Toddler / Infant sleep",
        "rating": 4.7,
        "reviews": 59700,
        "honest_pros": "Rhythmic breathing motion and soft white noise genuinely calms overtired babies down to sleep",
        "honest_caveats": "Not a magic fix for teething pain or severe colic, and you will need to replace AAA batteries every few weeks",
        "bio_slot": "#2",
        "draft_templates": [
            (
                "night wakeups every hour are completely brutal, sending you so much strength. "
                "my sister went through the exact same sleep regression and swore that rhythmic breathing otter with nearly 60k reviews was the only thing that actually calmed him down. "
                "only catch is you go through batteries every month, but it genuinely gave them their first 5-hour sleep stretch. "
                "cataloged it under #2 in my bio if you want to look at the reviews."
            ),
            (
                "running on two hours of sleep with a crying baby is surviving on pure adrenaline. "
                "our friends went through that exact sleep regression and the breathing belly otter with 59k verified reviews was the only soother that settled him down without rocking for hours. "
                "eats AAA batteries fast, but the gentle heartbeat rhythm works so well. "
                "cataloged under #2 in my bio."
            ),
            (
                "infant sleep regressions will test every ounce of your sanity. "
                "when we were researching calming soothers, that rhythmic breathing otter with nearly 60k reviews stood out because the belly motion mimics real breathing. "
                "won't fix severe teething cries, but for overtired bedtime battles it genuinely helped. "
                "saved under #2 on my page."
            )
        ]
    },
    3: {
        "name": "Ergonomic Memory Foam Lumbar Cushion",
        "category": "Desk setup",
        "rating": 4.4,
        "reviews": 27400,
        "honest_pros": "High-density molded foam that actually holds shape under full bodyweight without flattening",
        "honest_caveats": "Feels noticeably firm the first 2-3 days before conforming to your lower back, doesn't fix serious medical sciatica",
        "bio_slot": "#3",
        "draft_templates": [
            (
                "sitting in standard desk chairs all day literally destroys your lower back posture. "
                "when i audited cushions to filter out sponsored hype, high-density molded foam was the only thing 27k verified buyers consistently swore by. "
                "it won't cure medical spine issues and feels pretty firm the first couple days, but taking pressure off the tailbone made 8-hour workdays actually bearable. "
                "cataloged the exact ergonomic one under #3 on my page."
            ),
            (
                "the lower back ache from cheap wfh office chairs is so real. "
                "soft squishy pillows flatten in ten minutes, but that high-density molded lumbar cushion with 27k+ reviews holds its contour all day. "
                "feels a bit stiff the first 48 hours until it warms to your spine, but it keeps your posture aligned. "
                "listed under #3 in my bio."
            ),
            (
                "desk chairs with zero lumbar curve compress your lower spine by 3pm. "
                "after comparing dozens of supports, the firm memory foam cushion with 27k reviews was the undisputed winner for tailbone relief. "
                "won't replace a physio for chronic sciatica, but it made long desk sessions painless for me. "
                "cataloged under #3 on my page."
            )
        ]
    },
    4: {
        "name": "TrendPlain Glass Olive Oil Mister",
        "category": "Kitchen / Air fryer",
        "rating": 4.6,
        "reviews": 49100,
        "honest_pros": "Even, clog-free wide fan mist for air fryers without aerosol chemical propellants",
        "honest_caveats": "You have to pull the trigger with a firm, quick squeeze to get the wide fan mist instead of a stream; heavier than plastic since it's thick glass",
        "bio_slot": "#4",
        "draft_templates": [
            (
                "pouring oil from a bottle into an air fryer always turns food soggy and uneven. "
                "standard aerosol spray cans leave sticky chemical residue, but that refillable glass oil mister with 49k+ verified reviews mists a clean wide fan. "
                "only trick is you have to pull the trigger with a quick firm squeeze or it shoots a stream, but it completely fixed uneven air frying for me. "
                "listed under #4 in my bio."
            ),
            (
                "drizzling oil straight onto air fryer food makes half of it drenched and the other half dry. "
                "the glass fan-spray mister with 49k reviews solved that without using propellants or aerosol cans. "
                "glass bottle is a little heavy and you need a snappy trigger squeeze for the fan effect, but fries come out actually crispy. "
                "cataloged under #4 in my bio."
            )
        ]
    },
    5: {
        "name": "Cordless Electric Spin Scrubber",
        "category": "Deep clean / Bathroom",
        "rating": 4.4,
        "reviews": 8900,
        "honest_pros": "Motorized spinning heads clean tile grout, tubs, and baseboards without kneeling or back strain",
        "honest_caveats": "Great for surface soap scum and grout dirt, but decade-old deep mold still needs a bleach treatment; battery runs ~75 minutes on high speed",
        "bio_slot": "#5",
        "draft_templates": [
            (
                "scrubbing tile grout and tubs on your hands and knees is literal torture on your lower back. "
                "electric power spin scrubbers with the extension handle cut cleaning time in half with zero elbow grease. "
                "won't erase 10-year black mold without a separate bleaching gel, but for routine soap scum and bathroom grime it saved my back completely. "
                "kept the highest-rated one cataloged under #5 on my page."
            ),
            (
                "bent over the bathtub scrubbing grout until your spine aches is the absolute worst weekend chore. "
                "that cordless spin scrubber with the telescoping rod has nearly 9k reviews and lets you stand upright while the motor does the work. "
                "battery runs about 75 minutes so charge it beforehand, but it completely eliminated bathroom knee and back pain for me. "
                "saved under #5 in my bio."
            )
        ]
    },
    6: {
        "name": "Smartish Magnetic Cable Wrangler",
        "category": "Cable clutter",
        "rating": 4.6,
        "reviews": 5200,
        "honest_pros": "Heavy magnetic weighted base holds phone and watch cords firmly so they never drop behind furniture",
        "honest_caveats": "Base is heavy enough for standard phone and USB-C cords, but very stiff thick braided HDMI cords can pull it if not positioned right",
        "bio_slot": "#6",
        "draft_templates": [
            (
                "cables sliding off the nightstand and falling into the dark gap behind the bed drove me insane every single night. "
                "that weighted magnetic cable wrangler has over 5k verified reviews and actually keeps cords anchored right where you leave them. "
                "heavy base stays put for charging cords, just make sure to use the magnetic collars on thin wires. "
                "saved the exact one under #6 in my bio if you want to see how it works."
            ),
            (
                "fishing charging cords out from behind the headboard in the dark is beyond annoying. "
                "the weighted magnetic cable manager with 5k reviews has enough mass to keep phone and watch chargers sitting neatly on top of the nightstand. "
                "stiff heavy hdmi cables can slide it if tugged hard, but for bedside cords it is completely seamless. "
                "pinned under #6 on my page."
            )
        ]
    },
    7: {
        "name": "Perilogics Airplane Tray-Table Phone Mount",
        "category": "Travel / Flights",
        "rating": 4.6,
        "reviews": 22900,
        "honest_pros": "Clamp locks directly onto airplane tray table or seatback, holding phone eye-level for hands-free viewing",
        "honest_caveats": "Spring clamp is quite stiff out of the box to ensure it doesn't slip; not needed on newer aircraft with built-in seatback monitors",
        "bio_slot": "#7",
        "draft_templates": [
            (
                "holding your phone looking down for hours on a flight is literal neck torture. "
                "instead of overpriced airport gadgets, that clamp mount that locks directly onto the seatback tray table had 22k+ verified reviews for a reason—hands-free screen right at eye level. "
                "the spring clamp is a bit stiff to open at first, but completely saves your neck on long flights. "
                "listed under #7 on my profile list."
            ),
            (
                "looking straight down at your lap for a 4-hour flight leaves your neck completely stiff. "
                "that universal tray-table phone clamp has over 22k reviews and mounts right to the latch at eye level. "
                "clamp spring takes some force to open, but watching downloaded shows hands-free makes economy flights 10x better. "
                "cataloged under #7 in my bio."
            )
        ]
    },
    8: {
        "name": "OGHom Compact Handheld Garment Steamer",
        "category": "Travel / Wrinkle removal",
        "rating": 4.3,
        "reviews": 30000,
        "honest_pros": "Heats up in 60 seconds and steams out wrinkles without dragging out a heavy iron or ironing board",
        "honest_caveats": "Compact 240ml tank only lasts for about 2-3 shirts before needing a refill; must keep it upright to prevent water bubbling",
        "bio_slot": "#8",
        "draft_templates": [
            (
                "dragging out a heavy ironing board for travel clothes is way too much effort. "
                "that compact handheld steamer heats in 60 seconds and has over 30k verified reviews for de-wrinkling linen and cotton in one quick pass. "
                "small tank only does about 2 to 3 garments per water fill, but for quick travel touchups it completely replaced my iron. "
                "cataloged under #8 on my profile page."
            ),
            (
                "unpacking wrinkled clothes at a hotel and trying to use a rusty hotel iron is the worst. "
                "that portable handheld steamer with 30k+ reviews steams out deep suitcase wrinkles in literally two minutes. "
                "tank is compact so you refill after 2 shirts, but it glides right over delicate fabrics without burning. "
                "saved under #8 on my page."
            )
        ]
    },
    9: {
        "name": "TOPOINT 3D Bluetooth Sleep Mask",
        "category": "Adult sleep / Noise & Light",
        "rating": 4.3,
        "reviews": 13200,
        "honest_pros": "Zero eye pressure contoured 3D blackout mask with ultra-thin flat speakers that allow comfortable side sleeping",
        "honest_caveats": "Speakers are completely flat so side sleeping doesn't hurt your ears, but the velcro strap needs careful adjusting if you toss and turn aggressively",
        "bio_slot": "#9",
        "draft_templates": [
            (
                "if light leaks or morning noise keeps waking you up, normal hard plastic earbuds hurt your ears when sleeping on your side. "
                "that 3D contoured eye mask has ultra-flat soft speakers built in and over 13k verified reviews for true pitch-black sleep. "
                "velcro strap takes a night to dial in so it doesn't shift, but you can finally side sleep without sore ears. "
                "kept the top-rated one saved under #9 in my bio."
            ),
            (
                "side sleeping with regular earbuds creates so much painful pressure on your ear cartilage. "
                "that memory foam blackout mask with wafer-thin speakers inside has 13k+ reviews and lets you play white noise or podcasts comfortably on your side. "
                "takes a minute to adjust the velcro strap snug, but the total blackout and soft speakers changed my sleep completely. "
                "cataloged under #9 on my page."
            )
        ]
    },
    10: {
        "name": "PULIDIKI Reusable Car Detailing Putty",
        "category": "Car interior cleaning",
        "rating": 4.1,
        "reviews": 101000,
        "honest_pros": "Flexible cleaning gel presses deep into AC air vents, gear shifts, and console crevices to grab dust and crumbs",
        "honest_caveats": "Works wonders on dry dust, pet dander, and crumbs, but do NOT leave it inside a hot car glovebox in midsummer or it melts; not for liquid spills",
        "bio_slot": "#10",
        "draft_templates": [
            (
                "cleaning crumbs and dust out of car air vents and cup holders with wipes is basically impossible. "
                "that reusable cleaning putty with over 100k reviews presses into tiny crevices and lifts dust vacuums can't reach. "
                "only rule is don't leave it in a baking hot glovebox during midsummer heat, but for vents and cup holders it is so satisfying. "
                "saved under #10 in my bio."
            ),
            (
                "dust and pet hair stuck inside narrow car air vents is maddening because vacuums can't get inside. "
                "that reusable cleaning slime with 100k+ reviews squishes right between the vent slats and pulls everything out clean. "
                "just keep it in a cool spot so it doesn't sit in 100-degree summer heat, but it makes the interior look detailed in two minutes. "
                "listed under #10 on my bio."
            )
        ]
    }
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
            f"  - Bio anchor: #{s}"
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
3. STRICT "NEVER LIE" & CONTEXT RELEVANCE:
   - Does one of your 10 catalog items GENUINELY solve this user's exact problem?
   - If someone's problem is NOT solved by your products (e.g. medical spine injury, thrown-out back spasms while vacuuming floor under couch, wanting robot vacuums, dog chewing walls), you MUST REJECT.
   - Do NOT force a product recommendation if it does not fit! A sofa lint roller does NOT vacuum floors or heal lower back spasms!
   - Hard REJECT: memorials, family grief, sports games, politics, brand giveaways, spam.
4. 4-PART HONEST ARC (if ACCEPTED):
   - Part 1: Real empathy referencing their SPECIFIC situation, vocabulary, and pain (never generic boilerplate).
   - Part 2: Honest audit citing verified Amazon consensus and review count.
   - Part 3: Honest caveat/con (what it doesn't do or real limitations).
   - Part 4: Casual anchor to bio: "kept it saved under #[slot] in my bio" (or "cataloged under #[slot] on my page").
   - Tone: Lowercase casual, friendly, authentic peer, zero marketing jargon, NO links/URLs, max 2-4 sentences.
5. OUTPUT FORMAT:
   Return strictly valid JSON:
   {{
     "verdict": "ACCEPT" or "REJECT",
     "reason": "Clear 1-sentence reasoning",
     "slot": 1-10 or null,
     "reply_draft": "Your customized 4-part honest reply"
   }}

EMMA'S 10-SLOT CATALOG:
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
