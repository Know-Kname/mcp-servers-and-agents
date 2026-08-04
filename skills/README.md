# Skill Catalog

16 skills in [`.claude/skills/`](../.claude/skills/). Each is a directory —
`SKILL.md` plus `scripts/` and `references/` where they earn their place.

Skills follow the [Agent Skills](https://agentskills.io) open standard. Claude
Code reads `.claude/skills/` natively; other clients read the same layout
through their compatibility paths.

Invoke with `/<name>`, or let the model load one when the `description`
matches.

## MCP and infrastructure

| Skill | Purpose | Bundled |
|---|---|---|
| **mcp-health-check** | Config validity, server inventory, prerequisites, doc drift | `health-check.sh` |
| **security-audit** | Credential exposure, permission scope, supply chain | `audit.sh`, threat model |
| **mcp-server-build** | Add or replace a server; scope it correctly | — |

## Core workflow

| Skill | Purpose | Bundled |
|---|---|---|
| **research-organize** | Multi-source research, persisted with sources | — |
| **auto-deploy** | Pre-flight, sequencing, post-deploy verification | `preflight.sh` |
| **doc-pipeline** | Find doc drift; make claims mechanically checkable | — |
| **incident-response** | Stabilise, then diagnose, then write it up | — |

## Platform

| Skill | Purpose | Bundled |
|---|---|---|
| **github-workflow** | Branching, commit bodies, PRs, CI hygiene | `pre-push-check.sh` |
| **vercel-deploy** | Per-environment variables, build settings, preview vs prod | — |

## Development

| Skill | Purpose |
|---|---|
| **code-review** | Ordered by cost of being wrong; concrete failure paths |
| **testing** | Red-green discipline; why green suites miss bugs |
| **debugging** | Reproduce, narrow, confirm the mechanism |
| **api-design** | Resources, status codes, error shapes, idempotency |
| **database-design** | Constraints, reversible migrations, lock behaviour |
| **smart-refactor** | Safety net first; why bulk edits corrupt definitions |

## Research

| Skill | Purpose |
|---|---|
| **perplexity-research** | When paid search is justified, and how to verify it |

## `auto-deploy` cannot self-invoke

It sets `disable-model-invocation: true`. Deploying is a human decision, and a
model should not conclude the code looks ready. You invoke it explicitly.

## Dropped from the original 31

The old catalog listed thirty-one. Fifteen were not carried over — the
business-domain ones (`dataverse-operations`, `sharepoint-operations`,
`alm-pipeline`, `content-workflow`) belong with the real workflows they
describe, and several others (`scaffold-app`, `quick-prototype`,
`project-registry`, `task-orchestrator`, `learning-mode`) were thin enough that
a skill added nothing over asking directly.

Quality was the constraint: sixteen skills carrying working scripts and
specifics beat thirty-one carrying descriptions.

## Adding one

```text
.claude/skills/<name>/
├── SKILL.md          # name + description frontmatter required
├── scripts/          # executable, and referenced from SKILL.md
└── references/       # detail loaded only when needed
```

`name` must match the directory — that is where the `/command` comes from.
Validate with:

```bash
python3 scripts/validate-definitions.py .
```
