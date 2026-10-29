import unittest
import os
import sqlite3
import db
import reply_generator

class TestSystemImprovements(unittest.TestCase):
    def setUp(self):
        # Use an in-memory or test database
        self.test_url = "https://www.threads.net/@test_user_unique/post/xyz999"
        conn = db.get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM reply_approval_queue WHERE thread_url = ?", (self.test_url,))
        conn.commit()
        conn.close()

    def tearDown(self):
        conn = db.get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM reply_approval_queue WHERE thread_url = ?", (self.test_url,))
        conn.commit()
        conn.close()

    def test_strict_deduplication(self):
        # First insertion should succeed
        added1 = db.add_to_queue(
            ip_id="emma",
            author="test_user_unique",
            thread_url=self.test_url,
            thread_text="Office chair is killing my lower back",
            slot=3,
            product_name="Lumbar Cushion",
            draft_reply="Check out slot #3 in my bio",
            engagement_tier="⚡ FRESH SNIPER",
            likes_count=2,
            replies_count=0,
            opportunity_score=100
        )
        self.assertTrue(added1)

        # Thread should now be marked as already processed
        self.assertTrue(db.is_thread_already_processed(self.test_url, ip_id="emma"))

        # Duplicate insertion should fail and return False
        added2 = db.add_to_queue(
            ip_id="emma",
            author="test_user_unique",
            thread_url=self.test_url,
            thread_text="Office chair is killing my lower back",
            slot=3,
            product_name="Lumbar Cushion",
            draft_reply="Check out slot #3 in my bio",
            engagement_tier="⚡ FRESH SNIPER",
            likes_count=2,
            replies_count=0,
            opportunity_score=100
        )
        self.assertFalse(added2)

    def test_opportunity_scoring_order(self):
        url_high = "https://www.threads.net/@test_viral/post/viral1"
        url_low = "https://www.threads.net/@test_low/post/low1"

        conn = db.get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM reply_approval_queue WHERE thread_url IN (?, ?)", (url_high, url_low))
        conn.commit()
        conn.close()

        # Insert low score first
        db.add_to_queue("emma", "test_low", url_low, "text low", 1, "Prod 1", "Draft 1",
                        opportunity_score=50)
        # Insert high score second
        db.add_to_queue("emma", "test_viral", url_high, "text high", 1, "Prod 1", "Draft high",
                        opportunity_score=95)

        queue = db.get_pending_queue("emma")
        urls_in_queue = [item["thread_url"] for item in queue]
        
        # High score item should appear before low score item
        self.assertIn(url_high, urls_in_queue)
        self.assertIn(url_low, urls_in_queue)
        self.assertTrue(urls_in_queue.index(url_high) < urls_in_queue.index(url_low))

        # Cleanup
        conn = db.get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM reply_approval_queue WHERE thread_url IN (?, ?)", (url_high, url_low))
        conn.commit()
        conn.close()

    def test_template_hook_diversity(self):
        # Two different authors with the same slot query should receive diverse hook variations
        text = "Sitting in this office chair all day is destroying my lower back and spine."
        draft1 = reply_generator.evaluate_and_draft_local(text, author="user_alpha")["reply_draft"]
        draft2 = reply_generator.evaluate_and_draft_local(text, author="user_beta")["reply_draft"]
        draft3 = reply_generator.evaluate_and_draft_local(text, author="user_gamma")["reply_draft"]
        
        # Verify that drafts cite slot #3
        self.assertIn("#3", draft1)
        self.assertIn("#3", draft2)
        self.assertIn("#3", draft3)

if __name__ == "__main__":
    unittest.main()
