# Adding a New MCP Server

## 1. Choose Transport Type

| Type | When | Example |
|---|---|---|
| npx | npm package exists | `npx -y @org/server` |
| Docker | Docker image exists | `docker run -i --rm image` |
| Custom Node | Custom code | `node path/server.js` |
| Remote SSE | Cloud endpoint | `"url": "https://..."` |
| Python/uvx | Python package | `uvx package-name` |

## 2. Add to mcp.json

```json
"my-server": {
  "command": "npx",
  "args": ["-y", "@org/mcp-server"],
  "env": {
    "API_KEY": "${env:MY_API_KEY}"
  }
}
```

## 3. Set Secrets
Set API keys as system environment variables.

## 4. Restart Cursor
MCP servers only load on startup.

## 5. Test
Ask the AI to use a tool from the new server.

## 6. Document
Add to the server catalog with name, purpose, type, and required secrets.
