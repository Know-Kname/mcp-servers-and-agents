# Adding a New MCP Server

## 1. Choose Transport Type

**Check for a hosted endpoint first.** Most vendors now run one, and it beats every
local option: no runtime to install, no image to pull, OAuth instead of a stored
token, and updates happen server-side. Seven of the sixteen servers here are remote,
and four of those were local until the vendor shipped a hosted version.

| Type | When | Example |
|---|---|---|
| Remote HTTP | Vendor hosts an endpoint (**check first**) | `"url": "https://..."` |
| npx | npm package exists | `npx -y @org/server` |
| Docker | Docker image exists | `docker run -i --rm image` |
| Custom Node | Custom code | `node path/server.js` |
| Python/uvx | Python package | `uvx package-name` |

## 2. Add to mcp.json

Remote (preferred):
```json
"my-server": {
  "url": "https://mcp.example.com/mcp"
}
```

Local, when no hosted endpoint exists:
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
Set API keys as system environment variables. Remote servers using OAuth or Entra
sign-in need no secret at all — if you are adding one for a hosted server, check
whether it actually accepts bearer tokens. Some (Notion's, for one) reject them
outright and only support user OAuth.

## 3b. Scope it

Two questions worth answering before you move on, because both are easy to get
wrong in the direction of "too much access":

- **Does it need write access?** Some servers expose a read-only mode — GitHub's
  has a `/readonly` endpoint. Use it for anything research- or review-shaped.
- **Does it need every tool?** Servers with large tool counts often let you load a
  subset (GitHub's `/mcp/x/{toolset}`). Every tool costs context before any work
  starts, so load what the workflow uses.

For filesystem-style servers, the directory list *is* the security boundary. Name
the specific folders; never pass a drive root.

## 4. Restart Cursor
MCP servers only load on startup.

## 5. Test
Ask the AI to use a tool from the new server.

## 6. Document
Add to the server catalog with name, purpose, type, and required secrets.
