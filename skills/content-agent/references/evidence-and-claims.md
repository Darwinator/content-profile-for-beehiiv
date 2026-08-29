# Evidence and Claims

Editorial credibility depends on knowing what a source supports and refusing to make it support more.

## Source classes

Record the source's origin, date, privacy status, and limits.

- **Direct artifact:** document, message, log, screenshot, recording, or dataset available for inspection.
- **Founder recollection:** useful first-hand account whose precision may need checking.
- **Customer statement:** private unless permission and quotation terms are explicit.
- **Observed pattern:** multiple cases; record the sample and avoid implying universality.
- **Experiment or result:** preserve setup, time window, denominator, confounders, and whether the result was replicated.
- **External source:** retain title, author/organization, URL, publication date, and access date where material.
- **Agent inference:** reasoning from evidence, never a source itself.

When returning a draft, show public, non-sensitive URLs in chat by default. For a private or local source, show the source ID and description only. Before display or storage, strip signed query parameters, credentials, tokens, customer identifiers, and any other secret-bearing portion. Skip the list only if the founder asked.

## Claim test

For every consequential claim, ask:

1. What exactly is being asserted?
2. Which source IDs support it?
3. Does the wording match the strength and scope of that evidence?
4. What uncertainty or limitation would change a reader's interpretation?
5. Does privacy, permission, employment, or confidentiality restrict use?
6. Is the claim still current?

Use one of four outcomes:

- **Supported:** publishable as written with source retained.
- **Supported with qualification:** narrow or contextualize the wording.
- **Needs evidence:** show a visible placeholder and ask a focused question.
- **Do not use:** unverifiable, confidential, misleading, or outside permission.

## Quotations and anecdotes

- Never reconstruct a quote from memory and place it in quotation marks.
- Paraphrase only when the meaning is preserved and permission allows it.
- Remove identifying detail only when anonymization does not create a false impression.
- A vivid anecdote can illustrate a claim but cannot prove prevalence.
- Do not combine multiple people into a composite without clear disclosure.

## Numbers and results

Preserve:

- numerator and denominator;
- measurement period;
- baseline or comparison;
- relevant exclusions;
- whether the number is measured, estimated, or recalled;
- material causal uncertainty.

Avoid false precision. “About one in five in this small sample” may be more truthful than an unsupported percentage.

## Product and employer boundaries

Do not expose:

- customer identities or private communications without permission;
- unreleased product details;
- employer-confidential information;
- internal metrics whose publication is unauthorized;
- credentials, tokens, or private URLs;
- another person's work as the founder's first-hand experience.

When provenance or permission is unclear, stop and ask rather than sanitizing by guesswork.

A URL column is never permission to expose a link. If a URL is not clearly public and non-sensitive, leave the public-URL field blank and retain only the private source ID in Editorial Memory.

## Draft notation

Keep unresolved evidence visible using explicit markers such as:

- `[VERIFY: exact result and time window]`
- `[SOURCE NEEDED: claim]`
- `[PERMISSION NEEDED: customer example]`
- `[FOUNDER DECISION: include limitation?]`

A Send Check blocker remains a blocker until resolved or the claim is removed.
