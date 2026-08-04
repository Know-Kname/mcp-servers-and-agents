---
name: incident-response
description: Triage a production incident - stabilise first, diagnose second, and capture what actually happened. Use when something is broken in production and the priority is restoring service rather than understanding it.
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# Incident response

Order matters and it is counterintuitive: **stop the bleeding before you
understand it.** Diagnosis is not the goal during an incident — restored
service is.

## 1. Assess

- What is broken, for whom, since when?
- Is it degrading or stable?
- Is data at risk? That changes everything — it moves rollback from "preferred"
  to "possibly unsafe."

## 2. Stabilise

Prefer the fastest safe reversal:

1. **Roll back** to the last known-good deploy. Usually fastest and safest.
2. **Disable the feature** — flag off, route away.
3. **Forward-fix** only when rollback is impossible (a destructive migration
   already ran) or clearly slower.

Do not debug a live incident in production while users are affected. Restore,
then investigate with the pressure off.

**If a destructive migration ran, stop.** Rolling back code against a changed
schema can compound the damage. Assess data state before any further action.

## 3. Capture before it disappears

Ephemeral evidence, in this order — logs rotate and metrics windows close:

- Error text, verbatim, with timestamps
- The deployed commit SHA
- Recent config or secret changes
- Whether it correlates with a deploy

## 4. Diagnose, after stability

- **What changed?** Most incidents follow a change. Check deploys, config,
  secret rotations, and upstream vendor status.
- Reproduce in a non-production environment.
- Confirm the mechanism — don't stop at a plausible story. A wrong cause means
  a repeat.

## 5. Write it up

```
IMPACT     who was affected, how long
TRIGGER    the change or event that started it
CAUSE      the confirmed mechanism, and how it was confirmed
DETECTION  how it was noticed, and how long that took
FIX        what restored service
PREVENT    the check that would have caught it
```

**"Detection" is the field people skip and the one that pays.** If a human
noticed before monitoring did, that gap is a finding in its own right.

Prevention should be mechanical where possible — a validator, a CI check, an
alert. "Be more careful" is not a preventive control.
