#!/usr/bin/env bash
# Full MCP stack health check. Read-only: reports, never modifies.
# Exits non-zero only when the config validator reports errors, so this is
# safe to wire into CI or a pre-commit hook.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$ROOT" || exit 1
status=0

echo "=== MCP health check: $ROOT ==="
echo

echo "--- config validation ---"
if python3 scripts/validate-mcp-config.py mcp.json; then
  echo "config: OK"
else
  echo "config: ERRORS (see above)"
  status=1
fi
echo

echo "--- server inventory ---"
python3 - <<'PY'
import json, collections
try:
    servers = json.load(open("mcp.json"))["mcpServers"]
except Exception as exc:
    print(f"  could not read mcp.json: {exc}")
    raise SystemExit(0)

by_kind = collections.defaultdict(list)
for name, cfg in sorted(servers.items()):
    kind = "remote" if "url" in cfg else cfg.get("command", "?")
    by_kind[kind].append(name)

for kind, names in sorted(by_kind.items()):
    print(f"  {kind:8} ({len(names)}): {', '.join(names)}")

remote = len(by_kind.get("remote", []))
print(f"\n  total: {len(servers)} ({remote} remote, {len(servers)-remote} local)")
PY
echo

echo "--- local prerequisites ---"
# Only check what this machine can actually answer. Remote sign-in state is
# per-user and deliberately out of scope.
if command -v docker >/dev/null 2>&1; then
  if docker info >/dev/null 2>&1; then echo "  docker: running"
  else echo "  docker: installed but NOT running (needed by fetch, git, n8n)"; fi
else
  echo "  docker: not installed (needed by fetch, git, n8n)"
fi
command -v node >/dev/null 2>&1 && echo "  node:   $(node --version)" || echo "  node:   NOT FOUND (needed by npx servers)"
command -v python3 >/dev/null 2>&1 && echo "  python: $(python3 --version 2>&1)" || echo "  python: NOT FOUND"
echo
echo "  NOTE: remote servers need interactive sign-in. That cannot be checked"
echo "        here -- confirm in your client that each shows as connected."
echo

echo "--- documentation drift ---"
python3 - <<'PY'
import json, re, pathlib
try:
    servers = set(json.load(open("mcp.json"))["mcpServers"])
except Exception:
    raise SystemExit(0)

cat = pathlib.Path("servers/README.md")
if not cat.exists():
    print("  servers/README.md missing")
    raise SystemExit(0)

text = cat.read_text(encoding="utf-8")
missing = sorted(s for s in servers if s not in text)
print(f"  undocumented servers: {', '.join(missing) if missing else 'none'}")

readme = pathlib.Path("README.md")
if readme.exists():
    claims = {int(n) for n in re.findall(r"(\d+)\s+servers?\b", readme.read_text(encoding="utf-8"))}
    bad = sorted(c for c in claims if c != len(servers))
    print(f"  README count mismatch: {bad if bad else 'none'} (actual {len(servers)})")
PY
echo
echo "=== done (exit $status) ==="
exit $status
