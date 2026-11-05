"""Tests for CareSooner — safety rules are tested, not just happy paths."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from explainer import (  # noqa: E402
    BANNED_PHRASES, DURATIONS, PATTERNS, RED_FLAGS, TOPICS,
    explain, visit_note,
)


class TestExplainer(unittest.TestCase):
    def test_red_flag_goes_first(self):
        r = explain(["fever"], [RED_FLAGS[0]])
        self.assertEqual(r["priority"], "seek-emergency-care-now")
        self.assertIn("R1", " ".join(r["trace"]))
        self.assertIn("emergency", r["priority_text"].lower())

    def test_getting_worse_prompts_clinician_contact(self):
        r = explain(["fever"], [], "a few days", "getting worse")
        self.assertEqual(r["priority"], "contact-a-clinician-promptly")

    def test_routine_path_without_red_flag_or_worsening(self):
        r = explain(["skin-change"], [], "a few weeks", "comes and goes")
        self.assertEqual(r["priority"], "prepare-and-book-routine-care")

    def test_empty_topics_is_a_prompt_not_a_result(self):
        r = explain([], [])
        self.assertEqual(r["priority"], "choose-a-topic")

    def test_unknown_topic_rejected(self):
        with self.assertRaises(ValueError):
            explain(["not-a-topic"], [])

    def test_too_many_topics_rejected(self):
        with self.assertRaises(ValueError):
            explain([t["id"] for t in TOPICS[:4]], [])

    def test_unknown_red_flag_rejected(self):
        with self.assertRaises(ValueError):
            explain([], ["not a red flag"])

    def test_bad_duration_and_pattern_rejected(self):
        with self.assertRaises(ValueError):
            explain([], [], "yesterday", "not sure")
        with self.assertRaises(ValueError):
            explain([], [], "today", "sideways")

    def test_no_diagnosis_language_anywhere(self):
        for topic in TOPICS:
            r = explain([topic["id"]], [])
            blob = " ".join([r["priority_text"], r["disclaimer"]] +
                            [t["summary"] for t in r["topics"]]).lower()
            for phrase in BANNED_PHRASES:
                self.assertNotIn(phrase, blob)
        note = visit_note(["fever"], [], "a few days", "getting worse",
                          [{"date": "2026-10-29", "topic": "Fever", "note": "demo note"}])
        for phrase in BANNED_PHRASES:
            self.assertNotIn(phrase, note.lower())

    def test_visit_note_contains_disclaimer_topic_and_observation(self):
        note = visit_note(["fever"], [], "a few days", "getting worse",
                          [{"date": "2026-10-29", "topic": "Fever", "note": "demo note"}])
        self.assertIn("General information only", note)
        self.assertIn("Fever", note)
        self.assertIn("2026-10-29", note)
        self.assertIn("demo note", note)

    def test_topics_have_complete_fields_and_unique_ids(self):
        ids = [t["id"] for t in TOPICS]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(TOPICS), 8)
        for t in TOPICS:
            for key in ("id", "title", "summary", "notice", "questions", "red_flags"):
                self.assertIn(key, t)
                self.assertTrue(t[key], key)
        self.assertEqual(len(RED_FLAGS), 10)
        self.assertTrue(set(DURATIONS) and set(PATTERNS))


if __name__ == "__main__":
    unittest.main()
