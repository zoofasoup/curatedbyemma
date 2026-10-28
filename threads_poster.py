import json
import os
import sys
import time
from playwright.sync_api import sync_playwright
from threads_engine import generate_honest_reply

SESSION_FILE = "threads_session.json"

def login_and_save_session():
    """
    Opens a visible browser so you can log in to Threads/Instagram once.
    Saves your login session cookies to threads_session.json for future automated runs.
    """
    print("\n[1/3] Launching browser for one-time manual login...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("[2/3] Opening Threads.net... Please log in to your account.")
        page.goto("https://www.threads.net/login")

        print("\n👉 Log in using your Instagram credentials in the browser window.")
        print("👉 Once you are fully logged in and see your Threads home feed, return here and press ENTER.\n")
        
        input("Press [ENTER] after you have successfully logged in in the browser window...")

        # Save session cookies and storage
        storage = context.storage_state()
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(storage, f, indent=2)

        print(f"\n[3/3] ✓ Session saved successfully to {SESSION_FILE}!")
        print("You won't need to log in again for automated runs.\n")
        browser.close()

def post_new_thread(text: str, headless: bool = True):
    """
    Posts a new standalone thread to your profile.
    """
    if not os.path.exists(SESSION_FILE):
        print(f"[!] Session file {SESSION_FILE} not found. Run 'python threads_poster.py login' first.")
        return False

    print(f"\nPosting new thread: \"{text[:50]}...\"")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(storage_state=SESSION_FILE)
        page = context.new_page()

        page.goto("https://www.threads.net/")
        page.wait_for_timeout(3000)

        try:
            # Click the 'Start a thread' button or dialog
            start_btn = page.locator("div[role='button']:has-text('Start a thread'), div:has-text('What\'s new?')").first
            if start_btn.is_visible():
                start_btn.click()
            else:
                page.keyboard.press("KeyN") # Shortcut for new thread
            
            page.wait_for_timeout(1000)

            # Type text into the contenteditable div
            editor = page.locator("div[contenteditable='true']").first
            editor.click()
            editor.fill(text)
            page.wait_for_timeout(1000)

            # Click 'Post' button
            post_button = page.locator("div[role='button']:has-text('Post')").last
            post_button.click()
            page.wait_for_timeout(3000)

            print("✓ Thread posted successfully!")
            browser.close()
            return True
        except Exception as e:
            print(f"[X] Failed to post: {e}")
            browser.close()
            return False

def reply_to_thread(thread_url: str, custom_text: str = None, headless: bool = True):
    """
    Navigates to a specific Threads post, reads it (or uses custom_text),
    generates the honest curator reply, and posts it.
    """
    if not os.path.exists(SESSION_FILE):
        print(f"[!] Session file {SESSION_FILE} not found. Run 'python threads_poster.py login' first.")
        return False

    print(f"\nTargeting Thread: {thread_url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(storage_state=SESSION_FILE)
        page = context.new_page()

        page.goto(thread_url)
        page.wait_for_timeout(4000)

        # 1. Determine reply text
        if custom_text:
            reply_text = custom_text
        else:
            # Scrape thread post content
            post_el = page.locator("div[data-pressable-container='true']").first
            if post_el.is_visible():
                post_content = post_el.inner_text()
                print(f"Scraped Post: \"{post_content[:80]}...\"")
                res = generate_honest_reply(post_content)
                if not res["matched"]:
                    print("[i] No relevant product match found for this post. Skipping to avoid irrelevant spam.")
                    browser.close()
                    return False
                reply_text = res["reply_text"]
                print(f"Generated Reply: \"{reply_text}\"")
            else:
                print("[!] Could not read post content.")
                browser.close()
                return False

        # 2. Click the reply box / button
        try:
            reply_btn = page.locator("div[role='button']:has-text('Reply'), svg[aria-label='Reply']").first
            reply_btn.click()
            page.wait_for_timeout(1000)

            editor = page.locator("div[contenteditable='true']").first
            editor.click()
            editor.fill(reply_text)
            page.wait_for_timeout(1000)

            post_btn = page.locator("div[role='button']:has-text('Post')").last
            post_btn.click()
            page.wait_for_timeout(3000)

            print(f"✓ Successfully replied to thread: {thread_url}")
            browser.close()
            return True
        except Exception as e:
            print(f"[X] Failed to submit reply: {e}")
            browser.close()
            return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
Threads Bot CLI
Usage:
  python threads_poster.py login                          -> One-time browser login to save session
  python threads_poster.py post "Your message here"       -> Post a new thread
  python threads_poster.py reply <thread_url> ["reply"]   -> Reply to a specific thread
        """)
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "login":
        login_and_save_session()
    elif cmd == "post":
        msg = sys.argv[2] if len(sys.argv) > 2 else "testing automated post from vps"
        post_new_thread(msg, headless=False)
    elif cmd == "reply":
        if len(sys.argv) < 3:
            print("Please provide a thread URL to reply to.")
            sys.exit(1)
        url = sys.argv[2]
        custom = sys.argv[3] if len(sys.argv) > 3 else None
        reply_to_thread(url, custom_text=custom, headless=False)
    else:
        print(f"Unknown command: {cmd}")
