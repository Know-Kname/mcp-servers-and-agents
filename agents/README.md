# Subagent Catalog

8 subagents in [`.claude/agents/`](../.claude/agents/). Each runs in its own
context window with its own tool grants, so side work — searching, auditing,
researching — stays out of the main conversation.

Claude Code delegates automatically based on the `description` field, or you
can name one directly.

## Problem-solving

| Subagent | Purpose | Constraint |
|---|---|---|
| **troubleshooter** | One entry point for MCP, Docker, config, and error failures | — |

## Infrastructure

| Subagent | Purpose | Constraint |
|---|---|---|
| **mcp-architect** | Design and restructure MCP server entries | Researches upstream before recommending |
| **mcp-health-checker** | Validate config, inventory servers, detect drift | Diagnosis only |
| **security-auditor** | Credential exposure, permission scope, supply chain | `disallowedTools: Write, Edit` |

## Development

| Subagent | Purpose | Constraint |
|---|---|---|
| **code-reviewer** | Correctness, security, and fit review | `disallowedTools: Write, Edit` |
| **deploy-coordinator** | Pre-flight, sequencing, rollback | `permissionMode: default` |

## Research and decisions

| Subagent | Purpose | Constraint |
|---|---|---|
| **researcher** | Current external information, sourced | Enforces the cost ladder |
| **decision-advisor** | Architecture and technology choices | Recommends one option |

## Why some grants are restrictive

The constraints are load-bearing, not decoration:

- **`security-auditor` and `code-reviewer` cannot write.** A reviewer that
  silently fixes what it finds removes the human decision about whether the
  finding was intentional.
- **`deploy-coordinator` prompts on every action.** An agent should never
  conclude that code looks ready to ship.
- **`mcp-health-checker` is read-only.** A health check that edits the thing it
  measures is not a health check.

## Dropped from the original 16

The old catalog listed sixteen. Eight were not carried over:

| Dropped | Reason |
|---|---|
| planner, file-finder | Already covered by built-in Plan and Explore |
| productivity-coach | No delegation-shaped work — it was advice, not a task |
| design-sync, issue-tracker, automation-builder | Would have been invented content |
| dataverse-expert, power-platform-specialist | Domain-specific; better as personal skills where the real workflows live |

A subagent earns its place when a task would otherwise flood the main context,
or when a tool restriction genuinely changes what it can do. Splitting work
across agents that don't need separate contexts costs more than it saves.

## Adding one

Create `.claude/agents/<name>.md` with `name` and `description` frontmatter.
The `description` is what triggers automatic delegation — write it as *when to
use this*, not *what it is*. Validate with:

```bash
python3 scripts/validate-definitions.py .
```
