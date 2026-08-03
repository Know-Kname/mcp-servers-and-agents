# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT** open a public issue
2. Email: knowledgeknight99@protonmail.com
3. Include a description and steps to reproduce
4. Allow 48 hours for initial response

## Scope

This repository documents MCP server configurations and AI agent definitions. Security concerns include:
- Exposed API keys or tokens in config templates
- Unsafe MCP server permissions
- Agent prompt injection vulnerabilities
- Credential management in skill definitions

---

## Configuring MCP servers safely

An MCP server runs with whatever authority you hand it, and the model decides
when to call it. Most of the risk in a config repo is decided at config time,
not at runtime. Some of this is checked automatically —
`scripts/validate-mcp-config.py` runs in CI and fails the build on the
mechanically detectable cases — but the judgment calls below are yours.

### Scope every server to the least it needs

- **Filesystem access is an allow-list, not a suggestion.** The directories
  passed to a filesystem server are the complete boundary of what the model can
  read and write. Name specific project folders. Never pass a drive root
  (`c:/`, `/`) or a home directory — that exposes every other project plus
  system files. *(CI fails on this.)*
- **Prefer read-only when the work is read-only.** GitHub's server has a
  `/readonly` endpoint; use it for research and review sessions.
- **Load only the tools you use.** Servers with large tool counts often support
  subsets — GitHub's `/mcp/x/{toolset}`. Every loaded tool also costs context
  before any work starts.
- **Request narrow OAuth scopes.** Read-only scopes over read-write wherever
  the provider offers the choice.

### Keep credentials out of the config

- Use `${env:VAR}` references and set the real values as environment variables.
  Never write a literal key into `mcp.json` — this repo is public. *(CI fails
  on recognizable credential formats, including inside `Authorization` headers.)*
- **Prefer OAuth/Entra sign-in over stored tokens.** Seven of the sixteen
  servers here now need no credential at all. Short-lived, per-user, revocable.
- Use scoped, per-server credentials. Never reuse one token across servers.
- Store OAuth tokens in OS-native credential storage (Windows Credential
  Manager, macOS Keychain), not in plaintext config.
- Rotate anything that was ever pasted into a file, a chat, or a terminal
  history — treat it as disclosed.

### Treat tool definitions as untrusted input

Tool names, descriptions, and parameter schemas are fed to the model as
instructions. A malicious or compromised server can hide directives there
("tool poisoning"), and a server that behaved yesterday can change its
definitions tomorrow ("rug pull").

- Install servers only from vendors you already trust. Prefer the vendor's own
  hosted endpoint over a third-party wrapper of the same API.
- **Verify the package name before installing.** Typosquatting on
  near-miss npm/PyPI names is a known vector.
- Treat the *entire* schema as an injection surface, not just `description`.
- Don't blanket-enable auto-approval for tool calls. "Always allow" on a
  write-capable tool removes the last human check.
- Re-review a server's tools when it changes behavior unexpectedly.

### Pin what you can

Unpinned references drift between launches. `@latest` re-resolves every time,
and an untagged Docker image is whatever the registry currently serves — which
means the code you audited is not necessarily the code that runs next week.
Pin to a verified version where reproducibility matters. *(CI warns on these
rather than failing, since the tradeoff against staying patched is a judgment
call.)*

### Remote server notes

- Require `https`. *(CI fails on plaintext URLs.)*
- Confirm the endpoint hostname against the vendor's own documentation before
  adding it. A hosted MCP endpoint receives whatever the model sends it.
- Hosted servers act with *your* identity. Access is bounded by your own roles
  (Fabric and Foundry are RBAC-scoped and audit-logged under your account), so
  review what that identity can reach before connecting.

### Before you commit

```bash
python3 scripts/validate-mcp-config.py mcp.json
```

Checks transports resolve, credentials are referenced rather than embedded,
filesystem scopes are not drive roots, and URLs are https. It is a floor, not a
substitute for reading the diff.
