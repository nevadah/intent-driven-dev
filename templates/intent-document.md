---
unit: domain/capability
version: 0.1.0
status: draft
author: your.handle
reviewers: []
exposes:
  # Machine-readable list of public interfaces. Mirrors the "Exposes" prose in Dependencies and
  # Boundaries below — the frontmatter version is for tooling; the prose version adds explanation.
  - # e.g. POST /domain/capability, or an event name, or a public function signature
depends_on:
  - # e.g. other/unit — use the canonical unit identifier from its intent document
must_not_know:
  - # e.g. unrelated/domain — explicit boundary violations that must never appear in the implementation
tags: []
---

# Intent: [Capability Name]

<!-- One sentence: what does this unit do and for whom? -->

## Summary

<!-- Scope guidance: one intent document should cover one independently deployable or testable
     unit of behavior. Author at the feature or capability level — not the individual function
     level (too narrow) and not the service level (too broad). If you cannot describe the unit's
     behavior in a single paragraph without caveats, consider splitting it. -->

[What this unit does, stated as the outcome it delivers. Not how it works — what it achieves. One short paragraph.]

---

## Domain Semantics

<!-- Define the key terms and concepts this unit operates on. This is not a glossary of
     technical terms — it is a definition of what things *mean* in this domain. An agent
     reading only this section should understand the business context well enough to spot
     an implementation that is technically correct but semantically wrong. -->

**[Term]** — [What this concept means in this domain. Include what it is NOT if that boundary is non-obvious.]

**[Term]** — [...]

---

## Behavioral Contract

### Preconditions

<!-- What must be true before this unit can operate correctly? State as assertions, not
     as implementation steps. -->

- [...]

### Postconditions

<!-- What is guaranteed to be true after each significant outcome? Group by outcome. -->

**On [outcome]:**
- [...]

**On [outcome]:**
- [...]

### Invariants

<!-- What must always be true, regardless of input or path through the unit? These are
     the non-negotiable constraints an agent checks for in any implementation. -->

- [...]

### Scenarios

<!-- Use Gherkin. Each scenario must be independently understandable — no shared state
     between scenarios unless a Background block is used.

     Coverage checklist — ensure at least one scenario exists for each category:
     [ ] Happy path — the expected successful flow
     [ ] Edge cases — boundary values, empty inputs, concurrent operations
     [ ] Failure modes — each dependency failure, partial failures, rollback behavior
     [ ] Security-relevant paths — authentication, authorization, enumeration, rate limiting

     The Elicitation Agent will flag any uncovered category. -->

```gherkin
Feature: [Capability Name]

  # --- Happy path ---

  Scenario: [Happy path name]
    Given [initial state]
    When [action]
    Then [observable outcome]
    And [additional outcome]

  # --- Edge cases ---

  Scenario: [Edge case name]
    Given [...]
    When [...]
    Then [...]

  # --- Failure modes ---

  Scenario: [Failure mode name]
    Given [...]
    When [...]
    Then [...]

  # --- Security-relevant paths ---

  Scenario: [Security scenario name]
    Given [...]
    When [...]
    Then [...]
```

---

## Quality Attributes

<!-- Use the YAML block below. Remove sections that are not applicable.
     All numeric thresholds are treated as enforceable constraints by the compliance agent. -->

```yaml
security:
  # token_entropy_bits: 128
  # rate_limits:
  #   per_user:
  #     requests: 5
  #     window_minutes: 10

performance:
  # endpoint_p99_ms: 200
  # async_operations: []  # list operations that are fire-and-forget

failure_modes:
  # dependency_unavailable: return_503
  # partial_state_on_failure: describe_here
```

---

## Dependencies and Boundaries

<!-- Expand on the structured depends_on / must_not_know fields in the frontmatter.
     Explain *why* each dependency exists and what specifically this unit uses from it. -->

**Depends on:**
- `other/unit` — [what specifically is used from this unit and why]

**Exposes:**
<!-- This prose list mirrors the machine-readable `exposes` field in the frontmatter.
     The frontmatter version is for tooling; this version explains what each interface
     provides and what callers can rely on. Both must be kept in sync. -->
- `[interface]` — [what callers can expect from this interface]

**Must not know about:**
- `unrelated/domain` — [why this boundary exists]

---

## Rationale

<!-- Document decisions that are non-obvious or that have plausible-but-rejected
     alternatives. Each entry should name the decision, explain why it was made,
     and name what was considered and rejected. The goal is to prevent future
     contributors from re-litigating settled questions without context. -->

**[Decision name]**
[Why this choice was made. What the tradeoff is. What alternatives were considered and why they were rejected.]

**[Decision name]**
[...]
