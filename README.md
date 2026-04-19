# Intent-Driven Development

A methodology for treating human intent as the source of truth in software development, with generated code as a downstream artifact.

---

## The core idea

In most projects, source code is the source of truth. Documentation, if it exists, describes the code. Tests verify what the code does. When something changes, the code changes first and everything else follows.

This methodology inverts that. Source code is treated as a build artifact — analogous to a compiled binary or a Docker image — generated from something more fundamental: a structured, versioned, human-authored description of intent. The intent document is the source of truth. Code is generated from it. The code is never manually edited; doing so is equivalent to patching a compiled binary.

---

## The problem

Current AI coding tools have three structural problems:

**1. Intent evaporates.** When a session ends, the reasoning behind the code disappears. Institutional knowledge doesn't accumulate. The next session starts from the code, not from why the code is what it is.

**2. Iteration happens at the wrong level.** When requirements change, AI tools generate new code — but the intent was never captured, so there's nothing to update. The new code reflects the new conversation, not a versioned record of what changed and why.

**3. Ambiguity is invisible.** AI tools accept natural language and generate confident implementations. When the language is ambiguous, the model makes a silent interpretive choice. Nobody agreed to it; it just becomes the code.

---

## The solution

Three components, working together:

### 1. Structured intent documents

A formal document format that captures intent precisely enough for an AI to implement correctly, and richly enough to serve as the lasting record of what was built and why.

An intent document contains:
- **Behavioral contracts** — inputs, outputs, pre/postconditions, invariants, and Given/When/Then scenarios in Gherkin
- **Domain semantics** — what the concepts mean in this domain, not just technical descriptions
- **Quality attributes** — performance thresholds, security constraints, failure modes
- **Dependencies and boundaries** — what this unit relies on, exposes, and must never know about
- **Rationale** — why decisions were made and what alternatives were rejected

See [`templates/intent-document.md`](templates/intent-document.md) for the blank template and [`schema/intent-document.schema.json`](schema/intent-document.schema.json) for the machine-readable frontmatter schema. See [`examples/intent-password-reset.md`](examples/intent-password-reset.md) for a complete worked example.

### 2. A governed workflow

A staged lifecycle analogous to Gitflow, with explicit gates between stages. Intent is authored and reviewed before code generation begins. Two distinct human review seams catch different classes of error:

- **Business stakeholder review** — is this what the business needs?
- **Engineering review** — is this precise enough for the AI to implement correctly?

Neither review touches generated code. Review happens at the intent level, upstream of implementation.

See [`workflow/workflow.md`](workflow/workflow.md) for the full stage-by-stage definition with entry/exit gates.

### 3. An agent pipeline

Four AI agents enforce and assist the process:

| Agent | Stage | Role |
|---|---|---|
| **Elicitation Agent** | After authoring | Interviews the draft document, flags ambiguities, underspecified edge cases, and missing scenarios |
| **Intent Review Agent** | After elicitation | Stress-tests the document for internal contradictions, impossible postconditions, and boundary violations |
| **Compliance Agent** | After code generation | Verifies the implementation satisfies the intent document — independently of the test suite |
| **Intent Maintenance Agent** | Before any change | Ensures the intent document is updated before code changes; flags breaking changes and conflicts |

See [`agents/`](agents/) for ready-to-use system prompts for each agent.

---

## Why the Compliance Agent matters

AI tools write code and tests together. When an AI implements something incorrectly, it tends to write tests that confirm the incorrect implementation. The test suite passes; the intent was never satisfied.

The Compliance Agent breaks this circularity. It verifies the implementation against the intent document — a source of truth the AI did not produce — independently of whether the tests pass. This is the only reliable way to catch the class of error where the AI was confidently wrong about what was asked.

---

## How this differs from related work

**Spec-driven development** (GitHub Spec Kit, AWS Kiro, MindStudio Remy) — These tools solve the generation problem: write a spec, get code. They do not define a governed workflow, do not enforce that code remains read-only, and do not include a compliance verification step. Generation without governance.

**Change Intent Records (CIRs)** — Lightweight records of why a change was made, analogous to ADRs. Useful for the rationale layer of an intent document, but not a full methodology. No workflow, no agents, no behavioral contracts.

**Intent-Driven Development (IDD)** — The term is in use across several contexts, generally meaning "start with intent before writing code." This methodology gives that principle a concrete structure: a specific document format, a specific workflow with enforced gates, and a specific agent pipeline.

The distinguishing combination: **structured intent format + governed workflow + agent pipeline + read-only generated code**, as a single coherent system.

---

## What's in this repo

```
schema/                         # JSON Schema for intent document frontmatter
  intent-document.schema.json

templates/                      # Blank template for authoring intent documents
  intent-document.md

examples/                       # Worked examples
  intent-password-reset.md      # Complete example: email-based password reset

workflow/                       # The governed workflow
  workflow.md                   # Stage definitions, gates, and handoffs

agents/                         # Agent system prompts
  elicitation-agent.md
  review-agent.md
  compliance-agent.md
  maintenance-agent.md
```

---

## Status

Early-stage. The format, workflow, and agent prompts are a first version — usable, but expected to evolve as they are applied to real projects. Open questions include the right granularity for intent documents, how breaking changes to intent propagate through a dependency graph, and how this integrates with existing CI/CD tooling.

Contributions and feedback welcome.
