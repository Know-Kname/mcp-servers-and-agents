# MCP Servers and Agents

A portable agent toolkit: 16 MCP servers, 8 subagents, 16 skills, and the
working agreements that hold them together.

Built on two open standards, so the definitions work in whatever client you
use rather than one vendor's:

- **[AGENTS.md](https://agents.md)** — Linux Foundation (Agentic AI
  Foundation) standard for agent instructions. Read natively by Claude Code,
  Codex, Copilot, Cursor, Gemini CLI, Windsurf, Zed, Amp, and Devin.
- **[Agent Skills](https://agentskills.io)** — open standard for packaged
  skills. Claude Code reads `.claude/skills/` natively; other clients read the
  same layout through their compatibility paths.

## Quick Start

1. Copy `mcp.json` into your client's MCP configuration.
2. Replace the `<path-to...>` placeholders with real paths — especially the
   `filesystem` directory list, which is that server's entire security
   boundary. Never a drive root.
3. Set your API keys as **system environment variables**
   (`PERPLEXITY_API_KEY`, `CONTEXT7_API_KEY`, `N8N_API_URL`, `N8N_API_KEY`).
   Leave the `${env:...}` references in the file — they read from the
   environment, so nothing secret is written into the config.
4. Restart your client. MCP servers load at startup.
5. Sign in when prompted for the remote servers (GitHub, Notion, Fabric,
   Foundry, Vercel, Figma). These use OAuth or Entra and store no token.
6. Copy `.claude/agents/` and `.claude/skills/` into your project or
   `~/.claude/`.
7. Verify:

```bash
python3 scripts/validate-mcp-config.py mcp.json
python3 scripts/validate-definitions.py .
```

## Architecture

```text
AGENTS.md                 portable working agreements, every client
  |
  +-- .claude/agents/     8 subagents, isolated context + scoped tools
  |     troubleshooter, security-auditor, mcp-architect,
  |     mcp-health-checker, researcher, code-reviewer,
  |     deploy-coordinator, decision-advisor
  |
  +-- .claude/skills/     16 skills, each a directory with SKILL.md
  |     + bundled scripts/ and references/
  |
  +-- mcp.json            16 MCP servers
  |     Remote HTTP (7): github-official, context7, notion,
  |                      fabric, foundry, vercel, figma
  |     npx (4):         filesystem, memory, sequentialthinking, perplexity
  |     Docker (3):      fetch, git, n8n
  |     Custom Node (2): power-apps, sharepoint
  |
  +-- scripts/            validators, enforced in CI
```

## What's inside

| Component | Count | Description |
|---|---|---|
| MCP Servers | 16 | External tool integrations, 7 needing no local runtime |
| Subagents | 8 | Isolated-context workers with scoped tool grants |
| Skills | 16 | Packaged workflows with bundled scripts |
| Validators | 2 | Config and definition checks, run in CI |

## Documentation

- [Server Catalog](servers/README.md) — all 16 servers with setup and auth
- [Subagent Catalog](agents/README.md) — all 8, and why 8 of the original 16 were dropped
- [Skill Catalog](skills/README.md) — all 16, with what each bundles
- [Rules](rules/README.md) — where the original 14 rules went
- [Architecture](docs/architecture.md) — how the layers connect
- [Troubleshooting](docs/troubleshooting.md) — per-server fixes
- [Adding a Server](docs/adding-a-server.md) — step by step
- [Security](SECURITY.md) — configuring servers safely

## Requirements

- An MCP-compatible client supporting remote HTTP servers with interactive
  sign-in
- Node.js 20+ (npx servers)
- Python 3.11+ (validators; no third-party packages)
- Docker Desktop — only for `fetch`, `git`, `n8n`
- API keys: Perplexity, Context7, n8n. Everything else signs in interactively
  and stores nothing

## Validation

Both validators run in CI and must exit 0.

`validate-mcp-config.py` fails on unresolvable transports, literal credentials
(including inside `Authorization` headers), drive-root filesystem scopes, and
plaintext URLs. It warns on unpinned references, which are a judgment call
rather than a fault.

`validate-definitions.py` fails when a skill is missing `SKILL.md` or required
frontmatter, when a `name` disagrees with its directory or filename, when a
referenced script doesn't exist, or when a catalog count disagrees with what is
on disk. That last check exists because this repo previously advertised 61
definitions it did not contain — documentation drifting from reality is the bug
it is there to prevent.

## License

MIT
