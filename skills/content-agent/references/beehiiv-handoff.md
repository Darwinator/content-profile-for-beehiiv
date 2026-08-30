# Beehiiv Handoff

Content Agent uses beehiiv through whatever current MCP tools the user's installation actually exposes. The product does not freeze a tool inventory or infer capabilities from an old release note.

## Authoritative setup reference

Read the current first-party setup guide:

- https://www.beehiiv.com/features/mcp/getting-started

Connect using beehiiv's canonical OAuth endpoint:

- https://mcp.beehiiv.com/mcp

In Hermes, the distributed connector is disabled, marked `trust: untrusted`, and has `tools.include: []`. This exposes no server tools by default. After the user authenticates, inspect the live tools and let the user select the minimum tools needed for their job through the normal Hermes MCP configuration flow.

### Connecting when the founder is ready

Offer this only when draft handoff or a beehiiv job actually needs it — never as a setup prerequisite for editorial work. Prefer a native in-product consent/authorization flow when the runtime provides one (for example a `setup_mcp` enable/authorize card). Otherwise walk the founder through the CLI:

```bash
hermes mcp login beehiiv        # opens beehiiv's OAuth page in the browser
hermes mcp configure beehiiv    # live tool discovery; select the minimum tools
hermes mcp test beehiiv         # verify the connection works
```

Then start a fresh session (or `/reload-mcp` where supported) so the selected tools load, and return the founder directly to the prepared draft — do not restart onboarding. Complete tool selection before or immediately after enabling the server: on Hermes versions before 0.20.6 an empty `tools.include` list is treated as no filter once the server is enabled, so an explicit selected list must exist by the time the connector is live. If authentication or selection fails, say what actually happened, keep the local draft, and continue.

Do not treat a capability snapshot as durable. Tool names, schemas, plan requirements, and available actions can change. At the point of use:

1. inspect the live tool name, description, schema, and read/write annotations;
2. consult current first-party beehiiv documentation when capability or plan behavior is unclear;
3. use only operations the live installation actually supports; and
4. fail closed when the tool's authority or outcome is ambiguous.

## Stable product policy

Regardless of what a future MCP surface exposes, Content Agent must never publish, schedule, or send. The founder completes those final actions inside beehiiv unless a later explicit product decision changes this policy.

For any other mutating action:

1. prepare the editorial artifact first;
2. show the exact publication or object, intended change, and whether the operation is reversible;
3. obtain explicit approval for that exact mutation;
4. execute once, without blind retry after an unknown outcome;
5. read back the exact target and verify the requested state before claiming success; and
6. report failures or plan/permission limits honestly.

## Local artifact

Show completed editorial work inline first, then use `templates/beehiiv-handoff.md` to save the private editable copy under:

```text
$HERMES_HOME/workspace/editorial-memory/drafts/YYYY-MM-DD-working-slug.md
```

This is the **local Markdown fallback** whenever MCP is unavailable, unauthenticated, permission-blocked, plan-blocked, lacks the requested operation, or returns an unknown outcome. Never block the editorial loop on connector access.

## Sources by default

Show a short source list **in chat with the draft**, unless the founder asked to skip it. Each line says what the source supports and includes a public, non-sensitive URL only when safe.

For private/local material, show the source ID and description without its URL. Strip signed query parameters, credentials, tokens, customer identifiers, and unnecessary private paths before any display or storage. If safety is unclear, omit the URL and ask rather than guessing.

In the issue body, add a reader-facing link only where a subscriber would click. Public sources should remain inspectable; private provenance remains in Editorial Memory.

## Action state machine

1. **Prepared** — inline work, private fallback, source notes, and Send Check exist.
2. **Content approved** — founder approves the editorial content. This does not authorize an external mutation.
3. **Capability checked** — current docs and the live tool schema support the requested operation.
4. **Action proposed** — exact target and intended change are shown.
5. **Action approved** — founder explicitly approves this operation for this target.
6. **Submitted** — call the selected live tool once. Do not blind-retry an unknown outcome.
7. **Verified** — read back the exact target and verify the requested state.
8. **Failed or unknown** — report the actual outcome, preserve the local fallback, and ask before any retry.

Do not claim success from an accepted request alone.

## Handoff contents

Include:

- working title and bounded alternatives;
- subject-line options;
- preview text;
- issue body in editable Markdown;
- link and asset checklist;
- source/claim notes kept outside the publishable body;
- unresolved blockers or placeholders;
- Send Check verdict;
- content-approval and action-approval status;
- exact human next step in beehiiv.

If HTML is useful, generate a separate sibling file while preserving Markdown as the inspectable source. Avoid platform-specific markup whose meaning cannot be reviewed locally.
