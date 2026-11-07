import re
from build_50_catalog import ITEMS_50

# 1. Format CATALOG_SPECS for reply_generator.py
specs_code = "CATALOG_SPECS = {\n"
for item in ITEMS_50:
    specs_code += f"    {item['slot']}: {{\n"
    specs_code += f"        \"name\": {repr(item['name'])},\n"
    specs_code += f"        \"category\": {repr(item['category'])},\n"
    specs_code += f"        \"rating\": {item['rating']},\n"
    specs_code += f"        \"reviews\": {item['reviews']},\n"
    specs_code += f"        \"honest_pros\": {repr(item['honest_pros'])},\n"
    specs_code += f"        \"honest_caveats\": {repr(item['honest_caveats'])},\n"
    specs_code += f"        \"slug\": {repr(item['slug'])},\n"
    specs_code += f"        \"bio_slot\": \"#{item['slot']}\",\n"
    specs_code += f"        \"draft_templates\": [\n"
    for t in item["templates"]:
        specs_code += f"            (\n                {repr(t)}\n            ),\n"
    specs_code += "        ]\n"
    specs_code += "    },\n"
specs_code += "}\n"

with open("/Users/macbookair/.gemini/antigravity/scratch/affiliate-engine/reply_generator.py", "r", encoding="utf-8") as f:
    rg_content = f.read()

# Replace CATALOG_SPECS block
pattern = r"CATALOG_SPECS = \{.*?\n\}\n"
new_rg_content = re.sub(pattern, specs_code, rg_content, flags=re.DOTALL)

# Update system instruction prompt from 10-slot to 50-slot
new_rg_content = new_rg_content.replace(
    'EMMA\'S 10-SLOT CATALOG:',
    'EMMA\'S 50-SLOT CURATED VIRAL CATALOG:'
).replace(
    '"slot": 1-10 or null',
    '"slot": 1-50 or null'
).replace(
    'Does one of your 10 catalog items GENUINELY solve this user\'s exact problem?',
    'Does one of your 50 catalog items GENUINELY solve this user\'s exact problem?'
)

with open("/Users/macbookair/.gemini/antigravity/scratch/affiliate-engine/reply_generator.py", "w", encoding="utf-8") as f:
    f.write(new_rg_content)

print("Updated reply_generator.py with all 50 catalog items!")

