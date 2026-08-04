---
name: auto-deploy
description: Run a deployment safely - pre-flight checks, confirming secrets exist in the target, migration sequencing, and post-deploy verification. Invoke explicitly; this skill never runs on the model's own initiative.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
---

# Deploy

`disable-model-invocation: true` is set deliberately. An agent should never
decide that code looks ready to ship — you invoke this, always.

## Pre-flight — all of it, before anything ships

Run them and cite the output. "Should pass" is not a check.

```bash
scripts/preflight.sh
```

Then confirm what a script cannot:

1. **Green checks on the actual head SHA.** Not an earlier commit, not
   locally-only. Verify the SHA matches what you're shipping.
2. **Secrets exist in the target.** The check people skip, and it fails
   silently — a workflow referencing secrets nobody configured fails every run,
   and the failure reads like a code bug. Confirm *configured*, not *referenced*.
3. **Migrations** applied in order, and reversible.
4. **The rollback path**, concretely, before you need it.

## Sequencing

Order matters when schema and code ship together. Backwards means downtime.

1. Additive schema changes first — new nullable columns, new tables. Backward
   compatible, so old code keeps working.
2. Deploy code tolerating both shapes.
3. Backfill.
4. Destructive changes (drops, renames, NOT NULL) only once nothing reads the
   old shape.

**Never ship a destructive migration alongside the code that depends on it.**
There is no rollback that works.

## Verify after

Exit 0 is not proof it worked.

- Hit the deployed artifact — a real request, a real page load.
- Check runtime logs for errors that only appear under production config.
- Confirm the change is actually live. Cached builds and skipped steps are
  common and quiet.

## If a check fails

Stop and report. Do not deploy around it, and do not deploy while describing
the failure as probably fine.
