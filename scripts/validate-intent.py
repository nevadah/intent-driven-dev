#!/usr/bin/env python3
"""Validate intent document frontmatter against the JSON schema."""
import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml


def extract_frontmatter(content):
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


def main():
    schema = json.loads(Path("schema/intent-document.schema.json").read_text(encoding="utf-8"))

    files = []
    for directory in ["examples", "intent"]:
        p = Path(directory)
        if p.exists():
            files.extend(sorted(p.rglob("*.md")))

    if not files:
        print("No intent documents found.")
        sys.exit(0)

    errors = []
    checked = 0
    for f in files:
        content = f.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(content)
        if frontmatter is None or "unit" not in frontmatter:
            continue
        checked += 1
        try:
            jsonschema.validate(instance=frontmatter, schema=schema)
            print(f"  ok  {f}")
        except jsonschema.ValidationError as e:
            errors.append(f)
            print(f"  FAIL  {f}\n        {e.message}")

    print(f"\n{checked} document(s) checked, {len(errors)} error(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
