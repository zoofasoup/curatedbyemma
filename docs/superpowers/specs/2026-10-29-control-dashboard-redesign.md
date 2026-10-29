# Control Dashboard Redesign & Information Architecture Specification

**Date:** 2026-10-29  
**Target:** `public/control/index.html` & `dashboard_server.py`  
**Brand:** IP #1 Emma (`@curated_byemma`) · Amazon StoreID `curatedbyem0f-20`  
**Design Standard:** Anti-AI-Slop, Warm Daytime Paper (`oklch(0.985 0.004 85)`), Forest Green Accent (`oklch(0.42 0.09 150)`), Crisp 1px Borders, High Information Density.

---

## 1. Executive Summary & Goals
Transform the fragmented 7-tab operations dashboard (`Catalog`, `Testing & DB`, `Content`, `Reply tester`, `Persona`, `Lander`, `Activity`) into **4 focused, purposeful workspaces** aligned with real creator/operator workflows:
1. **Radar & Approvals** (`radar`): Live complaint sniffer, side-by-side human review cards (Left: original Threads complaint, Right: Emma 4-part honest reply), one-click topic radar pills, live sniffer console drawer, and SQLite dispatched audit stream.
2. **Feed Broadcasts** (`broadcast`): Curated feed posts with editorial Seattle photoshoot previews, publishing status badges (`Published [date]` vs `Queued`), and 1-click publishing.
3. **Catalog & Sprint** (`catalog`): Unified single-source data table combining Master Catalog metadata (#1–#10) with the 7-day conversion sprint (20-reply progress bar, Amazon clicks, orders, tier), plus an interactive slide-over Bio Lander preview.
4. **Persona & Rules** (`persona`): Editorial brand manifesto, "Never Lie" protocol, visual Banned Words wall, signature phrasing, and an interactive Reply Sandbox simulator.

---

## 2. Navigation & Information Architecture

### Workspace Tabs
```html
<div class="tabs" role="tablist">
  <button class="tab" data-tab="radar">Radar & Approvals <span class="badge" id="radar-pending-badge">0</span></button>
  <button class="tab" data-tab="broadcast">Feed Broadcasts <span class="badge">5</span></button>
  <button class="tab" data-tab="catalog">Catalog & Sprint <span class="badge">10</span></button>
  <button class="tab" data-tab="persona">Persona & Rules</button>
</div>
```

---

## 3. Workspace Specifications

### Workspace 1: Radar & Approvals (`radar`)
- **Top Bar / Radar Controls:**
  - Topic Pills for fast scanner triggering: `[All Topics]`, `[Back Pain]`, `[Pet Hair]`, `[Flight Neck]`, `[Cable Clutter]`.
  - Primary Action Button: `[🚀 Run Scanner (Batch 5)]` with spinner state.
  - Live Status Pill: `● Sniffer Ready` / `Scanning Threads GraphQL...`.
- **Hero: Human Approval Queue:**
  - When empty: Calm, non-intrusive empty state card with one-click trigger.
  - When drafts are present: **Side-by-side split cards (`grid-template-columns: 1fr 1fr` on desktop, stacked on mobile)**:
    - **Left Column: Complaint Thread (Context):**
      - Author handle `@username` + link to thread on Threads.
      - Engagement badge: `🔥 Viral Hijack (X likes, Y replies)` or `⚡ Fresh Sniper (X likes, 0 replies)`.
      - Full verbatim complaint text in clear editorial quote container.
    - **Right Column: Emma's 4-Part Honest Reply:**
      - Targeted Slot Badge: `Slot #X: [Product Title]`.
      - Draft text crafted under the 4-part arc (empathy -> audit review consensus -> single catch -> reference slot in bio).
      - "Never Lie Verified" security indicator.
      - Action footer:
        - `[✓ Approve & Dispatch]` (solid forest accent `#1e4620`, disables and displays loading state on click).
        - `[✕ Discard]` (subtle text button).
- **Collapsible Live Sniffer Stream Drawer:**
  - Compact `<details>` drawer below queue for debugging GraphQL network interception without cluttering the screen.
- **Dispatched Replies Audit Stream:**
  - Recent SQLite history of sent replies with timestamp, target author, slot #, and text.

### Workspace 2: Feed Broadcasts (`broadcast`)
- Grid/list of 5 scheduled editorial posts for `@curated_byemma`.
- Left: 64x64 thumbnail of authentic photoshoot image (Seattle coffee shop, cozy living room, desk setup).
- Middle: Title, assigned slot badges (`#3 #7`), formatted caption with linebreaks.
- Right: Publication status (`● Published Oct 29` or `Queued`) and `[Publish to Profile]` button.

### Workspace 3: Catalog & Sprint (`catalog`)
- **Header Actions:**
  - Sprint cycle dates: `Oct 28 – Nov 04 (Sprint #1)`.
  - Target: `20 replies / slot minimum`.
  - Top button: `[📱 Preview Bio Lander]` (toggles slide-over modal).
- **Unified Master Table:**
  - Column 1: Slot (`#1` to `#10`, immutable).
  - Column 2: Product (44px image, Title, editorial hook, Category).
  - Column 3: Rating & monthly velocity (`★ 4.6 (39K)`, `10K+ bought/mo`).
  - Column 4: 7-Day Sprint Progress (progress bar + `X / 20` replies).
  - Column 5: Amazon Clicks & Orders (editable / syncable).
  - Column 6: Status Tier (`🔥 Winner`, `⏳ Testing`, `💤 Underperform`).
  - Column 7: Actions (`[Amazon ↗]` and `[Update Metric]`).

### Workspace 4: Persona & Rules (`persona`)
- **Editorial Profile:** Emma's Seattle aesthetic, avatar, handle, bio copy.
- **Never Lie Protocol:** Clear, numbered ethical ground rules.
- **Banned Words Wall:** Strikethrough pills for forbidden AI affiliate cliches (`link in bio`, `game-changer`, `revolutionary`, etc.).
- **Signature Phrasings:** Inventory of Emma's genuine conversational transitions.
- **Reply Sandbox Simulator:**
  - Textarea to test any user complaint against keyword/vector slot matching in real time.

---

## 4. Visual & Token Specifications (Anti-AI-Slop)
- **Background:** `oklch(0.985 0.004 85)` (warm textured paper).
- **Card Surface:** `white` with subtle 1px border `rgba(0,0,0,0.07)` and minimal shadow `0 1px 3px rgba(0,0,0,0.03)`.
- **Accent:** Forest green `oklch(0.42 0.09 150)` (`#1d4b27`), calm dark ink `oklch(0.20 0.02 60)`.
- **Typography:** System serif/sans hybrid (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`), monospace for slot tags & metrics (`SF Mono, Menlo, monospace`).
- **Zero Generic Slop:** No purple/indigo neon gradients, no glassmorphism blur, no generic 3-card hype grids.
