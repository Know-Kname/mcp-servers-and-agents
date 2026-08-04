---
name: mcp-health-check
description: Check the health of every configured MCP server - validate mcp.json, inventory servers by transport, verify local prerequisites, and detect drift between the docs and the actual config. Use after editing mcp.json, before committing config changes, or when a server stops working.
allowed-tools: Read, Grep, Glob, Bash
---

# MCP health check

Reports health. Changes nothing — a check that edits what it measures is not a
check.

## Run it

```bash
scripts/health-check.sh
```

One command, covering config validity, the server inventory, local
prerequisites, and doc drift. Everything below explains how to read the output.

## Reading the results

### Errors vs. warnings

`validate-mcp-config.py` separates them deliberately:

- **Errors** — the server cannot work. Unresolvable transport, literal
  credential, drive-root filesystem scope, plaintext URL.
- **Warnings** — a judgment call, not a fault. Untagged Docker images and
  `@latest` refs trade reproducibility against staying patched. Report them;
  don't "fix" them reflexively.

### Prerequisites by transport

You cannot confirm a remote server is reachable without signing in, and this
skill does not try. It reports what each transport *needs*, so a human can
check the part that requires their identity.

| Transport | Needs | Silent-failure signature |
|---|---|---|
| Remote HTTP | Interactive sign-in complete | No tools appear — looks broken |
| `docker` | Daemon running | "Connection refused" |
| `npx` | Node 20+, network on first run | Hangs on first resolution |
| Custom Node | Script path exists, env set | ENOENT |

**The most common false alarm:** debugging Docker for a server whose entry is
`{"url": ...}`. Remote servers never touch Docker. If someone is pulling images
for `github-official` or `notion`, they are reading a stale config.

### Doc drift is a real finding

Counts and catalogs drift silently, and they are where people look. A server in
`mcp.json` with no `servers/README.md` entry, or a documented server that no
longer exists, is worth reporting even though nothing is "broken".

## Reporting

```
CONFIG      valid / invalid (validator exit code)
SERVERS     N total (N remote, N local)
ERRORS      each, with file:line
WARNINGS    each, with the tradeoff it represents
PREREQS     docker/node status; sign-ins a human must confirm
DOC DRIFT   counts or entries disagreeing with mcp.json
```

State what you could **not** verify. Remote reachability and auth status are
outside what this sees; calling a stack healthy on the strength of "its config
parses" would be misleading.

## Related

- `/security-audit` — permission scope and credential exposure
- `docs/troubleshooting.md` — per-server fixes
- `troubleshooter` subagent — when something is actually broken
