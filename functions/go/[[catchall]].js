/**
 * Cloudflare Pages Edge Function: CuratedByEmma Smart Outbound Redirector
 * Intercepts /go/[slug] (e.g. curatedbyemma.pages.dev/go/lumbar or curatedbyemma.pages.dev/go/3)
 * Completely cloaks Amazon Associates affiliate links from Meta / Threads spam shields.
 * Fire-and-forget logs click event to VPS, then returns instant 302 Redirect to Amazon US.
 */

const AMAZON_TAG = "curatedbyem0f-20";

const AMAZON_PRODUCTS = {
  // Slot #1: Pet Lint Roller
  "1": "https://www.amazon.com/dp/B07GV57JYJ?tag=" + AMAZON_TAG,
  "roller": "https://www.amazon.com/dp/B07GV57JYJ?tag=" + AMAZON_TAG,
  "lint-roller": "https://www.amazon.com/dp/B07GV57JYJ?tag=" + AMAZON_TAG,
  "pet-hair": "https://www.amazon.com/dp/B07GV57JYJ?tag=" + AMAZON_TAG,

  // Slot #2: Calming Otter Soother
  "2": "https://www.amazon.com/dp/B07N1JP56L?tag=" + AMAZON_TAG,
  "otter": "https://www.amazon.com/dp/B07N1JP56L?tag=" + AMAZON_TAG,
  "sleep-otter": "https://www.amazon.com/dp/B07N1JP56L?tag=" + AMAZON_TAG,
  "toddler-sleep": "https://www.amazon.com/dp/B07N1JP56L?tag=" + AMAZON_TAG,

  // Slot #3: Memory Foam Lumbar Cushion
  "3": "https://www.amazon.com/dp/B074C9F45S?tag=" + AMAZON_TAG,
  "lumbar": "https://www.amazon.com/dp/B074C9F45S?tag=" + AMAZON_TAG,
  "cushion": "https://www.amazon.com/dp/B074C9F45S?tag=" + AMAZON_TAG,
  "chair-cushion": "https://www.amazon.com/dp/B074C9F45S?tag=" + AMAZON_TAG,
  "back-pain": "https://www.amazon.com/dp/B074C9F45S?tag=" + AMAZON_TAG,

  // Slot #4: Glass Olive Oil Mister
  "4": "https://www.amazon.com/dp/B0CY1S56JZ?tag=" + AMAZON_TAG,
  "mister": "https://www.amazon.com/dp/B0CY1S56JZ?tag=" + AMAZON_TAG,
  "oil-sprayer": "https://www.amazon.com/dp/B0CY1S56JZ?tag=" + AMAZON_TAG,
  "airfryer-oil": "https://www.amazon.com/dp/B0CY1S56JZ?tag=" + AMAZON_TAG,

  // Slot #5: BEAUTURAL Fabric Shaver & Defuzzer
  "5": "https://www.amazon.com/dp/B01NAQD0KD?tag=" + AMAZON_TAG,
  "shaver": "https://www.amazon.com/dp/B01NAQD0KD?tag=" + AMAZON_TAG,
  "defuzzer": "https://www.amazon.com/dp/B01NAQD0KD?tag=" + AMAZON_TAG,
  "fabric-shaver": "https://www.amazon.com/dp/B01NAQD0KD?tag=" + AMAZON_TAG,
  "sweater": "https://www.amazon.com/dp/B01NAQD0KD?tag=" + AMAZON_TAG,

  // Slot #6: Smartish Cable Wrangler
  "6": "https://www.amazon.com/dp/B07BB4YXHW?tag=" + AMAZON_TAG,
  "cables": "https://www.amazon.com/dp/B07BB4YXHW?tag=" + AMAZON_TAG,
  "cable-wrangler": "https://www.amazon.com/dp/B07BB4YXHW?tag=" + AMAZON_TAG,
  "cord-holder": "https://www.amazon.com/dp/B07BB4YXHW?tag=" + AMAZON_TAG,

  // Slot #7: Airplane Tray Table Phone Mount
  "7": "https://www.amazon.com/dp/B08TKPRKBN?tag=" + AMAZON_TAG,
  "flight-mount": "https://www.amazon.com/dp/B08TKPRKBN?tag=" + AMAZON_TAG,
  "airplane-mount": "https://www.amazon.com/dp/B08TKPRKBN?tag=" + AMAZON_TAG,
  "plane-mount": "https://www.amazon.com/dp/B08TKPRKBN?tag=" + AMAZON_TAG,

  // Slot #8: Compact Handheld Garment Steamer
  "8": "https://www.amazon.com/dp/B0FYF2X322?tag=" + AMAZON_TAG,
  "steamer": "https://www.amazon.com/dp/B0FYF2X322?tag=" + AMAZON_TAG,
  "travel-steamer": "https://www.amazon.com/dp/B0FYF2X322?tag=" + AMAZON_TAG,
  "garment-steamer": "https://www.amazon.com/dp/B0FYF2X322?tag=" + AMAZON_TAG,

  // Slot #9: 3D Bluetooth Sleep Mask
  "9": "https://www.amazon.com/dp/B07DG279MB?tag=" + AMAZON_TAG,
  "sleep-mask": "https://www.amazon.com/dp/B07DG279MB?tag=" + AMAZON_TAG,
  "audio-mask": "https://www.amazon.com/dp/B07DG279MB?tag=" + AMAZON_TAG,
  "bluetooth-mask": "https://www.amazon.com/dp/B07DG279MB?tag=" + AMAZON_TAG,

  // Slot #10: ThermoPro Instant Read Meat Thermometer
  "10": "https://www.amazon.com/dp/B01IHHLB3W?tag=" + AMAZON_TAG,
  "thermometer": "https://www.amazon.com/dp/B01IHHLB3W?tag=" + AMAZON_TAG,
  "meat-thermometer": "https://www.amazon.com/dp/B01IHHLB3W?tag=" + AMAZON_TAG,
  "food-temp": "https://www.amazon.com/dp/B01IHHLB3W?tag=" + AMAZON_TAG
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
  } else {
    // Default fallback to Emma's Bio Lander
    targetUrl = "https://curatedbyemma.pages.dev/";
  }

  // 2. Fire-and-forget Click Beacon to VPS Database
  try {
    const backendHost = "https://tiger-taxation-cindy-toilet.trycloudflare.com";
    context.waitUntil(
      fetch(`${backendHost}/api/track`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          event: "slot_click",
          slot: slotNum,
          product: slug,
          target: targetUrl,
          referrer: context.request.headers.get("Referer") || "threads_direct_comment",
          user_agent: context.request.headers.get("User-Agent") || ""
        })
      }).catch(() => {})
    );
  } catch (e) {}

  // 3. Instant 302 Redirect directly to Amazon product page
  return Response.redirect(targetUrl, 302);
}
