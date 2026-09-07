"""Source-contract regressions, not proof of rendered UI or model behavior.

Guard editorial outcomes and safety without requiring a visible workflow report.
"""

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
    def test_supporting_guidance_does_not_restore_launch_or_option_rituals(self) -> None:
        paths = [ROOT / "SOUL.md", SKILL]
        paths += [p for p in REFERENCES.glob("*.md") if p.name not in ("beehiiv-handoff.md", "release-marker.md")]
        paths += list((SKILL.parent / "templates").rglob("*.md"))
        obsolete = ("five-question kickoff", "five kickoff questions", "delivery envelope",
                    "without inline work, checklist state", "first sitting should end with a draft",
                    "Offer two alternatives plus Other.", "In the launch checklist and decision log:")
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for phrase in obsolete:
                self.assertNotIn(phrase, text, f"{path.name}: obsolete {phrase}")
        for name in ("naming", "issue-format", "welcome"):
            self.assertIn("when a choice needs comparison", (REFERENCES / f"{name}.md").read_text())

    def test_private_records_are_lazy_linked_and_portable_without_reset(self) -> None:
        skill = authored_text("skills/content-profile/SKILL.md")
        for required in ("existing file paths", "lazily", "optional", "issue history", "preserve existing user bytes",
                         "Outside Hermes", "explicit private workspace", "own file and memory tools",
                         "skip the Hermes updater", "do not infer a Hermes home"):
            self.assertIn(required, skill)
        self.assertNotIn("approval-based reconciliation", skill)

    def test_weekly_work_does_not_retrieve_launch_scaffolding(self) -> None:
        skill = authored_text("skills/content-profile/SKILL.md")
        table = re.search(r"Use the minimum retrieval set:(.*?)(?=\n##)", skill, re.S).group(1)
        for row in table.splitlines():
            if any(job in row for job in ("Select", "Develop", "Draft / review", "Learning")):
                self.assertNotIn("launch checklist", row)
        for text in (skill, authored_text("skills/content-profile/references/launch-checklist.md")):
            self.assertIn("launch readiness", text)
            self.assertIn("material transitions", text)
            self.assertIn("consequential blocker", text)
        self.assertNotIn("Every deliverable must update", authored_text("skills/content-profile/references/launch-checklist.md"))

    def test_release_markers_agree_with_manifest(self) -> None:
        manifest = authored_text("distribution.yaml")
        versions = re.findall(r"(?m)^version: (\d+\.\d+\.\d+)$", manifest)
        self.assertEqual(len(versions), 1)
        for relative in ("skills/content-profile/SKILL.md",
                         "skills/content-profile/references/release-marker.md"):
            markers = re.findall(r"(?mi)^version: (\d+\.\d+\.\d+)$", authored_text(relative))
            self.assertEqual(markers, versions, relative)

    def test_distribution_ships_no_model_or_provider_choice(self) -> None:
        config = (ROOT / "config.yaml").read_text(encoding="utf-8")
        self.assertNotRegex(config, r"(?m)^model:")
        self.assertNotIn("provider:", config)
        self.assertNotIn("gpt-", config)
        self.assertNotIn("openai-codex", config)
        readme = authored_text("README.md")
        self.assertIn("hermes -p content-profile model", readme)
        self.assertIn("doesn't choose a provider or copy your existing model configuration", readme)
        self.assertIn("Editorial quality varies by model", readme)

    def test_first_sitting_earns_an_issue_or_names_the_exact_essential_gap(self) -> None:
        skill = authored_text("skills/content-profile/SKILL.md")
        for required in ("complete inline first issue", "editable private artifact", "bounded research",
                         "narrower treatment", "exact missing evidence or permission",
                         "No issue draft is complete", "not a first-issue success",
                         "Welcome email draft", "Signup copy", "offered, not forced", "Do not draft future issues"):
            self.assertIn(required, skill)
        for obsolete in ("everything except pressing send exists", "return The Next Three, help the founder select"):
            self.assertNotIn(obsolete, skill)

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
        self.assertIn("card IDs stay private", skill)
        self.assertIn("never force-fit an anchor", skill)
        onboarding = authored_text("skills/content-profile/references/onboarding.md")
        self.assertIn("newsletters or writers you actually read", onboarding)
        self.assertIn("Skipping is fine", onboarding)
        self.assertIn("references/decision-cards.md", onboarding)

    def test_kickoff_resolves_fields_and_preserves_typed_answer_popup(self) -> None:
        onboarding = authored_text("skills/content-profile/references/onboarding.md")
        for field in ("Current work / business", "Credible perspective", "Reader and useful change",
                      "Newsletter objective", "Existing direction and assets"):
            self.assertIn(field, onboarding)
        for required in ("five resolved fields", "Reuse answers", "one answer may resolve several fields",
                         "typed-answer popup", "free text", "I don't know yet", "text fallback",
                         "missing meaningful question", "information resolved", "not confirmed durable truth"):
            self.assertIn(required, onboarding)
        for obsolete in ("exactly five", "Setup 1 of 5", "next numbered kickoff question", "After the fifth answer"):
            self.assertNotIn(obsolete, onboarding)

    def test_kickoff_routes_by_known_context_not_saved_brief(self) -> None:
        skill = authored_text("skills/content-profile/SKILL.md")
        for required in ("known context and the requested job", "saving was declined", "five resolved fields",
                         "typed-answer popup", "visible assistant text before the tool call",
                         "text fallback", "Reuse the founder's explicit direction", "final content approval"):
            self.assertIn(required, skill)
        for obsolete in ("Setup 1 of 5", "Do not end the first response without asking that question",
                         "Ask exactly five", "After question five"):
            self.assertNotIn(obsolete, skill)

    def test_soul_keeps_expert_friend_voice_and_weekly_editorial_job(self) -> None:
        soul = authored_text("SOUL.md")
        for required in ("newsletter editor", "warm expert friend", "willing to disagree", "each week",
                         "Never invent", "Never publish, schedule, or send", "explicit approval", "read back",
                         "load the `content-profile` skill", "first-issue draft", "Orient in visible text before asking"):
            self.assertIn(required, soul)
        self.assertNotIn("If no approved publication brief exists", soul)
        self.assertNotIn("https://", soul)
        self.assertLess(len(soul), 4000)

    def test_unknowns_use_one_working_recommendation_without_menu_quota(self) -> None:
        onboarding = authored_text("skills/content-profile/references/onboarding.md")
        for required in ("one working recommendation", "reversible", "Alternatives help only",
                         "permission remains unknown", "explicit approval", "taste question is optional"):
            self.assertIn(required, onboarding)
        self.assertNotIn("2–3 alternatives", onboarding)

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

    def test_supply_is_publication_planning_not_issue_eligibility(self) -> None:
        kind = authored_text("skills/content-profile/references/publication-kind.md")
        for required in ("This is a classification, not five products", "Building a company",
                         "do not run the founder script", "Never tell a founder to write like a named operator"):
            self.assertIn(required, kind)
        landscape = authored_text("skills/content-profile/references/publication-landscape.md")
        for required in ("cadence or territories", "real cycles show strain", "shorter pilot", "reversible",
                         "invite correction", "not an eligibility test for today's issue"):
            self.assertIn(required, landscape)
        judgment = authored_text("skills/content-profile/references/idea-judgment.md")
        self.assertNotIn("six months", judgment)
        self.assertNotIn("**Supply:**", judgment)
        self.assertIn("uncertain future supply does not veto a worthwhile issue", judgment)
        strategy = authored_text("skills/content-profile/references/publication-strategy.md")
        self.assertIn("cadence or territories", strategy)

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

    def test_originality_is_editorial_judgment_without_taxonomy_quota(self) -> None:
        landscape = authored_text("skills/content-profile/references/publication-landscape.md")
        for required in ("baseline, not a market study", "10 minutes", "If tools are unavailable",
                         "Unknown", "Reuse", "plain language", "not a mandatory taxonomy"):
            self.assertIn(required, landscape)
        judgment = authored_text("skills/content-profile/references/idea-judgment.md")
        self.assertIn("what this adds", judgment)
        self.assertNotIn("one crowding line", judgment)
        self.assertNotIn("say whether this is crowded, distinctive, thin, or unknown", judgment)
        brief = authored_text("skills/content-profile/templates/issue-brief.md")
        self.assertNotIn("Field label:", brief)

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

    def test_consequential_decisions_preserve_approval_and_reversibility_without_class_quota(self) -> None:
        decision_log = authored_text("skills/content-profile/templates/editorial-memory/decision-log.md")
        for required in ("consequential", "Scope", "Rationale", "Evidence", "verbatim", "Supersedes",
                         "Reassessment", "issue record"):
            self.assertIn(required, decision_log)
        self.assertNotIn("Class:", decision_log)

    def test_templates_link_context_instead_of_copying_it(self) -> None:
        idea = authored_text("skills/content-profile/templates/editorial-memory/idea-ledger.md")
        brief = authored_text("skills/content-profile/templates/issue-brief.md")
        publication = authored_text("skills/content-profile/templates/editorial-memory/publication-brief.md")
        self.assertIn("Related issue record", idea)
        self.assertIn("Rejection or parking reason", idea)
        self.assertIn("Publication context link", brief)
        self.assertIn("issue-specific", brief)
        self.assertNotIn("Business and industry interests:", idea + brief)
        self.assertNotIn("Launch Readiness Summary", publication)
        self.assertIn("launch-checklist.md", publication)
        for name in ("idea-ledger", "publication-brief", "source-ledger", "voice-and-boundaries", "learning-proposals"):
            text = authored_text(f"skills/content-profile/templates/editorial-memory/{name}.md")
            self.assertIn("optional", text.lower())
        handoff = authored_text("skills/content-profile/templates/beehiiv-handoff.md")
        self.assertNotIn("Workflow Continuation", handoff)
        self.assertNotIn("1.\n2.\n3.", handoff)
        self.assertIn("exact target", handoff)
        self.assertIn("read back", handoff)
        review = authored_text("skills/content-profile/references/editorial-review.md")
        self.assertIn("this founder, this business, this reader, and this promise", review)

    def test_delivery_is_artifact_first_without_a_status_envelope(self) -> None:
        delivery = authored_text("skills/content-profile/references/delivery-continuity.md")
        for required in ("inline", "Do not default to cron", "material caveat", "one recommended next action",
                         "bounded request can simply end", "Long multi-option deliverables",
                         "Do not use this split for a single draft", "public, non-sensitive URLs only"):
            self.assertIn(required, delivery)
        for obsolete in ("Required delivery envelope", "Every substantive returned deliverable includes",
                         "reopen the checklist", "**Updated launch path:**", "**After your answer:**"):
            self.assertNotIn(obsolete, delivery)
        skill = authored_text("skills/content-profile/SKILL.md")
        self.assertIn("Artifact-first", skill)
        self.assertNotIn("Every deliverable reopens", skill)
        self.assertNotIn("Use the delivery envelope", skill)

    def test_mcp_policy_keeps_final_sending_human_and_mutations_verified(self) -> None:
        soul = authored_text("SOUL.md")
        handoff = authored_text("skills/content-profile/references/beehiiv-handoff.md")
        combined = soul + "\n" + handoff
        self.assertIn("Never publish, schedule, or send", combined)
        self.assertIn("founder completes those final actions inside beehiiv", combined)
        self.assertIn("explicit approval", combined)
        self.assertIn("read back", combined)
        self.assertIn("local Markdown fallback", combined)
        self.assertIn("source list in chat with the draft unless the user asks to skip it", handoff)
        for boundary in ("Content approval is not action approval", "unknown outcome",
                         "Read back the exact target", "explicit approval"):
            self.assertIn(boundary, handoff)

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
            "not a remembered capability list",
            "explicit approval",
            "read back",
            "never publish, schedule, or send",
            "local Markdown fallback",
        ):
            self.assertIn(required.lower(), combined.lower())
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
            "LICENSE",
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
