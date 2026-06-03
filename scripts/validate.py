#!/usr/bin/env python3
"""Structural validator for the bi-copilot plugin. Zero deps. Exit nonzero on any failure."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECTED = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "LICENSE",
    "README.md",
    "skills/groundwork/SKILL.md",
    "skills/groundwork/references/completeness-models.md",
    "skills/groundwork/references/kb-core-templates.md",
    "skills/groundwork/references/kb-catalog.md",
    "skills/requirements-interrogator/SKILL.md",
    "skills/requirements-interrogator/references/frameworks.md",
    "skills/defend-my-number/SKILL.md",
    "skills/defend-my-number/references/archetypes.md",
    "skills/defend-my-number/references/defense-sheet.md",
    "skills/kpi-contract/SKILL.md",
    "skills/kpi-contract/references/fork-points.md",
    "skills/review-my-query/SKILL.md",
    "skills/review-my-query/references/failure-modes.md",
    "skills/review-my-query/references/query-review.md",
]
fails = []

def fail(m): fails.append(m)

for rel in EXPECTED:
    if not os.path.isfile(os.path.join(ROOT, rel)):
        fail(f"missing file: {rel}")

for rel in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"):
    p = os.path.join(ROOT, rel)
    if os.path.isfile(p):
        try: json.load(open(p))
        except Exception as e: fail(f"invalid JSON {rel}: {e}")

def check_skill(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.isfile(p): return
    text = open(p, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m: fail(f"{rel}: missing YAML frontmatter"); return
    fm, body = m.group(1), m.group(2)
    for key in ("name:", "description:", "allowed-tools:"):
        if key not in fm: fail(f"{rel}: frontmatter missing {key}")
    at = [l for l in fm.splitlines() if l.strip().startswith("allowed-tools:")]
    if at and "*" in at[0]: fail(f"{rel}: allowed-tools must not grant '*'")
    n = len(body.strip().splitlines())
    if n > 200: fail(f"{rel}: body {n} lines > 200 (move depth to references/)")

# Validate every skill under skills/*/SKILL.md (accretion: new skills are auto-covered)
skills_dir = os.path.join(ROOT, "skills")
if os.path.isdir(skills_dir):
    for name in sorted(os.listdir(skills_dir)):
        skill_md = os.path.join("skills", name, "SKILL.md")
        if os.path.isfile(os.path.join(ROOT, skill_md)):
            check_skill(skill_md)
        elif os.path.isdir(os.path.join(skills_dir, name)):
            fail(f"skills/{name}/ has no SKILL.md")

if fails:
    print("VALIDATION FAILED:")
    for f in fails: print("  -", f)
    sys.exit(1)
print(f"VALIDATION PASSED: {len(EXPECTED)} files OK")
