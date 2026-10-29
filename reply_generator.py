"""
Contextual Reply Generator for Emma (@curated_byemma).
Uses Gemini API or local heuristic evaluator to:
1. Hard-filter context: Reject memorial/family stories, jokes, sports, news, and non-complaints.
2. Generate authentic, contextual replies following the 4-Part Honest Arc (Never Lie, Honest Caveat, Bio Anchor).
"""

import os
import sys
import json
import re

# Master product specs for authentic citation (NEVER LIE)
CATALOG_SPECS = {
    3: {
        "name": "Ergonomic Memory Foam Lumbar Cushion",
        "category": "Desk setup",
        "rating": 4.4,
        "reviews": 27400,
        "price_tier": "$30 - $35",
        "honest_pros": "High-density molded foam that actually holds shape under full bodyweight",
        "honest_caveats": "Feels noticeably firm the first 2-3 days before conforming to your lower back, doesn't fix serious medical sciatica",
        "target_problem": "Lower back pain, tailbone pressure, or poor posture from standard/cheap office chairs",
        "bio_slot": "#3"
    },
    1: {
        "name": "PetLovers Extra-Sticky Lint Roller (5 pack)",
        "category": "Pet hair",
        "rating": 4.6,
        "reviews": 39300,
        "price_tier": "$14 - $18",
        "honest_pros": "Adhesive is sticky enough to pull embedded undercoat fur from velvet and textured woven sofas",
        "honest_caveats": "You burn through sheets quickly if you have a massive double-coated dog, peeling diagonal sheets takes a second to get used to",
        "target_problem": "Dog/cat shedding embedded into couch fabric, velvet furniture, or car seats",
        "bio_slot": "#1"
    },
    7: {
        "name": "Perilogics Airplane Tray-Table Phone Mount",
        "category": "Travel / Flights",
        "rating": 4.6,
        "reviews": 22900,
        "price_tier": "$20 - $22",
        "honest_pros": "Sturdy clamp mounts directly to folded or down airplane tray table, holds phone eye level for 4+ hour flights",
        "honest_caveats": "Spring clamp is quite stiff out of the box, not needed if the plane already has built-in seatback screens",
        "target_problem": "Severe neck strain from looking down or holding a phone for hours during flights",
        "bio_slot": "#7"
    }
}

EVALUATION_PROMPT = """
You are an expert content moderator and social media strategist for an authentic consumer researcher named Emma (@curated_byemma).

Your job is to evaluate if a Threads post is a GENUINE FIRST-PERSON COMPLAINT where a practical product recommendation would be helpful and socially appropriate.

CRITICAL REJECTION RULES (Return REJECT immediately if ANY of these match):
- Memorial, funeral, family nostalgia, grandparents, grief, or emotional personal milestones.
- Sports news, baseball/football, athletes, match reports.
- Jokes, satire, memes, or casual metaphors (e.g. someone calling a friend a dog).
- Commercial brands, ads, affiliate marketers, or sponsored posts.
- Medical emergencies, severe diagnosed disease, hospital visits, surgery.
- Posts that are NOT in English or where the poster is not personally experiencing the problem.

ACCEPTANCE CRITERIA:
- The person is actively venting/struggling with:
  * Slot 3: Sore lower back/bad posture from sitting in an office or desk chair.
  * Slot 1: Extreme pet hair / cat / dog fur stuck on couch, sofa, or car seats.
  * Slot 7: Severe neck cramp or fatigue from holding their phone during a flight/travel.

Return JSON format:
{
  "verdict": "ACCEPT" or "REJECT",
  "slot": 1 or 3 or 7 or null,
  "rejection_reason": "explanation if rejected",
  "reply_draft": "Your contextual 4-part reply if ACCEPTED, otherwise empty"
}

IF ACCEPTED, write a 100% contextual, authentic reply following Emma's 4-Part Arc:
1. Direct empathy acknowledging their exact specific detail (not a generic template).
2. Honest audit: Cite the verified Amazon review count and specs. Never claim she invented it or has owned it for 10 years.
3. Honest caveat: State the realistic limitation/con.
4. Non-promotional anchor: Point to bio #[slot] on her page. No URLs. Lowercase casual style, zero hype buzzwords.
"""

