# Content Agent for founders publishing on beehiiv

A dedicated Hermes profile that acts as a private, longitudinal editorial partner for solo founders and small-business owners publishing useful newsletters on beehiiv.

> It learns your business. We keep teaching it publishing.

This repository is the clean profile-distribution source. It contains the agent's identity, operating procedure, maintained editorial guidance, templates, and safety tests. It deliberately does **not** contain a founder's private publication history, sources, drafts, credentials, conversations, or Editorial Memory.

This is an independent product. It is not an official beehiiv product and does not imply beehiiv endorsement or privileged access.

## Current product slice

Version `0.1.4` supports:

1. a finite five-question founder/business kickoff and confirmation;
2. evidence-aware source capture;
3. no more than three worthwhile editorial opportunities;
4. collaborative Issue Brief development;
5. drafting and Send Check review;
6. inline draft delivery, a private Markdown fallback, and approved beehiiv actions when the user's live MCP tools support them;
7. a persistent lean-launch checklist covering beehiiv readiness, capture, welcome, promotion, preview/test, approval, and founder-completed sending;
8. inspectable learning proposals that require human approval.

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

The agent should initialize Editorial Memory, orient the founder, ask exactly five typed questions one at a time, show setup progress and the launch path, turn uncertainty into reversible choices, and seek confirmation before saving durable publication strategy.

## Beehiiv connector boundary

The distribution points to beehiiv's canonical OAuth MCP endpoint but ships disabled, untrusted, and with `tools.include: []`, so it exposes no server tools until the user reviews the live surface. Read the current first-party setup guide at https://www.beehiiv.com/features/mcp/getting-started and connect to https://mcp.beehiiv.com/mcp. After authentication, run live discovery and select only the tools needed for the user's job.

Hermes `>=0.20.6` is recommended: earlier versions treat an empty `tools.include` list as no filter once a server is enabled, which would expose the full tool surface without review. The shipped connector is disabled, so nothing is exposed until a human enables it — on older Hermes versions, always complete tool selection (`hermes mcp configure beehiiv`) in the same step as enabling, and never enable the server with the include list still empty.

Note for existing installs: `hermes profile update` preserves the profile's `config.yaml`, so connector-config changes in a new release do not reach an already-installed profile automatically. Until a migration path exists, apply config changes by reinstalling the profile fresh or by reviewing and merging the new `config.yaml` manually.

The profile does not freeze a beehiiv capability list. It directs the agent to inspect the live tools and current first-party documentation, use only supported operations, request explicit approval for mutations, and read back the exact target before claiming success. As a stable product policy, Content Agent must never publish, schedule, or send. A private local Markdown fallback remains available whenever the requested operation is unavailable or blocked.

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
