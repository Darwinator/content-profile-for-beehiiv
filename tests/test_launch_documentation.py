"""Public documentation checks, not model-behavior or OAuth evaluations."""
import re
import unittest
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


class LaunchDocumentationTests(unittest.TestCase):
    def test_readme_is_a_short_entry_point(self):
        text = (ROOT / "README.md").read_text()
        self.assertLess(len(text.split()), 1000)
        self.assertLess(text.index("## Quick start"), text.index("## How it works"))
        self.assertNotIn("exactly five questions", text.lower())
        self.assertNotIn("everything except pressing send", text.lower())

    def test_readme_explains_cost_privacy_control_and_feedback(self):
        text = (ROOT / "README.md").read_text().lower()
        for concept in ("free", "model", "connected services", "github",
                        "conversations", "approval", "https://x.com/darwinbinesh",
                        "source-available", "updates"):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)
        self.assertNotIn("nothing phones home", text)
        self.assertNotIn("your only running cost is your model usage", text)

    def test_connector_commands_target_the_profile_and_select_before_enabling(self):
        text = (ROOT / "skills/content-profile/references/beehiiv-handoff.md").read_text()
        for command in ("mcp login beehiiv", "mcp configure beehiiv", "mcp test beehiiv"):
            self.assertIn(f"hermes -p content-profile {command}", text)
        selection = text.index("hermes -p content-profile mcp configure beehiiv")
        enabled = text.index("hermes -p content-profile config set mcp_servers.beehiiv.enabled true")
        self.assertLess(selection, enabled)

    def test_model_setup_does_not_claim_configuration_inheritance(self):
        text = (ROOT / "config.yaml").read_text().lower()
        self.assertNotIn("inherits the model", text)
        self.assertIn("hermes -p content-profile model", text)

    def test_relative_documentation_links_resolve(self):
        for source in [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]:
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", source.read_text()):
                link = urlsplit(target)
                if link.scheme or not link.path:
                    continue
                with self.subTest(source=source.name, target=target):
                    self.assertTrue((source.parent / link.path).exists())


if __name__ == "__main__":
    unittest.main()
