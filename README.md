# Content Agent for founders publishing on beehiiv

A dedicated Hermes profile that acts as a private, longitudinal editorial partner for solo founders and small-business owners publishing useful newsletters on beehiiv.

> It learns your business. We keep teaching it publishing.

This repository is the clean profile-distribution source. It contains the agent's identity, operating procedure, maintained editorial guidance, templates, and safety tests. It deliberately does **not** contain a founder's private publication history, sources, drafts, credentials, conversations, or Editorial Memory.

This is an independent product. It is not an official beehiiv product and does not imply beehiiv endorsement or privileged access.

## Current product slice

The first vertical slice supports:

1. publication onboarding and confirmation;
2. evidence-aware source capture;
3. no more than three worthwhile editorial opportunities;
4. collaborative Issue Brief development;
5. drafting and Send Check review;
6. an editable Markdown handoff for manual work in beehiiv;
7. inspectable learning proposals that require human approval.

It may say that something is not worth publishing yet. It never sends, schedules, or publishes.

## Architecture and ownership

### Distribution-owned

```text
distribution.yaml
SOUL.md
config.yaml
skills/content-agent/
```

These files are copied into an installed Hermes profile and may be replaced by an explicit distribution update.

### User-owned

```text
$HERMES_HOME/workspace/editorial-memory/
$HERMES_HOME/memories/
$HERMES_HOME/sessions/
$HERMES_HOME/auth.json
$HERMES_HOME/.env
$HERMES_HOME/local/
$HERMES_HOME/state.db
```

The included real install/update test places byte-pinned sentinels across these surfaces and verifies that shared intelligence updates while all private sentinels remain hash-identical.

## Repository map

```text
.
├── AGENTS.md
├── README.md
├── SOUL.md
├── config.yaml
├── distribution.yaml
├── scripts/
│   └── validate_distribution.py
├── skills/
│   └── content-agent/
│       ├── SKILL.md
│       ├── references/
│       ├── scripts/
│       │   └── init_workspace.py
│       └── templates/
└── tests/
```

Read `AGENTS.md` before editing. It contains the product contract, ownership boundary, and collaboration rules.

## Validate the source

Use the actual Hermes executable available on the machine:

```bash
HERMES_BIN=/path/to/hermes python3 scripts/validate_distribution.py
```

This runs:

- static distribution and credential-hygiene checks;
- reference and manifest contract checks;
- create-if-missing Editorial Memory initialization tests;
- a real isolated `hermes profile install` / `hermes profile update` preservation test.

Static-only validation is available for review environments without Hermes:

```bash
python3 scripts/validate_distribution.py --skip-tests
```

## Install a local dogfood profile

Install from the clean checkout into a separate named profile:

```bash
hermes profile install . --name content-agent --yes
```

Resolve the installed home through the profile runtime rather than assuming a global path. Do not point `HERMES_HOME` at this repository.

Initialize blank private Editorial Memory inside the installed profile:

```bash
HERMES_HOME=/path/to/profile \
python3 /path/to/profile/skills/content-agent/scripts/init_workspace.py
```

The initializer uses create-if-missing semantics. Re-running it leaves every existing user-authored byte unchanged.

## Start the profile

```bash
hermes -p content-agent
```

The first prompt should be a normal conversation, for example:

> Help me set up the publication you will work on with me.

The agent should initialize Editorial Memory, ask one focused question at a time, distinguish confirmed facts from inferences, and seek confirmation before saving durable publication strategy.

## Beehiiv connector boundary

The distribution includes an optional disabled Beehiiv MCP configuration. Beehiiv's first-party documentation described MCP v1 as read-only when verified on 2026-08-12. The connector is fail-closed: it ships disabled with a deliberately nonmatching tool allowlist, and prompts, resources, sampling, and elicitation are disabled. A human must authenticate, inspect the live tool names, replace the placeholder with reviewed read-only tools, and only then enable it. It does not provide draft creation, scheduling, or publishing in this release.

The v0 deliverable is an editable local Markdown handoff for human review and manual import into beehiiv. A future write-capable integration must pass the upgrade gate in `skills/content-agent/references/beehiiv-handoff.md`.

## Collaboration workflow

A second local agent can safely review this checkout if it:

1. reads `AGENTS.md`;
2. inspects current Git status before editing;
3. works only in the clean source checkout, never in the installed profile;
4. does not copy private dogfood artifacts into fixtures or examples;
5. runs the validator before proposing a commit;
6. treats GitHub publishing, profile updates, and connector authentication as explicit side-effect boundaries.

Use branches or Git worktrees for concurrent writes. Do not let two agents edit the risky shared files (`SOUL.md`, `SKILL.md`, `config.yaml`, `distribution.yaml`) simultaneously.

## Status

This is an initial private dogfood scaffold, not a public release. It must complete real How to beehiiv editorial cycles and demonstrate retained-context improvement before cohort expansion or broad product claims.
