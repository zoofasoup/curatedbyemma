/**
 * Cloudflare Pages Function: API Reverse Proxy
 * Proxies /api/* calls from https://curatedbyemma.pages.dev directly to the VPS backend.
 * Eliminates browser Mixed Content (HTTPS -> HTTP) and CORS issues.
 */
export async function onRequest(context) {
  const url = new URL(context.request.url);
  const vpsHost = "http://202.10.42.133:7860";
  const targetUrl = `${vpsHost}${url.pathname}${url.search}`;

  const requestInit = {
    method: context.request.method,
    headers: {
      "Content-Type": context.request.headers.get("Content-Type") || "application/json",
      "User-Agent": context.request.headers.get("User-Agent") || "Cloudflare-Edge-Proxy",
      "X-Forwarded-For": context.request.headers.get("CF-Connecting-IP") || "",
      "Referer": context.request.headers.get("Referer") || ""
    },
    redirect: "follow"
  };

  // Only attach body for non-GET / non-HEAD requests
  if (context.request.method !== "GET" && context.request.method !== "HEAD") {
    try {
      requestInit.body = await context.request.clone().arrayBuffer();
    } catch (e) {
      // Body empty or already consumed
    }
  }

  try {
    const response = await fetch(targetUrl, requestInit);
    const newHeaders = new Headers(response.headers);
    newHeaders.set("Access-Control-Allow-Origin", "*");
    newHeaders.set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    newHeaders.set("Access-Control-Allow-Headers", "Content-Type");
    newHeaders.set("Cache-Control", "no-cache, no-store, must-revalidate");

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: newHeaders
    });
  } catch (err) {
    return new Response(
      JSON.stringify({ error: "Failed to connect to VPS backend", details: err.message }),
      {
        status: 502,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        }
      }
    );
  }
}
