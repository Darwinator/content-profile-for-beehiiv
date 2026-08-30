# Delivery Continuity

A completed artifact is a workflow state transition, not an endpoint.

## Default execution mode

When the founder is present and the work can be completed now, research, draft, review, and revise in the current conversation. Return the useful result **inline** first. Saving an editable private artifact is additional durability, not a retrieval burden.

Do not default to cron, background work, a local-file-only answer, or a retrieval phrase. Use deferred execution only when timing genuinely matters or the founder explicitly requests later delivery.

## Long multi-option deliverables

Keep ordinary work **inline**: one brief, one draft, one short rec, one question. Do not open a side preview for those.

Split presentation only when **both** are true:

1. the founder must choose among multiple options; and
2. the full writeup would be long enough to bury the choice.

Then:

- **Chat** holds the decision: the recommendation, one line per option, Not now if needed, and the choice control.
- **One private artifact** holds the full cards under `$HERMES_HOME/workspace/editorial-memory/idea-options/YYYY-MM-DD-working-slug.md`. Open it in a side preview when that surface exists. If it does not, keep the artifact available without making the founder hunt for a retrieval phrase.
- Store only the decision material needed for the choice. Include public, non-sensitive URLs only. Private or local sources stay as source IDs and descriptions; remove credentials, signed query parameters, customer identifiers, and unnecessary raw excerpts.
- Retain or delete the artifact under the same private Editorial Memory policy as the related idea decision; do not copy it into the distribution or a public preview.

Do not use this split for a single draft, a single brief, or a short recommendation. Do not dump the full cards into chat *and* the preview.

## Background-work gate

If background work is justified:

1. explain why it cannot or should not be completed inline;
2. name the exact running gate and expected completion condition;
3. keep the launch checklist visible and update its status;
4. advance safe independent work in parallel;
5. return results automatically to the active conversation or a designated thread;
6. cancel, replace, or avoid duplicate and obsolete future schedules;
7. never require the founder to remember a retrieval phrase.

Automatic delivery alone is not continuity. A returned result must reopen the checklist and advance the journey.

## Required delivery envelope

Every substantive returned deliverable includes:

1. **Completed:** what was produced or decided.
2. **Caveats:** evidence gaps, placeholders, permissions, or fit concerns.
3. **Updated launch path:** compact checklist state.
4. **Review:** the current review gate and decision: ready for founder review, needs revision, blocked, or approved for use in beehiiv.
5. **Next:** the smallest next action recommended to the founder.
6. **After your answer:** what happens after the answer and what the agent will do next.
7. **Remaining:** the meaningful launch work still open, including promotion and founder-completed sending inside beehiiv.

Do not bury the artifact beneath process commentary. Show the work, then the continuation envelope.

## User-action boundary

When a next step requires beehiiv permission, confirmation, preview, testing, scheduling, or sending, label it as a founder action. Scheduling and sending always remain founder actions inside beehiiv. The agent may prepare and, where the live tool surface and `references/beehiiv-handoff.md` action state machine allow it, execute an explicitly approved draft mutation — but it must never imply it completed an action it could not verify by reading back the target.