def evaluate_and_draft_local(post_text, author="user"):
    """
    Robust rule-based evaluator with strict context gating.
    Acts as safety fallback and local intelligence engine.
    """
    text_lower = post_text.lower()

    # 1. HARD REJECT LIST (Immediate veto)
    memorial_words = ["passed away", "died", "funeral", "grave", "rip", "grandfather", "grandmother", "lolo", "lola", "ancestor", "memory of", "childhood", "growing up", "undas", "toddler", "heaven", "miss him", "miss her"]
    sports_words = ["pitcher", "innings", "game 2", "game 3", "mlb", "nba", "nfl", "touchdown", "strikeout", "mariners", "dodgers", "yankees", "stray kids", "concert", "kpop", "barricade", "tour"]
    marketing_words = ["giveaway", "discount code", "link in bio", "dm for link", "shop now", "article:", "read more:", "tinyurl", "bit.ly", "check out my"]

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

    # Slot 3: Desk Back Pain (Must have BOTH chair/sitting context AND physical back pain)
    has_chair = any(w in text_lower for w in ["office chair", "desk chair", "sitting all day", "sitting at my desk", "wfh chair", "work chair", "computer chair"])
    has_back_pain = any(w in text_lower for w in ["back hurting", "back pain", "lower back", "spine hurting", "back is killing me", "back aches", "posture is terrible", "lumbar"])
    if has_chair and has_back_pain:
        matched_slot = 3

    # Slot 1: Pet Hair on Furniture (Must have BOTH pet/fur AND furniture/couch)
    has_pet = any(w in text_lower for w in ["dog hair", "cat hair", "golden retriever fur", "shedding so much", "pet fur everywhere", "cat shedding", "dog shedding"])
    has_furniture = any(w in text_lower for w in ["couch", "sofa", "cushion", "velvet", "car seat", "rug", "blanket", "vacuuming"])
    if has_pet and has_furniture:
        matched_slot = 1

    # Slot 7: Airplane / Flight Neck Pain (Must have flight context AND phone holding / neck strain)
    has_flight = any(w in text_lower for w in ["flight", "flying", "airplane", "plane ride", "tray table", "seatback"])
    has_phone_neck = any(w in text_lower for w in ["holding my phone", "holding phone", "neck strain", "neck cramp", "neck hurts", "watching movies on my phone"])
    if has_flight and has_phone_neck:
        matched_slot = 7

    if not matched_slot:
        return {"verdict": "REJECT", "reason": "No clear first-person physical pain point matched"}

    # 3. DRAFT CONTEXTUAL 4-PART REPLY
    spec = CATALOG_SPECS[matched_slot]
    
    if matched_slot == 3:
        draft = (
            f"sitting in standard desk chairs all day literally destroys your lower back posture. "
            f"when i audited cushions to filter out sponsored hype, high-density molded foam was the only thing 27k verified buyers with chronic desk fatigue consistently swore by. "
            f"it won't cure medical spine issues and feels pretty firm the first couple days, but taking pressure off the tailbone made 8-hour workdays actually bearable. "
            f"cataloged the exact ergonomic one under #3 on my page."
        )
    elif matched_slot == 1:
        draft = (
            f"trying to get stubborn pet hair off couch fabric is the most frustrating workout ever. "
            f"regular sticky tape rollers lose their grip in two swipes, but that extra-sticky roller with over 39k verified reviews is the consensus winner for deep fur. "
            f"only catch is you go through sheets fast with a heavy shedder, but it actually pulls what vacuums miss. "
            f"kept it saved under #1 in my bio."
        )
    elif matched_slot == 7:
        draft = (
            f"holding your phone looking down for hours on a flight is literal neck torture. "
            f"instead of overpriced airport gadgets, that clamp mount that locks directly onto the seatback tray table had 22k+ verified reviews for a reason—hands-free screen right at eye level. "
            f"the spring clamp is a bit stiff to open at first, but completely saves your neck on long flights. "
            f"listed under #7 on my profile list."
        )

    return {
        "verdict": "ACCEPT",
        "slot": matched_slot,
        "product_name": spec["name"],
        "reply_draft": draft
    }

if __name__ == "__main__":
    test_snappy = "While scrolling through my phone this week, I came across a quiet and raw entry I had written... about my maternal grandfather... he surprised me with a bankito (small wooden chair)..."
    res1 = evaluate_and_draft_local(test_snappy)
    print("Test Memorial Story:", res1)

    test_real_pain = "Sitting in this cheap office chair 9 hours a day is destroying my lower back. My spine is in so much pain by 3 PM."
    res2 = evaluate_and_draft_local(test_real_pain)
    print("Test Real Office Pain:", res2)
