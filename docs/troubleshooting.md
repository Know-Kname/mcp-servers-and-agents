# Troubleshooting Guide

## Quick Diagnostics

```
MCP NOT WORKING?
|
+-- 1. Restart Cursor (fixes most issues)
+-- 2. Check Docker: docker info
+-- 3. Validate JSON: Get-Content ~/.cursor/mcp.json | ConvertFrom-Json
+-- 4. Check env vars: PERPLEXITY_API_KEY, GITHUB_PERSONAL_ACCESS_TOKEN
+-- 5. Clear npm cache: npm cache clean --force
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
- Install Azure CLI: `winget install Microsoft.AzureCLI`
- Login: `az login`

### power-apps / sharepoint
- Check Azure creds in mcp.json
- Verify DATAVERSE_URL / SHAREPOINT_SITE_URL
- Ensure app registration has API permissions

### context7
- Call `resolve-library-id` first, then `query-docs`
- Use specific questions, not keywords

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
