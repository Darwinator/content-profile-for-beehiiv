# Working on Content Profile

This is the public source for a newsletter editor built for beehiiv and Hermes. It is a source-available product distribution, not a customer workspace or a general agent framework.

## Product

Help founders, small-business owners and newsletter side-hustlers make useful issues. The reader should benefit even if they never buy anything. A publication can use the founder's name, cover an adjacent industry or be a business itself.

Understand enough to help, do the editorial work, and remember what matters for next time. Keep the typed-answer popup for meaningful kickoff gaps; resolve five areas of context rather than requiring five replies. The first issue is the goal when material supports it. Otherwise develop a concrete direction and identify the essential missing evidence, permission or decision.

The experience should feel like a knowledgeable, opinionated editor, not a project tracker. Return the work rather than a mandatory status report. Keep private records proportionate and linked, with launch planning only when relevant. Voice, evidence and willingness to reject weak material matter more than filling templates.

This is independent of beehiiv. Do not imply endorsement, privileged access or employer-confidential knowledge.

## Ownership and learning

`distribution.yaml` owns the manifest, root `LICENSE`, `SOUL.md`, starter `config.yaml` and `skills/content-profile/`. Updates replace shared material; Hermes preserves the user's existing config. The skill folder carries an identical license for standalone reuse.

User memories, sessions, editorial workspace, drafts, credentials, OAuth data, `.env`, `auth.json`, local overrides and business context stay out of this repository and its fixtures. An installed profile is a separate Hermes home. Don't point `HERMES_HOME` at this checkout.

Use current user direction, then approved private context, then shared guidance, then generic model knowledge. Inferred lasting changes require an inspectable proposal and approval. One-off edits stay with the issue. Shared updates don't authorize changing private decisions.

## Beehiiv

Use https://www.beehiiv.com/features/mcp/getting-started and the live tools at https://mcp.beehiiv.com/mcp. The starter connector is disabled, untrusted and has no allowed tools. Review authentication and tool selection before enabling it in the intended profile.

For an external mutation, show the exact target and change, obtain explicit approval, execute once and read back the result. Content approval is separate from action approval. Preserve the local editable draft when a connection or action is unavailable. Sending, scheduling and publishing remain human actions in beehiiv.

## Development

- Read Git status first. Use separate branches/worktrees for concurrent writers; one owner per file.
- Write failing tests before changing scripts or behavior. Prefer Python's standard library.
- Preserve existing private bytes on initialization. Legacy cleanup should deactivate recognized old content without destroying it; preserve uncertain or customized content.
- Keep one small orchestration skill, job-specific references and optional templates. No user facts in shared instructions or public examples.
- Treat source pushes, installed-profile updates and announcements as separate authorized actions.

Run the [validator and tests](docs/development.md) before committing:

```bash
python3 scripts/validate_distribution.py --hermes-bin /path/to/hermes
```

Real disposable install/update tests should prove private-state preservation. Text checks verify instructions exist, not that a model follows them. Check a few clean conversations when changing the experience; don't build a second product to evaluate the first.
