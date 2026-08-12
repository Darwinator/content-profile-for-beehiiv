# Beehiiv Handoff

The v0 integration boundary is an editable local artifact for human review and import into beehiiv.

## Current capability boundary

Beehiiv's first-party MCP documentation described MCP v1 as read-only when checked on 2026-08-12. It supports publication and post context, but the documentation says write capabilities are forthcoming. Verify current first-party documentation and inspect live tools before changing this assumption.

First-party references:

- https://www.beehiiv.com/features/mcp
- https://www.beehiiv.com/features/mcp/getting-started

Until write access is both documented and live-verified:

- use MCP only to read authorized publication/post context;
- do not claim the agent can create or update a beehiiv draft through MCP;
- never send, schedule, or publish;
- do not block the editorial loop on connector access.

The connector is fail-closed: it is shipped disabled with a deliberately nonmatching tool allowlist, and prompts, resources, sampling, and elicitation are disabled. OAuth authentication and enabling are explicit local user actions. Before enabling it, inspect the live tool surface and replace the placeholder only with reviewed read-only tool names. OAuth tokens remain user-owned runtime data.

## Handoff artifact

Use `templates/beehiiv-handoff.md`. Save the private copy under:

```text
$HERMES_HOME/workspace/editorial-memory/drafts/YYYY-MM-DD-working-slug.md
```

Include:

- working title and two bounded alternatives;
- subject-line options;
- preview text;
- issue body in editable Markdown;
- link and asset checklist;
- source/claim notes kept outside the publishable body;
- unresolved blockers or placeholders;
- Send Check verdict;
- founder approval status;
- explicit human next step in beehiiv.

If HTML is useful, generate a separate sibling file while preserving Markdown as the inspectable source. Avoid platform-specific markup whose meaning cannot be reviewed locally.

## Live connector upgrade gate

A future write-capable connector may be added only after all of these pass:

1. first-party documentation confirms the operation and access requirements;
2. live tool discovery confirms exact tool names and schemas;
3. least-privilege filtering exposes draft-only operations;
4. a disposable publication test proves no send, schedule, or publish action is possible;
5. human content approval remains separate from the draft-creation action;
6. local Markdown handoff remains available as a fallback;
7. credential and update-preservation tests remain green.

Do not infer write access from older REST API documentation or from a product announcement about future MCP capability.
