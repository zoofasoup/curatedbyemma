import json
import re
import sys
import time
from typing import List, Dict, Optional
from curl_cffi import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

console = Console()

DEFAULT_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}

DEFAULT_COOKIES = {
    "i18n-prefs": "USD",
    "lc-main": "en_US",
}

AUDIT_CATEGORIES = [
    {
        "category": "Sleep & Kids",
        "pain_point": "Baby crying, toddler sleep struggles, exhaustion",
        "query": "baby sleep soother sound machine"
    },
    {
        "category": "Pets & Fur",
        "pain_point": "Pet hair covering couch, clothes, rugs",
        "query": "pet hair remover roller reusable"
    },
    {
        "category": "Back & Posture",
        "pain_point": "Lower back pain from long sitting / desk work",
        "query": "seat cushion office chair lower back pain"
    },
    {
        "category": "Home & Deep Clean",
        "pain_point": "Tiring bathroom scrub, tile grime, bathtub cleaning",
        "query": "electric spin scrubber bathroom"
    },
    {
        "category": "Desk & Clutter",
        "pain_point": "Tangled charging cables dropping off desk",
        "query": "magnetic cable clips desk organizer"
    },
    {
        "category": "Adult Sleep & Insomnia",
        "pain_point": "Light waking you up, snoring partner, migraine",
        "query": "bluetooth sleep eye mask blackout"
    },
    {
        "category": "Car & Daily Hacks",
        "pain_point": "Dust and crumbs in car air vents and cup holders",
        "query": "car cleaning gel putty detailing"
    },
    {
        "category": "Kitchen Frustrations",
        "pain_point": "Pouring too much oil, uneven spraying on air fryer",
        "query": "oil sprayer for cooking glass"
    }
]

def clean_text(text: Optional[str]) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()

def parse_price(price_str: str) -> float:
    if not price_str:
        return 0.0
    match = re.search(r"[\$]?([\d,]+\.?\d*)", price_str)
    if match:
        try:
            return float(match.group(1).replace(",", ""))
        except ValueError:
            return 0.0
    return 0.0

def parse_rating(rating_str: str) -> float:
    if not rating_str:
        return 0.0
    match = re.search(r"([\d\.]+)\s*out of", rating_str, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return 0.0
    return 0.0

def parse_reviews_count(reviews_str: str) -> int:
    if not reviews_str:
        return 0
    clean = reviews_str.replace("(", "").replace(")", "").strip()
    match = re.search(r"([\d\.]+)\s*([KkMm])?", clean)
    if match:
        val = float(match.group(1))
        unit = match.group(2)
        if unit and unit.upper() == "K":
            return int(val * 1000)
        elif unit and unit.upper() == "M":
            return int(val * 1000000)
        return int(val)
    return 0

def parse_bought_past_month(text: str) -> str:
    match = re.search(r"(\d+K?\+?\s+bought in past month)", text, re.IGNORECASE)
    return match.group(1) if match else "N/A"

def calculate_winning_score(rating: float, reviews: int, price: float, bought_text: str) -> float:
    score = 0.0
    if rating >= 4.6:
        score += 25
    elif rating >= 4.3:
        score += 20
    elif rating >= 4.0:
        score += 10
        
    if reviews >= 20000:
        score += 35
    elif reviews >= 5000:
        score += 30
    elif reviews >= 1000:
        score += 22
    elif reviews >= 300:
        score += 12
        
    # Impulse sweet spot ($10 - $45)
    if 12.0 <= price <= 45.0:
        score += 20
    elif 8.0 <= price <= 75.0:
        score += 15
    elif price > 0:
        score += 8

    # Velocity
    if "10K+" in bought_text or "20K+" in bought_text:
        score += 20
    elif "5K+" in bought_text:
        score += 18
    elif "1K+" in bought_text or "2K+" in bought_text:
        score += 14
    elif "bought" in bought_text:
        score += 8

    return round(score, 1)

def scrape_category_top_product(session: requests.Session, cat_meta: Dict, affiliate_tag: str = "curator-20") -> Optional[Dict]:
    keyword = cat_meta["query"]
    search_url = f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}"
    
    try:
        response = session.get(search_url, headers=DEFAULT_HEADERS, timeout=15)
    except Exception as e:
        console.print(f"[red]Error fetching {keyword}: {e}[/red]")
        return None

    if "Robot Check" in response.text or response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "lxml")
    cards = soup.select("div[data-component-type='s-search-result']")

    best_candidate = None
    highest_score = -1.0

    for card in cards:
        asin = card.get("data-asin", "")
        if not asin:
            continue

        h2 = card.select_one("h2")
        title = clean_text(h2.text) if h2 else ""
        if not title:
            continue

        price_el = card.select_one(".a-price .a-offscreen")
        price = parse_price(price_el.text if price_el else "")

        rating_el = card.select_one(".a-icon-alt")
        rating = parse_rating(rating_el.text if rating_el else "")

        card_text = card.text
        reviews_match = re.search(r"\((\d+[\d\.,]*K?)\)", card_text)
        reviews = parse_reviews_count(reviews_match.group(1)) if reviews_match else 0

        bought = parse_bought_past_month(card_text)

        img_el = card.select_one("img.s-image")
        img_url = img_el.get("src", "") if img_el else ""

        if price <= 0 or rating <= 0 or reviews < 500:
            continue

        score = calculate_winning_score(rating, reviews, price, bought)

        if score > highest_score:
            highest_score = score
            best_candidate = {
                "asin": asin,
                "category": cat_meta["category"],
                "target_pain_point": cat_meta["pain_point"],
                "title": title,
                "price": price,
                "currency": "USD",
                "rating": rating,
                "reviews_count": reviews,
                "bought_past_month": bought,
                "winning_score": score,
                "image_url": img_url,
                "affiliate_url": f"https://www.amazon.com/dp/{asin}?tag={affiliate_tag}"
            }

    return best_candidate

