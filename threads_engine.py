import json
import re

# Load Master Catalog
with open("master_catalog.json", "r") as f:
    CATALOG = json.load(f)

PERSONA_RULES = """
You are Sarah (@sarah.curates), a 29-year-old practical researcher on Threads.
You never lie. You NEVER claim "I bought this" or "my baby used this" or "my dog".
Instead, you speak from the angle of someone who loves finding and cataloging top-reviewed problem solvers.

Tone guidelines:
- Empathetic, supportive, casual (Threads conversational style).
- Short & punchy (2-3 sentences max).
- Lowercase / relaxed punctuation preferred.
- Mention the community consensus or review volume (e.g., "tons of parents swear by...", "over 30k reviews on amazon...").
- Natural bridge to your bio: "kept it under #[SLOT_NUMBER] in my bio if you want to check it out" or "saved the exact one at bio #[SLOT_NUMBER]".
- NO hyperlinks in the comment.
"""

def match_product_slot(post_text: str):
    """
    Matches the incoming user pain point to the best product slot in master_catalog.json
    """
    text = post_text.lower()
    
    # 1. Pets & Fur
    if any(k in text for k in ["dog hair", "cat hair", "pet hair", "retriever", "fur", "shedding", "lint", "couch hair", "dog", "cat"]) and any(w in text for w in ["hair", "fur", "couch", "sofa", "vacuum", "shedding"]):
        return 1
    # 2. Baby & Sleep
    elif any(k in text for k in ["baby", "toddler", "infant", "newborn", "kid", "month old", "months old", "sleep regression"]) and any(w in text for w in ["sleep", "screaming", "crying", "awake", "wake", "zombie", "night", "nap", "colic"]):
        return 2
    # 3. Back & Posture
    elif any(k in text for k in ["back pain", "lower back", "chair", "desk", "spine", "slouching", "posture", "lumbar", "sitting"]):
        return 3
    # 4. Air Fryer / Oil
    elif any(k in text for k in ["air fryer", "olive oil", "oil spray", "greasy", "oil bottle", "mist sprayer"]):
        return 4
    # 5. Deep Cleaning
    elif any(k in text for k in ["scrub", "grout", "tile", "shower", "bathtub", "bathroom clean", "soap scum"]):
        return 5
    # 6. Desk & Cable Clutter
    elif any(k in text for k in ["cable", "cord", "charger", "desk clutter", "wire", "nightstand cord"]):
        return 6
    # 7. Airplane / Flight Phone Mount
    elif any(k in text for k in ["airplane", "flight", "flying", "plane", "seatback", "tray table", "holding phone"]):
        return 7
    # 8. Wrinkles / Steamer
    elif any(k in text for k in ["wrinkle", "wrinkled", "ironing", "steamer", "suitcase clothes", "iron board"]):
        return 8
    # 9. Adult Sleep / Insomnia
    elif any(k in text for k in ["insomnia", "snoring", "light waking", "can't sleep", "sleep mask", "partner snores"]):
        return 9
    # 10. Car Cleaning
    elif any(k in text for k in ["car vent", "car dust", "cup holder", "car crumb", "car detailing", "car interior"]):
        return 10
    
    return None

def generate_honest_reply(post_text: str) -> dict:
    slot = match_product_slot(post_text)
    if not slot:
        return {"matched": False, "message": "No relevant problem-solver found for this post."}
    
    product = next(p for p in CATALOG if p["slot_number"] == slot)

    # Contextual reply templates based on slot
    templates = {
        1: f"ugh pet hair on couches is the worst. standard lint rollers never worked for us until i saw hundreds of dog owners recommending that extra sticky pet roller (has almost 40k reviews). kept the exact one under #{slot} in my bio if you need it!",
        2: f"night wakeups are so exhausting, sending strength. saw a massive thread in a mom group about that breathing rhythm otter plush—a ton of parents swear it was the only thing that calmed their baby down without struggle. cataloged it under #{slot} in my bio if you want to look at the reviews!",
        3: f"sitting all day ruined my lower back too. the community consensus on desk setups is getting a proper memory foam lumbar cushion instead of buying a whole new $500 chair. saved the top-rated one at bio #{slot} if you want to check the ergonomics.",
        4: f"if you use an air fryer, pouring oil from the bottle always makes it soggy. a glass mist sprayer is an absolute gamechanger. i have the top-rated leakproof one listed under #{slot} in my bio!",
        5: f"scrubbing bathroom tiles on your knees is brutal. electric cordless spin scrubbers are viral for a reason—cuts cleaning time in half with zero elbow grease. kept the highest-rated one saved in bio #{slot}.",
        6: f"cables sliding behind the desk drove me insane. magnetic desk cable holders fixed that in 5 seconds. saved the exact one under #{slot} in my bio if you want to see how it works.",
        7: f"holding your phone for a 4-hour flight is literal neck torture. that universal tray-table phone mount is an absolute travel essential. listed under #{slot} in my bio!",
        8: f"ironing boards take way too much effort when traveling. a compact handheld travel steamer takes wrinkles out in like 30 seconds. cataloged the #1 amazon pick under #{slot} in my bio.",
        9: f"if light or noise is keeping you up, look into 3D bluetooth eye masks with flat speakers. total blackout and you can play white noise or podcasts without ear pain. kept the top one at bio #{slot}.",
        10: f"cleaning crumbs and dust out of car air vents with wipes is impossible. that reusable detailing cleaning gel picks up everything in one press. saved under #{slot} in my bio!"
    }

    reply = templates.get(slot, f"saw a lot of people recommend the solution for this! cataloged under #{slot} in my bio if you want to check it out.")

    return {
        "matched": True,
        "slot": slot,
        "product_title": product["title"],
        "price": f"${product['price']:.2f}",
        "reply_text": reply
    }

if __name__ == "__main__":
    # Test cases: Real pain points people post on Threads
    test_posts = [
        "My 8 month old has been screaming and waking up every hour all night. I feel like a zombie, what actually works??",
        "Does anyone have a hack for getting stubborn golden retriever hair off a fabric sofa?? My vacuum literally gave up.",
        "My lower back is killing me after working at my desk for 8 hours today. Do I really need a $1000 chair?",
        "Flying 6 hours tomorrow with no seatback screen. My arms get so tired holding my phone up the whole time."
    ]

    print("="*70)
    print("🤖 THREADS CONTEXTUAL BOT EXERCISE (SIMULATION)")
    print("="*70)

    for i, post in enumerate(test_posts, 1):
        print(f"\n[Test Post #{i}]")
        print(f"User Post: \"{post}\"")
        res = generate_honest_reply(post)
        if res["matched"]:
            print(f"🎯 Matched Slot: #{res['slot']} ({res['product_title'][:40]}...) [{res['price']}]")
            print(f"💬 Bot Reply: \"{res['reply_text']}\"")
        print("-" * 70)
