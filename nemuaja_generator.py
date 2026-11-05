"""
NemuAja.id Contextual Reply & Dynamic Link Generator (Fase 3 Dynamic Engine).
Evaluates real user complaints on Indonesian Threads and drafts authentic, casual 4-part replies
with direct cloaked affiliate links (nemuaja.pages.dev/go/[slug]).

Enforces Shopee Affiliate ID: 11324391980
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

AFFILIATE_ID = "11324391980"

# Pre-curated core solutions (high conversion evergreen)
CORE_PRESETS = {
    "serbuk": {
        "keywords": ["wajan", "panci", "gosong", "kerak", "pantat panci", "minyak membandel"],
        "name": "Serbuk Ajaib Pembersih Kerak Wajan & Panci",
        "slug": "serbuk",
        "caveat": "olesnya wajib pake sarung tangan ya biar kulit ga sensitif",
        "magnet": "wajan lu bahan teflon apa stainless steel?"
    },
    "rak": {
        "keywords": ["kamar mandi", "kosan", "kos", "sabun berantakan", "shampoo", "ngebor", "tembok"],
        "name": "Rak Sudut Tempel Kamar Mandi Tanpa Bor",
        "slug": "rak",
        "caveat": "lap keramik sampe bener-bener kering dulu sebelum ditempel biar rekat maksimal",
        "magnet": "tembok kamar mandi kosan lu keramik licin kan?"
    },
    "pel": {
        "keywords": ["ngepel", "kain pel", "lantai", "becek", "peras pel", "tangan kotor", "debu"],
        "name": "Flat Mop Pel Otomatis Peras Sendiri",
        "slug": "pel",
        "caveat": "kain mikrofibernya setelah pakai langsung bilas biar ga bau apek",
        "magnet": "kosan/rumah lu lantainya luas bgt ga?"
    },
    "tawas": {
        "keywords": ["bau ketiak", "bau badan", "burket", "ketiak asem", "baju kuning", "deodorant", "roll on"],
        "name": "Tawas Spray Deodorant Alami",
        "slug": "tawas",
        "caveat": "semprot 2-3 kali pas ketiak kering abis mandi, jangan pas lagi keringetan",
        "magnet": "lu biasanya pake deodorant roll-on apa spray?"
    },
    "acne": {
        "keywords": ["jerawat", "jerawat batu", "jerawat mendem", "nanah", "pencet jerawat", "bopeng"],
        "name": "Hydrocolloid Acne Patch Penghisap Jerawat",
        "slug": "acne",
        "caveat": "tempel pas muka bersih dan kering sebelum skincare tebel biar nempel kenceng",
        "magnet": "jerawatnya tipe mendem sakit atau udah ada matanya?"
    }
}

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

def pre_screen_indo(post_text, author="user"):
    """
    Fast rule-based pre-screener for Indonesian threads.
    Rejects ads, job vacancies, politics, grief, or non-complaints before calling LLM.
    """
    text_lower = post_text.lower()
    
    # Red flags
    banned_keywords = [
        "loker", "lowongan", "innalillahi", "turut berduka", "rip",
        "judi", "slot", "gacor", "zeus", "pragmatic",
        "promo", "diskon", "dm for order", "open po", "ready stock",
        "partai", "pilkada", "capres", "anies", "prabowo", "jokowi", "gibran"
    ]
    for b in banned_keywords:
        if b in text_lower:
            return False, f"Banned keyword detected: {b}"

    # Must be at least 15 chars
    if len(post_text.strip()) < 15:
        return False, "Post too short"

    return True, "Passed pre-screen"

def generate_reply_indo_llm(post_text, author="user", timeout=25):
    """
    Generate authentic Indonesian Threads reply with direct cloaked affiliate link.
    """
    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        return None

    model = os.environ.get("OPENROUTER_MODEL", "google/gemini-2.5-flash").strip()

    system_instruction = f"""Kamu adalah NemuAja (@nemuaja.id), kurator barang Shopee pemecah masalah harian di Indonesia (anak kos & millennial friendly).
