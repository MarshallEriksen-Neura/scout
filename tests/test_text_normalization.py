import unittest

from app.services.text_normalization import normalize_crawled_markdown


class TextNormalizationTests(unittest.TestCase):
    def test_removes_zero_width_and_normalizes_newlines(self) -> None:
        normalized, metadata = normalize_crawled_markdown("a\u200bb\r\nc\rd\u200c")

        self.assertEqual("ab\nc\nd", normalized)
        self.assertEqual(metadata["removed_zero_width_chars"], 2)
        self.assertFalse(metadata["removed_bom"])
        self.assertTrue(metadata["normalized_newlines"])

    def test_tracks_bom_removal(self) -> None:
        normalized, metadata = normalize_crawled_markdown("\ufeffhello")

        self.assertEqual("hello", normalized)
        self.assertTrue(metadata["removed_bom"])

