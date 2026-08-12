from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "content-agent" / "SKILL.md"


class DistributionContractTests(unittest.TestCase):
    def test_distribution_contains_no_host_specific_paths_or_secret_values(self) -> None:
        forbidden_fragments = (
            "/opt" + "/data/",
            "/ho" + "me/",
            "gh" + "p_",
            "github" + "_pat_",
            "s" + "k-",
            "access" + "_token",
            "refresh" + "_token",
            "client" + "_secret:",
        )
        authored_suffixes = {".md", ".yaml", ".yml", ".json", ".py", ".sh"}
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or path.suffix not in authored_suffixes:
                continue
            text = path.read_text(encoding="utf-8")
            for fragment in forbidden_fragments:
                self.assertNotIn(fragment, text, f"{fragment!r} found in {path.relative_to(ROOT)}")

    def test_beehiiv_connector_is_runtime_configured_disabled_and_read_only(self) -> None:
        config = (ROOT / "config.yaml").read_text(encoding="utf-8")
        self.assertRegex(config, r"(?m)^mcp_servers:\s*$")
        self.assertRegex(config, r"(?m)^  beehiiv:\s*$")
        self.assertIn("url: https://mcp.beehiiv.com/mcp", config)
        self.assertRegex(config, r"(?m)^    auth: oauth\s*$")
        self.assertRegex(config, r"(?m)^    enabled: false\s*$")
        self.assertEqual(len(re.findall(r"(?m)^      enabled: false\s*$", config)), 2)
        self.assertIn("- __enable_only_after_reviewing_read_only_tool_names__", config)
        self.assertRegex(config, r"(?m)^      prompts: false\s*$")
        self.assertRegex(config, r"(?m)^      resources: false\s*$")
        self.assertFalse((ROOT / "mcp.json").exists(), "current Hermes runtime reads MCP config from config.yaml")

    def test_every_reference_named_by_the_skill_exists(self) -> None:
        skill_text = SKILL.read_text(encoding="utf-8")
        references = set(re.findall(r"references/[a-z0-9-]+\.md", skill_text))
        self.assertGreaterEqual(len(references), 8)
        missing = [relative for relative in sorted(references) if not (SKILL.parent / relative).is_file()]
        self.assertEqual(missing, [])

    def test_manifest_owns_only_the_content_agent_product_surface(self) -> None:
        manifest = (ROOT / "distribution.yaml").read_text(encoding="utf-8")
        expected = {
            "distribution.yaml",
            "SOUL.md",
            "config.yaml",
            "skills/content-agent/",
        }
        owned = {
            match.group(1).strip()
            for match in re.finditer(r"(?m)^  - ([^#\n]+)$", manifest)
        }
        self.assertEqual(owned, expected)
        for user_owned in ("workspace", "memories", "sessions", "auth.json", ".env", "local"):
            self.assertNotIn(user_owned, manifest)

    def test_distribution_json_files_are_valid(self) -> None:
        for path in ROOT.rglob("*.json"):
            if ".git" not in path.parts:
                json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
