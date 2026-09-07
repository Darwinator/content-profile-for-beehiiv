# Setup and reuse

## Model and profile

Install and start from the [README quick start](../README.md#quick-start). Use `hermes -p content-profile model` to choose a provider and model for this profile. Distribution installation is not a clone of your default profile. Hermes may reuse a supported shared sign-in, but that is separate from model configuration.

Profiles keep configuration, conversations and memory separate; they are not filesystem sandboxes. Run the agent in a suitable working directory and keep private editorial files out of this source checkout. See [Hermes profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles) for Desktop, messaging and other profile entry points.

## Connect beehiiv

Writing and research work without this connection. Set it up when you want a draft in beehiiv.

1. Read [beehiiv's MCP setup guide](https://www.beehiiv.com/features/mcp/getting-started). The endpoint is `https://mcp.beehiiv.com/mcp`.
2. Prefer Hermes's in-app consent flow to authorize the existing beehiiv connection and review its tool selection. Content Profile ships with the connection disabled and no tools allowed.
3. If using the CLI, authenticate and choose the tools while the connection remains disabled:

   ```bash
   hermes -p content-profile mcp login beehiiv
   hermes -p content-profile mcp configure beehiiv
   ```

4. Confirm that `mcp_servers.beehiiv.tools.include` contains an explicit list of the selected live tool names. An empty list allows no tools on supported Hermes versions; a missing filter allows all tools. Leave sending, scheduling and publishing tools unselected. If discovery or selection fails, keep the connection disabled.
5. After successful selection, enable and test it:

   ```bash
   hermes -p content-profile config set mcp_servers.beehiiv.enabled true
   hermes -p content-profile mcp test beehiiv
   ```

Start a fresh conversation, or use `/reload-mcp` on a surface that supports it. Return to your draft; no new onboarding is needed. A connection test checks connectivity, not whether a particular writing action succeeded.

Content Profile checks the live tools rather than shipping a fixed capability list. It asks for approval of the exact target and change before an external write, then reads the result back. A local editable draft remains available if authentication, permissions or a requested action get in the way. You handle final preview, testing and sending in beehiiv.

## Updates

```bash
hermes profile update content-profile
```

Updates replace the distributed identity, skills, references and license. Your editorial workspace, memory, sessions, credentials, local overrides and unrelated skills remain yours. Hermes preserves existing `config.yaml` even though the manifest includes a starter config for new installs.

When an update changes suggested connector settings, review and apply those specific settings in the installed profile. Keep your model, credentials and tool choices. Reinstalling or deleting the profile isn't the default remedy. Shared skill edits may be replaced; put personal preferences in private memory or a separate local skill.

Older installs may still contain `skills/content-agent/`. Initialization moves a recognized legacy skill, including customizations, to `local/legacy-skills/content-agent/` inside that profile. It preserves uncertain identities, symlinked paths and an existing archive rather than deleting or overwriting them. If an old skill remains active, review it before choosing a cleanup action.

## Use the skill or references

Copy the complete [skill folder](../skills/content-profile/), including its `LICENSE`, into the location your agent uses for skills. Ask that agent to read `SKILL.md`, choose a private workspace with you and map the file/memory operations to its tools. Outside Hermes, skip Hermes profile commands and update checks. If explicitly using the Python initializer, supply your chosen private root with `--hermes-home`; it has no implicit default-home fallback.

You can also point an agent at the repository and ask which guidance would help your existing setup. Reading it is not permission to change your identity, connect accounts or install the full profile.

References are ordinary Markdown. Reuse them without adopting the workflow. The [license](../LICENSE) permits adaptation for your own personal or commercial newsletter, not redistribution as another product or service.
