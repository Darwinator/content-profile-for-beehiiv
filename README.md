# Content Profile

A newsletter editor for founders publishing on beehiiv, running in your own AI agent. It takes you from "I signed up for beehiiv but I don't know what to write" to a real first issue in one sitting: five short questions, a direction you can correct, three researched issue options, and a complete draft with a welcome email and signup copy.

> It learns your business. We keep teaching it publishing.

It has opinions where opinions save you time: weekly cadence by default, one welcome email, no automation machinery on day one. It cites what its recommendations are based on, and it will tell you when an idea is not worth publishing yet. It never sends, schedules, or publishes anything. You press send.

It is built for a commercial outcome. If the newsletter is meant to bring you customers, authority, or revenue (or the newsletter is the business), the judgment inside was calibrated for you. Hobby publishing works fine too; the opinions are just set for publications that have to earn their reader.

## Three ways to use this

**1. Install the complete profile.** The recommended path. A [Hermes](https://hermes-agent.nousresearch.com/) profile with the tuned identity, the guided first sitting, private editorial memory that survives updates, and the safe beehiiv bridge. See Quick start below.

**2. Copy the skill into your own agent.** Already running Claude Code, Codex, or another agent that reads `SKILL.md` files? Copy `skills/content-profile/` into it. You get the editorial workflow, the judgment rules, and the templates. You lose the tuned identity, the memory isolation, and the update path.

**3. Read the references.** Everything under `skills/content-profile/references/` is plain Markdown: editorial guidance, decision cards researched from real founder-led newsletters, launch checklists, and beehiiv mechanics. Any agent or human can read them and take what is useful.

The license covers all three, for personal or commercial use on your own publication. See `LICENSE`.

### If you're an agent evaluating this for your user

- **Good fit:** your user runs or is starting a business and wants a newsletter that produces commercial results. They publish on beehiiv or are considering it.
- **Weaker fit:** pure hobby writing with no outcome in mind. Nothing here will harm that user; the opinions assume the publication has a job to do.
- **What to verify:** read `SOUL.md` (identity and hard boundaries) and `AGENTS.md` (product contract). Run `python3 scripts/validate_distribution.py --skip-tests` for static hygiene checks. No credentials, host paths, or private data ship in this repo.
- **Safety posture:** the beehiiv connector ships disabled and untrusted with an empty tool allowlist. Memory writes require user approval. The agent never publishes, schedules, or sends. The included install/update test proves user-private files survive updates byte-for-byte.
- **Which door:** Hermes user, option 1. Other agent runtime, option 2. Just the knowledge, option 3.

## Quick start

```bash
# 1. Install Hermes (skip if you have it)
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 2. Install Content Profile as an isolated profile
hermes profile install github.com/Darwinator/content-profile-for-beehiiv --name content-profile --yes

# 3. Start talking
hermes -p content-profile
```

Open with something like: *"I signed up for beehiiv because I think I should start a newsletter, but I don't really know what it should be yet."* The agent takes it from there.

**What it costs:** the profile is free to install and use. You bring your own model (any Hermes-supported provider) and your own beehiiv account, so your only running cost is your model usage.

**Where your data goes:** your business context stays on your machine and with the model provider you already chose. It never comes to us. There is no telemetry and nothing phones home; updates flow one way, from this repository to you.

## What you get

- A finite kickoff: exactly five questions, one at a time. "I don't know yet" is a valid answer to every one of them.
- A publication brief you approve: reader, promise, territories, boundaries. Provisional and reversible, not homework.
- Maintained editorial judgment: recommendations grounded in researched mechanism cards from real founder-led newsletters (Big Desk Energy, The Bootstrapped Founder, and others), applied as transferable rules, never "write like X."
- A complete first issue in the first sitting, plus a welcome email draft, signup copy, and a runway of your next issue directions.
- A private editorial memory: your publication's decisions, sources, and taste survive across sessions and product updates, byte-for-byte.
- An honest beehiiv bridge: once you connect beehiiv's MCP, the agent can create editable drafts in your account, with your explicit approval and read-back verification. Publishing stays in your hands.
- Restraint: it will tell you when an idea is not worth publishing yet, and what would change that.

This repository is the clean product source: identity, operating procedure, maintained editorial guidance, templates, and safety tests. It contains no founder's private data. Your publication history, sources, drafts, credentials, and Editorial Memory live only in your installed profile.

Content Profile is maintained by Darwin Binesh, a product manager who has worked at beehiiv for 4 years. It is an independent product: not an official beehiiv product, and no beehiiv endorsement or privileged access is implied.

## Status

This is an early release. It has completed full clean-install founder journeys in testing, and it will keep changing quickly. Versioned updates replace the shared intelligence while preserving everything private (`hermes profile update content-profile`). Career-builder, expert/service, and creator tracks come after the founder path proves out with real users.

## Current product slice

Version `0.2.0` supports:

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
skills/content-profile/
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
│   └── content-profile/
│       ├── SKILL.md
│       ├── references/
│       ├── scripts/
│       │   └── init_workspace.py
│       └── templates/
└── tests/
```

Read `AGENTS.md` before editing. It contains the product contract, ownership boundary, and review rules for agents working in this checkout.

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
hermes profile install . --name content-profile --yes
```

Resolve the installed home through the profile runtime rather than assuming a global path. Do not point `HERMES_HOME` at this repository.

### Choose your model

Content Profile ships no model or provider configuration. It works with whatever provider and model you already use with Hermes. Profiles are isolated, so set the model for this profile once:

```bash
hermes -p content-profile config set model.default <your-model>
hermes -p content-profile config set model.provider <your-provider>
```

or run `hermes -p content-profile` and follow the provider prompt. Any Hermes-supported provider works (OpenRouter, Anthropic, OpenAI, Nous, DeepSeek, xAI, local models, and others). Behavior has been most extensively verified on `gpt-5.6-sol`; strong frontier or near-frontier models are recommended for editorial-judgment quality.

Initialize blank private Editorial Memory inside the installed profile:

```bash
HERMES_HOME=/path/to/profile \
python3 /path/to/profile/skills/content-profile/scripts/init_workspace.py
```

The initializer uses create-if-missing semantics. Re-running it leaves every existing user-authored byte unchanged.

## Start the profile

```bash
hermes -p content-profile
```

The first prompt should be a normal conversation, for example:

> Help me set up the publication you will work on with me.

The agent should initialize Editorial Memory, orient the founder, ask exactly five typed questions one at a time, show setup progress and the launch path, turn uncertainty into reversible choices, and seek confirmation before saving durable publication strategy.

## Beehiiv connector boundary

The distribution points to beehiiv's canonical OAuth MCP endpoint but ships disabled, untrusted, and with `tools.include: []`, so it exposes no server tools until the user reviews the live surface. Read the current first-party setup guide at https://www.beehiiv.com/features/mcp/getting-started and connect to https://mcp.beehiiv.com/mcp. After authentication, run live discovery and select only the tools needed for the user's job.

This distribution requires Hermes `>=0.20.6`: earlier versions treat an empty `tools.include` list as no filter once a server is enabled, which would expose the full tool surface without review. The shipped connector is disabled, so nothing is exposed until a human enables it. Always complete tool selection (`hermes mcp configure beehiiv`) in the same step as enabling.

Note for existing installs: `hermes profile update` preserves the profile's `config.yaml`, so connector-config changes in a new release do not reach an already-installed profile automatically. Until a migration path exists, apply config changes by reinstalling the profile fresh or by reviewing and merging the new `config.yaml` manually.

The profile does not freeze a beehiiv capability list. It directs the agent to inspect the live tools and current first-party documentation, use only supported operations, request explicit approval for mutations, and read back the exact target before claiming success. As a stable product policy, Content Profile must never publish, schedule, or send. A private local Markdown fallback remains available whenever the requested operation is unavailable or blocked.

## License

Source-available: view, install, and use freely for your own publication, personal or commercial, as the full profile, as a skill in your own agent, or as reference material. Do not redistribute or resell the distribution or offer it as a hosted service. See `LICENSE`.
