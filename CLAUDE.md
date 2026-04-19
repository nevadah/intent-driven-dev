# CLAUDE.md — intent-driven-dev

Read `WORKING_STYLE.md` at session start. It contains cross-project preferences that apply here.

---

## Project

A methodology and tooling framework for treating human intent as the source of truth in software development, with generated code as a downstream artifact. This repo contains the specification, schema, templates, examples, and agent prompts that define the methodology.

There is no build, no test suite, and no linter. Quality gates from WORKING_STYLE.md still apply to documentation: audit for staleness before any push.

---

## Repo Structure

```
schema/               # JSON Schema definitions for structured formats
templates/            # Blank templates for authors to fill in
examples/             # Worked examples demonstrating the format
```

---

## Environment Note

The `gh` CLI and `bd` (Beads) may not be on PATH in bash sessions. Prepend both before use:

```bash
export PATH="$PATH:/c/Program Files/GitHub CLI:/c/Users/Nevada/AppData/Local/Programs/bd"
```

---

## Methodology Constraints

This repo follows the methodology it defines. Intent documents for the repo's own components live in `examples/` and must be kept current. The repo itself is the canonical demonstration that the methodology is self-applicable.


<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->
