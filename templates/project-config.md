# Project Configuration

<!-- One project config per repository. This document is passed to every code generation
     invocation alongside the relevant intent document. It captures environment and
     conventions — the things that apply to all generated code in this project.

     What belongs here:
     - Target language, runtime, and framework versions
     - Coding standards and style rules
     - Repository layout conventions
     - Shared dependencies and how they are used
     - Test framework and coverage expectations
     - Logging, observability, and error handling conventions

     What does NOT belong here:
     - Behavioral contracts (those belong in intent documents)
     - Domain semantics (those belong in intent documents)
     - Unit-specific quality attributes (those belong in intent documents)

     If you find yourself writing the same constraint in every intent document,
     it belongs here instead. -->

---

## Language and Runtime

```yaml
language: # e.g. TypeScript, Python, Go
runtime_version: # e.g. Node 22, Python 3.12, Go 1.22
framework: # e.g. Express, FastAPI, none
```

---

## Repository Layout

<!-- Describe where generated code should be placed and how it should be organized.
     The convention recommended by the methodology:
       intent/<domain>/<capability>.md  →  src/<domain>/<capability>/
     Override here if your project uses a different structure. -->

```yaml
intent_root: intent/
source_root: src/
test_root: # e.g. src/ (co-located) or tests/
```

---

## Coding Standards

<!-- Reference an external style guide if one exists, or enumerate key rules here.
     Keep this to rules that are not already enforced by linting — those are implicit. -->

- [...]

---

## Shared Dependencies

<!-- List dependencies that generated code may use freely without declaring them
     as intent-document-level concerns. Things like logging libraries, HTTP clients,
     database connectors, and internal SDK packages. -->

| Package | Purpose | Usage notes |
|---|---|---|
| `[package]` | [what it does] | [any constraints on how it should be used] |

---

## Test Conventions

```yaml
test_framework: # e.g. Jest, pytest, Go test
coverage_threshold_percent: # e.g. 80
test_style: # e.g. unit, integration, or both
mocking_policy: # e.g. mock at boundary only, no internal mocks
```

---

## Observability

<!-- How should generated code handle logging, metrics, and tracing? -->

```yaml
logging:
  library: # e.g. pino, structlog, slog
  level_default: info
  format: json
  include_trace_id: true

error_handling:
  # e.g. never swallow errors silently, always log at error level with context
```

---

## Notes

<!-- Anything else the code generation agent should know about this project that
     does not fit the categories above. -->
