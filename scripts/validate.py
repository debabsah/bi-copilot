#!/usr/bin/env python3
"""Structural validator for the bi-copilot plugin. Zero deps. Exit nonzero on any failure."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECTED = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "LICENSE",
    "README.md",
    "skills/bi-copilot-router/SKILL.md",
    "skills/groundwork/SKILL.md",
    "skills/groundwork/references/completeness-models.md",
    "skills/groundwork/references/kb-core-templates.md",
    "skills/groundwork/references/kb-catalog.md",
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

for rel in ("skills/bi-copilot-router/SKILL.md", "skills/groundwork/SKILL.md"):
    check_skill(rel)

if fails:
    print("VALIDATION FAILED:")
    for f in fails: print("  -", f)
    sys.exit(1)
print(f"VALIDATION PASSED: {len(EXPECTED)} files OK")
