---
name: debugging
description: Systematic bug investigation - reproduce, bisect, confirm the mechanism, and verify the fix against the original failing case. Use when something is broken and the cause is not yet known.
allowed-tools: Read, Grep, Glob, Bash
---

# Debugging

The discipline is refusing to act on a plausible story. Most wasted debugging
time goes into fixing something that was never the cause.

## 1. Reproduce

Reliably, and as small as you can make it. If you cannot reproduce it, you
cannot confirm you fixed it — and "it stopped happening" is not a fix.

Capture the **exact** error text. Paraphrased errors send you to the wrong
place.

## 2. What changed?

Most bugs follow a change. Before theorising:

```bash
git log --oneline -20
git diff HEAD~5 -- <suspect-path>
```

`git bisect` beats reasoning when the history is long — it is mechanical and it
cannot talk itself into a wrong answer.

## 3. Narrow before theorising

Bisect the *system*, not just the history: is it the data, the config, or the
code? Confirm the failing layer before reading code in it.

Check the boring causes first — they are boring because they're common:

- Config change that never took effect (process not restarted)
- Environment variable missing in this environment but present in another
- Stale build or cached artifact
- A dependency that resolved to a different version than expected

## 4. Confirm the mechanism

The bar: **you can explain why it fails, and make it fail on demand.**

If you cannot make the bug appear and disappear by toggling your suspected
cause, you have a correlation, not a diagnosis.

Add instrumentation at the boundary between "known good" and "known bad" rather
than scattering logs. Narrow the interval; don't sample it randomly.

## 5. Fix and verify against the original case

- Fix the cause, not the symptom. Silencing an error usually relocates the bug
  to somewhere less obvious.
- **Re-run the original reproduction.** Not a similar case — the exact one.
- Write a regression test that fails without the fix (see `/testing`).
- One change at a time. Batched fixes hide which one worked, and you will need
  to know that later.

## Report

```
SYMPTOM   observed behaviour, verbatim
CAUSE     the confirmed mechanism, and how you confirmed it
FIX       the change
EVIDENCE  original repro now passing, with output
```

If the cause is unconfirmed, say so and list what you ruled out. An
unconfirmed diagnosis stated as fact is worse than an open question.
