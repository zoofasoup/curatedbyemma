import json

with open("master_catalog.json") as f:
    items = json.load(f)

for p in items:
    s = p['slot_number']
    cat = p['category']
    title = p['title']
    price = p['price']
    rating = p['rating']
    reviews = p['reviews_count']
    vel = p['bought_past_month']
    pain = p['target_pain_point']
    print(f"Slot #{s}: [{cat}]")
    print(f"  Product: {title}")
    print(f"  Price: ${price:.2f} | Rating: {rating}★ ({reviews:,} reviews) | Velocity: {vel}")
    print(f"  Pain Solved: {pain}\n")
