# Content Agent for founders publishing on beehiiv

Your newsletter's editor, running in your own AI agent. Content Agent is a [Hermes](https://hermes-agent.nousresearch.com/) profile that takes a founder from "I signed up for beehiiv but I don't know what to write" to a real first issue: five short questions, a publication direction you can correct, three researched issue options, and a complete draft with a welcome email and signup copy — in one sitting.

> It learns your business. We keep teaching it publishing.

It is opinionated where it saves you time (weekly default, one welcome email, no automation machinery on day one) and honest where it matters: it cites what its recommendations are based on, refuses ideas that aren't worth publishing yet, and **never sends, schedules, or publishes** — you always press send.

## Quick start

```bash
# 1. Install Hermes (skip if you have it)
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 2. Install Content Agent as an isolated profile
hermes profile install github.com/Darwinator/content-agent-for-beehiiv --name content-agent --yes

# 3. Start talking
hermes -p content-agent
```

Open with something like: *"I signed up for beehiiv because I think I should start a newsletter, but I don't really know what it should be yet."* The agent takes it from there. You bring your own model (any Hermes-supported provider) and your own beehiiv account; nothing about your business ever leaves your machine.

## What you get

- **A finite kickoff** — exactly five questions, one at a time. "I don't know yet" is a valid answer to every one of them.
- **A publication brief you approve** — reader, promise, territories, boundaries. Provisional and reversible, not homework.
- **Maintained editorial judgment** — recommendations grounded in researched mechanism cards from real founder-led newsletters (Big Desk Energy, The Bootstrapped Founder, and others), applied as transferable rules, never "write like X."
- **A complete first issue in the first sitting** — plus a welcome email draft, signup copy, and a runway of your next issue directions.
- **A private editorial memory** — your publication's decisions, sources, and taste survive across sessions and product updates, byte-for-byte.
- **An honest beehiiv bridge** — when you connect beehiiv's MCP, the agent can create editable drafts in your account with your explicit approval and read-back verification. Publishing stays yours.
- **Restraint** — it will tell you when an idea isn't worth publishing yet, and what would change that.

This repository is the clean product source: identity, operating procedure, maintained editorial guidance, templates, and safety tests. It deliberately contains **no** founder's private data — your publication history, sources, drafts, credentials, and Editorial Memory live only in your installed profile.

Content Agent is an independent product. It is not an official beehiiv product and does not imply beehiiv endorsement or privileged access.

## Status

Early and honest: this is a `0.1.x` release that has completed full clean-install founder journeys in testing. Expect rough edges; expect fast iteration. Versioned updates replace the shared intelligence while preserving everything private (`hermes profile update content-agent`). Career-builder, expert/service, and creator tracks are on the roadmap after the founder path proves itself in the wild.

## Current product slice

Version `0.1.6` supports:

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

## Install from a local checkout (development)

Install from the clean checkout into a separate named profile:

```bash
hermes profile install . --name content-agent --yes
```

Resolve the installed home through the profile runtime rather than assuming a global path. Do not point `HERMES_HOME` at this repository.

### Choose your model

Content Agent ships no model or provider configuration — it works with whatever provider and model you already use with Hermes. Profiles are isolated, so set the model for this profile once:

```bash
hermes -p content-agent config set model.default <your-model>
hermes -p content-agent config set model.provider <your-provider>
```

or run `hermes -p content-agent` and follow the provider prompt. Any Hermes-supported provider works (OpenRouter, Anthropic, OpenAI, Nous, DeepSeek, xAI, local models, and others). Behavior has been most extensively verified on `gpt-5.6-sol`; strong frontier or near-frontier models are recommended for editorial-judgment quality.

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

## License

Source-available: view, install, and use freely for your own publication (personal or commercial). Do not redistribute or resell the distribution or offer it as a hosted service. See `LICENSE`.
