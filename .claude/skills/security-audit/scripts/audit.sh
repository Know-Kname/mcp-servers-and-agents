#!/usr/bin/env bash
# Mechanical security sweep. Read-only.
# Exit 1 if the config validator errors or a probable credential is found.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$ROOT" || exit 1
status=0

echo "=== security audit: $ROOT ==="
echo

echo "--- config validation ---"
python3 scripts/validate-mcp-config.py mcp.json || status=1
echo

echo "--- credential scan (tracked files) ---"
# Prefixes mirror SECRET_PREFIXES in scripts/validate-mcp-config.py, which is
# the single source of truth; this widens them to the whole repo.
#
# Two refinements learned by running it. Both matter -- a scanner that cries
# wolf gets ignored, which is worse than not having one:
#   \b anchors the prefix to a word start. Without it, `sk-` matched inside
#   "task-orchestrator" and "task-automation".
#   {16,} requires a plausible secret length. Without it, `secret_` matched
#   GitHub's `secret_protection` toolset name, and `pplx-` matched the
#   documented placeholder `pplx-xxxx...`.
# Distinctive prefixes (ghp_, AKIA, ...) need no length guard -- they do not
# occur in ordinary prose.
PATTERN='\b(ghp_|gho_|ghu_|ghs_|ghr_|github_pat_|ntn_|xoxb-|xoxp-|AKIA|AIza)[A-Za-z0-9_-]{8,}|\b(sk-|pplx-|secret_)[A-Za-z0-9_-]{16,}'
hits=$(git grep -nE "$PATTERN" -- . ':!scripts/validate-mcp-config.py' ':!.claude/skills/security-audit' 2>/dev/null || true)
if [ -n "$hits" ]; then
  echo "$hits"
  echo "  ^ review each: placeholder/doc example, or a real credential?"
  status=1
else
  echo "  no credential-shaped strings found"
fi
echo

echo "--- standing long-lived secrets in mcp.json ---"
python3 - <<'PY'
import json
try:
    servers = json.load(open("mcp.json"))["mcpServers"]
except Exception:
    raise SystemExit(0)

# A server holding an env-referenced secret is not a defect, but it is the
# standing-credential inventory someone should be able to see at a glance.
found = False
for name, cfg in sorted(servers.items()):
    secrets = [k for k in (cfg.get("env") or {}) if any(
        t in k.upper() for t in ("SECRET", "KEY", "TOKEN", "PASSWORD"))]
    if secrets:
        found = True
        print(f"  {name}: {', '.join(secrets)}")
if not found:
    print("  none -- every server uses interactive auth")
else:
    print("\n  Prefer OAuth/Entra where the vendor supports it: short-lived,")
    print("  per-user, revocable, and nothing is stored.")
PY
echo

echo "--- unpinned references ---"
python3 - <<'PY'
import json
try:
    servers = json.load(open("mcp.json"))["mcpServers"]
except Exception:
    raise SystemExit(0)

rows = []
for name, cfg in sorted(servers.items()):
    for arg in cfg.get("args", []):
        if isinstance(arg, str) and arg.endswith("@latest"):
            rows.append(f"  {name}: {arg} (re-resolves every launch)")
    if cfg.get("command") == "docker":
        for arg in cfg.get("args", []):
            if isinstance(arg, str) and "/" in arg and not arg.startswith(("-", "C:", "c:")):
                if ":" not in arg.split("/")[-1]:
                    rows.append(f"  {name}: {arg} (untagged)")
                break
print("\n".join(rows) if rows else "  none")
print("\n  Tradeoff, not a fault: pinning buys reproducibility, floating stays patched.")
PY
echo
echo "=== done (exit $status) ==="
exit $status