Gaya bicaramu santai, akrab, solutif, anti-gimmick, menggunakan bahasa gaul percakapan Threads sehari-hari (gue/lu, bgt, wkwk, asli, deh, beneran). BUKAN bahasa robot, BUKAN bahasa sales iklan.

ATURAN UTAMA:
1. TARGET PASAR INDONESIA:
   - Post harus berbahasa Indonesia / bahasa gaul sehari-hari.
   - Jika post bahasa Inggris, tolak (REJECT).
2. HANYA RESPON KELUHAN / FRUSTRASI NYATA:
   - Respon keluhan tentang rumah tangga, kosan, kebersihan, perawatan diri (jerawat, bau badan), anabul, barang rusak/kotor, kerapian, dsb.
   - TOLAK jika post sekadar pamer, curhat cinta rumit, politik, duka cita, atau postingan jualan orang lain.
3. STRUKTUR REPLY 4-BAGIAN (HARUS MENGANDUNG LINK LANGSUNG):
   - Bagian 1: Empati relatable singkat ("asli relate bgt...", "wkwk sama bgt gue dulu pusing...", "beneran males bgt kalo...")
   - Bagian 2: Solusi konkrit barang Shopee + LINK LANGSUNG:
     Format link: `nemuaja.pages.dev/go/[slug-singkat]`
     Contoh slug: `nemuaja.pages.dev/go/serbuk`, `nemuaja.pages.dev/go/rak`, `nemuaja.pages.dev/go/kucing-pipis`, `nemuaja.pages.dev/go/pembersih-sepatu`
     (Slug harus huruf kecil, pisahkan kata pakai tanda strip -).
   - Bagian 3: Tips jujur / honest caveat pemakaian agar tidak zonk (misal: "tapi pas oles wajib sarung tangan ya", "lap keramik sampe beneran kering sebelum tempel").
   - Bagian 4: Pertanyaan pancingan diskusi di akhir (Conversation Magnet) agar pemilik thread membalas dan reply kita jadi Top Comment!
4. NADA BICARA:
   - Huruf kecil santai (lowercase casual).
   - Jangan pakai tanda seru berlebihan, jangan terdengar seperti admin toko.
   - Maksimal 2-3 kalimat ringkas padat.

OUTPUT FORMAT (JSON MURNI):
{{
  "verdict": "ACCEPT" atau "REJECT",
  "reason": "Alasan singkat",
  "product_name": "Nama solusi barang",
  "slug": "slug-produk",
  "reply_text": "teks reply lengkap dalam huruf kecil santai"
}}
"""

    user_payload = {
        "author": author,
        "post_text": post_text
    }

    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)}
        ],
        "temperature": 0.3,
        "response_format": {"type": "json_object"}
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://nemuaja.pages.dev",
            "X-Title": "NemuAja Indonesian Affiliate Engine"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            return parsed
    except Exception as e:
        print(f"[NemuAja Generator] LLM Error: {e}")
        return None

if __name__ == "__main__":
    test_posts = [
        "wajan teflon gue pantatnya udah gosong item tebel bgt, disikat pake sabun colek ga mempan samsek mau nangis",
        "kamar mandi kosan gue sempit bgt mana ga boleh dipaku ato dibor sm bapak kos, sabun shampoo berserakan di ember",
        "ada yg tau ga cara ngilangin bau ketiak asem kalo siang2 keringetan? pake roll on biasa malah bikin baju kemeja putih jd kuning",
        "selamat pagi semuanya jangan lupa sarapan yaa semoga hari ini lancar",
        "kucing gue hobi bgt pipis sembarangan di kasur sm karpet, bau pesingnya ga ilang2 walau udah dipel berkali kali"
    ]
    print("Testing NemuAja Fase 3 Reply Generator:\n" + "="*50)
    for p in test_posts:
        print(f"\n[POST]: {p}")
        res = generate_reply_indo_llm(p)
        print(f"[RESULT]: {json.dumps(res, indent=2, ensure_ascii=False)}")
