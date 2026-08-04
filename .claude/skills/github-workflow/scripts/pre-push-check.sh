#!/usr/bin/env bash
# Pre-push sanity checks. Read-only: reports, never modifies or pushes.
set -uo pipefail
status=0

echo "=== pre-push checks ==="

branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "?")
echo "branch: $branch"
if [ "$branch" = "main" ] || [ "$branch" = "master" ]; then
  echo "  ERROR: on the default branch -- branch before committing"
  status=1
fi

echo
echo "--- uncommitted changes ---"
if [ -n "$(git status --porcelain)" ]; then
  git status --short
  echo "  NOTE: the above is not committed and will not be pushed"
else
  echo "  clean"
fi

echo
echo "--- commits ahead of origin ---"
upstream=$(git rev-parse --abbrev-ref '@{upstream}' 2>/dev/null || true)
if [ -n "$upstream" ]; then
  git log --oneline "$upstream"..HEAD 2>/dev/null || echo "  none"
else
  echo "  no upstream set -- first push needs: git push -u origin $branch"
fi

echo
echo "--- commit message quality ---"
# A body is where the "why" lives. Subject-only commits lose it permanently.
while read -r sha; do
  [ -z "$sha" ] && continue
  subject=$(git log -1 --format=%s "$sha")
  body=$(git log -1 --format=%b "$sha" | grep -v '^Co-Authored-By:' | grep -v '^Claude-Session:' | tr -d '[:space:]')
  if ! echo "$subject" | grep -qE '^(feat|fix|docs|refactor|chore|test|perf|build|ci)(\(.+\))?!?: '; then
    echo "  WARN ${sha:0:8}: subject is not conventional-commit shaped"
  fi
  if [ -z "$body" ]; then
    echo "  WARN ${sha:0:8}: no body -- the 'why' is not recorded anywhere"
  fi
done < <(git log --format=%H "${upstream:-HEAD~1}"..HEAD 2>/dev/null || true)

echo
echo "--- staged secrets ---"
PATTERN='\b(ghp_|gho_|ghu_|ghs_|ghr_|github_pat_|ntn_|xoxb-|xoxp-|AKIA|AIza)[A-Za-z0-9_-]{8,}|\b(sk-|pplx-|secret_)[A-Za-z0-9_-]{16,}'
if git diff --cached | grep -nE "$PATTERN"; then
  echo "  ERROR: credential-shaped string staged"
  status=1
else
  echo "  none"
fi

echo
echo "=== done (exit $status) ==="
exit $status
