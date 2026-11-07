/**
 * Cloudflare Pages Edge Function: CuratedByEmma Smart Outbound Redirector
 * Maps 50 Curated Viral Amazon Problem-Solvers to Cloaked Redirects.
 * Direct ASIN fallback and Shopee Indonesia fallbacks supported.
 */

const AMAZON_TAG = "curatedbyem0f-20";

const AMAZON_PRODUCTS = {
  // Slot #1: PetLovers Extra-Sticky Lint Roller (5 pack)
  "1": "https://www.amazon.com/dp/B07GV57JYJ?tag=" + AMAZON_TAG,
  "roller": "https://www.amazon.com/dp/B07GV57JYJ?tag=" + AMAZON_TAG,

  // Slot #2: Fisher-Price Calming Otter Sleep Soother
  "2": "https://www.amazon.com/dp/B07N1JP56L?tag=" + AMAZON_TAG,
  "otter": "https://www.amazon.com/dp/B07N1JP56L?tag=" + AMAZON_TAG,

  // Slot #3: Ergonomic Memory Foam Lumbar Cushion
  "3": "https://www.amazon.com/dp/B074C9F45S?tag=" + AMAZON_TAG,
  "lumbar": "https://www.amazon.com/dp/B074C9F45S?tag=" + AMAZON_TAG,

  // Slot #4: TrendPlain Glass Olive Oil Mister
  "4": "https://www.amazon.com/dp/B0CY1S56JZ?tag=" + AMAZON_TAG,
  "mister": "https://www.amazon.com/dp/B0CY1S56JZ?tag=" + AMAZON_TAG,

  // Slot #5: BEAUTURAL Fabric Shaver and Sweater Defuzzer
  "5": "https://www.amazon.com/dp/B01NAQD0KD?tag=" + AMAZON_TAG,
  "defuzzer": "https://www.amazon.com/dp/B01NAQD0KD?tag=" + AMAZON_TAG,

  // Slot #6: Smartish Magnetic Cable Wrangler
  "6": "https://www.amazon.com/dp/B07BB4YXHW?tag=" + AMAZON_TAG,
  "cables": "https://www.amazon.com/dp/B07BB4YXHW?tag=" + AMAZON_TAG,

  // Slot #7: Perilogics Airplane Tray-Table Phone Mount
  "7": "https://www.amazon.com/dp/B08TKPRKBN?tag=" + AMAZON_TAG,
  "flight-mount": "https://www.amazon.com/dp/B08TKPRKBN?tag=" + AMAZON_TAG,

  // Slot #8: OGHom Compact Handheld Garment Steamer
  "8": "https://www.amazon.com/dp/B0FYF2X322?tag=" + AMAZON_TAG,
  "steamer": "https://www.amazon.com/dp/B0FYF2X322?tag=" + AMAZON_TAG,

  // Slot #9: TOPOINT 3D Bluetooth Sleep Mask
  "9": "https://www.amazon.com/dp/B07DG279MB?tag=" + AMAZON_TAG,
  "sleep-mask": "https://www.amazon.com/dp/B07DG279MB?tag=" + AMAZON_TAG,

  // Slot #10: ThermoPro TP03B Digital Meat Thermometer
  "10": "https://www.amazon.com/dp/B01IHHLB3W?tag=" + AMAZON_TAG,
  "thermometer": "https://www.amazon.com/dp/B01IHHLB3W?tag=" + AMAZON_TAG,

  // Slot #11: TubShroom Revolutionary Tub Drain Hair Catcher
  "11": "https://www.amazon.com/dp/B01BYMTYBS?tag=" + AMAZON_TAG,
  "tubshroom": "https://www.amazon.com/dp/B01BYMTYBS?tag=" + AMAZON_TAG,

  // Slot #12: The Pink Stuff Miracle Cleaning Paste
  "12": "https://www.amazon.com/dp/B00DU5SRIY?tag=" + AMAZON_TAG,
  "pink-stuff": "https://www.amazon.com/dp/B00DU5SRIY?tag=" + AMAZON_TAG,

  // Slot #13: ChomChom Roller Reusable Pet Hair Remover
  "13": "https://www.amazon.com/dp/B00BAGT4VO?tag=" + AMAZON_TAG,
  "chomchom": "https://www.amazon.com/dp/B00BAGT4VO?tag=" + AMAZON_TAG,

  // Slot #14: Angry Mama Microwave Steam Cleaner
  "14": "https://www.amazon.com/dp/B01G717M9M?tag=" + AMAZON_TAG,
  "angry-mama": "https://www.amazon.com/dp/B01G717M9M?tag=" + AMAZON_TAG,

  // Slot #15: BISSELL Little Green Portable Carpet & Upholstery Cleaner
  "15": "https://www.amazon.com/dp/B0016HF5GK?tag=" + AMAZON_TAG,
  "little-green": "https://www.amazon.com/dp/B0016HF5GK?tag=" + AMAZON_TAG,

  // Slot #16: Scotchgard Fabric Water Shield Spray
  "16": "https://www.amazon.com/dp/B000063515?tag=" + AMAZON_TAG,
  "fabric-shield": "https://www.amazon.com/dp/B000063515?tag=" + AMAZON_TAG,

  // Slot #17: MAXTID Under Door Draft Stopper Seal
  "17": "https://www.amazon.com/dp/B0836Z3T75?tag=" + AMAZON_TAG,
  "draft-stopper": "https://www.amazon.com/dp/B0836Z3T75?tag=" + AMAZON_TAG,

  // Slot #18: Linda's Essentials Silicone Stove Counter Gap Covers
  "18": "https://www.amazon.com/dp/B073VWB4F9?tag=" + AMAZON_TAG,
  "stove-gap": "https://www.amazon.com/dp/B073VWB4F9?tag=" + AMAZON_TAG,

  // Slot #19: Full Circle Bubble Up Ceramic Soap Dispenser & Dish Brush
  "19": "https://www.amazon.com/dp/B0038K2FES?tag=" + AMAZON_TAG,
  "dish-brush": "https://www.amazon.com/dp/B0038K2FES?tag=" + AMAZON_TAG,

  // Slot #20: OXO Good Grips Jar Opener with Base Pad
  "20": "https://www.amazon.com/dp/B00004OCL8?tag=" + AMAZON_TAG,
  "jar-opener": "https://www.amazon.com/dp/B00004OCL8?tag=" + AMAZON_TAG,

  // Slot #21: Pumie Heavy Duty Pumice Scouring Stick
  "21": "https://www.amazon.com/dp/B000092N2X?tag=" + AMAZON_TAG,
  "pumice-stick": "https://www.amazon.com/dp/B000092N2X?tag=" + AMAZON_TAG,

  // Slot #22: Bar Keepers Friend Cookware Cleanser & Polish
  "22": "https://www.amazon.com/dp/B000V72992?tag=" + AMAZON_TAG,
  "bar-keepers": "https://www.amazon.com/dp/B000V72992?tag=" + AMAZON_TAG,

  // Slot #23: Kasa Smart Plug Ultra Mini (15A)
  "23": "https://www.amazon.com/dp/B091FXLMS8?tag=" + AMAZON_TAG,
  "smart-plug": "https://www.amazon.com/dp/B091FXLMS8?tag=" + AMAZON_TAG,

  // Slot #24: Anker Magnetic Phone Ring Holder (MagGo)
  "24": "https://www.amazon.com/dp/B099596FYR?tag=" + AMAZON_TAG,
  "magsafe-ring": "https://www.amazon.com/dp/B099596FYR?tag=" + AMAZON_TAG,

  // Slot #25: Yogasleep Dohm Classic Natural Sound Machine
  "25": "https://www.amazon.com/dp/B000KUHFGM?tag=" + AMAZON_TAG,
  "dohm": "https://www.amazon.com/dp/B000KUHFGM?tag=" + AMAZON_TAG,

  // Slot #26: Liquid I.V. Hydration Multiplier Packets
  "26": "https://www.amazon.com/dp/B01IT9NLHW?tag=" + AMAZON_TAG,
  "hydration": "https://www.amazon.com/dp/B01IT9NLHW?tag=" + AMAZON_TAG,

  // Slot #27: Loop Quiet Ear Plugs for Sleep
  "27": "https://www.amazon.com/dp/B08MFH1BHS?tag=" + AMAZON_TAG,
  "loop-quiet": "https://www.amazon.com/dp/B08MFH1BHS?tag=" + AMAZON_TAG,

  // Slot #28: Bedsure Satin Pillowcase for Hair & Skin
  "28": "https://www.amazon.com/dp/B072LXQ7PT?tag=" + AMAZON_TAG,
  "satin-pillow": "https://www.amazon.com/dp/B072LXQ7PT?tag=" + AMAZON_TAG,

  // Slot #29: Glisten Garbage Disposer Cleaner & Deodorizer
  "29": "https://www.amazon.com/dp/B000BQWJ6K?tag=" + AMAZON_TAG,
  "disposal-cleaner": "https://www.amazon.com/dp/B000BQWJ6K?tag=" + AMAZON_TAG,

  // Slot #30: Dawn Platinum Powerwash Dish Spray
  "30": "https://www.amazon.com/dp/B07VN9QY29?tag=" + AMAZON_TAG,
  "powerwash": "https://www.amazon.com/dp/B07VN9QY29?tag=" + AMAZON_TAG,

  // Slot #31: Zulay Original Milk Frother Handheld Wand
  "31": "https://www.amazon.com/dp/B074ZL35DH?tag=" + AMAZON_TAG,
  "frother": "https://www.amazon.com/dp/B074ZL35DH?tag=" + AMAZON_TAG,

  // Slot #32: Fullstar Vegetable Chopper Pro (4 Blades)
  "32": "https://www.amazon.com/dp/B0764HS44J?tag=" + AMAZON_TAG,
  "veggie-chopper": "https://www.amazon.com/dp/B0764HS44J?tag=" + AMAZON_TAG,

  // Slot #33: Dash Rapid Egg Cooker (6-Capacity)
  "33": "https://www.amazon.com/dp/B00DDXWFY0?tag=" + AMAZON_TAG,
  "egg-cooker": "https://www.amazon.com/dp/B00DDXWFY0?tag=" + AMAZON_TAG,

  // Slot #34: Bagail 8 Set Compression Packing Cubes
  "34": "https://www.amazon.com/dp/B07XDN7T54?tag=" + AMAZON_TAG,
  "packing-cubes": "https://www.amazon.com/dp/B07XDN7T54?tag=" + AMAZON_TAG,

  // Slot #35: Etekcity Digital Hanging Luggage Scale
  "35": "https://www.amazon.com/dp/B00NW62PCA?tag=" + AMAZON_TAG,
  "luggage-scale": "https://www.amazon.com/dp/B00NW62PCA?tag=" + AMAZON_TAG,

  // Slot #36: Nite Ize Gear Tie Reusable Rubber Twist Ties
  "36": "https://www.amazon.com/dp/B00SHBO284?tag=" + AMAZON_TAG,
  "gear-tie": "https://www.amazon.com/dp/B00SHBO284?tag=" + AMAZON_TAG,

  // Slot #37: Slideep 2-Tier Under Sink Organizer with Sliding Drawer
  "37": "https://www.amazon.com/dp/B09TSMT3L2?tag=" + AMAZON_TAG,
  "sink-organizer": "https://www.amazon.com/dp/B09TSMT3L2?tag=" + AMAZON_TAG,

  // Slot #38: Mellanni Deep Pocket Microfiber Bed Sheet Set
  "38": "https://www.amazon.com/dp/B00NLLUMOE?tag=" + AMAZON_TAG,
  "bed-sheets": "https://www.amazon.com/dp/B00NLLUMOE?tag=" + AMAZON_TAG,

  // Slot #39: Rubbermaid Reveal Cordless Battery Power Scrubber
  "39": "https://www.amazon.com/dp/B0032V1UPC?tag=" + AMAZON_TAG,
  "power-scrubber": "https://www.amazon.com/dp/B0032V1UPC?tag=" + AMAZON_TAG,

  // Slot #40: Conair Battery Operated Compact Fabric Defuzzer
  "40": "https://www.amazon.com/dp/B008I25368?tag=" + AMAZON_TAG,
  "conair-shaver": "https://www.amazon.com/dp/B008I25368?tag=" + AMAZON_TAG,

  // Slot #41: Hero Cosmetics Mighty Patch Original Acne Patches
  "41": "https://www.amazon.com/dp/B074PVTPBW?tag=" + AMAZON_TAG,
  "pimple-patch": "https://www.amazon.com/dp/B074PVTPBW?tag=" + AMAZON_TAG,

  // Slot #42: Aquaphor Healing Ointment Advanced Therapy
  "42": "https://www.amazon.com/dp/B006IB5T4W?tag=" + AMAZON_TAG,
  "aquaphor": "https://www.amazon.com/dp/B006IB5T4W?tag=" + AMAZON_TAG,

  // Slot #43: O'Keeffe's Working Hands Hand Cream Jar
  "43": "https://www.amazon.com/dp/B00121UVU0?tag=" + AMAZON_TAG,
  "working-hands": "https://www.amazon.com/dp/B00121UVU0?tag=" + AMAZON_TAG,

  // Slot #44: Wet & Forget Shower Daily Cleaner Spray
  "44": "https://www.amazon.com/dp/B0019KTH0M?tag=" + AMAZON_TAG,
  "shower-spray": "https://www.amazon.com/dp/B0019KTH0M?tag=" + AMAZON_TAG,

  // Slot #45: Command Large Picture Hanging Strips (16 Pairs)
  "45": "https://www.amazon.com/dp/B073XR4X72?tag=" + AMAZON_TAG,
  "command-strips": "https://www.amazon.com/dp/B073XR4X72?tag=" + AMAZON_TAG,

  // Slot #46: Mueller Double-Wall Stainless Steel French Press
  "46": "https://www.amazon.com/dp/B07JDFXWLS?tag=" + AMAZON_TAG,
  "french-press": "https://www.amazon.com/dp/B07JDFXWLS?tag=" + AMAZON_TAG,

  // Slot #47: ThermoPro TP50 Digital Room Thermometer & Hygrometer
  "47": "https://www.amazon.com/dp/B01H1R0K68?tag=" + AMAZON_TAG,
  "hygrometer": "https://www.amazon.com/dp/B01H1R0K68?tag=" + AMAZON_TAG,

  // Slot #48: Gorilla Grip Heat Resistant Silicone Oven Mitts
  "48": "https://www.amazon.com/dp/B079J8XQ7Q?tag=" + AMAZON_TAG,
  "oven-mitts": "https://www.amazon.com/dp/B079J8XQ7Q?tag=" + AMAZON_TAG,

  // Slot #49: Sleepy Ride Airplane Footrest Under Seat Hammock
  "49": "https://www.amazon.com/dp/B071JM1T46?tag=" + AMAZON_TAG,
  "airplane-footrest": "https://www.amazon.com/dp/B071JM1T46?tag=" + AMAZON_TAG,

  // Slot #50: FurZapper Pet Hair Remover for Washer and Dryer
  "50": "https://www.amazon.com/dp/B074CHX3HH?tag=" + AMAZON_TAG,
  "furzapper": "https://www.amazon.com/dp/B074CHX3HH?tag=" + AMAZON_TAG,

};

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
  const slug = url.pathname.replace(/^\/go\/?/, "").toLowerCase().trim();

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
    const asin = slug.replace(/^dp\//, "").toUpperCase();
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
