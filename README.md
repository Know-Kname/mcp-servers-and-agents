# MCP Servers and Agents

A complete, documented AI/MCP infrastructure: 15 servers, 16 agents, 31 skills, and 14 rules working together in Cursor IDE.

This repo captures the full stack of MCP (Model Context Protocol) integrations, AI agent definitions, reusable skills, and behavioral rules that power an advanced AI-assisted development workflow.

## Quick Start

1. Copy `mcp.json` to `~/.cursor/mcp.json`
2. Replace placeholder secrets (`${env:...}`) with your actual API keys
3. Restart Cursor
4. Copy agent definitions from `agents/` to `~/.cursor/agents/`
5. Copy rules from `rules/` to `~/.cursor/rules/`

## Architecture

```
Cursor IDE
  |
  +-- mcp.json (15 MCP servers)
  |     +-- npx servers (memory, sequential-thinking, perplexity, context7)
  |     +-- Docker servers (fetch, git, github, notion, n8n)
  |     +-- Custom Node servers (filesystem, power-apps, sharepoint)
  |     +-- Remote SSE servers (vercel, figma)
  |     +-- Python/uvx servers (fabric)
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
| MCP Servers | 15 | External tool integrations (GitHub, Notion, Vercel, etc.) |
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

- [Cursor IDE](https://cursor.com) (or any MCP-compatible client)
- Node.js 20+ (for npx-based servers)
- Docker Desktop (for Docker-based servers)
- Python 3.11+ with `uv` (for Fabric server)
- API keys: GitHub PAT, Perplexity, Notion, Azure AD (optional)

## License

MIT
