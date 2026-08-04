---
name: code-review
description: Review a diff for correctness, security, and fit before opening a PR - ordered by cost of being wrong, with concrete failure paths rather than speculation. Use after writing or modifying code.
allowed-tools: Read, Grep, Glob, Bash
---

# Code review

## Scope it

```bash
git diff --stat && git diff
```

Read the surrounding code too. A diff read in isolation is how you miss that a
"fix" contradicts an invariant established forty lines up.

## Order — cost of being wrong, descending

### Correctness
- Does it do what the commit message claims?
- Edge cases: empty, null, zero, single element, boundaries.
- Error paths handled, or swallowed by a bare `catch {}`?
- Async: unhandled rejections, races, missing `await`.
- Dates: `toISOString()` for a local date is an off-by-one day in every
  non-UTC timezone. A recurring, quiet bug.

### Security
- Credentials in code or config.
- Injection surfaces: SQL, shell, path traversal.
- Scope — does this grant more access than the task needs?
- New dependencies: maintained? correct name?

### Does it actually run
- **Self-referential definitions.** Bulk regex edits can rewrite the definition
  they match, producing infinitely recursive functions and circular type
  aliases that look fine in a diff. Read the definition sites of anything a
  bulk edit touched.
- Do referenced files, scripts, and paths exist?
- Do types hold, or is a cast hiding a mismatch?

### Fit
- Matches surrounding naming, structure, idiom?
- Reuses existing utilities, or reimplements them? Search before accepting a
  new helper.
- Comments explain *why*, at the density of their neighbours.

### Tests
- Coverage for new logic.
- **Does the test fail without the fix?** A test passing either way tests
  nothing — the most common defect in test additions.

## Verify, don't infer

Run the type-checker, linter, and tests if you can, and cite the output. A
finding from reading alone is still worth reporting — say that's what it is.

## Report

```
[CRITICAL|HIGH|MEDIUM|LOW] file:line
  WHAT   the defect, one sentence
  WHY    concrete failure: inputs or state -> wrong output
  FIX    the specific change
```

Every finding needs a **concrete failure path**. "This could break" without one
is speculation, and speculation dressed as a finding wastes the author's time.

End with what you reviewed and found clean, so the author knows their coverage.
