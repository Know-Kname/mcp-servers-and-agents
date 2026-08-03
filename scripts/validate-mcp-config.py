#!/usr/bin/env python3
"""Validate mcp.json beyond plain JSON syntax.

The CI already checks that mcp.json parses. Parsing is a low bar: an entry can
be perfectly valid JSON and still grant an agent read/write access to an entire
drive, hardcode a live API key, or point at a server that cannot start.

This script encodes the review rules that would otherwise live only in someone's
head. It is deliberately conservative -- it flags things a human should look at
rather than trying to be clever.

Exit codes: 0 = clean or warnings only, 1 = at least one error.

Usage:  python3 scripts/validate-mcp-config.py [path-to-mcp.json]
"""

import json
import re
import sys
from pathlib import Path

# Placeholders are expected in a template repo; they are not real secrets.
PLACEHOLDER = re.compile(r"\$\{env:[A-Z0-9_]+\}|^<.*>$|YOUR_|<username>|<path-to")

# Prefixes used by real credentials. If one of these shows up literally in the
# config, it is almost certainly a live key that should not be committed.
SECRET_PREFIXES = (
    "ghp_", "gho_", "ghu_", "ghs_", "ghr_", "github_pat_",
    "pplx-", "sk-", "secret_", "ntn_", "xoxb-", "xoxp-",
    "AKIA", "AIza",
)

# Roots that expose far more than any single project needs. The directory list
# passed to a filesystem-style server is that server's entire security boundary.
DRIVE_ROOTS = {"/", "\\", "c:/", "c:\\", "d:/", "d:\\", "~", "~/", "/home", "/users"}

errors: list[str] = []
warnings: list[str] = []


def err(server: str, msg: str) -> None:
    errors.append(f"{server}: {msg}")


def warn(server: str, msg: str) -> None:
    warnings.append(f"{server}: {msg}")


def looks_like_secret(value: str) -> bool:
    if PLACEHOLDER.search(value):
        return False
    # Header values carry an auth scheme in front of the credential
    # ("Authorization": "Bearer ghp_..."), so strip it before matching --
    # otherwise every header check silently passes.
    for scheme in ("Bearer ", "Token ", "token ", "Basic "):
        if value.startswith(scheme):
            value = value[len(scheme):]
            break
    return value.startswith(SECRET_PREFIXES)


def check_transport(name: str, cfg: dict) -> None:
    """Exactly one transport must be defined, or the server silently never starts."""
    has_cmd, has_url = "command" in cfg, "url" in cfg
    if has_cmd and has_url:
        err(name, "defines both 'command' and 'url' -- pick one transport")
    elif not has_cmd and not has_url:
        err(name, "defines neither 'command' nor 'url' -- it cannot start")

    url = cfg.get("url")
    if url and not url.startswith("https://"):
        err(name, f"remote URL is not https: {url}")


def check_secrets(name: str, cfg: dict) -> None:
    """Credentials belong in the environment, never inline in the config."""
    for field in ("env", "headers"):
        for key, value in (cfg.get(field) or {}).items():
            if isinstance(value, str) and looks_like_secret(value):
                err(name, f"{field}.{key} looks like a literal credential -- use ${{env:VAR}}")

    for arg in cfg.get("args", []):
        if isinstance(arg, str) and looks_like_secret(arg):
            err(name, f"argument looks like a literal credential: {arg[:12]}...")


def check_filesystem_scope(name: str, cfg: dict) -> None:
    """A drive root here hands the model everything on the machine."""
    args = cfg.get("args", [])
    if not any("server-filesystem" in str(a) for a in args):
        return
    idx = next(i for i, a in enumerate(args) if "server-filesystem" in str(a))
    roots = [a for a in args[idx + 1:] if isinstance(a, str)]
    if not roots:
        warn(name, "filesystem server has no directory allow-list")
    for root in roots:
        if root.strip().lower().rstrip("/\\") in {r.rstrip("/\\") for r in DRIVE_ROOTS}:
            err(name, f"'{root}' exposes an entire drive/home -- list specific directories")


def check_pinning(name: str, cfg: dict) -> None:
    """Unpinned references drift silently between launches."""
    args = cfg.get("args", [])
    for arg in args:
        if isinstance(arg, str) and arg.endswith("@latest"):
            warn(name, f"'{arg}' resolves on every launch -- pin a version for reproducibility")

    if cfg.get("command") == "docker":
        for arg in args:
            if not isinstance(arg, str) or arg.startswith("-"):
                continue
            # First bare token after the flags is the image reference.
            if "/" in arg and not arg.startswith(("run", "C:", "c:")):
                if ":" not in arg.split("/")[-1]:
                    warn(name, f"docker image '{arg}' is untagged -- resolves to whatever the registry serves")
                break


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "mcp.json")
    if not path.exists():
        print(f"error: {path} not found")
        return 1

    try:
        servers = json.loads(path.read_text())["mcpServers"]
    except (json.JSONDecodeError, KeyError) as exc:
        print(f"error: could not read mcpServers from {path}: {exc}")
        return 1

    for name, cfg in servers.items():
        if not isinstance(cfg, dict):
            err(name, "entry is not an object")
            continue
        check_transport(name, cfg)
        check_secrets(name, cfg)
        check_filesystem_scope(name, cfg)
        check_pinning(name, cfg)

    remote = sum(1 for c in servers.values() if isinstance(c, dict) and "url" in c)
    print(f"Checked {len(servers)} servers in {path} ({remote} remote, {len(servers) - remote} local)")

    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"\nNo errors ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
