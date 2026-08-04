#!/usr/bin/env bash
# Deployment pre-flight. Read-only: runs checks, deploys nothing.
set -uo pipefail
status=0
run() { # run <label> <cmd...>
  local label="$1"; shift
  printf '  %-14s ' "$label"
  if "$@" >/tmp/preflight.$$ 2>&1; then echo "PASS"
  else echo "FAIL"; sed 's/^/      /' /tmp/preflight.$$ | tail -15; status=1; fi
  rm -f /tmp/preflight.$$
}

echo "=== deploy pre-flight ==="
echo "commit: $(git rev-parse HEAD 2>/dev/null || echo '?')"
echo "branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')"
echo

if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  echo "  WARN: uncommitted changes -- you may not be shipping what you're testing"
  git status --short | sed 's/^/    /'
  echo
fi

echo "--- repo validators ---"
[ -f scripts/validate-mcp-config.py ] && run "mcp-config" python3 scripts/validate-mcp-config.py mcp.json
[ -f scripts/validate-definitions.py ] && run "definitions" python3 scripts/validate-definitions.py .

if [ -f package.json ]; then
  echo
  echo "--- project checks ---"
  for s in typecheck lint test:run build; do
    if node -e "process.exit(require('./package.json').scripts?.['$s']?0:1)" 2>/dev/null; then
      run "$s" npm run "$s"
    fi
  done
fi

echo
echo "--- reminders a script cannot check ---"
echo "  [ ] target secrets are CONFIGURED, not just referenced"
echo "  [ ] migrations are additive-first and reversible"
echo "  [ ] rollback path is known"
echo "  [ ] CI is green on THIS SHA, not an earlier one"
echo
echo "=== done (exit $status) ==="
exit $status
