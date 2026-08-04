---
name: doc-pipeline
description: Keep documentation true to the code - finding drift between docs and reality, deciding what is worth documenting, and making claims mechanically checkable. Use after changing behaviour, adding components, or when docs are suspected stale.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Documentation that stays true

Documentation is a liability when it's wrong. A confidently stale doc is worse
than no doc — readers trust it and act on it.

## Find drift first

Drift is usually **counts, paths, and instructions**, not prose:

```bash
python3 scripts/validate-definitions.py .        # catalog counts vs disk
.claude/skills/mcp-health-check/scripts/health-check.sh
```

Then check by hand what scripts can't:

- **Do the instructions actually work?** Follow your own Quick Start literally.
  This repo's told readers to copy files that don't exist, and to replace
  `${env:...}` placeholders with live API keys — both survived because nobody
  executed them as written.
- **Do referenced paths exist?** Directories, scripts, config files.
- **Do documented mechanisms exist?** Cursor never had a `~/.cursor/agents/`
  directory, but the docs pointed at it for months.
- **Are version and product names current?** Renames silently break searches —
  *Azure AI Foundry* → *Microsoft Foundry* 404s every old link.

## Make claims checkable

The durable fix isn't rewriting prose — it's making the claim mechanically
verifiable so it can't rot quietly. A count in a README will drift. A count
that CI compares against disk cannot.

Prefer, in order:
1. A validator that fails CI on the mismatch
2. A generated section
3. Prose, with a date

## What to write

- **Why over what.** The code shows what. Record the constraint, the rejected
  alternative, the failure that motivated the design.
- **Failure signatures.** "Connects but returns nothing → missing Viewer role"
  saves more time than a feature list.
- **What you could not verify.** Explicit uncertainty beats false confidence,
  and tells the next person where to look.

## What not to write

- Line-by-line narration of self-evident code.
- Aspirational documentation — describing what something *should* do. Every
  false claim here started as an intention.
- Duplicated facts. Two copies drift; link instead.

## After changing behaviour

Update in the same commit: the module's own comments, the catalog or index
listing it, counts anywhere, the troubleshooting entry, and CHANGELOG if the
repo keeps one. Docs updated in a later commit are docs that don't get updated.
