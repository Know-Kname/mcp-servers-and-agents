---
name: database-design
description: Schema, migration, and query practice - modelling for the constraints you actually need, writing reversible migrations, and avoiding the changes that cause downtime. Use when designing tables, writing migrations, or diagnosing slow queries.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Database design

## Let the database enforce what matters

Constraints in the schema hold regardless of which code path writes. Constraints
in application code hold until someone writes a new path.

- `NOT NULL` wherever a value is genuinely required.
- Foreign keys with explicit `ON DELETE` behaviour — decide it, don't inherit it.
- `UNIQUE` on anything that must not duplicate.
- `CHECK` for enumerable values and ranges.

**`NOT NULL` without a default is a loaded gun.** Every insert must supply the
column, and any code path that doesn't will fail at runtime, not at review.
This exact bug shipped three times in a sibling repo — status columns that were
`NOT NULL` with no default, omitted by their create paths, so every insert
violated the constraint. Either give it a default or verify every writer
supplies it.

## Verify the schema before writing code against it

Don't infer a schema from application types — they drift. Query it:

```sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'your_table'
ORDER BY ordinal_position;
```

Writing to a column that doesn't exist fails only at runtime, and untyped
clients accept it silently.

## Migrations

- **Additive first.** New nullable columns and new tables are backward
  compatible; old code keeps working.
- **Reversible**, or explicitly documented as not.
- **One logical change per migration**, so a rollback is precise.
- Never ship a destructive change with the code depending on it. Split across
  releases: add → deploy tolerant code → backfill → drop.

Order for a rename, which has no safe single-step version:
1. Add the new column
2. Write both
3. Backfill
4. Read from new
5. Stop writing old
6. Drop old

### Locking

`ALTER TABLE` behaviour varies by engine and version, and the difference is
between instant and an outage. Adding a nullable column is usually cheap;
adding `NOT NULL` with a default, changing a type, or adding a constraint that
validates existing rows can rewrite the whole table.

On a large table, verify the lock behaviour for **your** engine version before
running it in production.

## Indexes

- Index foreign keys. Unindexed FKs make joins and cascading deletes slow, and
  it is the most common missing index.
- Composite index column order follows query predicate order — leftmost prefix.
- Every index costs write throughput. Add for a measured query, not a guess.
- `EXPLAIN ANALYZE` before and after. "Should be faster" is not a measurement.

## Queries

- Never `SELECT *` in application code — it breaks when columns change.
- Watch for N+1: a query inside a loop over results is the usual shape.
- Parameterised queries only. String interpolation into SQL is an injection.
