# Architecture Guide

Four layers, each with a distinct job. The boundaries matter: putting something
in the wrong layer is the most common way this kind of stack rots.

```text
AGENTS.md            always loaded, every client
    |
.claude/agents/      loaded when delegated to
    |
.claude/skills/      loaded when invoked or matched
    |
mcp.json             tools, available from session start
```

## Layer 1: AGENTS.md — the working agreements

Always in context. Carries what applies to every task regardless of what you
are doing: the research cost ladder, verification standards, code quality,
security, git conventions, working style.

[AGENTS.md](https://agents.md) is a Linux Foundation (Agentic AI Foundation)
standard read natively by Claude Code, Codex, Copilot, Cursor, Gemini CLI,
Windsurf, Zed, Amp, and Devin — plain Markdown, no frontmatter.

**Keep it short.** It costs context on every single turn. Anything that is a
procedure rather than a principle belongs one layer down.

## Layer 2: Subagents — isolated context

8 definitions in `.claude/agents/`. Each runs in its own context window with
its own tool grants and returns a summary, so exploration and audit output
never enter the main conversation.

Two reasons to reach for one:

- **Context preservation.** Work that would flood the main conversation with
  search results or logs you'll never reference again.
- **Constraint.** A tool restriction that changes what the worker *can* do —
  `security-auditor` and `code-reviewer` cannot write; `deploy-coordinator`
  prompts on every action.

Delegation is automatic, driven by the `description` field. There is no routing
table to maintain — which is why the old `master-router` rule was dropped
rather than ported.

## Layer 3: Skills — procedures loaded on demand

16 directories in `.claude/skills/`, each with `SKILL.md` plus `scripts/` and
`references/` where useful. Following the
[Agent Skills](https://agentskills.io) open standard.

The economics are what make this layer worth having: only the `description` is
in context until a skill is actually used. Long reference material costs almost
nothing until needed — the opposite of AGENTS.md.

Progressive disclosure, in three stages:

1. `description` — always visible, this is what triggers loading
2. `SKILL.md` body — loaded on invocation
3. `references/`, `scripts/` — loaded or executed only when the body says to

`auto-deploy` sets `disable-model-invocation: true`, so only a human can start
a deployment.

## Layer 4: MCP servers — the tools

16 servers. Every tool definition occupies context from session start, before
any work happens, so breadth is a standing cost rather than a free option.

- **Remote HTTP (7)**: github-official, context7, notion, fabric, foundry,
  vercel, figma
- **npx (4)**: filesystem, memory, sequentialthinking, perplexity-ask
- **Docker (3)**: fetch, git, n8n
- **Custom Node (2)**: power-apps, sharepoint

The remote tier is the one that grows. Four of these were local until the
vendor shipped a hosted endpoint. Each authenticates interactively rather than
holding a long-lived token, and updates server-side — no image to pull, no
credential to rotate.

That leaves three secrets in the config (`PERPLEXITY_API_KEY`,
`CONTEXT7_API_KEY`, the n8n pair) plus the Azure service-principal credentials
on `power-apps` and `sharepoint` — the only standing long-lived credentials
left.

### Scoping is part of configuration

`github-official` ships pointed at the default toolset. `/mcp/x/all` can expose
100+ tools; per-toolset and read-only endpoints exist so a session can load
what it uses. See the [server catalog](../servers/README.md).

## Which layer does this belong in?

| It is... | Put it in |
|---|---|
| A principle applying to every task | AGENTS.md |
| A procedure with steps | A skill |
| Work needing isolated context or restricted tools | A subagent |
| An external capability | An MCP server |

Getting this wrong is expensive in a specific way: a procedure in AGENTS.md
costs context on every turn forever, while a principle buried in a skill only
applies when that skill happens to load.

## Enforcement

Both validators run in CI:

```bash
python3 scripts/validate-mcp-config.py mcp.json   # config safety
python3 scripts/validate-definitions.py .          # definition integrity
```

The definition validator compares catalog counts against what is on disk.
This repo previously advertised 61 definitions it did not contain; that
drift is now a build failure rather than something a reader discovers.

## Example: research

```text
"Does library X still support Y?"
  -> AGENTS.md says cheapest source first
  -> delegated to `researcher` (isolated context)
  -> Context7 answers it; Perplexity never touched
  -> returns sourced finding, not fetched pages
  -> /research-organize persists it with a date
```

## Example: config change

```text
"Add server Z"
  -> /mcp-server-build: hosted endpoint? scope? key stability?
  -> validate-mcp-config.py
  -> `security-auditor` reviews scope (cannot edit)
  -> catalogs updated; health-check.sh confirms no drift
```
