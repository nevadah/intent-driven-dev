PROJECT BRIEFING: AI-Native Development Methodology
Core Concept
A new software development methodology built on two linked ideas:

Code is a build artifact, not the source of truth
Human intent is the source of truth

Just as a compiled JAR, Docker image, or npm package is considered a downstream artifact of source code, source code itself should be considered a downstream artifact of structured, versioned, human-authored intent. AI coding tools generate the code from the intent. The code is never manually edited — doing so breaks the model.
The Three Structural Problems This Solves
These were articulated in a LinkedIn post that prompted this project:

Current AI tools don't capture human intent in any meaningful, reusable way. Insights evaporate when a session ends. Institutional knowledge doesn't accumulate.
They iterate over source code, not over intent. When intent shifts, the tool generates new code but the intent was never captured, structured, or versioned.
They rely on natural language alone to communicate intent. Natural language is ambiguous. The model silently interprets and generates confidently against assumptions nobody agreed to.

The Proposed Solution
A formal methodology with three components:

A structured intent document format — capturing intent in a way that is precise, human-readable, versioned, and machine-consumable
A governed workflow — analogous to Gitflow, defining stages, gates, and handoffs from intent authoring through review to code generation
An agent pipeline — AI agents that enforce and assist the process

The Intent Document
The intent document is the source of truth. It has multiple layers:

Behavioral contracts — inputs/outputs, pre/postconditions, invariants, Given/When/Then scenarios
Domain semantics — what the concepts mean, business rules, not just technical descriptions
Quality attributes — performance, security, failure modes, scalability constraints
Dependencies and boundaries — what this unit relies on, exposes, and must not know about
Rationale — why decisions were made, what alternatives were rejected

The Workflow (analogous to Gitflow)
Key principles:

Intent must be authored and reviewed before code generation begins
Generated code is read-only — never manually edited
Intent documents are versioned in the repository alongside or instead of code
Reviews happen at the intent level, not the code level
Two distinct review seams: (1) business stakeholder to engineer — is this what the business needs? (2) engineer to AI — is this precise enough for the AI to implement correctly?

The Agent Pipeline
Four proposed agents:

Intent Elicitation Agent — interviews engineer/stakeholder, identifies ambiguities, flags underspecified edge cases, ensures nothing is left vague
Intent Review Agent — stress-tests completed intent documents, finds internal contradictions, missing constraints, boundary conditions
Compliance Agent — after code generation, verifies implementation actually satisfies the intent document (independent of test results)
Intent Maintenance Agent — when changes are requested, ensures intent document is updated first, flags conflicts with existing intent

Why This Matters Now

AI tools write code and tests, creating circular verification — the AI can implement something incorrectly and write tests that confirm the incorrect implementation. Independent intent documents break this circularity.
The craft of engineering is shifting from writing good code to authoring good intent — closer to requirements engineering and domain modeling than programming
PR reviews of AI-generated code are increasingly superficial — review needs to move upstream to the intent layer
This is a cultural and methodological shift analogous to CI/CD — needs tooling that makes compliance the path of least resistance

Relationship to Existing Work
This space is active. Related projects and concepts to be aware of:

Spec-driven development — GitHub's Spec Kit, AWS Kiro, MindStudio's Remy. Closest to this concept but mostly solve the generation problem, not the governance and verification pipeline
Change Intent Records (CIRs) — lightweight format for capturing why a change was made, analogous to ADRs. Relevant to the rationale layer of intent documents
Intent Integrity Chain — cryptographically hashes behavioral assertions before implementation begins, tamper-proof verification. Relevant to the compliance layer
Intent-Driven Development (IDD) — term already in use, worth being aware of for naming/positioning

This methodology is distinguished by combining: structured intent format + governed workflow + agent pipeline + explicit read-only treatment of generated code, into a single coherent system.
What the GitHub Repo Should Contain (MVP)

README — the philosophy, the problem, the solution, how this differs from existing approaches
Intent document template and schema — with examples of good and bad entries
Workflow definition — the stages, gates, and handoffs (probably a diagram plus written description)
Agent prompts — starter prompts for the elicitation, review, compliance, and maintenance agents
The methodology itself demonstrated by example — the repo's own intent documents should follow the format

Naming
Not yet decided. Requirements: distinctive, not already taken, signals the core concept. "IntentFirst" is a strong candidate but used as a descriptive phrase. Most obvious names (IntentFlow, Blueprint, Meridian, Provenance, Bedrock, Groundwork) are taken. Name can be decided later — focus on building the content first.
Open Questions

What is the right granularity for an intent document? (per service, per feature, per function?)
How does intent versioning work in practice — what does a breaking change to intent look like?
How do you handle the boundary/interface contracts between intent units?
What file format works best — Markdown with structured sections, YAML, a custom schema?
How does this integrate with existing tools (GitHub, Jira, CI/CD pipelines)?