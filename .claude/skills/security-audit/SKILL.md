---
name: security-audit
description: Audit MCP and agent configuration for credential exposure, over-broad permission scope, and supply-chain risk. Use before committing config changes, when adding a server, or on a periodic sweep. Reports findings for a human to act on.
allowed-tools: Read, Grep, Glob, Bash
---

# Security audit

Reports findings. Does not remediate — silently "fixing" a security finding
hides it from the person who has to decide whether the scope was intentional.

## Mechanical pass first

```bash
scripts/audit.sh
```

Wraps `scripts/validate-mcp-config.py` and adds repo-wide credential scanning.
This is the **floor**. It catches literal credentials, drive-root filesystem
scopes, plaintext URLs, and broken transports. Everything it cannot judge is
below.

## The judgment pass

### Scope — ask "why this much?"

- **Filesystem allow-lists are the entire security boundary.** Every entry
  should be a specific working directory. A drive root or home directory
  exposes every other project plus system files.

  *This shipped in this repo.* `filesystem` had `c:/` as a root — read/write
  over the whole drive. It is why the validator exists, and it is the first
  thing to check on any filesystem-style server.

- **Write access nobody needs.** GitHub's server has `/readonly` and
  per-toolset endpoints. Research and review workflows should use them.
- **Tool count.** `/mcp/x/all` can expose 100+ tools. Every one costs context
  before work starts and widens the blast radius of a bad call.
- **OAuth scopes.** Read-only where the provider offers the choice.

### Credentials — ask "what happens when this leaks?"

- Anything literal in a committed config is **disclosed**. This repo is public.
- Long-lived service-principal secrets are the highest-value target here.
  `power-apps` and `sharepoint` carry `AZURE_CLIENT_SECRET` and are the only
  standing long-lived credentials left in this stack.
- Prefer OAuth/Entra: short-lived, per-user, revocable, stores nothing. Seven
  servers here already need no credential at all.
- Anything ever pasted into a file, chat, or shell history is disclosed.
  Rotate it — don't reason about whether anyone saw it.

### Supply chain — ask "whose code is this?"

- A third-party wrapper where the vendor ships their own server. *Happened
  here:* `fabric` ran a community package while Microsoft shipped an official
  one.
- Package names, character by character. Typosquatting near-miss npm/PyPI names
  is a known vector.
- Unpinned refs (`@latest`, untagged images): the code you audited is not
  necessarily the code that runs next week.
- Deprecated upstreams stop getting security fixes. `notion`'s local server is
  explicitly being sunset by Notion.

### Tool definitions are untrusted input

Names, descriptions, and parameter schemas are fed to the model as
instructions. Treat the **whole schema** as an injection surface, not just
`description`. Flag blanket auto-approval on any write-capable tool — that
removes the last human check.

## Severity

| Level | Meaning |
|---|---|
| **CRITICAL** | Live credential exposed, or drive-root/home filesystem scope |
| **HIGH** | Long-lived secret where OAuth exists; unnecessary write access |
| **MEDIUM** | Over-broad tool loading; unpinned refs; deprecated upstream |
| **LOW** | Cheap hardening |

## Reporting

```
[SEVERITY] file:line — finding
  RISK      what an attacker or accident gets
  EVIDENCE  the actual line or command output
  FIX       specific change (do not apply it)
```

End with what you checked and found **clean**. An audit listing only problems
doesn't tell the reader what coverage they got.

## Reference

`references/threat-model.md` — the MCP-specific attack classes and the controls
that address them.
