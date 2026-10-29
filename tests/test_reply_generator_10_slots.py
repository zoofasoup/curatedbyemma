import unittest
from reply_generator import evaluate_and_draft_local

class TestReplyGeneratorAllSlots(unittest.TestCase):

    def test_rejection_rules(self):
        # Memorial story
        res = evaluate_and_draft_local("In loving memory of my grandfather who passed away last week in his favorite wooden chair.")
        self.assertEqual(res["verdict"], "REJECT")
        
        # Sports match
        res = evaluate_and_draft_local("Yankees pitcher had a terrible 3rd inning with back spasms in the dugout.")
        self.assertEqual(res["verdict"], "REJECT")

        # Promotional spam
        res = evaluate_and_draft_local("Huge giveaway! Use discount code CHAIR20 and link in bio to shop now.")
        self.assertEqual(res["verdict"], "REJECT")

    def test_all_10_slots_matching(self):
        cases = [
            (1, "Golden retriever shedding is out of control. My black velvet couch looks like a sheep."),
            (2, "My 7 month old baby wakes up crying every hour and won't go down. Running on 2 hours of sleep."),
            (3, "Sitting in this cheap office chair 9 hours a day is literally destroying my lower spine and lower back."),
            (4, "Whenever I use my air fryer, pouring oil from the bottle makes everything soggy and greasy. Need a real oil mister."),
            (5, "Scrubbing bathroom tile grout and the bathtub on my hands and knees is literal torture on my back."),
            (6, "My phone charging cables keep sliding off my nightstand and falling into the gap behind the bed."),
            (7, "Holding my phone for a 5 hour flight from NY to LA gave me a severe neck cramp with no seatback screen."),
            (8, "Unpacked my suitcase at the hotel and all my linen shirts are horribly wrinkled. Hate dragging out the hotel iron."),
            (9, "Can't sleep because light keeps waking me up and normal earbuds hurt my ears when sleeping on my side."),
            (10, "Dust and crumbs stuck inside my car air vents and cup holders that normal wipes cannot reach.")
        ]

        for expected_slot, text in cases:
            res = evaluate_and_draft_local(text)
            self.assertEqual(res["verdict"], "ACCEPT", f"Failed for text: {text}")
            self.assertEqual(res["slot"], expected_slot, f"Expected slot #{expected_slot}, got #{res.get('slot')} for text: {text}")
            self.assertIn(f"#{expected_slot}", res["reply_draft"], f"Draft must reference slot #{expected_slot}")

if __name__ == "__main__":
    unittest.main()
