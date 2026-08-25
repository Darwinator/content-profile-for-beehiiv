# Beehiiv Handoff

The current integration boundary is inline delivery plus an editable local artifact for human review and use inside beehiiv.

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

There is no “approve and send” flow. Approval is the founder's content decision; the founder completes the final send inside beehiiv. The beehiiv MCP rule remains no send, schedule, or publish. A future Send API or another write-capable connector may eventually support bounded direct actions, but that is not a current capability and must not be promised.

The connector is fail-closed: it is shipped disabled with a deliberately nonmatching tool allowlist, and prompts, resources, sampling, and elicitation are disabled. OAuth authentication and enabling are explicit local user actions. Before enabling it, inspect the live tool surface and replace the placeholder only with reviewed read-only tool names. OAuth tokens remain user-owned runtime data.

## Handoff artifact

Show the completed draft inline first, then use `templates/beehiiv-handoff.md` to save the private editable copy under:

```text
$HERMES_HOME/workspace/editorial-memory/drafts/YYYY-MM-DD-working-slug.md
```

## Sources by default

Show a short source list **in chat with the draft**, unless the founder asked to skip it. Each line: what the source supports, and the URL.

In the **issue body**, add a reader-facing link only where a subscriber would click. Do not turn the issue into a footnote paper. Do not leave URLs only in the private ledger.

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
