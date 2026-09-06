"""Public-copy contracts, not behavioral model evaluations."""
import unittest
from pathlib import Path


class LaunchDocumentationTests(unittest.TestCase):
    def test_readme_explains_ongoing_value_privacy_and_feedback(self):
        text = (Path(__file__).resolve().parents[1] / 'README.md').read_text()
        for phrase in ('## After the first issue', 'approved preferences',
                       'connected services', 'Update checks contact GitHub',
                       'DM me on Twitter', 'https://x.com/DarwinBinesh',
                       'Compatibility is not a quality guarantee'):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertNotIn('nothing phones home', text)
        self.assertNotIn('your only running cost is your model usage', text)


if __name__ == '__main__':
    unittest.main()
