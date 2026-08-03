# MCP Server Catalog

16 servers across 4 categories powering AI-assisted development.

> Transport note: the category once called "Remote SSE" is now **Remote HTTP**.
> Current MCP clients connect to hosted servers over Streamable HTTP; SSE is the
> legacy transport. In Cursor's `mcp.json` a remote server is still just a `url`
> entry — the client negotiates the transport — so no config change is needed
> beyond the name.

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
| **notion** | `mcp/notion` | Notion pages, databases, blocks |
| **n8n** | `mcp/n8n` | Workflow automation orchestration |

### Setup
```bash
docker pull mcp/fetch
docker pull mcp/git
docker pull mcp/notion
docker pull mcp/n8n
```

### Required Secrets
- `NOTION_API_KEY` -- notion.so/my-integrations
- `N8N_API_URL` + `N8N_API_KEY` -- from your n8n instance

> **github-official moved out of this category.** It used to run as a local
> Docker container against a PAT. It now points at GitHub's hosted server —
> see below. The Docker image is still published and still works; it is
> documented as a fallback rather than the default.

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

> These two carry a long-lived `AZURE_CLIENT_SECRET` in the environment. The
> newer `foundry` server below uses interactive Entra ID sign-in instead and
> stores no secret at all. If/when these servers are rebuilt, workload identity
> or `DefaultAzureCredential` would remove the standing secret.

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

## Remote HTTP Servers (no local install)

| Server | URL | Purpose | Auth |
|---|---|---|---|
| **github-official** | `https://api.githubcopilot.com/mcp/` | GitHub API (issues, PRs, repos, code search, Actions, security) | OAuth |
| **foundry** | `https://mcp.ai.azure.com` | Microsoft Foundry models, projects, agents | Entra ID |
| **vercel** | `https://mcp.vercel.com` | Vercel deployments, domains, env vars | OAuth |
| **figma** | `https://mcp.figma.com/mcp` | Figma design files, components, tokens | OAuth |

---

## github-official (GitHub's hosted MCP server)

**Default entry:**
```json
"github-official": {
  "url": "https://api.githubcopilot.com/mcp/"
}
```

Sign-in happens through OAuth on first use. There is no `GITHUB_PERSONAL_ACCESS_TOKEN`
to create, store, or rotate, and the server updates itself — the pinned-container
drift problem goes away.

The server key stayed `github-official` deliberately. Tool names are derived from
it, so keeping the key means existing rules and agent definitions that reference
these tools keep working unchanged.

### Toolset scoping (the main tuning knob)

The default endpoint loads the **default** toolset: `context`, `repos`, `issues`,
`pull_requests`, `users`. Every toolset is also addressable as its own endpoint,
which is how you keep tool count — and therefore context cost — under control.

| Pattern | Effect |
|---|---|
| `/mcp/` | Default toolset |
| `/mcp/x/all` | Every available tool |
| `/mcp/x/{toolset}` | One toolset only (single name, **not** comma-separated) |
| `/mcp/readonly` | Default toolset, read-only |
| `/mcp/x/{toolset}/readonly` | One toolset, read-only |

Available toolsets: `actions`, `code_quality`, `code_security`, `copilot`,
`copilot_issue_intents`, `copilot_spaces`, `dependabot`, `discussions`, `gists`,
`git`, `github_support_docs_search`, `issues`, `labels`, `notifications`, `orgs`,
`projects`, `pull_requests`, `repos`, `secret_protection`, `security_advisories`,
`stargazers`, `users`.

Two patterns worth knowing:

```json
"github-readonly": { "url": "https://api.githubcopilot.com/mcp/readonly" }
```
Read-only browsing — nothing can write to a repo. Good default for research and
review sessions.

```json
"github-actions": { "url": "https://api.githubcopilot.com/mcp/x/actions" }
```
A single toolset when you only care about CI. Registering narrow endpoints under
separate keys beats loading `x/all` and hoping the model picks well.

### Local Docker fallback

Still supported, and still the right answer for GitHub Enterprise Server, air-gapped
work, or when you want a token you control rather than an interactive login.

```json
"github-official": {
  "command": "docker",
  "args": [
    "run", "-i", "--rm",
    "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
    "-e", "GITHUB_TOOLSETS",
    "-e", "GITHUB_READ_ONLY",
    "ghcr.io/github/github-mcp-server"
  ],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_PERSONAL_ACCESS_TOKEN}",
    "GITHUB_TOOLSETS": "repos,issues,pull_requests,actions",
    "GITHUB_READ_ONLY": ""
  }
}
```

Environment variables the container understands:

