# MCP threat model — the config owner's view

Most MCP guidance targets people *implementing* servers. This covers what
someone *configuring and consuming* them controls. Grounded in the OWASP MCP
Security Cheat Sheet and the MCP specification's security guidance.

## Attack classes

### Tool poisoning
Malicious instructions hidden in a tool's name, description, or parameter
schema. These are fed to the model as instructions, so the whole schema is an
injection surface — not just `description`.

**Controls:** install only from trusted vendors; review tool schemas before
approving; never blanket-auto-approve write-capable tools.

### Rug pull
A server that behaved correctly changes its tool definitions later. You audited
one thing; something else is running now.

**Controls:** pin versions where reproducibility matters; re-review when a
server changes behavior unexpectedly; prefer vendors with a deprecation policy.

### Typosquatting
Near-miss npm/PyPI package names. A single wrong character installs someone
else's code with your credentials.

**Controls:** verify package names character by character; prefer the vendor's
own hosted endpoint over any local package.

### Over-scoped filesystem access
The directory allow-list is the complete boundary. A drive root exposes every
project on the machine plus system files.

**Controls:** name specific working directories; never a drive root or home.
*Enforced* — `validate-mcp-config.py` fails the build on this.

### Credential exposure
Literal credentials in a committed config are disclosed permanently.

**Controls:** `${env:VAR}` references only; OS-native credential storage for
tokens; prefer OAuth so there is nothing to store. *Partly enforced* — the
validator fails on recognizable credential formats, including behind an auth
scheme in an `Authorization` header.

### Confused deputy
A server with broad ambient authority is manipulated into acting beyond what
the requester should be able to do.

**Controls (config side):** prefer servers that act with *your* identity and are
RBAC-scoped — Fabric and Foundry are audit-logged under the calling account, so
they cannot exceed access you already have. Avoid servers holding standing
elevated credentials shared across users.

## Control summary

| Control | Enforced by |
|---|---|
| No drive-root filesystem scope | CI (error) |
| No literal credentials in config | CI (error) |
| HTTPS-only remote endpoints | CI (error) |
| Transport resolves | CI (error) |
| Version pinning | CI (warning) |
| Least-privilege tool/scope selection | Human review |
| Vendor trust and package verification | Human review |
| Tool-schema inspection | Human review |
