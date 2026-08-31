# Content Profile Working Protocol

This repository is the clean, publisher-owned source for Content Profile, a private editorial partner for founders publishing useful newsletters on beehiiv. It is a Hermes profile distribution, not a customer workspace. This file is the contract for any agent (or human) reading, reviewing, or contributing to this checkout.

## Product contract

The agent follows this loop:

> Orient → understand founder and business → make reversible choices → show one launch path → do useful work now → return the artifact as the next gate → learn only with approval.

The initial customer is a solo founder or small-business owner building a useful newsletter on beehiiv. The newsletter must still reward the reader if the reader never buys the founder's product.

The agent is a longitudinal editorial partner. It is not a generic AI writer, content calendar, creator clone, autonomous publisher, or beehiiv support replacement. It must be willing to say that material is not worth publishing yet.

Public positioning is beehiiv-only and independent. Do not imply beehiiv endorsement, official status, privileged access, or employer-confidential knowledge.

## Ownership boundary

Publisher-owned and replaceable on profile update:

- `distribution.yaml`
- `SOUL.md`
- `config.yaml`
- `skills/content-profile/**`

User-owned and never allowed in this repository:

- memories and sessions;
- `workspace/editorial-memory/**` and issue/draft history;
- credentials, OAuth data, `.env`, and `auth.json`;
- business context, private sources, conversations, and local configuration.

A source checkout and an installed profile must stay separate. The installed profile belongs under `$HERMES_HOME/profiles/<name>`. Never point `HERMES_HOME` at this repository.

## Memory and recommendation precedence

1. Current explicit user instruction.
2. Confirmed private Editorial Memory and boundaries.
3. Current shared product intelligence from this distribution.
4. Generic model knowledge.

When shared guidance conflicts with a confirmed private decision, explain the conflict and propose reassessment. Do not silently overwrite the decision.

Durable learning uses: propose → show the change → confirm → apply. Keep it inspectable and reversible.

## Beehiiv boundary

Version `0.1.0` does not encode a beehiiv capability snapshot. The authoritative setup guide is https://www.beehiiv.com/features/mcp/getting-started and the canonical OAuth endpoint is https://mcp.beehiiv.com/mcp. The distributed connector stays disabled, untrusted, and empty until the user authenticates and reviews the live tool surface. At the point of use, inspect the live tools and current first-party documentation; use only supported operations. Mutations require an exact target, explicit approval, one execution attempt, and read back verification. Never publish, schedule, or send. Preserve the local Markdown fallback when MCP or a requested action is unavailable.

## Development rules

- Use tests first for scripts and behavioral changes.
- Use Python's standard library unless a dependency is demonstrably required.
- Initialize private workspace files with create-if-missing semantics. Repeated initialization must preserve every existing user byte.
- Keep one lean orchestration skill; place branch-specific knowledge in `references/` and reusable private-file starters in `templates/`.
- Never write user-specific facts into `SOUL.md`, the skill, references, templates, evaluations, fixtures, or Git history.
- Do not add competing newsletter-platform guidance or marketing.
- Treat repository publishing, profile updates, and connector authentication as explicit side-effect boundaries: they happen only on the maintainer's explicit direction, never as a side effect of routine work.

## Review workflow for agents

An agent reviewing or contributing to this checkout should:

1. read this file first;
2. inspect current Git status before editing;
3. work only in the source checkout, never in an installed profile;
4. never copy private user artifacts into fixtures, examples, or documentation;
5. run the validator before proposing a commit;
6. use branches or Git worktrees for concurrent writes, and never let two agents edit the risky shared files (`SOUL.md`, `SKILL.md`, `config.yaml`, `distribution.yaml`) simultaneously.

## Verification commands

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_distribution.py
```

A release is not safe until a real local install/update test proves that shared files change while private memory, workspace, sessions, credentials, config overrides, and unrelated user skills remain byte-identical.
