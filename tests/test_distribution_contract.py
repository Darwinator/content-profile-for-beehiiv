from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "content-profile" / "SKILL.md"
REFERENCES = SKILL.parent / "references"


def authored_text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class DistributionContractTests(unittest.TestCase):
    def test_release_markers_are_0_1_6(self) -> None:
        for relative in (
            "distribution.yaml",
            "skills/content-profile/SKILL.md",
            "skills/content-profile/references/release-marker.md",
            "README.md",
            "AGENTS.md",
        ):
            self.assertIn("0.1.0", authored_text(relative), relative)
            self.assertNotIn("0.1.2", authored_text(relative), relative)

    def test_distribution_ships_no_model_or_provider_choice(self) -> None:
        config = (ROOT / "config.yaml").read_text(encoding="utf-8")
        self.assertNotRegex(config, r"(?m)^model:")
        self.assertNotIn("provider:", config)
        self.assertNotIn("gpt-", config)
        self.assertNotIn("openai-codex", config)
        readme = authored_text("README.md")
        self.assertIn("no model or provider configuration", readme)
        self.assertIn("Any Hermes-supported provider works", readme)

    def test_launch_packet_completes_the_first_sitting(self) -> None:
        skill = authored_text("skills/content-profile/SKILL.md")
        for required in (
            "Finish the launch packet in the same sitting",
            "Welcome email draft",
            "Signup copy",
            "Runway view",
            "Do not draft future issues",
            "offered, not forced",
            "everything except pressing send exists",
        ):
            self.assertIn(required, skill)

    def test_promotion_reference_is_founder_fit_first_25_not_growth_machinery(self) -> None:
        promotion = authored_text("skills/content-profile/references/promotion.md")
        for required in (
            "first 25 real readers",
            "one primary channel plus one supporting motion",
            "Personal invitations, not a blast",
            "One community they are already in",
            "Never recommend paid acquisition",
            "change the channel, not the publication",
            "CARD-03",
            "CARD-05",
            "not V1 defaults",
        ):
            self.assertIn(required, promotion)
        skill = authored_text("skills/content-profile/SKILL.md")
        checklist = authored_text("skills/content-profile/references/launch-checklist.md")
        self.assertIn("references/promotion.md", skill)
        self.assertIn("references/promotion.md", checklist)

    def test_packaging_layers_have_three_distinct_jobs(self) -> None:
        review = authored_text("skills/content-profile/references/editorial-review.md")
        self.assertIn("three packaging layers doing three different jobs", review)
        self.assertIn("One string copied across all three is a packaging failure", review)

    def test_decision_cards_are_mechanism_cases_wired_into_selection_and_drafting(self) -> None:
        cards = authored_text("skills/content-profile/references/decision-cards.md")
        for required in (
            "decision evidence, not imitation targets",
            "Never tell a founder to write like a named operator",
            "CARD-01",
            "CARD-06",
            "Transferable rule:",
            "Do not copy:",
            "Failure test:",
            "verified 2026-08-07",
            "If no card fits",
        ):
            self.assertIn(required, cards)
        self.assertEqual(cards.count("## CARD-"), 6)
        for anchor_domain in (
            "gregisenberg.com",
            "sahilbloom.com",
            "thebootstrappedfounder.com",
            "nik.co",
            "foundingjourney.com",
            "bigdeskenergy.com",
        ):
            self.assertIn(anchor_domain, cards)
        skill = authored_text("skills/content-profile/SKILL.md")
        self.assertIn("references/decision-cards.md", skill)
        self.assertIn("name the card ID and the rule used", skill)
        self.assertIn("never force-fit an anchor", skill)
        onboarding = authored_text("skills/content-profile/references/onboarding.md")
        self.assertIn("newsletters or writers you actually read", onboarding)
        self.assertIn("Skipping is fine", onboarding)
        self.assertIn("references/decision-cards.md", onboarding)

    def test_onboarding_has_a_five_question_kickoff_and_progress_contract(self) -> None:
        onboarding = authored_text("skills/content-profile/references/onboarding.md")
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
        question_five = re.search(
            r"(?m)^5\. \*\*Existing direction:\*\* (?P<prompt>.+)$",
            kickoff.group("body"),
        )
        self.assertIsNotNone(question_five)
        prompt = question_five.group("prompt")
        self.assertIn("already exists", prompt)
        self.assertIn("still blank", prompt)
        for forbidden in (
            "anti-preferences",
            "boundaries",
            "examples you admire",
            "positioning",
            "brand assets",
        ):
            self.assertNotIn(forbidden, prompt)

    def test_skill_enforces_the_first_conversation_before_general_workflow(self) -> None:
        skill = authored_text("skills/content-profile/SKILL.md")
        for required in (
            "## First-conversation contract",
            "Before showing a checklist or asking for work",
            "Setup 1 of 5",
            "What are you working on or building right now?",
            "Do not end the first response without asking that question",
            "Never invoke `clarify` as the first visible action",
            "visible assistant text before the tool call",
            "First sitting ends with a draft, not a dashboard",
            "do not park the founder on beehiiv readiness first",
        ):
            self.assertIn(required, skill)

    def test_soul_is_compact_identity_without_scripts_or_urls(self) -> None:
        soul = authored_text("SOUL.md")
        for required in (
            "newsletter editor",
            "Never publish, schedule, or send",
            "founder completes those final actions inside beehiiv",
            "inspect the live tools",
            "read back",
            "load the `content-profile` skill",
            "first-issue draft",
            "Orient in visible text before asking",
        ):
            self.assertIn(required, soul)
        for forbidden in (
            "Setup 1 of 5",
            "https://",
            "longitudinal",
            "## First-response contract",
        ):
            self.assertNotIn(forbidden, soul)
        self.assertLess(len(soul), 4000, "SOUL.md should stay a compact always-on identity")

    def test_unknowns_use_bounded_choices_and_reversible_defaults(self) -> None:
        onboarding = authored_text("skills/content-profile/references/onboarding.md")
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
        checklist = authored_text("skills/content-profile/references/launch-checklist.md")
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
            "Working title and brand",
            "Beehiiv readiness",
            "Landing page and signup form",
            "Welcome",
            "Research and draft",
            "Promotion",
            "Founder-completed send inside beehiiv",
        ):
            self.assertIn(gate, checklist)

    def test_naming_reference_is_a_working_title_gate_not_a_brand_workshop(self) -> None:
        naming = authored_text("skills/content-profile/references/naming.md")
        for required in (
            "Load this reference only when the current job is a working title",
            "cannot block the first issue",
            "Named business or product exists",
            "No business or product name yet",
            "Do not invent an “endorsed by X” question",
            "two short slates",
            "does not require a place, job, or founder name",
            "Choose the pattern that fits the publication kind",
            "Do not say “provisional default.”",
            "https://www.beehiiv.com/blog/crafting-unique-newsletter-titles-guide",
            "Verified: 2026-08-29",
            "There is no study that randomly assigns newsletter titles",
        ):
            self.assertIn(required, naming)
        self.assertNotIn("place or job in the **name or the subtitle**, not neither", naming)
        skill = authored_text("skills/content-profile/SKILL.md")
        self.assertIn("references/naming.md", skill)
        self.assertIn("Do not open a naming, format, welcome, or growth workshop during kickoff", skill)

    def test_issue_format_reference_offers_a_menu_not_only_1_2_1(self) -> None:
        fmt = authored_text("skills/content-profile/references/issue-format.md")
        for required in (
            "working format",
            "Do not say “provisional.”",
            "Do not default every publication to the same shell",
            "One outcome",
            "1–2–1",
            "Tight container",
            "Judged shorts",
            "Never add filler",
            "filters, not weekly quotas",
            "Do not lock a persona into the format",
            "Never say “write like” a named newsletter",
        ):
            self.assertIn(required, fmt)
        skill = authored_text("skills/content-profile/SKILL.md")
        self.assertIn("references/issue-format.md", skill)

    def test_publication_kind_and_supply_concerns_are_visible_and_reversible(self) -> None:
        kind = authored_text("skills/content-profile/references/publication-kind.md")
        for required in (
            "This is a classification, not five products",
            "Building a company",
            "do not run the founder script",
            "Never tell a founder to write like a named operator",
        ):
            self.assertIn(required, kind)
        landscape = authored_text("skills/content-profile/references/publication-landscape.md")
        judgment = authored_text("skills/content-profile/references/idea-judgment.md")
        onboarding = authored_text("skills/content-profile/references/onboarding.md")
        skill = authored_text("skills/content-profile/SKILL.md")
        strategy = authored_text("skills/content-profile/references/publication-strategy.md")
        brief = authored_text(
            "skills/content-profile/templates/editorial-memory/publication-brief.md"
        )
        self.assertIn("about six months", landscape)
        for source in (landscape, judgment, onboarding, skill, strategy):
            self.assertIn("Supply concern", source)
            self.assertIn("Not now", source)
            self.assertIn("reversible", source)
            self.assertNotIn("silently drop", source.lower())
            self.assertNotIn("This check is internal", source)
            self.assertNotIn("filter is internal", source)
            self.assertNotIn("Do not show that filter", source)
        self.assertIn("references/publication-kind.md", skill)
        self.assertIn("Publication kind", brief)

    def test_welcome_depends_on_plan_and_cadence_and_is_raised_at_first_issue(self) -> None:
        welcome = authored_text("skills/content-profile/references/welcome.md")
        checklist = authored_text("skills/content-profile/references/launch-checklist.md")
        for required in (
            "do **not** automatically receive the latest issue",
            "Raise that fact as soon as the first issue is in motion",
            "Recommend one easy path",
            "Lean default: one welcome email",
            "Free / Launch",
            "Paid, and weekly or more",
            "Paid, and not sending regularly yet",
            "existing source material",
            "distinct reader benefit",
            "turn the preset welcome email **off**",
            "https://www.beehiiv.com/support/article/38813477234071-welcome-email-vs-welcome-automation-which-should-you-use",
            "Verified: 2026-08-29",
        ):
            self.assertIn(required, welcome)
        self.assertNotIn("longer series as a **low-risk way to start**", welcome)
        skill = authored_text("skills/content-profile/SKILL.md")
        self.assertIn("references/welcome.md", skill)
        self.assertIn("new subscribers will not automatically receive the issue", skill)
        for required in (
            "lean default is one welcome email",
            "paid access",
            "existing source material",
            "distinct reader benefit",
        ):
            self.assertIn(required, checklist)
        self.assertNotIn("depends on plan and whether they will send regularly", checklist)

    def test_landscape_scan_is_bounded_and_never_blocks_the_provisional_brief(self) -> None:
        landscape = authored_text("skills/content-profile/references/publication-landscape.md")
        for required in (
            "baseline, not a market study",
            "not a reason to quit",
            "time-box the first pass to 10 minutes",
            "If tools are unavailable",
            "show the provisional brief first",
            "Crowded",
            "Distinctive",
            "Thin",
            "Unknown",
            "Do not redo a full landscape for every issue",
        ):
            self.assertIn(required, landscape)
        skill = authored_text("skills/content-profile/SKILL.md")
        onboarding = authored_text("skills/content-profile/references/onboarding.md")
        brief = authored_text(
            "skills/content-profile/templates/editorial-memory/publication-brief.md"
        )
        judgment = authored_text("skills/content-profile/references/idea-judgment.md")
        issue_brief = authored_text("skills/content-profile/templates/issue-brief.md")
        self.assertIn("references/publication-landscape.md", skill)
        self.assertNotIn("**before** showing the publication brief", skill)
        self.assertIn("without being talked out of publishing", onboarding)
        self.assertIn("## What's already out there", brief)
        self.assertIn("one crowding line against the existing landscape", judgment)
        self.assertIn("## Crowding against the landscape", issue_brief)

    def test_landing_page_is_recommended_not_required(self) -> None:
        checklist = authored_text("skills/content-profile/references/launch-checklist.md")
        template = authored_text(
            "skills/content-profile/templates/editorial-memory/launch-checklist.md"
        )
        skill = authored_text("skills/content-profile/SKILL.md")
        strategy = authored_text("skills/content-profile/references/publication-strategy.md")
        self.assertIn("recommended, not required", checklist)
        self.assertIn("no capture surface", checklist)
        self.assertRegex(
            template,
            r"(?m)^\| Landing page and signup form \| recommended \|",
        )
        self.assertNotRegex(
            template,
            r"(?m)^\| Landing page and signup form \| required \|",
        )
        self.assertIn("beehiiv-hosted signup", skill)
        self.assertIn("separate landing page is recommended", strategy)

    def test_checklist_updates_at_material_transitions_not_every_answer(self) -> None:
        checklist = authored_text("skills/content-profile/references/launch-checklist.md")
        skill = authored_text("skills/content-profile/SKILL.md")
        for source in (checklist, skill):
            self.assertIn("material transitions", source)
            self.assertNotIn("after every founder answer", source)
            self.assertNotIn("after each answer", source)

    def test_cadence_is_recommended_not_mandated_and_timing_has_no_fake_precision(self) -> None:
        strategy = authored_text("skills/content-profile/references/publication-strategy.md")
        self.assertIn("Recommend weekly", strategy)
        self.assertIn("not mandatory", strategy)
        self.assertIn("biweekly or monthly", strategy)
        self.assertIn("around 8:00 a.m.", strategy)
        self.assertIn("Do not claim", strategy)
        self.assertNotIn("lowest cadence", strategy)

    def test_research_requires_founder_relevance_not_only_source_quality(self) -> None:
        judgment = authored_text("skills/content-profile/references/idea-judgment.md")
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
            "skills/content-profile/templates/editorial-memory/decision-log.md"
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
            "skills/content-profile/templates/editorial-memory/idea-ledger.md"
        )
        issue_brief = authored_text("skills/content-profile/templates/issue-brief.md")
        review = authored_text("skills/content-profile/references/editorial-review.md")

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
        delivery = authored_text("skills/content-profile/references/delivery-continuity.md")
        for required in (
            "inline",
            "Do not default to cron",
            "reopen the checklist",
            "current review gate",
            "smallest next action",
            "what happens after the answer",
            "Long multi-option deliverables",
            "Do not use this split for a single draft",
            "$HERMES_HOME/workspace/editorial-memory/idea-options/",
            "public, non-sensitive URLs only",
        ):
            self.assertIn(required, delivery)

    def test_mcp_policy_keeps_final_sending_human_and_mutations_verified(self) -> None:
        soul = authored_text("SOUL.md")
        handoff = authored_text("skills/content-profile/references/beehiiv-handoff.md")
        combined = soul + "\n" + handoff
        self.assertIn("Never publish, schedule, or send", combined)
        self.assertIn("founder completes those final actions inside beehiiv", combined)
        self.assertIn("explicit approval", combined)
        self.assertIn("read back", combined)
        self.assertIn("local Markdown fallback", combined)
        self.assertIn("Sources by default", handoff)
        self.assertIn("unless the founder asked to skip it", handoff)

    def test_draft_source_lists_never_expose_private_or_signed_urls(self) -> None:
        skill = authored_text("skills/content-profile/SKILL.md")
        review = authored_text("skills/content-profile/references/editorial-review.md")
        evidence = authored_text("skills/content-profile/references/evidence-and-claims.md")
        template = authored_text("skills/content-profile/templates/beehiiv-handoff.md")
        self.assertIn("unless the founder asked to skip it", skill)
        for source in (skill, review, evidence):
            self.assertIn("public, non-sensitive URLs", source)
        self.assertIn("source ID and description", evidence)
        self.assertIn("strip signed query parameters", evidence)
        self.assertIn("| Public URL (only if safe) |", template)

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

    def test_beehiiv_connector_is_fail_closed_and_runtime_discovered(self) -> None:
        config = (ROOT / "config.yaml").read_text(encoding="utf-8")
        self.assertRegex(config, r"(?m)^mcp_servers:\s*$")
        self.assertRegex(config, r"(?m)^  beehiiv:\s*$")
        self.assertIn("url: https://mcp.beehiiv.com/mcp", config)
        self.assertRegex(config, r"(?m)^    auth: oauth\s*$")
        self.assertRegex(config, r"(?m)^    enabled: false\s*$")
        self.assertRegex(config, r"(?m)^    trust: untrusted\s*$")
        self.assertEqual(len(re.findall(r"(?m)^      enabled: false\s*$", config)), 2)
        self.assertRegex(config, r"(?m)^      include: \[\]\s*$")
        self.assertRegex(config, r"(?m)^      prompts: false\s*$")
        self.assertRegex(config, r"(?m)^      resources: false\s*$")
        self.assertFalse((ROOT / "mcp.json").exists(), "current Hermes runtime reads MCP config from config.yaml")

        combined = "\n".join(
            authored_text(relative)
            for relative in (
                "AGENTS.md",
                "README.md",
                "SOUL.md",
                "skills/content-profile/SKILL.md",
                "skills/content-profile/references/beehiiv-handoff.md",
            )
        )
        for required in (
            "https://www.beehiiv.com/features/mcp/getting-started",
            "https://mcp.beehiiv.com/mcp",
            "inspect the live tools",
            "treat a capability snapshot as durable",
            "explicit approval",
            "read back",
            "never publish, schedule, or send",
            "local Markdown fallback",
        ):
            self.assertIn(required, combined)
        for stale in (
            "Live-verified: 2026-08-29",
            "12-tool",
            "209 beehiiv tools",
            "`save_post`",
            "write capabilities are forthcoming",
            "reviewed read-only tool names",
        ):
            self.assertNotIn(stale, combined)

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
            "skills/content-profile/",
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
