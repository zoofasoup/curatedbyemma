import sqlite3
import re

SLUG_MAP = {
    1: "roller",
    2: "otter",
    3: "lumbar",
    4: "mister",
    5: "defuzzer",
    6: "cables",
    7: "flight-mount",
    8: "steamer",
    9: "sleep-mask",
    10: "thermometer"
}

def update_pending_queue(db_path="data/affiliate.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, matched_slot, draft_reply FROM reply_approval_queue WHERE ip_id = 'emma' AND status = 'pending'")
    rows = c.fetchall()

    updated_count = 0
    patterns = [
        r"(?:i'?ve?\s+)?(?:kept\s+it\s+)?saved\s+(?:the\s+exact\s+one\s+)?under\s+#\d+\s+(?:in\s+my\s+bio|on\s+my\s+page)(?:\s+if\s+you\s+want\s+to\s+check\s+it\s+out)?\.?",
        r"cataloged\s+(?:it\s+)?under\s+#\d+\s+(?:in\s+my\s+bio|on\s+my\s+page)(?:\s+if\s+you\s+want\s+to\s+look\s+at\s+the\s+reviews)?\.?",
        r"listed\s+under\s+#\d+\s+(?:in\s+my\s+bio|on\s+my\s+page)\.?",
        r"pinned\s+under\s+#\d+\s+on\s+my\s+page\.?"
    ]

    for q_id, slot, draft in rows:
        slug = SLUG_MAP.get(slot, "lumbar")
        direct_link_text = f"found the exact one here: curatedbyemma.pages.dev/go/{slug}."

        new_draft = draft
        for pat in patterns:
            new_draft = re.sub(pat, direct_link_text, new_draft, flags=re.IGNORECASE)

        if new_draft != draft:
            c.execute("UPDATE reply_approval_queue SET draft_reply = ? WHERE id = ?", (new_draft.strip(), q_id))
            updated_count += 1

    conn.commit()
    conn.close()
    print(f"✅ Successfully converted {updated_count} pending drafts to direct comment links!")

if __name__ == "__main__":
    update_pending_queue()
