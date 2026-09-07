# Beehiiv handoff

Load this when the user wants to work in beehiiv. Writing does not depend on a connection. Use the user's live MCP tools and current first-party documentation, not a remembered capability list.

## Connect when needed

Read https://www.beehiiv.com/features/mcp/getting-started. The canonical OAuth endpoint is https://mcp.beehiiv.com/mcp.

The Hermes starter config is disabled, `trust: untrusted`, with `tools.include: []`. Prefer the native in-app consent/authorization flow, such as `setup_mcp`, and review the selected tools. For a user operating the CLI, target their actual profile name (shown here as `content-profile`):

```bash
hermes -p content-profile mcp login beehiiv
hermes -p content-profile mcp configure beehiiv
```

Keep the server disabled until authentication and selection succeed. Verify that `tools.include` contains explicit selected tool names; selecting everything can remove the filter. Leave send, schedule and publish tools unselected. An empty list exposes no tools on Hermes >=0.20.6; older versions are unsupported. Then:

```bash
hermes -p content-profile config set mcp_servers.beehiiv.enabled true
hermes -p content-profile mcp test beehiiv
```

Start a fresh session or use `/reload-mcp` where supported, then return to the prepared draft. A connectivity test isn't proof of a successful draft handoff. On authentication or selection failure, preserve the draft and continue local work. Existing config is preserved by distribution updates; review specific connector settings rather than replacing the user's config or reinstalling their profile.

## Before a write

Inspect the live tool name, description, schema and read/write annotations. Consult current beehiiv docs for unclear capabilities or plan requirements. If authority or support is unclear, keep the work local.

Content Profile never publishes, schedules, or sends. The user completes those actions in beehiiv. For another external mutation:

1. Prepare the work, then show the exact target and intended change, including a consequential irreversible effect.
2. Obtain explicit approval for that operation and target. Content approval is not action approval.
3. Execute once. An unknown outcome is not permission to retry.
4. Read back the exact target and verify the requested state before claiming success. Report an error or unknown outcome plainly and ask before another attempt.

Keep those distinctions in the issue record; they aren't a status report to recite in every conversation.

## Deliver the draft

Return the work inline and save an editable private copy. `templates/beehiiv-handoff.md` is a starter, not a field-completion requirement. In Hermes, use:

```text
$HERMES_HOME/workspace/editorial-memory/drafts/YYYY-MM-DD-working-slug.md
```

This local Markdown fallback remains available if MCP is unavailable, unauthenticated, permission-blocked, plan-blocked, missing an operation or uncertain. Outside Hermes, use the private workspace already agreed with the user.

For a complete handoff, include the title, subject, preview text and issue body, with any material source/claim notes, unresolved facts and the next human action outside the publishable body. Offer alternatives when useful, not to fill a quota. An editable draft is not a configured or published newsletter. Preserve Markdown if generating a sibling HTML file.

## Sources

Show a short useful source list in chat with the draft unless the user asks to skip it. Say what each source supports. Include a public, non-sensitive URL where appropriate; reader-facing links belong in the issue only where readers benefit.

For private/local material, use an ID and description without its URL. Omit signed URLs, credentials, tokens, customer identifiers and unnecessary private paths from display and saved artifacts. Keep safe private provenance in Editorial Memory. If disclosure is uncertain, omit the link and ask.
