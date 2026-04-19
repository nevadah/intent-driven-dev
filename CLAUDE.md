# CLAUDE.md — intent-driven-dev

Read `WORKING_STYLE.md` at session start. It contains cross-project preferences that apply here.

---

## Project

A methodology and tooling framework for treating human intent as the source of truth in software development, with generated code as a downstream artifact. This repo contains the specification, schema, templates, examples, and agent prompts that define the methodology.

There is no build, no test suite, and no linter. Quality gates from WORKING_STYLE.md still apply to documentation: audit for staleness before any push.

---

## Issue Tracker

GitHub Issues (`gh issue`). File an issue before starting any work item.

```bash
gh issue list
gh issue create --title "..." --body "..."
gh issue close <number>
```

---

## Repo Structure

```
schema/               # JSON Schema definitions for structured formats
templates/            # Blank templates for authors to fill in
examples/             # Worked examples demonstrating the format
```

---

## Environment Note

The `gh` CLI is installed at `C:\Program Files\GitHub CLI\` and may not be on PATH in bash sessions. Prepend to PATH before use:

```bash
export PATH="$PATH:/c/Program Files/GitHub CLI"
```

---

## Methodology Constraints

This repo follows the methodology it defines. Intent documents for the repo's own components live in `examples/` and must be kept current. The repo itself is the canonical demonstration that the methodology is self-applicable.
