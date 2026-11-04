/**
 * Cloudflare Pages Edge Function: Smart Shopee Affiliate Redirector
 * Intercepts /go/[slug] (e.g. /go/serbuk, /go/rak, /go/pel, /go/tawas, /go/acne)
 * Logs outbound click event, then returns an instant 302 Redirect to the Shopee Universal Link.
 * Completely cloaks the raw affiliate link from Meta's spam shield.
 */

const SHOPEE_LINKS = {
  "serbuk": "https://shopee.co.id/search?keyword=serbuk%20pembersih%20kerak%20panci%20gosong",
  "rak": "https://shopee.co.id/search?keyword=rak%20sudut%20kamar%20mandi%20tempel%20tanpa%20bor",
  "pel": "https://shopee.co.id/search?keyword=alat%20pel%20flat%20mop%20peras%20otomatis",
  "tawas": "https://shopee.co.id/search?keyword=deodorant%20tawas%20spray%20ketiak",
  "acne": "https://shopee.co.id/search?keyword=acne%20patch%20jerawat%20hydrocolloid"
};

export async function onRequest(context) {
  const url = new URL(context.request.url);
  // Extract slug after /go/
  const slug = url.pathname.replace(/^\/go\/?/, "").toLowerCase().trim();
  
  const targetUrl = SHOPEE_LINKS[slug] || "https://shopee.co.id";

  // Edge tracking ping (Fire-and-forget back to VPS logger via tunnel)
  try {
    const backendHost = "https://tiger-taxation-cindy-toilet.trycloudflare.com";
    const trackPayload = JSON.stringify({
      event: "shopee_click",
      slug: slug,
      target: targetUrl,
      referrer: context.request.headers.get("Referer") || "threads_direct",
      user_agent: context.request.headers.get("User-Agent") || ""
    });

    context.waitUntil(
      fetch(`${backendHost}/api/track`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: trackPayload
      }).catch(() => {})
    );
  } catch (e) {
    // Non-blocking
  }

  // Instant 302 Redirect directly to Shopee
  return Response.redirect(targetUrl, 302);
}
