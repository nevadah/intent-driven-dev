# CI/CD Integration

## Overview

The Governed Intent Development workflow has three CI gates. One runs on intent documents; two run on generated code. Together they enforce the methodology's core constraints automatically: intent must be valid and approved before code exists, generated code must satisfy its intent, and generated code must pass an adversarial security audit before it merges.

---

## The three CI gates

| Gate | Trigger | What it checks | Blocks merge? |
|---|---|---|---|
| **Intent document validation** | PR touching `intent/` or `examples/` | Frontmatter parses and conforms to schema | Yes |
| **Compliance check** | PR containing generated implementation | Implementation satisfies the intent document | Yes (FAIL); No (UNVERIFIABLE) |
| **Security audit** | PR containing generated implementation | Implementation has no statically detectable vulnerabilities | Yes (VULNERABILITY); No (UNVERIFIABLE) |

These are distinct checks for distinct failures. Schema validation catches structural problems. The compliance check catches semantic divergence from declared intent. The security audit catches vulnerability classes that are not declared in the intent document — the implementation may correctly reflect the intent while still being insecure.

---

## Gate 1: Intent document validation

Validates that every intent document in the repository has well-formed frontmatter that conforms to the JSON schema in `schema/intent-document.schema.json`.

**When to run:** On any PR that touches files in `intent/`, `examples/`, or `schema/`.

**Gate behavior:** Fails the check and blocks merge if any document fails schema validation.

**Reference implementation:** This repository uses this gate. See [`.github/workflows/validate-intent.yml`](../.github/workflows/validate-intent.yml) and [`scripts/validate-intent.py`](../scripts/validate-intent.py) for a working example.

---

## Gate 2: Compliance check

Invokes the Compliance Agent against the generated implementation and its corresponding intent document. This requires an LLM API call and is therefore different in kind from a conventional CI check.

**When to run:** On any PR that includes generated implementation files (typically files in `src/` or your project's equivalent).

**Gate behavior:**
- `FAIL` result — blocks merge. The implementation diverges from the intent document. The correct response is to regenerate, not to patch the code.
- `UNVERIFIABLE` items — surface as annotations or warnings, do not block merge. These require runtime verification (load testing, security scanning) that static analysis cannot provide.
- `PASS` result — check succeeds.

**How to invoke:** The Compliance Agent is an LLM-based check. In a GitHub Actions context, run it as a step that calls the Anthropic API with the intent document and implementation as inputs, then parses the resulting compliance report. The API key should be stored as a repository secret.

**Surfacing findings:** Post the compliance report as a PR comment or job summary so reviewers can see the specific findings without reading raw CI logs. UNVERIFIABLE items should be visible but clearly labeled as not blocking.

---

## Gate 3: Security audit

Invokes the Security Agent against the generated implementation and its corresponding intent document. Like the compliance check, this requires an LLM API call.

**When to run:** On any PR that includes generated implementation files, after the compliance check passes.

**Gate behavior:**
- `VULNERABILITY` result — blocks merge. Routes to intent update + regeneration (if the vulnerability reveals an intent gap) or regeneration alone (if the intent specifies the security property but the generated code violates it).
- `UNVERIFIABLE` items — surface as annotations or warnings, do not block merge. Document for pre-production runtime verification or penetration testing.
- `PASS` result — check succeeds.

**On model selection:** If a model with security research specialization is available in your environment, use it for this check rather than the general-purpose model used for compliance. See [`agents/security-agent.md`](../agents/security-agent.md) for details.

**Surfacing findings:** Post the security audit report as a PR comment or job summary. VULNERABILITY findings with intent gaps should be clearly identified — they require an intent document update before regeneration, not just a re-run of generation.

---

## Intent document status enforcement

A CI check can verify that every implementation file being merged has a corresponding intent document in `approved` status. This prevents generated code from reaching the main branch when its intent document is still `draft` or `review`.

**Pattern:** For each implementation file changed in a PR, locate the corresponding intent document by path convention (`src/auth/password-reset/` → `intent/auth/password-reset.md`) and assert that its `status` field is `approved`.

**When to run:** On any PR containing files in the implementation directory.

**Gate behavior:** Blocks merge if a corresponding intent document is missing or not in `approved` status.

This check enforces at the merge boundary what the workflow enforces by process: code generation cannot begin until the intent document is approved.

---

## Branch protection recommendations

For a repository using this methodology, the following branch protection rules on `main` enforce the workflow:

```
Require status checks to pass before merging:
  - Intent document validation
  - Compliance check (once implemented)
  - Security audit (once implemented)

Require branches to be up to date before merging: Yes
Do not allow bypassing the above settings: Yes
Allow force pushes: No
Allow deletions: No
```

The "do not allow bypassing" setting (enforce for administrators) is important: a methodology that can be bypassed by the same person who set it up is not a governed methodology.

---

## Connecting generation to the pipeline

Code generation (Stage 6) is typically triggered locally or in a dedicated environment — not as part of the standard PR pipeline. The recommended pattern:

1. The engineer triggers generation against an approved intent document
2. The AI agent generates an implementation and commits it to a feature branch
3. The engineer opens a PR from the feature branch to `main`
4. The compliance check runs automatically on the PR
5. The security audit runs automatically on the PR
6. On compliance pass and security audit pass, the PR can merge

This keeps the CI pipeline as a verification layer rather than a generation trigger. Generation on demand, compliance on every PR.

---

## Failure handling

| Situation | Correct response |
|---|---|
| Schema validation fails | Fix the intent document frontmatter before advancing |
| Compliance `FAIL` — implementation diverges from intent | Regenerate from the intent document; do not patch the code |
| Compliance `FAIL` — intent document has internal conflict (Document Integrity section) | Return the intent document to Stage 3 (Intent Review Agent) before regenerating |
| Compliance `UNVERIFIABLE` | Note for runtime verification; does not block merge |
| Security `VULNERABILITY` with intent gap | Update the intent document via the Intent Maintenance Agent, then regenerate |
| Security `VULNERABILITY` without intent gap | Regenerate from the existing intent document |
| Security `UNVERIFIABLE` | Document for pre-production penetration testing or runtime verification; does not block merge |
| Intent document not `approved` | Complete the review workflow before generating |

**Neither the compliance agent nor the security agent determines whether the intent was right** — only whether the implementation matches it, and whether the implementation is secure. Failures that reveal a gap in the intent should route through the Intent Maintenance Agent before any regeneration.
