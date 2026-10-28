import json
import re
import sys
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

BEST_SELLER_CATEGORIES = {
    "baby": "https://www.amazon.com/gp/bestsellers/baby-products/",
    "baby_sleep": "https://www.amazon.com/gp/bestsellers/baby-products/166866011/",
    "health_household": "https://www.amazon.com/gp/bestsellers/hpc/",
    "home_kitchen": "https://www.amazon.com/gp/bestsellers/home-garden/",
    "beauty": "https://www.amazon.com/gp/bestsellers/beauty/",
    "gadgets": "https://www.amazon.com/gp/bestsellers/electronics/",
}

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
    """
    Winning Score (0 - 100):
    - Social Proof (Reviews count): up to 35 pts
    - High Rating (>= 4.4): up to 25 pts
    - Velocity / Impulse Buy: 'X+ bought in past month': up to 20 pts
    - Sweet spot price ($15 - $50): up to 20 pts
    """
    score = 0.0
    
    # Rating
    if rating >= 4.6:
        score += 25
    elif rating >= 4.3:
        score += 20
    elif rating >= 4.0:
        score += 10
        
    # Reviews
    if reviews >= 10000:
        score += 35
    elif reviews >= 3000:
        score += 28
    elif reviews >= 1000:
        score += 22
    elif reviews >= 300:
        score += 12
        
    # Price ($15 - $45 is highest impulse conversion)
    if 15.0 <= price <= 45.0:
        score += 20
    elif 10.0 <= price <= 80.0:
        score += 15
    elif price > 0:
        score += 8

    # Velocity / Bought past month
    if "10K+" in bought_text or "5K+" in bought_text:
        score += 20
    elif "1K+" in bought_text or "2K+" in bought_text:
        score += 15
    elif "bought" in bought_text:
        score += 8

    return round(score, 1)

def scrape_search(keyword: str, max_items: int = 10, affiliate_tag: str = "curator-20") -> List[Dict]:
    search_url = f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}"
    console.print(f"[bold green]Searching Amazon for:[/bold green] '{keyword}'")
    
    session = requests.Session(impersonate="chrome124")
    for k, v in DEFAULT_COOKIES.items():
        session.cookies.set(k, v, domain=".amazon.com")

    try:
        response = session.get(search_url, headers=DEFAULT_HEADERS, timeout=15)
    except Exception as e:
        console.print(f"[bold red]Connection error:[/bold red] {e}")
        return []

    if "Robot Check" in response.text or response.status_code == 503:
        console.print("[bold red]Amazon Bot Check triggered.[/bold red]")
        return []

    soup = BeautifulSoup(response.text, "lxml")
    cards = soup.select("div[data-component-type='s-search-result']")
    
    products = []
    seen_asins = set()

    for card in cards:
        asin = card.get("data-asin", "")
        if not asin or asin in seen_asins:
            continue
        seen_asins.add(asin)

        # Title
        h2 = card.select_one("h2")
        title = clean_text(h2.text) if h2 else ""
        if not title:
            continue

        # Price
        price_el = card.select_one(".a-price .a-offscreen")
        price = parse_price(price_el.text if price_el else "")

        # Rating
        rating_el = card.select_one(".a-icon-alt")
        rating = parse_rating(rating_el.text if rating_el else "")

        # Reviews
        card_text = card.text
        reviews_match = re.search(r"\((\d+[\d\.,]*K?)\)", card_text)
        reviews = parse_reviews_count(reviews_match.group(1)) if reviews_match else 0

        # Bought past month
        bought = parse_bought_past_month(card_text)

        # High-res Image
        img_el = card.select_one("img.s-image")
        img_url = img_el.get("src", "") if img_el else ""

        # Score
        score = calculate_winning_score(rating, reviews, price, bought)

        # Only keep legit products with price & rating
        if price > 0 and rating > 0:
            products.append({
                "asin": asin,
                "title": title,
                "price": price,
                "currency": "USD",
                "rating": rating,
                "reviews_count": reviews,
                "bought_past_month": bought,
                "winning_score": score,
                "image_url": img_url,
                "affiliate_url": f"https://www.amazon.com/dp/{asin}?tag={affiliate_tag}"
            })
            if len(products) >= max_items:
                break

    return sorted(products, key=lambda x: x["winning_score"], reverse=True)

def display_table(products: List[Dict]):
    table = Table(title="🏆 Amazon Winning Products for Affiliate Campaigns", show_header=True, header_style="bold magenta")
    table.add_column("Score", style="bold green", width=7, justify="center")
    table.add_column("ASIN", width=12)
    table.add_column("Title", width=42)
    table.add_column("Price", justify="right", width=9)
    table.add_column("Rating", justify="center", width=8)
    table.add_column("Reviews", justify="right", width=9)
    table.add_column("Monthly Velocity", justify="center", style="cyan", width=18)

    for p in products:
        table.add_row(
            f"{p['winning_score']}",
            p["asin"],
            p["title"][:40] + ("..." if len(p["title"]) > 40 else ""),
            f"${p['price']:.2f}",
            f"{p['rating']} ★",
            f"{p['reviews_count']:,}",
            p["bought_past_month"]
        )

    console.print(table)

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "baby sleep soother"
    tag = sys.argv[2] if len(sys.argv) > 2 else "curator-20"
    
    items = scrape_search(query, max_items=8, affiliate_tag=tag)
    if items:
        display_table(items)
        with open("winning_products.json", "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        console.print(f"[bold green]✓ Successfully extracted {len(items)} winning products to winning_products.json[/bold green]")
    else:
        console.print("[yellow]No products retrieved. Check connection or keyword.[/yellow]")
