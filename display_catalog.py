import json
from rich.console import Console
from rich.table import Table

console = Console()
with open("master_catalog.json") as f:
    items = json.load(f)

table = Table(title="Top 10 All-Time Amazon Problem Solvers (Master Catalog)", show_header=True, header_style="bold magenta")
table.add_column("Slot", style="bold yellow", width=6, justify="center")
table.add_column("Category", width=22)
table.add_column("Product Title", width=38)
table.add_column("Price", justify="right", width=8)
table.add_column("Rating", justify="center", width=7)
table.add_column("Reviews", justify="right", width=9)
table.add_column("Monthly Velocity", justify="center", style="cyan", width=18)

for p in items:
    slot = f"#{p['slot_number']}"
    cat = p['category']
    title = p['title'][:36] + "..."
    price = f"${p['price']:.2f}"
    rating = f"{p['rating']}★"
    reviews = f"{p['reviews_count']:,}"
    vel = p['bought_past_month']
    table.add_row(slot, cat, title, price, rating, reviews, vel)

console.print(table)
