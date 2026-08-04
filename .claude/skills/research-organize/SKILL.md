---
name: research-organize
description: Conduct multi-source research and persist the findings so they survive the session - enforcing the cheapest-source-first ladder, first-party sourcing, and a durable written record. Use for any question needing current external information.
allowed-tools: Read, Write, Grep, Glob, WebSearch, WebFetch
---

# Research and persist

Research that lives only in a conversation gets re-done. This produces a
written record with sources.

## The ladder — escalate only on failure

1. **Memory / context** — free. What do you already have?
2. **Context7** (`resolve-library-id` → `query-docs`) — free. Correct for any
   library, framework, SDK, CLI, or cloud service. Use it *even when confident*
   — training data goes stale here first.
3. **WebSearch / WebFetch** — free. Release notes, vendor announcements,
   maintenance status, anything dated.
4. **Perplexity** — **paid**. Only after the above genuinely fail.

Don't skip to the bottom because it's easier; don't stop at the top because you
feel sure.

## Source discipline

**First-party beats everything.** Vendor README or docs site > blog summarising
it > aggregator. When they disagree, first-party wins — and the disagreement is
itself a finding.

**Never transcribe an identifier from a summarised source.** SHAs, digests,
URLs, version numbers, package names must come from the primary source or be
cross-checked. If you can't verify to that standard, say so and recommend
verifying before use.

## Questions people forget to ask

- Still maintained, or deprecated?
- Has the vendor shipped an official version of this third-party thing?
- Is there a hosted endpoint replacing the local install?
- Has it been **renamed**? Renames silently break doc searches — *Azure AI
  Foundry* → *Microsoft Foundry* 404s every old path.
- GA or preview?

## Persist it

Write findings where they'll be found again — the relevant `docs/` file, a
catalog entry, or a dated research note. Record:

```
QUESTION    what was asked
FINDING     the answer, stated directly
SOURCE      first-party URL + date on the page
CONFIDENCE  confirmed / corroborated / single-source
CAVEATS     preview status, version constraints, what's unverified
DATE        when this was checked — findings expire
```

The date matters more than it looks. A finding without one can't be judged
stale, so it gets trusted indefinitely.

## Reporting

Lead with the answer. Quote only load-bearing text — exact config blocks,
normative statements, deprecation notices — not paragraphs of context. Separate
what you **confirmed** from what you **inferred**, and never present the second
as the first.