def run_audit(affiliate_tag: str = "curator-20"):
    console.print("\n[bold cyan]🔍 Starting Live Amazon Winning Products Audit across Evergreen Categories...[/bold cyan]\n")
    session = requests.Session(impersonate="chrome124")
    for k, v in DEFAULT_COOKIES.items():
        session.cookies.set(k, v, domain=".amazon.com")

    audited_products = []

    for i, cat_meta in enumerate(AUDIT_CATEGORIES):
        console.print(f"Auditing [yellow]{cat_meta['category']}[/yellow] ({cat_meta['query']})...")
        product = scrape_category_top_product(session, cat_meta, affiliate_tag)
        if product:
            audited_products.append(product)
            console.print(f"  [green]✓ Found:[/green] {product['title'][:45]}... (${product['price']:.2f} | {product['rating']}★ | {product['reviews_count']:,} reviews)")
        else:
            console.print(f"  [red]✗ No top qualifier found for {cat_meta['category']}[/red]")
        time.sleep(1.0) # Politeness delay

    # Assign Slot numbers based on winning score
    audited_products.sort(key=lambda x: x["winning_score"], reverse=True)
    for idx, p in enumerate(audited_products, start=1):
        p["slot_number"] = idx

    # Display Table
    table = Table(title="🏆 AUDIT: Top All-Time Amazon Winning Products (Categorized Master Catalog)", show_header=True, header_style="bold magenta")
    table.add_column("Slot", style="bold yellow", width=6, justify="center")
    table.add_column("Score", style="bold green", width=7, justify="center")
    table.add_column("Category", width=16)
    table.add_column("Product Title", width=38)
    table.add_column("Price", justify="right", width=8)
    table.add_column("Rating", justify="center", width=7)
    table.add_column("Reviews", justify="right", width=9)
    table.add_column("Velocity", justify="center", style="cyan", width=16)

    for p in audited_products:
        table.add_row(
            f"#{p['slot_number']}",
            f"{p['winning_score']}",
            p["category"],
            p["title"][:36] + "...",
            f"${p['price']:.2f}",
            f"{p['rating']}★",
            f"{p['reviews_count']:,}",
            p["bought_past_month"]
        )

    console.print("\n")
    console.print(table)

    output_path = "master_catalog.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(audited_products, f, indent=2, ensure_ascii=False)

    console.print(f"\n[bold green]✓ Master catalog saved to {output_path} with {len(audited_products)} audited products![/bold green]\n")

if __name__ == "__main__":
    tag = sys.argv[1] if len(sys.argv) > 1 else "findshunter-20"
    run_audit(tag)
