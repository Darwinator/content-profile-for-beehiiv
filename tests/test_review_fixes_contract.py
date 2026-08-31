"""Contract tests for the 0.2.0 fixes driven by the independent review of the
2026-08-30 four-instance coverage run (REVIEW.md).

Each test names the review finding it closes. These are text contracts on the
shared intelligence, in the same style as test_distribution_contract.py.
"""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def authored_text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class ReviewFixesContractTests(unittest.TestCase):
    # Review §4 #1 / blocker 2: the adjacent sitting recorded
    # "Issue 1 approved … Confirmed by: founder" when the founder never
    # approved anything. Approval states may only flip on an explicit
    # founder approval statement, recorded verbatim.
    def test_approval_states_require_an_explicit_founder_statement(self) -> None:
        skill = authored_text("skills/content-profile/SKILL.md")
        for required in (
            "## Approval integrity",
            "explicit founder statement",
            "verbatim",
            "Silence is not approval",
            "a request to continue with other work is not approval",
            "resent message is not approval",
        ):
            self.assertIn(required, skill)

        checklist = authored_text("skills/content-profile/references/launch-checklist.md")
        self.assertIn("explicit founder approval statement", checklist)
        self.assertIn("asking for the welcome, signup copy, or runway does not approve the issue", checklist)

        decision_log = authored_text(
            "skills/content-profile/templates/editorial-memory/decision-log.md"
        )
        self.assertIn("Founder words (verbatim, required when Confirmed by is the founder):", decision_log)

        launch_template = authored_text(
            "skills/content-profile/templates/editorial-memory/launch-checklist.md"
        )
        self.assertIn("verbatim founder approval statement", launch_template)

    # Review §4 #3: the career sitting reinterpreted the identical resent
    # message three different ways, including one unrequested draft rewrite.
    def test_duplicate_messages_are_confirmed_not_reinterpreted(self) -> None:
        delivery = authored_text("skills/content-profile/references/delivery-continuity.md")
        for required in (
            "## Repeated messages",
            "verbatim or near-verbatim repeat",
            "do not take a new or different action",
            "Never edit a saved artifact",
            "confirm what the founder wants",
        ):
            self.assertIn(required, delivery)
        skill = authored_text("skills/content-profile/SKILL.md")
        self.assertIn("repeated founder message", skill)

    # Review §4 #4: cards fired invisibly/unnamed for the undecided-founder
    # track (Rina) — the exact persona the product is wedged on. Card
    # provenance must land in the saved artifacts, not only in reasoning.
    def test_card_provenance_is_named_in_saved_artifacts(self) -> None:
        skill = authored_text("skills/content-profile/SKILL.md")
        self.assertIn("name the card ID", skill)
        self.assertIn("in the saved options and brief artifacts", skill)
        cards = authored_text("skills/content-profile/references/decision-cards.md")
        self.assertIn("card ID must appear in the saved artifact", cards)
        self.assertIn("An undecided founder is not an exception", cards)
        issue_brief = authored_text("skills/content-profile/templates/issue-brief.md")
        self.assertIn("Decision card applied (ID and rule, or 'no card fits'):", issue_brief)

    # Review §5 product issues: welcome copy promised weekly while the runway
    # said weekly supply was unproven. The promise must match the runway.
    def test_cadence_promises_match_runway_supply_honesty(self) -> None:
        welcome = authored_text("skills/content-profile/references/welcome.md")
        for required in (
            "cadence the runway can already support",
            "most weeks",
            "Do not promise a cadence the runway calls unproven",
        ):
            self.assertIn(required, welcome)
        skill = authored_text("skills/content-profile/SKILL.md")
        self.assertIn("cadence wording in the welcome and signup copy must match the runway", skill)

    # Review §4 #5: a sentence was added to the BDE draft to satisfy the
    # citation checker, and an arbitrary citation-density threshold had to be
    # overridden mid-run. Sources serve the draft, never the reverse.
    def test_sources_serve_the_draft_not_the_checker(self) -> None:
        evidence = authored_text("skills/content-profile/references/evidence-and-claims.md")
        for required in (
            "Sources serve the draft",
            "Never add or reshape a sentence so that a registered source gets used",
            "drop it from the source list without touching the prose",
            "No citation-density quota",
        ):
            self.assertIn(required, evidence)
        review = authored_text("skills/content-profile/references/editorial-review.md")
        self.assertIn("an unused registered source is dropped, not consumed", review)

    # Review §6 fast-follow: career welcome shipped with a literal
    # "[Your name]". A bracketed placeholder blocks "ready for founder review".
    def test_unresolved_placeholders_block_ready_for_founder_review(self) -> None:
        review = authored_text("skills/content-profile/references/editorial-review.md")
        for required in (
            "placeholder scan",
            "[Your name]",
            "cannot be called ready for founder review",
        ):
            self.assertIn(required, review)


class ReleaseMarker016Tests(unittest.TestCase):
    def test_release_markers_are_0_1_6(self) -> None:
        for relative in (
            "distribution.yaml",
            "skills/content-profile/SKILL.md",
            "skills/content-profile/references/release-marker.md",
            "README.md",
            "AGENTS.md",
        ):
            self.assertIn("0.2.0", authored_text(relative), relative)
            self.assertNotIn("0.1.5", authored_text(relative), relative)


if __name__ == "__main__":
    unittest.main()
