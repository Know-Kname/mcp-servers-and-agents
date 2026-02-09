# MCP Server Catalog

15 servers across 4 categories powering AI-assisted development.

## npx-based Servers (Node.js required)

| Server | Package | Purpose | Cost |
|---|---|---|---|
| **memory** | `@modelcontextprotocol/server-memory` | Persistent knowledge graph across sessions | Free |
| **sequentialthinking** | `@modelcontextprotocol/server-sequential-thinking` | Multi-step reasoning and problem decomposition | Free |
| **perplexity-ask** | `@perplexity-ai/mcp-server` | Web research, fact verification, deep analysis | Paid |
| **context7** | `@upstash/context7-mcp@latest` | Library/framework documentation lookup | Free |

### Setup
```bash
# Auto-install on first use via npx. Just need Node.js 20+
node --version
```

### Required Secrets
- `PERPLEXITY_API_KEY` -- get from perplexity.ai/settings/api

---

## Docker-based Servers (Docker Desktop required)

| Server | Image | Purpose |
|---|---|---|
| **fetch** | `mcp/fetch` | Fetch and parse web pages |
| **git** | `mcp/git` | Git operations on local repos |
| **github-official** | `ghcr.io/github/github-mcp-server` | GitHub API (issues, PRs, repos, code search) |
| **notion** | `mcp/notion` | Notion pages, databases, blocks |
| **n8n** | `mcp/n8n` | Workflow automation orchestration |

### Setup
```bash
docker pull mcp/fetch
docker pull mcp/git
docker pull ghcr.io/github/github-mcp-server
docker pull mcp/notion
docker pull mcp/n8n
```

### Required Secrets
- `GITHUB_PERSONAL_ACCESS_TOKEN` -- github.com/settings/tokens
- `NOTION_API_KEY` -- notion.so/my-integrations
- `N8N_API_URL` + `N8N_API_KEY` -- from your n8n instance

---

## Custom Node.js Servers

| Server | Purpose |
|---|---|
| **filesystem** | Read/write/search local files |
| **power-apps** | Microsoft Dataverse / Power Apps queries |
| **sharepoint** | SharePoint file and list operations |

### Required Secrets (Azure AD)
- `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`
- `DATAVERSE_URL` (power-apps), `SHAREPOINT_SITE_URL` (sharepoint)

---

## Python/uvx Server

| Server | Package | Purpose |
|---|---|---|
| **fabric** | `microsoft-fabric-mcp` | Microsoft Fabric lakehouse queries |

### Setup
```bash
pip install uv
az login
```

---

## Remote SSE Servers (no local install)

| Server | URL | Purpose |
|---|---|---|
| **vercel** | `https://mcp.vercel.com` | Vercel deployments, domains, env vars |
| **figma** | `https://mcp.figma.com/mcp` | Figma design files, components, tokens |
