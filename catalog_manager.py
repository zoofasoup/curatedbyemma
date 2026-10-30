"""
Catalog Manager for CuratedByEmma.
Handles swapping products in Slots #1–#10 across:
1. master_catalog.json
2. public/index.html (Bio Lander)
3. reply_generator.py (LLM Evaluation Specs)
"""

import os
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(BASE_DIR, "master_catalog.json")
LANDER_PATH = os.path.join(BASE_DIR, "public", "index.html")

def get_catalog():
    if not os.path.exists(CATALOG_PATH):
        return []
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def update_slot_product(slot: int, product_data: dict) -> bool:
    """
    Updates a product slot across master_catalog.json and public/index.html.
    """
    catalog = get_catalog()
    found = False
    for i, item in enumerate(catalog):
        if item.get("slot_number") == slot:
            # Merge updates
            item.update(product_data)
            item["slot_number"] = slot
            found = True
            break

    if not found:
        product_data["slot_number"] = slot
        catalog.append(product_data)

    # Save master_catalog.json
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    # Update public/index.html CATALOG array
    if os.path.exists(LANDER_PATH):
        try:
            with open(LANDER_PATH, "r", encoding="utf-8") as f:
                lander_html = f.read()

            # Format catalog items for public/index.html
            formatted_items = []
            for it in sorted(catalog, key=lambda x: x.get("slot_number", 0)):
                s = it.get("slot_number")
                asin = it.get("asin", "")
                tag = "curatedbyem0f-20"
                formatted_items.append({
                    "slot": s,
                    "title": it.get("title", f"Product #{s}"),
                    "category": it.get("category", "Trending"),
                    "cat_tag": it.get("cat_tag", "HOME"),
                    "hook": it.get("target_pain_point", it.get("hook", "")),
                    "image": it.get("image_url", ""),
                    "velocity": it.get("bought_past_month", it.get("velocity", "10K+ bought last month")),
                    "rating": float(it.get("rating", 4.5)),
                    "reviews": int(it.get("reviews_count", it.get("reviews", 10000))),
                    "url": f"https://www.amazon.com/dp/{asin}?tag={tag}"
                })

            json_str = json.dumps(formatted_items, indent=4)
            # Replace const CATALOG = [...] in public/index.html
            pattern = r"const CATALOG = \[.*?\];"
            replacement = f"const CATALOG = {json_str};"
            new_html = re.sub(pattern, replacement, lander_html, flags=re.DOTALL)

            with open(LANDER_PATH, "w", encoding="utf-8") as f:
                f.write(new_html)
        except Exception as e:
            print(f"Error updating public/index.html: {e}")

    return True

if __name__ == "__main__":
    c = get_catalog()
    print("Catalog loaded, total slots:", len(c))
