#!/usr/bin/env python3
"""Validate skill and subagent definitions against their published formats.

This repo's original defect was a catalog that described 61 definitions which
did not exist. Documentation drifting from reality is exactly the bug being
fixed, so it should not be able to recur silently -- this script fails CI when
it does.

Checks, as errors:
  - SKILL.md exists in every skill directory, with `name` and `description`
  - a skill's `name` matches its directory (that is what the command becomes)
  - subagent files carry `name` and `description`, and `name` matches filename
  - `name` values are lowercase-and-hyphens, and contain no ':'
  - every scripts/ file referenced from a SKILL.md body actually exists
  - referenced scripts are executable
  - catalog counts in README.md match what is on disk

Exit codes: 0 = clean or warnings only, 1 = at least one error.

Usage:  python3 scripts/validate-definitions.py [repo-root]
"""

import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# Deliberately not a YAML parser: the frontmatter here is flat scalars, and a
# dependency-free check runs anywhere CI happens to be.
FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")

errors: list[str] = []
warnings: list[str] = []


def err(where: str, msg: str) -> None:
    errors.append(f"{where}: {msg}")


def warn(where: str, msg: str) -> None:
    warnings.append(f"{where}: {msg}")


def parse_frontmatter(path: Path) -> tuple[dict, str] | None:
    """Return (fields, body) or None when no frontmatter block is present."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    fields = {}
    for line in parts[1].splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = FIELD_RE.match(line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields, parts[2]


def check_name(where: str, value: str, expected: str, kind: str) -> None:
    if ":" in value:
        err(where, f"{kind} name contains ':' -- reserved for plugin scoping")
    if not NAME_RE.match(value):
        err(where, f"{kind} name '{value}' must be lowercase letters, digits, hyphens")
    if value != expected:
        err(where, f"{kind} name '{value}' does not match '{expected}' -- "
                   "the command comes from the directory/filename, so these must agree")


def check_skill(skill_dir: Path, root: Path) -> None:
    rel = skill_dir.relative_to(root)
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        err(str(rel), "no SKILL.md -- the directory is not a skill")
        return

    parsed = parse_frontmatter(skill_md)
    if parsed is None:
        err(f"{rel}/SKILL.md", "missing or malformed YAML frontmatter")
        return
    fields, body = parsed

    for required in ("name", "description"):
        if not fields.get(required):
            err(f"{rel}/SKILL.md", f"frontmatter missing required field '{required}'")

    if "name" in fields:
        check_name(f"{rel}/SKILL.md", fields["name"], skill_dir.name, "skill")

    desc = fields.get("description", "")
    if desc and len(desc) < 30:
        warn(f"{rel}/SKILL.md",
             "description is very short -- it is the only thing the model sees "
             "when deciding whether to load this skill")

    # Every scripts/ path named in the body must exist and be runnable.
    #
    # A reference resolves against either the skill's own directory or the repo
    # root: skills legitimately call shared tooling (scripts/validate-*.py) and
    # each other's scripts, not only their own bundled ones. Checking against
    # the skill dir alone flags every shared-tool reference as broken.
    # The leading [A-Za-z0-9_./-]* captures any path prefix. Without it the
    # pattern matches the `scripts/health-check.sh` tail out of the middle of a
    # valid full path like `.claude/skills/mcp-health-check/scripts/...` and
    # reports a working reference as broken.
    for ref in sorted(set(re.findall(r"[A-Za-z0-9_./-]*scripts/[A-Za-z0-9_./-]+", body))):
        candidates = [skill_dir / ref, root / ref]
        target = next((c for c in candidates if c.exists()), None)
        if target is None:
            err(f"{rel}/SKILL.md",
                f"references '{ref}' — not found in the skill directory or repo root")
        elif target.suffix in (".sh", ".py") and not (target.stat().st_mode & 0o111):
            warn(f"{rel}/SKILL.md", f"referenced script '{ref}' is not executable")


def check_agent(path: Path, root: Path) -> None:
    rel = path.relative_to(root)
    parsed = parse_frontmatter(path)
    if parsed is None:
        err(str(rel), "missing or malformed YAML frontmatter")
        return
    fields, _ = parsed

    for required in ("name", "description"):
        if not fields.get(required):
            err(str(rel), f"frontmatter missing required field '{required}'")

    if "name" in fields:
        check_name(str(rel), fields["name"], path.stem, "subagent")

    # `tools` that resolves to nothing makes the subagent fail to launch.
    if "tools" in fields and not fields["tools"].strip():
        err(str(rel), "'tools' is empty -- subagent would launch with zero tools")


def check_catalog_counts(root: Path, n_skills: int, n_agents: int) -> None:
    readme = root / "README.md"
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    for label, actual in (("skills", n_skills), ("subagents", n_agents)):
        # set(): the same claim usually appears in both the intro line and the
        # component table, and reporting it twice is just noise.
        for claimed in sorted(set(re.findall(rf"(\d+)\s+{label}\b", text))):
            if int(claimed) != actual:
                err("README.md",
                    f"claims {claimed} {label} but {actual} exist on disk")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

    skills_root = root / ".claude" / "skills"
    agents_root = root / ".claude" / "agents"

    skill_dirs = sorted(d for d in skills_root.iterdir() if d.is_dir()) if skills_root.exists() else []
    agent_files = sorted(agents_root.glob("*.md")) if agents_root.exists() else []

    if not skill_dirs:
        warn(".claude/skills", "no skills found")
    if not agent_files:
        warn(".claude/agents", "no subagents found")

    for d in skill_dirs:
        check_skill(d, root)
    for f in agent_files:
        check_agent(f, root)

    check_catalog_counts(root, len(skill_dirs), len(agent_files))

    print(f"Checked {len(skill_dirs)} skill(s) and {len(agent_files)} subagent(s) in {root}")
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
