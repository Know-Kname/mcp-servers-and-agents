---
name: smart-refactor
description: Restructure code without changing behaviour - establishing a safety net first, making mechanical changes reviewable, and avoiding the bulk-edit failures that silently corrupt definitions. Use when consolidating duplication or reshaping an interface.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Refactoring

Refactoring changes structure, not behaviour. The moment behaviour changes it
is a rewrite, and it needs a rewrite's testing.

## Establish the safety net first

If the code has no tests, **write characterisation tests before touching it** —
tests that assert what it does now, right or wrong. Without them you cannot
distinguish "refactored" from "broke it subtly."

Confirm the suite passes *before* you start. Starting from red means you can
never tell what you caused.

## Is this worth doing?

Duplication is only worth removing when the copies change together. Two things
that look alike but change for different reasons should stay separate —
premature consolidation couples them, and the next change has to fight it.

Good reasons: the same edit must be made in several places; a bug was fixed in
one copy and not the others; the shape actively obstructs work.

Not good reasons: it looks repetitive; a pattern would be more elegant.

## Bulk edits are where this goes wrong

A regex applied across a file **matches its own definition site**. Replacing a
call pattern rewrites the function that implements it, producing infinite
recursion or a circular type alias — both of which look plausible in a diff and
compile-fail somewhere confusing.

This is not hypothetical: a single refactor pass produced both a self-recursive
helper and two self-referential type aliases (`type CreateInput<T> =
CreateInput<T>`), each from a regex that matched its own definition.

Rules:
- **Exclude definition sites** from the pattern, or fix them immediately after.
- **Read the diff of the definition**, specifically. Don't skim the call sites
  and assume the rest.
- Run the type-checker after every bulk edit, not at the end.

## Work in reviewable steps

- One transformation per commit. A commit mixing a rename with a behaviour
  change cannot be reviewed or reverted cleanly.
- Green after every step — type-check, lint, test. Not just at the end.
- Migrate one caller first and review it before doing the remaining twenty.
  If the pattern is wrong, you find out after one, not twenty.

## Verify equivalence

- Full suite green, with the same assertions as before.
- Where a test needed changing, ask hard whether behaviour changed. A test
  edited to accommodate a refactor is the usual sign that it did.
- For pure functions, run old and new against the same inputs and diff.

## Know when to stop

Refactoring competes with the work it was meant to enable. If the safety net
doesn't exist and building it costs more than the change is worth, say so and
scope the change smaller instead of proceeding without one.
