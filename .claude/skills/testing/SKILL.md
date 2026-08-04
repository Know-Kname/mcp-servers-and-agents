---
name: testing
description: Write tests that would actually catch the bug - red-green discipline, what deserves coverage, and the failure modes that make suites pass while the code is broken. Use when adding tests or when a bug shipped through a green suite.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Testing

## The one rule

**A test must fail before the fix and pass after.** If you didn't watch it
fail, you don't know it tests anything.

This is the single most common defect in test additions: a test written after
the fix, asserting current behaviour, that would have passed before the bug was
found. It adds runtime and false confidence.

```bash
git stash          # remove the fix
npm run test:run   # the new test MUST fail
git stash pop
npm run test:run   # now it passes
```

## What deserves a test

Weight by cost of being wrong, not by ease of writing:

- **Logic that has broken before.** Regression tests are the highest-value
  tests in any suite.
- **Boundaries** — empty, zero, single element, min/max, off-by-one.
- **Timezone- and locale-dependent behaviour.** Date handling breaks in
  non-UTC environments and passes in UTC CI. Pin the timezone in test config
  and assert against a non-UTC zone.
- **Error paths.** Usually untested, and where bugs hide.
- **Data transformation boundaries** — case conversion, serialisation, schema
  mapping.

Not worth it: framework behaviour, getters, anything asserting the
implementation rather than the contract.

## Failure modes that keep suites green while code is broken

- **Asserting the implementation.** Tests that mirror the code change whenever
  the code does, and catch nothing.
- **Over-mocking.** Mock the boundary you don't own; mock past that and you're
  testing your mocks.
- **Snapshot tests updated on failure.** A snapshot regenerated without being
  read is not an assertion.
- **Environment set after startup.** Runtimes read some environment at process
  start — setting `TZ` in a setup file can leave the resolved zone unchanged.
  Set it before the runtime initialises and **assert it took effect**, rather
  than assuming.

## Structure

Arrange / act / assert, one behaviour per test. The name should say what breaks
when it fails: `formatDateForInput returns local date, not UTC` beats
`test date formatting`.

## Before claiming coverage

Run the suite and report the real result. If tests fail, say so with the
output — a suite reported as green when it isn't is worse than no suite.
