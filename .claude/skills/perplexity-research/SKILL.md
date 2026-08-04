---
name: perplexity-research
description: Use Perplexity deliberately and last, after the free research tiers have failed. Covers when paid search is actually justified, how to write a query worth paying for, and how to verify what comes back. Use when cheaper sources could not answer the question.
allowed-tools: Read, WebSearch, WebFetch
---

# Perplexity, used deliberately

Perplexity is the **paid** tier. This skill exists to make its use a decision
rather than a reflex.

## Justify it first

Before querying, confirm all three failed:

1. **Context7** — free, and correct for libraries, frameworks, SDKs, CLIs,
   cloud services. Most "I need to search" questions end here.
2. **WebSearch** — free. Vendor announcements, release notes, dated material.
3. **WebFetch on the first-party source** — free. If you know the vendor, fetch
   their docs directly instead of asking anyone about them.

**Perplexity is justified when:** the question spans many sources needing
synthesis; the landscape is genuinely contested; you need current information
where you don't know which source holds it.

**It is not justified for:** anything a vendor documents (fetch the vendor);
anything Context7 indexes; a question you can answer from context; a fact you
just want confirmed — cross-check the primary source instead.

## Write a query worth paying for

One good query beats three vague ones, and costs a third as much.

- **Be specific about scope and recency.** "What changed in X between v2 and
  v3" beats "tell me about X".
- **Name the decision.** "Which of A or B for <constraint>" gets a comparison;
  "A vs B" gets a feature list.
- **Ask for sources explicitly** so you can verify.
- **Don't ask it to fetch one page.** That's WebFetch, and free.

## Verify what comes back

Synthesised answers are exactly where identifiers get corrupted.

- **Never take an identifier from the synthesis.** Version numbers, package
  names, endpoint URLs, SHAs — follow the citation to the primary source.
- **Check citation dates.** Confident answers get built on stale posts.
- **Confirm anything load-bearing** against the vendor before acting.
- **Note disagreement between cited sources** rather than accepting the
  synthesis's resolution of it.

## Record it

Perplexity results are paid artifacts. Persist them via `/research-organize` so
the same question isn't bought twice.