# 2. Update threads_sniffer.py with search queries for all categories
sniffer_queries = {
    1: ["dog hair couch", "cat fur sofa", "pet shedding couch"],
    2: ["baby wont sleep", "toddler sleep regression", "baby crying night"],
    3: ["desk chair back pain", "office chair lumbar", "wfh lower back"],
    4: ["air fryer oil", "air fryer soggy", "airfryer greasy"],
    5: ["sweater pilling", "fleece fuzz balls", "knit cardigan pill"],
    6: ["charging cables falling", "nightstand cords", "cables behind bed"],
    7: ["holding phone flight", "airplane tray mount", "plane neck cramp phone"],
    8: ["travel clothes wrinkled", "hotel iron ruined", "steamer travel clothes"],
    9: ["earbuds hurt side sleeping", "sleeping with earbuds", "sleep mask audio"],
    10: ["meat thermometer turkey", "undercooked chicken", "dry turkey roast"],
    11: ["shower drain hair clog", "hair clogging drain", "tub drain hair snake"],
    12: ["burnt pan bottom", "scorched skillet grease", "the pink stuff cleaning"],
    13: ["chomchom roller", "dog hair furniture", "cat fur couch removal"],
    14: ["microwave splatter", "microwave grease baked", "clean microwave crust"],
    15: ["carpet pet stain", "couch coffee spill", "bissell little green"],
    16: ["spilled wine couch", "couch fabric stain protection", "scotchgard furniture"],
    17: ["draft under door", "apartment hallway noise bedroom", "drafty door winter"],
    18: ["food between stove counter", "crumbs side of stove", "stove gap crack"],
    19: ["messy dish soap bottle", "dish brush sink clutter", "sink sponge smell"],
    20: ["cant open jar lid", "stuck pickle jar", "jar lid vacuum sealed"],
    21: ["hard water ring toilet", "toilet mineral stains", "pumice toilet cleaning"],
    22: ["burnt stainless steel pot", "bar keepers friend stainless", "heat stains cookware"],
    23: ["smart plug space heater", "turn off lamp bed", "smart plug timer"],
    24: ["dropped phone on face bed", "phone slip hand grip", "magsafe ring kickstand"],
    25: ["loud upstairs neighbors", "stomping neighbor ceiling", "white noise sleep machine"],
    26: ["dehydrated flight", "dry throat airplane", "liquid iv travel hydration"],
    27: ["snoring partner earplugs", "loop earplugs sleep", "side sleeping earplugs"],
    28: ["frizzy morning hair bedhead", "satin pillowcase curls", "sleep creases face"],
    29: ["garbage disposal smell", "kitchen sink sewer odor", "stinky disposal blades"],
    30: ["greasy baking sheet soak", "burnt cheese pan", "dawn powerwash spray"],
    31: ["clumpy protein powder", "milk frother wand", "lumpy matcha powder"],
    32: ["crying chopping onions", "onion fumes eyes", "chopping vegetables meal prep"],
    33: ["hard to peel boiled eggs", "boiled egg shell sticking", "rapid egg cooker"],
    34: ["overpacked suitcase", "carry on suitcase explosion", "compression packing cubes"],
    35: ["overweight baggage fee", "airline luggage scale", "baggage 50 lbs airport"],
    36: ["tangled appliance cords", "extension cord knot", "cord organizer drawer"],
    37: ["under sink clutter", "cabinet under sink dark", "pull out sink organizer"],
    38: ["fitted sheet popping off", "bed sheet corner slipping", "deep pocket sheets"],
    39: ["scrubbing grout toothbrush", "bathroom tile grout mildew", "power scrubber grout"],
    40: ["leggings pilling", "fuzz on wool coat", "fabric defuzzer pills"],
    41: ["whitehead popped scab", "pimple patch whitehead", "picking at acne face"],
    42: ["cracked winter lips", "bleeding knuckles winter", "dry hands aquaphor"],
    43: ["cracked dry fingertips", "working hands cream", "painful skin cracks fingers"],
    44: ["scrubbing shower glass", "soap scum shower walls", "daily shower cleaner spray"],
    45: ["hanging pictures apartment rental", "command strips frames", "drywall nail holes deposit"],
    46: ["glass french press broke", "shattered french press sink", "stainless steel french press"],
    47: ["apartment air dry winter", "static shock blankets", "room humidity monitor"],
    48: ["burned hands oven pad", "thin potholder burn", "silicone oven mitts skillet"],
    49: ["swollen feet long flight", "airplane economy leg ache", "airplane footrest hammock"],
    50: ["pet hair in laundry dryer", "dog fur on washed clothes", "furzapper laundry wash"]
}

queries_code = "SLOT_SEARCH_QUERIES = {\n"
for s, q_list in sniffer_queries.items():
    queries_code += f"    {s}: {repr(q_list)},\n"
queries_code += "}\n"

with open("/Users/macbookair/.gemini/antigravity/scratch/affiliate-engine/threads_sniffer.py", "r", encoding="utf-8") as f:
    sn_content = f.read()

pattern_sn = r"SLOT_SEARCH_QUERIES = \{.*?\n\}\n"
new_sn_content = re.sub(pattern_sn, queries_code, sn_content, flags=re.DOTALL)

with open("/Users/macbookair/.gemini/antigravity/scratch/affiliate-engine/threads_sniffer.py", "w", encoding="utf-8") as f:
    f.write(new_sn_content)

print("Updated threads_sniffer.py with search queries for all 50 slots!")
