# Content Agent Working Protocol

This repository is the clean, publisher-owned source for the Content Agent for founders publishing on beehiiv. It is a Hermes profile distribution, not a customer workspace and not part of Stacko.

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
- `skills/content-agent/**`

User-owned and never allowed in this repository:

- memories and sessions;
- `workspace/editorial-memory/**` and issue/draft history;
- credentials, OAuth data, `.env`, and `auth.json`;
- business context, private sources, conversations, and local configuration.

The authored source checkout and the installed dogfood profile must be separate directories. The installed profile belongs under `$HERMES_HOME/profiles/content-agent`. Never point `HERMES_HOME` at this repository while dogfooding.

## Memory and recommendation precedence

1. Current explicit user instruction.
2. Confirmed private Editorial Memory and boundaries.
3. Current shared product intelligence from this distribution.
4. Generic model knowledge.

When shared guidance conflicts with a confirmed private decision, explain the conflict and propose reassessment. Do not silently overwrite the decision.

Durable learning uses: propose → show the change → confirm → apply. Keep it inspectable and reversible.

## Beehiiv boundary

As verified from beehiiv's first-party MCP documentation on 2026-08-12, MCP v1 is read-only and write access is described as forthcoming. Treat MCP as read-only until current first-party docs and a live tool inspection prove otherwise. Version `0.1.2` returns completed work inline and preserves an editable Markdown/HTML handoff for use inside beehiiv. There is no “approve and send” flow: never send, schedule, or publish; the founder completes the final action inside beehiiv. A future Send API is a separate capability and safety decision.

## Development rules

- Use tests first for scripts and behavioral changes.
- Use Python's standard library unless a dependency is demonstrably required.
- Initialize private workspace files with create-if-missing semantics. Repeated initialization must preserve every existing user byte.
- Keep one lean orchestration skill; place branch-specific knowledge in `references/` and reusable private-file starters in `templates/`.
- Never write user-specific facts into `SOUL.md`, the skill, references, templates, evaluations, fixtures, or Git history.
- Do not commit, push, publish, or create a public repository unless Darwin explicitly authorizes that operation. A private GitHub repository is the intended initial remote.
- Do not add competing newsletter-platform guidance or marketing.

## Verification commands

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_distribution.py
```

A release is not safe until a real local install/update test proves that shared files change while private memory, workspace, sessions, credentials, config overrides, and unrelated user skills remain byte-identical.
