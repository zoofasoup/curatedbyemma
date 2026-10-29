# Control Dashboard Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Overhaul the `/control` operations dashboard into 4 clean, purposeful workspaces (Radar & Approvals, Feed Broadcasts, Catalog & Sprint, Persona & Rules) with side-by-side human review cards and zero AI slop.

**Architecture:** Refactor the single-page application in `public/control/index.html` to adopt an intuitive 4-workspace mental model. The human approval queue renders in a responsive 2-column comparison layout (Left: original Threads complaint post with engagement badges, Right: Emma's 4-part honest reply with slot info and dispatch actions). The Master Catalog and 7-day sprint metrics are unified into a single comprehensive data table.

**Tech Stack:** Vanilla HTML/CSS/JavaScript (zero heavy framework dependencies, instant load), SQLite backend API (`dashboard_server.py`), Playwright for headless visual QA verification.

**Spec:** `docs/superpowers/specs/2026-10-29-control-dashboard-redesign.md`

---

## Tasks

- [ ] **Task 1: CSS & Visual Tokens Refactor (Anti-AI-Slop & Side-by-Side Layout)**
  - Update design tokens in `public/control/index.html`: warm paper surface `oklch(0.985 0.004 85)`, forest accent `#1d4b27`, crisp 1px borders, subtle card elevation.
  - Implement `.approval-card` with side-by-side split grid (`grid-template-columns: 1fr 1fr` on screens > 768px, stacked on mobile).
  - Add typography hierarchy: clear section titles, monospaced slot numbers, and editorial quote styles for original complaints and drafts.
  - Commit changes to git.

- [ ] **Task 2: Workspace Navigation & State Management**
  - Replace the 7-tab list (`catalog`, `experiments`, `content`, `replies`, `persona`, `lander`, `activity`) with 4 workspaces:
    1. `radar`: Radar & Approvals (with live badge for pending review count)
    2. `broadcast`: Feed Broadcasts (with badge for post count)
    3. `catalog`: Catalog & Sprint (with badge for 10 slots)
    4. `persona`: Persona & Rules
  - Update route handling `go(ip, tab)` and hash navigation to default to `#/${ip}/radar`.
  - Commit changes to git.

- [ ] **Task 3: Implement Workspace 1 (`renderRadar`)**
  - Implement top radar toolbar with topic shortcut pills (*All*, *Back Pain*, *Pet Hair*, *Flight Neck*, *Cables*).
  - Implement side-by-side Human Approval Queue rendering:
    - Left column: Original complaint, author handle, direct thread link, engagement badge (`🔥 Viral Hijack` vs `⚡ Fresh Sniper`).
    - Right column: Emma's 4-part honest reply, targeted slot title, *Never Lie* verified indicator, `[✓ Approve & Dispatch]` and `[✕ Discard]` buttons.
  - Retain live background polling and event binding for instant approval and discard.
  - Include collapsible live crawler log drawer and SQLite sent replies audit list.
  - Commit changes to git.

- [ ] **Task 4: Implement Workspace 3 (`renderCatalogSprint`)**
  - Merge the separate Master Catalog table and the 7-Day Sprint matrix into a single table.
  - Display Slot `#1–#10`, Product Thumbnail + Title + Hook, Rating & Velocity, 20-reply progress bar, Amazon Clicks & Orders, Status Tier (`🔥 Winner`, `⏳ Testing`, `💤 Underperform`), and Action buttons.
  - Add slide-over / modal trigger for Bio Lander preview.
  - Commit changes to git.

- [ ] **Task 5: Implement Workspace 2 (`renderBroadcast`) & Workspace 4 (`renderPersona`)**
  - Update `renderBroadcast`: clean editorial cards with Seattle photoshoot photos, status badge (`Published [date]` vs `Queued`), and 1-click publishing.
  - Update `renderPersona`: Seattle editorial bio, "Never Lie" protocol, visual Banned Words wall with strikethrough styling, signature phrasing list, and the interactive Reply Sandbox simulator.
  - Commit changes to git.

- [ ] **Task 6: Visual & Functional Verification via Playwright**
  - Run Playwright script to capture full-page desktop (1440x900) screenshots of all 4 tabs on `http://localhost:7860/#/emma/radar`.
  - Test clicking between tabs and verify zero console errors, zero layout overflow, and perfect side-by-side rendering in the Approval Queue.
  - Commit verified code.

- [ ] **Task 7: Push to GitHub & Deploy to Cloudflare Pages**
  - Push branch `main` to `origin` (`https://github.com/zoofasoup/curatedbyemma.git`).
  - Confirm live sync and report final status to user.
