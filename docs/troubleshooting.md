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

### Docker servers (fetch, git, github, notion, n8n)
1. Open Docker Desktop, wait 60s
2. Verify: `docker info`
3. Pull missing images: `docker pull mcp/fetch`

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
