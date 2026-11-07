"""
Process-wide concurrency lock for Playwright browser instances on low-RAM VPS.
Prevents concurrent Chromium instances from exhausting RAM and thrashing swap.
"""
import fcntl
import os
import time
from contextlib import contextmanager

LOCK_FILE_PATH = "/tmp/emma_playwright_browser.lock"

@contextmanager
def acquire_browser_lock(timeout_seconds=180, poll_interval=1.5):
    """
    Acquires an exclusive file lock before launching Playwright/Chromium.
    If another process holds the lock, waits up to timeout_seconds.
    """
    lock_file = open(LOCK_FILE_PATH, "w")
    start_time = time.time()
    acquired = False
    try:
        while time.time() - start_time < timeout_seconds:
            try:
                fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
                break
            except (IOError, OSError):
                time.sleep(poll_interval)
        if not acquired:
            raise TimeoutError(f"Could not acquire Playwright browser lock after {timeout_seconds}s (system busy).")
        yield lock_file
    finally:
        if acquired:
            try:
                fcntl.flock(lock_file, fcntl.LOCK_UN)
            except Exception:
                pass
        try:
            lock_file.close()
        except Exception:
            pass
