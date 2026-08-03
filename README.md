# MCP Servers and Agents

A complete, documented AI/MCP infrastructure: 16 servers, 16 agents, 31 skills, and 14 rules working together in Cursor IDE.

This repo captures the full stack of MCP (Model Context Protocol) integrations, AI agent definitions, reusable skills, and behavioral rules that power an advanced AI-assisted development workflow.

## Quick Start

1. Copy `mcp.json` to `~/.cursor/mcp.json`
2. Replace the `<path-to...>` placeholders with real paths — especially the
   `filesystem` directory list, which is that server's entire security boundary
3. Set your API keys as **system environment variables** (`PERPLEXITY_API_KEY`,
   `CONTEXT7_API_KEY`, `N8N_API_URL`, `N8N_API_KEY`). Leave the `${env:...}`
   references in the file as they are — they read from the environment, so
   nothing secret is ever written into the config
4. Restart Cursor
5. Sign in when prompted for the remote servers (GitHub, Notion, Fabric,
   Foundry, Vercel, Figma) — these use OAuth/Entra and need no stored token
6. Verify: `python3 scripts/validate-mcp-config.py ~/.cursor/mcp.json`

> Step 3 previously read *"replace placeholder secrets (`${env:...}`) with your
> actual API keys"* — which would write live credentials into a file this repo
> then asks you to commit. `${env:VAR}` exists precisely so that never happens.
>
> **What this repo actually ships:** `mcp.json`, the catalogs under `servers/`,
> `agents/`, `skills/`, and `rules/`, and the docs. The agent, skill, and rule
> **definitions are not in the repo** — those directories hold catalogs
> describing them, not the `.mdc`/`SKILL.md` files themselves. Contributing them
> is tracked as follow-up work.

## Architecture

```
Cursor IDE
  |
  +-- mcp.json (16 MCP servers)
  |     +-- npx servers (filesystem, memory, sequential-thinking, perplexity)
  |     +-- Docker servers (fetch, git, n8n)
  |     +-- Custom Node servers (power-apps, sharepoint)
  |     +-- Remote HTTP servers (github-official, context7, notion,
  |     |                        fabric, foundry, vercel, figma)
  |
  +-- rules/ (14 behavioral rules)
  |     +-- master-router.mdc (routes tasks to right tool/skill/agent)
  |     +-- research-workflow.mdc (cost-optimized research hierarchy)
  |     +-- code-quality.mdc (TypeScript/React coding standards)
  |     +-- ... 11 more
  |
  +-- agents/ (16 specialized agents)
  |     +-- troubleshooter, researcher, code-reviewer...
  |
  +-- skills/ (31 reusable workflows)
        +-- scaffold-app, auto-deploy, research-organize...
```

## What's Inside

| Component | Count | Description |
|---|---|---|
| MCP Servers | 16 | External tool integrations (GitHub, Foundry, Notion, Vercel, etc.) |
| Agents | 16 | Specialized AI personas for different tasks |
| Skills | 31 | Reusable workflow templates |
| Rules | 14 | Behavioral guidelines that shape AI responses |

## Documentation

- [Server Catalog](servers/README.md) -- all 15 servers with setup instructions
- [Agent Catalog](agents/README.md) -- all 16 agents with descriptions
- [Skill Catalog](skills/README.md) -- all 31 skills by category
- [Rule Catalog](rules/README.md) -- all 14 rules with summaries
- [Architecture Guide](docs/architecture.md) -- how everything connects
- [Troubleshooting Guide](docs/troubleshooting.md) -- common issues and fixes
- [Adding a New Server](docs/adding-a-server.md) -- step-by-step guide

## Requirements

- [Cursor IDE](https://cursor.com) (or any MCP-compatible client that supports
  remote HTTP servers with interactive sign-in)
- Node.js 20+ (for npx-based servers)
- Docker Desktop (only for `fetch`, `git`, `n8n`)
- API keys: Perplexity, Context7, n8n, Azure AD (optional)
- Interactive sign-in: GitHub (OAuth), Notion (OAuth), Fabric (Entra ID),
  Foundry (Entra ID), Vercel, Figma — no stored tokens. A GitHub PAT is only
  needed for the Docker fallback or GitHub Enterprise; see the
  [server catalog](servers/README.md).
- `uv` only if you add the optional `foundry-local` server

## License

MIT
