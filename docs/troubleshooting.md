# Troubleshooting Guide

## Quick Diagnostics

```
MCP NOT WORKING?
|
+-- 1. Restart Cursor (fixes most issues)
+-- 2. Remote server? Check sign-in, not Docker -- 7 of 16 are remote now
+-- 3. Check Docker: docker info   (only fetch, git, n8n need it)
+-- 4. Validate JSON: Get-Content ~/.cursor/mcp.json | ConvertFrom-Json
+-- 5. Check env vars: PERPLEXITY_API_KEY, CONTEXT7_API_KEY, N8N_API_KEY
+-- 6. Clear npm cache: npm cache clean --force
```

## Server-Specific Fixes

### perplexity-ask
- Check PERPLEXITY_API_KEY format: `pplx-xxxx...`
- Keys expire -- regenerate at perplexity.ai/settings/api
- Restart Cursor after config change

### Docker servers (fetch, git, notion, n8n)
1. Open Docker Desktop, wait 60s
2. Verify: `docker info`
3. Pull missing images: `docker pull mcp/fetch`

### github-official (remote)
- No Docker needed — if you are debugging Docker for GitHub, the config is stale.
  The entry should be `{"url": "https://api.githubcopilot.com/mcp/"}`.
- Auth is OAuth on first use. Not signed in -> no tools appear. Re-run the sign-in
  from Cursor's MCP panel rather than adding a PAT.
- Too many tools / context bloat: point at a narrower endpoint, e.g.
  `/mcp/x/repos` or `/mcp/readonly`. See the [server catalog](../servers/README.md).
- Writes rejected: check whether the URL ends in `/readonly`.
- 404 on the endpoint: `/mcp/x/{toolset}` takes exactly one toolset name — a
  comma-separated list is not valid in the URL (only in `GITHUB_TOOLSETS`).
- GitHub Enterprise: the hosted github.com endpoint will not reach it. Use the
  ghe.com Copilot URL, or the Docker fallback with `GITHUB_HOST`.

### foundry
- Public preview — expect tool changes and occasional outages; don't build
  production automation on it.
- "Access denied" / permission errors: you need **Contributor or higher** on the
  Foundry project. The server uses On-Behalf-Of with your Entra ID identity, so
  your own role is what matters.
- Server won't start: confirm the URL is exactly `https://mcp.ai.azure.com`.
- No sign-in prompt: the client must be signed in with a Microsoft account that
  has access to the subscription.
- Searching docs: Microsoft renamed *Azure AI Foundry* to *Microsoft Foundry*.
  Current docs are under `learn.microsoft.com/azure/foundry/`; older
  `azure/ai-foundry/` URLs redirect or 404.
- Need evaluation or fine-tuning tools? The hosted endpoint doesn't expose them —
  add the local `foundry-local` server (see the server catalog).

### fabric
- Now the hosted Core server — `az login` and the Azure CLI are no longer part of
  the path. The entry should be `https://api.fabric.microsoft.com/v1/mcp/core`.
- Connects but returns nothing: you need at least **Viewer** on one Fabric
  workspace. Every call is RBAC-scoped to your own role.
- Connection fails: disconnect and reconnect the server in Cursor to redo the
  OAuth flow. Auth scope is `https://api.fabric.microsoft.com/.default`.
- Preview — configuration may change before GA.
- Need OneLake file operations or offline API specs? Core doesn't cover those.
  That's the local Fabric MCP Server; run both side by side.

### notion
- No Docker and no `NOTION_API_KEY`. The hosted server is **OAuth only** and
  rejects bearer tokens outright — if you're setting a token, the config is stale.
- No tools appear: complete the Notion OAuth sign-in from Cursor's MCP panel.
- Pages missing: the OAuth grant controls which pages are shared with the
  integration. Re-run the authorization and widen the page selection in Notion.
- The old local server still exists but Notion has said it may be sunset and is
  not actively monitored. Don't reintroduce it.

### context7
- Call `resolve-library-id` first, then `query-docs`. Use specific questions,
  not keywords.
- Throttled or rate-limited: set `CONTEXT7_API_KEY` (context7.com/dashboard).
  The key is passed as an `Authorization: Bearer` header, not an env var on a
  local process.
- Using the stdio form instead? The key becomes a `--api-key` CLI flag; OAuth is
  HTTP-only and won't work over stdio.

### filesystem
- "Access denied" outside your project: expected. The trailing args in `mcp.json`
  are the full allow-list of reachable directories — add the directory you need.
- Do **not** re-add `c:/` as a root to make an error go away. That exposes the
  whole drive to the model. Add the specific folder instead.
- No longer runs a hand-built `dist/index.js`; it uses the published
  `@modelcontextprotocol/server-filesystem` package via npx.

### power-apps / sharepoint
- Check Azure creds in mcp.json
- Verify DATAVERSE_URL / SHAREPOINT_SITE_URL
- Ensure app registration has API permissions

## Common Errors

| Error | Fix |
|---|---|
| "Tool not found" | Restart Cursor |
| "401 Unauthorized" | Rotate API key |
| "Connection refused" | Start Docker |
| "ENOENT" | Check file path |
| "Invalid JSON" | Validate mcp.json syntax |
| "Rate limit" | Wait or rotate token |

## Shell Performance
PowerShell profile takes 20-30s. Use file tools instead of shell, set block_until_ms to 60000+, batch commands with &&.