| Variable | Purpose |
|---|---|
| `GITHUB_PERSONAL_ACCESS_TOKEN` | Auth credential |
| `GITHUB_TOOLSETS` | Comma-separated toolsets (`all` / `default` accepted) |
| `GITHUB_TOOLS` | Enable specific individual tools |
| `GITHUB_READ_ONLY` | `1` blocks all write tools |
| `GITHUB_HOST` | GHES or ghe.com hostname — prefix with `https://` |
| `GITHUB_OAUTH_CALLBACK_PORT` | OAuth callback port (Docker can do OAuth too) |
| `GITHUB_LOCKDOWN_MODE` | Restrict public-repo content access |
| `GITHUB_INSIDERS` | `true` for early-access tools |

CLI equivalents of the two most useful ones: `--toolsets repos,issues` and `--read-only`.

**On pinning:** GitHub's own docs use the untagged `ghcr.io/github/github-mcp-server`,
which tracks the newest build. If you want reproducibility, pin to a release tag —
the current release is **v1.8.0** (30 Jul 2026). Confirm the exact tag string on the
[releases page](https://github.com/github/github-mcp-server/releases) before pinning;
the container registry also publishes `edge`, `nightly`, `main`, and `sha-<commit>`
tags, and an unverified tag fails at container-resolution time, before the server
ever starts.

**GitHub Enterprise (ghe.com), hosted:**
```json
"github-octocorp": {
  "url": "https://copilot-api.octocorp.ghe.com/mcp",
  "headers": { "Authorization": "Bearer ${env:GITHUB_PERSONAL_ACCESS_TOKEN}" }
}
```

---

## foundry (Microsoft Foundry MCP Server)

**Entry:**
```json
"foundry": {
  "url": "https://mcp.ai.azure.com"
}
```

Cloud-hosted, no infrastructure to deploy. Gives agents read and write access to
Foundry services — models, projects, agents — without calling the backend APIs
directly. Authentication is Microsoft Entra ID using an On-Behalf-Of flow, so it
acts as *you*: there is no client secret in the config and nothing to rotate.

> **Status: public preview.** Provided without an SLA and not recommended for
> production workloads. Pin production automation to the SDK, not to this server.

### Requirements

- Azure subscription with a Foundry project
- **Contributor or higher** on the Foundry project — "Access denied" almost always
  means the role is missing, not that the URL is wrong
- An MCP client that supports remote HTTP servers with interactive sign-in

**Naming:** Microsoft rebranded *Azure AI Foundry* to *Microsoft Foundry*. Docs now
live under `learn.microsoft.com/azure/foundry/`; older `azure/ai-foundry/` paths
redirect or 404.

**Verify it works** — ask the model:

```text
What tools can I use from Foundry MCP Server?
Tell me about the latest models on Foundry
```

### Local alternative: `mcp-foundry`

The hosted server exposes a curated tool set. The open-source
[`azure-ai-foundry/mcp-foundry`](https://github.com/azure-ai-foundry/mcp-foundry)
server goes deeper — **evaluation** and **fine-tuning** tool groups the hosted
endpoint does not cover, plus knowledge/index management against Azure AI Search.
Add it *alongside* `foundry` when you need those:

```json
"foundry-local": {
  "command": "uvx",
  "args": [
    "--prerelease=allow",
    "--from", "git+https://github.com/azure-ai-foundry/mcp-foundry.git",
    "run-azure-ai-foundry-mcp",
    "--envFile", "<path-to>/.env"
  ]
}
```

Tool groups: **Models** (explore, build, deploy) · **Knowledge** (index, document,
query, indexer, data source, skill set, content) · **Evaluation** (text, agent,
agent service) · **Fine-tuning** (jobs, metrics, events, files).

Environment (via `--envFile`):

| Variable | Used for |
|---|---|
| `AZURE_AI_PROJECT_ENDPOINT` | Agent services |
| `AZURE_AI_SEARCH_ENDPOINT` | Knowledge/index tools (required) |
| `SEARCH_AUTHENTICATION_METHOD` | Entra vs key-based (required) |
| `AZURE_AI_SEARCH_API_KEY` | Key-based auth only |
| `AZURE_TENANT_ID` / `AZURE_CLIENT_ID` / `AZURE_CLIENT_SECRET` | Service-principal auth |
| `AZURE_OPENAI_ENDPOINT` / `_API_KEY` / `_DEPLOYMENT` / `_API_VERSION` | Evaluation tools |
| `EVAL_DATA_DIR` | Evaluation output directory |
| `GITHUB_TOKEN` | Model testing (optional) |

Requires `uv` (`pip install uv`). Prefer Entra over `AZURE_CLIENT_SECRET` where you can.

### Related: Azure MCP Server

For Azure resources beyond Foundry — storage, Key Vault, Cosmos, Monitor, and
Foundry extension tools — Microsoft ships a single [Azure MCP Server](https://github.com/microsoft/mcp)
(`servers/Azure.Mcp.Server`) covering all of them. Worth adding if this stack grows
past Foundry into general Azure operations; it overlaps `fabric` and would replace
the hand-rolled `power-apps` / `sharepoint` servers over time.
