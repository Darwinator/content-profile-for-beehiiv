from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "content-agent" / "SKILL.md"
REFERENCES = SKILL.parent / "references"


def authored_text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class DistributionContractTests(unittest.TestCase):
    def test_release_markers_are_0_1_1(self) -> None:
        self.assertRegex(authored_text("distribution.yaml"), r"(?m)^version: 0\.1\.1$")
        self.assertRegex(authored_text("skills/content-agent/SKILL.md"), r"(?m)^version: 0\.1\.1$")
        self.assertIn(
            "Version: 0.1.1",
            authored_text("skills/content-agent/references/release-marker.md"),
        )

    def test_onboarding_has_a_five_question_kickoff_and_progress_contract(self) -> None:
        onboarding = authored_text("skills/content-agent/references/onboarding.md")
        for required in (
            "beehiiv-tuned",
            "exactly five",
            "typed-answer popup",
            "1 of 5",
            "I don't know yet",
            "paragraph-style conversation",
            "Founder and business baseline",
            "Reader and promise",
        ):
            self.assertIn(required, onboarding)

        kickoff = re.search(
            r"## Five-question kickoff\n(?P<body>.*?)(?=\n## )",
            onboarding,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(kickoff)
        numbered = re.findall(r"(?m)^\d+\. \*\*", kickoff.group("body"))
        self.assertEqual(len(numbered), 5)

    def test_soul_enforces_the_first_response_before_general_workflow(self) -> None:
        soul = authored_text("SOUL.md")
        for required in (
            "## First-response contract",
            "Before showing a checklist or asking for work",
            "Setup 1 of 5",
            "What are you working on or building right now?",
            "Do not end the first response without asking that question",
            "Never invoke `clarify` as the first visible action",
            "visible assistant text before the tool call",
        ):
            self.assertIn(required, soul)

    def test_unknowns_use_bounded_choices_and_reversible_defaults(self) -> None:
        onboarding = authored_text("skills/content-agent/references/onboarding.md")
        for required in (
            "Mandatory safeguard",
            "Provisional default",
            "Learned preference",
            "Consequential choice",
            "2–3 alternatives",
            "Other",
            "keep moving",
            "Do not merely leave the answer open and advance",
            "Current work and industry interests",
        ):
            self.assertIn(required, onboarding)

    def test_launch_checklist_covers_the_minimum_viable_launch(self) -> None:
        checklist = authored_text("skills/content-agent/references/launch-checklist.md")
        for state in (
            "complete",
            "current",
            "required",
            "recommended",
            "optional",
            "blocked",
            "deferred",
        ):
            self.assertIn(f"`{state}`", checklist)
        for gate in (
            "Founder and business baseline",
            "Reader, promise, and positioning",
            "Beehiiv readiness",
            "Landing page and signup form",
            "Welcome email or short welcome series",
            "Research and draft",
            "Promotion",
            "Founder-completed send inside beehiiv",
        ):
            self.assertIn(gate, checklist)

    def test_cadence_is_recommended_not_mandated_and_timing_has_no_fake_precision(self) -> None:
        strategy = authored_text("skills/content-agent/references/publication-strategy.md")
        self.assertIn("Recommend weekly", strategy)
        self.assertIn("not mandatory", strategy)
        self.assertIn("biweekly or monthly", strategy)
        self.assertIn("around 8:00 a.m.", strategy)
        self.assertIn("Do not claim", strategy)
        self.assertNotIn("lowest cadence", strategy)

    def test_research_requires_founder_relevance_not_only_source_quality(self) -> None:
        judgment = authored_text("skills/content-agent/references/idea-judgment.md")
        for required in (
            "founder's current or intended business",
            "business and industry interests",
            "this founder",
            "this reader",
            "this promise",
        ):
            self.assertIn(required, judgment)

    def test_decisions_preserve_class_state_provenance_and_reassessment(self) -> None:
        decision_log = authored_text(
            "skills/content-agent/templates/editorial-memory/decision-log.md"
        )
        for required in (
            "mandatory safeguard",
            "provisional default",
            "learned preference",
            "consequential choice",
            "active | inactive | superseded",
            "Rationale:",
            "Source or evidence IDs:",
            "Reassessment trigger:",
        ):
            self.assertIn(required, decision_log)

    def test_relevance_rationale_persists_from_selection_through_send_check(self) -> None:
        idea_ledger = authored_text(
            "skills/content-agent/templates/editorial-memory/idea-ledger.md"
        )
        issue_brief = authored_text("skills/content-agent/templates/issue-brief.md")
        review = authored_text("skills/content-agent/references/editorial-review.md")

        for required in (
            "Founder/business relevance",
            "Business and industry interests",
            "Why this belongs in this newsletter",
            "Rejection or parking reason",
        ):
            self.assertIn(required, idea_ledger)
        for required in (
            "Founder and Business Relevance",
            "Business and industry interests",
            "Why this belongs in this newsletter",
        ):
            self.assertIn(required, issue_brief)
        self.assertIn("this founder, this business, this reader, and this promise", review)

    def test_delivery_is_inline_continuous_and_does_not_default_to_cron(self) -> None:
        delivery = authored_text("skills/content-agent/references/delivery-continuity.md")
        for required in (
            "inline",
            "Do not default to cron",
            "reopen the checklist",
            "current review gate",
            "smallest next action",
            "what happens after the answer",
        ):
            self.assertIn(required, delivery)

    def test_current_mcp_never_promises_approve_and_send(self) -> None:
        soul = authored_text("SOUL.md")
        handoff = authored_text("skills/content-agent/references/beehiiv-handoff.md")
        combined = soul + "\n" + handoff
        self.assertIn("There is no “approve and send” flow", combined)
        self.assertIn("founder completes the final send inside beehiiv", combined)
        self.assertIn("future Send API", combined)
        self.assertIn("not a current capability", combined)

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
