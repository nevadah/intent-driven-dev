# Dependency Propagation Policy

When an intent document changes, units that depend on it may be affected. This policy defines how breaking changes are identified, how downstream dependents are notified, and when re-review is required.

This is a provisional policy. It is based on first principles rather than observed practice. It should be revised as real dependency graphs are encountered.

---

## Classifying Changes

Not all changes to an intent document affect dependents equally. The classification determines what downstream action is required.

### Breaking changes

A change is **breaking** if it alters the observable contract that dependent units rely on. Dependent units declare their reliance through `depends_on` — they expect the depended-on unit's `exposes` interfaces to behave as specified. A breaking change invalidates that expectation.

Breaking changes include:

- **Removed or renamed interface** — an entry in `exposes` is removed or its identifier changes
- **Changed postcondition on an exposed interface** — a dependent unit may rely on a postcondition (e.g., "the token is always invalidated on redemption"); changing it breaks that assumption
- **Changed invariant** — invariants are implicit contracts visible to any caller; tightening or relaxing them can break dependents
- **New precondition on an exposed interface** — the caller must now satisfy an additional precondition it was not previously required to meet
- **Removed scenario** — a scenario represents a supported behavior path; removing one removes a guarantee

### Non-breaking changes

A change is **non-breaking** if it adds capability without altering existing guarantees, or if it is purely internal.

Non-breaking changes include:

- **New scenario added** — adds a supported path without modifying existing ones
- **New entry in `exposes`** — extends the interface without changing existing entries
- **Clarification to domain semantics** — wording changes that do not alter behavior
- **Quality attribute improvements** — tightening a performance threshold or increasing security entropy does not break callers
- **Rationale additions or corrections** — no behavioral change
- **Changes to `must_not_know`** — boundary constraints are internal; callers are unaffected

### Indeterminate changes

Some changes require human judgment to classify:

- **Modified scenario** — may be a clarification (non-breaking) or a behavioral change (breaking); the Intent Maintenance Agent flags these for the approving engineer to classify
- **Modified postcondition** — depends on whether dependent units relied on the specific wording or the behavior it described

---

## Identifying Affected Dependents

The dependency graph is derived from the `depends_on` fields across all intent documents in the repository. A unit is a **downstream dependent** of a changed unit if it declares `depends_on: changed/unit` in its frontmatter.

The Intent Maintenance Agent is responsible for identifying downstream dependents when producing a maintenance report. The report must include:

- The list of dependent units (by `unit` identifier)
- For each dependent: whether the change is likely to affect it (based on which `exposes` entries the dependent references in its own prose sections)
- The classification of the change (breaking, non-breaking, or indeterminate)

If the dependency graph has not been fully mapped (i.e., intent documents exist in the repository that do not have machine-readable `depends_on` fields), the maintenance report must note this as a limitation.

---

## Required Actions by Classification

### Breaking change

1. **All downstream dependents require re-review.** Each dependent unit's intent document must be reviewed for continued accuracy — at minimum at Stage 5 (Engineering Review). If the change alters business-visible behavior, stakeholder review (Stage 4) is also required.
2. **Notification is mandatory.** The authors of dependent units must be explicitly notified before the changed unit's intent document advances past Stage 5.
3. **Dependent units revert to `draft`.** A dependent unit's `status` reverts to `draft` when a breaking change to one of its dependencies is approved. It cannot advance to `approved` again until reviewed in light of the breaking change.
4. **Generated code from dependent units is invalidated.** Code generated from a dependent unit before the breaking change was made cannot be assumed to remain correct. Regeneration is required after the dependent's intent document is reviewed and re-approved.

### Non-breaking change

1. **Downstream dependents do not require automatic re-review.**
2. **Notification is recommended but not required.** Dependent unit authors should be informed so they can assess whether the non-breaking change affects their unit's intent in ways not captured by the formal classification.
3. **Dependent unit status is unchanged.** An `approved` dependent unit remains `approved`.
4. **Generated code from dependent units is not automatically invalidated.** The engineer responsible for the dependent unit may choose to trigger a review if the change is significant in context.

### Indeterminate change

1. **Treat as breaking until classified.** The approving engineer for the changed unit must explicitly classify the change before it advances past Stage 5.
2. **Follow the breaking change procedure** until the classification is resolved.

---

## Known Limitations

This policy has not been validated against real multi-unit dependency graphs. The following are known gaps:

**Transitive dependencies are not addressed.** If Unit A depends on Unit B, and Unit B depends on Unit C, and Unit C changes, this policy covers the B→C relationship but does not specify whether A must also be reviewed. Provisional guidance: treat transitive dependencies as non-breaking unless the change propagates visibly through B's interface.

**Circular dependencies are not addressed here.** The Intent Review Agent flags circular `depends_on` chains as errors. This policy assumes a directed acyclic dependency graph.

**Cross-repository dependencies are not addressed.** If `depends_on` references a unit in a different repository, the notification and re-review mechanisms are manual. Tooling support for cross-repo propagation is out of scope for this version of the policy.

**Version pinning is not defined.** A `depends_on` entry currently references a unit by identifier only, not by version. This means a dependent unit implicitly tracks the latest approved version of its dependency. Explicit version pinning — and the semantics of upgrading a pinned dependency — are deferred to a future revision.
