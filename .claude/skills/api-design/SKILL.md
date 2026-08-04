---
name: api-design
description: Design HTTP APIs that are hard to misuse - resource modelling, status codes, error shapes, pagination, idempotency, and versioning. Use when adding or changing an endpoint, or reviewing an API surface.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# API design

The goal is an interface that is hard to misuse. Consistency beats cleverness:
callers learn one pattern and apply it everywhere.

## Match what exists

Before designing anything, read the neighbouring endpoints. A "better" pattern
introduced next to three existing ones makes four patterns, and every caller
now has to know which is which. Consistency with the surrounding API almost
always wins.

## Resources and methods

- Nouns, plural: `/invoices`, `/invoices/{id}/payments`.
- Verbs in the method, not the path. `POST /invoices/{id}/void` is acceptable
  for a genuine action that isn't CRUD; `/getInvoice` is not.
- `GET` must be side-effect free. `PUT` and `DELETE` must be idempotent.
- Nest only to show ownership, and only one level. Deeper nesting encodes
  assumptions that break when the model changes.

## Status codes that mean something

| Code | Meaning |
|---|---|
| 200 / 201 / 204 | Success / created / success-no-body |
| 400 | Malformed request |
| 401 / 403 | Not authenticated / authenticated but not allowed |
| 404 | Not found — **also** use for "exists but you can't see it," so you don't leak existence |
| 409 | Conflict with current state |
| 422 | Well-formed but semantically invalid |
| 429 | Rate limited — always include `Retry-After` |

Never return 200 with an error in the body. Every client's error handling
depends on the status line.

## Errors are an interface

Callers parse these. Design them once, keep them stable:

```json
{
  "error": {
    "code": "insufficient_funds",
    "message": "Human-readable, safe to display",
    "field": "amount",
    "request_id": "req_01H..."
  }
}
```

- A **stable machine code** — clients branch on it, so it cannot change.
- A message safe to show a user. Never leak internals, SQL, or stack traces.
- `request_id` on every response, success or failure. Without it, supporting a
  reported failure means guessing.

## Pagination

Cursor-based by default. Offset pagination skips and duplicates rows when the
underlying data changes mid-iteration — which it does, in exactly the cases
where pagination matters.

Return the cursor and whether more exists. Never return an unbounded list;
enforce a maximum page size regardless of what was requested.

## Idempotency

Any operation that creates or moves money needs an idempotency key. Networks
retry; clients retry. Without a key, a retried `POST` charges twice.

Store the key with its result and return the original response on replay —
don't just suppress the duplicate.

## Versioning

Version when you must break; add optional fields when you can. Adding an
optional field is compatible; removing one, renaming one, or narrowing a type
is not. Treat response shapes as contracts.
