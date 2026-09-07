# Content Profile

Your newsletter editor, built for beehiiv and [Hermes](https://hermes-agent.nousresearch.com/).

Content Profile helps you find something worth saying, turn it into a strong issue, and keep improving the next one. It brings publishing guidance and examples I maintain; you bring the business, experience and taste that make the newsletter yours.

It's for founders, small-business owners and people building a newsletter as a side hustle. Write under your own name, start a separate industry publication, or make the newsletter the business. Every issue should be useful to someone who never buys anything from you. This is less suited to hobby writing where commercial intent isn't part of the goal.

## Quick start

Use [Hermes 0.20.6 or newer](https://hermes-agent.nousresearch.com/docs/user-guide/quickstart). Install Content Profile, choose your model for this profile, then start a conversation:

```bash
hermes profile install github.com/Darwinator/content-profile-for-beehiiv --name content-profile
hermes -p content-profile model
hermes -p content-profile
```

The model picker handles provider setup when needed. Content Profile doesn't choose a provider or copy your existing model configuration. Hermes manages any supported shared sign-in separately.

Try: **“I want to start a newsletter, but I'm not sure what it should be about.”**

It uses what you already know and asks focused typed-answer questions where something important is missing. You'll work toward your first issue together. If the material doesn't support one yet, it helps develop the direction and identifies what you need to finish it.

You don't need to connect beehiiv to start writing. When you're ready to move a draft into your account, follow the [connection guide](docs/setup.md#connect-beehiiv).

## Things to ask

These are ordinary messages, not special commands:

- “Here are my notes from this week. What's worth an issue?”
- “This draft feels generic. Tell me what's missing, then help me fix it.”
- “Keep my argument, but make the opening sound more like me.”
- “What should I write next without repeating last week's issue?”

## How it works

Think of an editor who gets to know your publication. It helps choose the angle, develop the argument, check the evidence and improve the draft. Its starting voice is knowledgeable and conversational, closer to a friend with an opinion than a corporate writer. It will also tell you when the material needs more work.

The useful context stays with you between issues: your reader, approved preferences, sources, past drafts and decisions worth remembering. You don't have to manage those records. Lasting changes to what it remembers require your approval; an edit to one issue isn't automatically a new standing preference.

I keep updating the shared skills, guidance and references. The agent can flag available updates, and you choose when to install them:

```bash
hermes profile update content-profile
```

Updates replace the shared material while preserving private editorial records and your profile configuration. Put personal preferences in private memory, not the shared skill files. [More about updates](docs/setup.md#updates).

## Already like your agent?

Keep it. You can copy the [skill folder](skills/content-profile/) into an existing agent or just use the [references](skills/content-profile/references/). The folder includes its license. Another runtime may need to adapt storage and tools; the full Hermes identity, isolation and managed update path don't come with a folder copy. [Reuse details](docs/setup.md#use-the-skill-or-references).

## Price, privacy and control

The profile is free. You pay for your chosen model and any beehiiv plan, tools or hosting you use. Editorial quality varies by model; stronger models generally make better editors.

Your records live where you run Hermes. Your model provider and connected services process the context needed for their work. I don't receive your conversations or drafts unless you share them. Update checks contact GitHub, not an author analytics service, and don't send your editorial records.

The agent can prepare an editable beehiiv draft when your connected tools support it, with your approval and a read-back check. **You decide what gets published. Content Profile doesn't send, schedule or publish.**

## About

I'm [Darwin Binesh](https://x.com/DarwinBinesh), a product manager at beehiiv. Content Profile is independent, not an official beehiiv product. This is an early release; [DM me on Twitter](https://x.com/DarwinBinesh) with feedback, leaving out credentials and private customer information.

This is a **source-available product**, free to use and adapt for your own personal or commercial newsletter, not to repackage or offer as a service. See the [license](LICENSE).

[Editorial approach](SOUL.md) · [Setup and reuse](docs/setup.md) · [Development and tests](docs/development.md)
