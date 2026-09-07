# Development

Read [AGENTS.md](../AGENTS.md) before editing. This is the product source, not an installed profile or a place for customer data.

## Layout

- `SOUL.md`: identity, voice and boundaries.
- `skills/content-profile/SKILL.md`: the editorial workflow.
- `skills/content-profile/references/`: guidance loaded for the current job.
- `skills/content-profile/templates/`: optional private-file starters.
- `skills/content-profile/scripts/init_workspace.py`: create missing workspace files and preserve legacy skill content during migration.
- `distribution.yaml`: the install/update manifest.
- `config.yaml`: starter settings; existing installed config is preserved by Hermes.
- `LICENSE` and `skills/content-profile/LICENSE`: identical terms for both installation surfaces.

Private publication context, drafts, memories, sessions, credentials and local changes belong in the installed profile, outside the shared distribution paths.

## Check a change

Use Python's standard library and the Hermes executable on your machine:

```bash
python3 scripts/validate_distribution.py --hermes-bin /path/to/hermes
```

The validator runs selected source-hygiene checks and the test suite, including real local install/update tests in disposable Hermes homes. Those tests check preserved private bytes and updated shared files. They don't authenticate with beehiiv or establish editorial quality.

Without Hermes, run static checks only:

```bash
python3 scripts/validate_distribution.py --skip-tests
```

Static checks are not a general secret scanner, YAML schema validator or proof that the agent follows its instructions. Conversation checks should use synthetic context and the actual product instructions, without adding the desired behavior to the user's test prompt. Check a rich opening, a sparse opening, a returning issue and genuinely missing evidence. Keep any author credentials or private material out of fixtures and Git history.

## Local installation

From the clean source checkout:

```bash
hermes profile install . --name content-profile-dev
hermes -p content-profile-dev model
hermes -p content-profile-dev
```

This creates a separate profile; it does not make the checkout a profile. Don't set `HERMES_HOME` to the source directory. For automated tests, use a disposable root with separate HOME and HERMES_HOME, not an existing user's profile.

Use the [setup guide](setup.md) for model, connector and update behavior. Source changes, installing those changes into a private profile and making a public announcement are separate actions.
