# Rules

**The rules moved.** They are now [`AGENTS.md`](../AGENTS.md) at the repo root.

## Why

The original 14 rules were Cursor `.mdc` files — a Cursor-only mechanism, in a
stack that no longer uses Cursor.

[AGENTS.md](https://agents.md) is a Linux Foundation (Agentic AI Foundation)
open standard, adopted by 60,000+ repositories and read natively by Claude
Code, Codex, Copilot, Cursor, Gemini CLI, Windsurf, Zed, Amp, and Devin. Plain
Markdown, no frontmatter. The same content now works in every client instead of
one.

## Where each rule went

| Original rule | Now |
|---|---|
| agentic-workflow | AGENTS.md — verification over intention |
| research-workflow | AGENTS.md — the cost ladder; `/research-organize` |
| code-quality | AGENTS.md — code quality |
| github-standards | AGENTS.md + `/github-workflow` |
| deployment-safety | AGENTS.md + `/auto-deploy` |
| environment-context | AGENTS.md — what this repo is |
| productivity-patterns | AGENTS.md — working style |
| mcp-troubleshooting | `docs/troubleshooting.md` + `troubleshooter` subagent |
| mcp-server-design | `/mcp-server-build` |
| automation-patterns | Folded into the skills that use it |
| design-system | Dropped — project-specific, belongs with its project |
| power-platform-patterns | Dropped — domain-specific |
| **master-router** | **Dropped** — see below |
| **multi-agent-coordination** | **Dropped** — see below |

## The two that were dropped rather than ported

**master-router** dispatched tasks to the right tool, skill, or agent. That is
no longer a rule's job: Claude Code routes on subagent and skill `description`
fields. A hand-maintained routing table would drift out of sync with the
definitions and start sending work to the wrong place.

**multi-agent-coordination** prevented file conflicts between concurrent
agents. Subagents run in isolated contexts, and worktree isolation exists for
agents that genuinely need to write in parallel. The rule was solving a Cursor
problem.

## Adding guidance

- Applies to any agent, any client → **AGENTS.md**
- A procedure with steps → a **skill** in `.claude/skills/`
- Delegation-shaped work needing its own context → a **subagent**
