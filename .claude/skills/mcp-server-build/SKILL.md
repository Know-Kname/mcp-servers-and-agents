---
name: mcp-server-build
description: Add, replace, or restructure an MCP server entry - choosing between hosted and local transports, scoping toolsets and permissions, and updating the catalogs. Use when integrating a new service or when an existing server entry has gone stale.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch
---

# Add or replace an MCP server

## 1. Check for a hosted endpoint — first, always

The highest-value question, and the easiest to skip. Most vendors now run one,
and it beats every local option: no runtime, no image, OAuth instead of a
stored token, updates server-side.

**Four of this repo's sixteen servers were local until the vendor shipped a
hosted version.** Assume that pattern continues.

Resolve from **first-party sources**:

1. Does the vendor host an endpoint? Exact URL?
2. Auth — OAuth, Entra, bearer token, none?
3. Is the local option deprecated? *(Notion's is explicitly being sunset.)*
4. Vendor's own package, or a third party wrapping their API?
5. GA or preview?

Never transcribe an endpoint URL, image digest, or version tag out of a
summarised source without cross-checking. It fails at connect time, far from
where you introduced it.

## 2. Pick the transport

| Transport | When |
|---|---|
| **Remote HTTP** | Vendor hosts an endpoint — check first |
| npx | Published npm package, no hosted option |
| Docker | Published image; air-gapped or pinned deployment |
| Custom Node/Python | No published server exists |

## 3. Scope it — adding is not finishing

- **Write access needed?** Some servers expose read-only modes (GitHub's
  `/readonly`). Use them for research and review workflows.
- **Every tool needed?** Large servers often support subsets
  (`/mcp/x/{toolset}`). Every loaded tool costs context before work starts.
- **Filesystem servers:** the directory list *is* the security boundary. Name
  specific folders. Never a drive root.

## 4. Keep the server key stable

Tool names derive from the key, so renaming it breaks every skill, subagent,
and rule referencing those tools. When the transport changes underneath, keep
the key — that is why `github-official` kept its name after moving to the
hosted endpoint.

## 5. Validate

```bash
python3 scripts/validate-mcp-config.py mcp.json
```

Errors block: unresolvable transport, literal credential, drive-root scope,
plaintext URL.

## 6. Update the catalogs — they drift silently

- `servers/README.md` — entry with purpose, auth, setup
- `docs/troubleshooting.md` — a section for it, including its silent-failure
  signature
- `README.md` and `docs/architecture.md` — category counts

`.claude/skills/mcp-health-check/scripts/health-check.sh` reports drift between
`mcp.json` and these files. Run it after.

## Building an actual server

Only when no published one exists. Load the `mcp-builder` skill if available —
it covers FastMCP and the TypeScript SDK properly. Design notes that matter
regardless:

- **Tool descriptions are the interface.** The model chooses from them; an
  ambiguous description produces wrong calls no amount of prompting fixes.
- **Return structured content**, not prose the caller has to re-parse.
- **Annotate read-only tools** so clients can offer safe modes.
- **Fail loudly with actionable errors.** "Request failed" tells the model
  nothing it can act on.
