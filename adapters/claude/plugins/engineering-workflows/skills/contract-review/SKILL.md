---
name: contract-review
description: Test whether an implementation contract is correct, complete, and executable.
disable-model-invocation: true
---

# Contract Review

Decide whether the contract is ready to hand to an implementer. This workflow is read-only unless the user separately asks to edit the contract.

## Bind the evidence

- Honor the requested revision, branch, scope, and read restrictions. When the contract is bound to a commit, read repository evidence from that commit and do not mix in the working tree.
- Read applicable repository instructions, the complete contract, its declared prerequisites, its named primary sources, and the affected code, tests, interfaces, or data.
- Treat every quotation, number, repository claim, and claimed precedent as something to verify.
- Separate observed evidence, supported inference, assumptions, and unknowns. An unavailable source is a coverage gap, not confirmation.

## Challenge the contract

Check the parts that could make implementation or acceptance wrong:

1. **Outcome:** The requested behavior, exclusions, and prerequisites agree with each other.
2. **Source accuracy:** Quotations, ranges, protocol rules, formulas, and external facts match the named primary sources.
3. **Arithmetic:** Counts, boundaries, matrices, and derived totals recompute exactly.
4. **Repository coverage:** Every affected caller, test, interface, invariant, compatibility statement, and documentation sentence is accounted for.
5. **Acceptance power:** Each required test can fail for the defect it claims to detect. Controls are meaningful. Mutation or negative cases have observable killers.
6. **Execution clarity:** File scope, sequencing, edge behavior, failure behavior, and completion proof leave no material choice for the implementer to guess.
7. **Scope discipline:** Claimed precedents and future work do not silently justify broader implementation than the present evidence requires.

Search beyond paths named by the contract when a bounded repository search can reveal missed affected surfaces. Do not broaden into unrelated architecture review.

## Findings

Use the repository's severity language when it has one. Otherwise use:

- **BLOCKING:** The contract can produce an incorrect implementation, a false acceptance result, or unavoidable material guesswork.
- **AMEND:** A concrete omission or ambiguity should be corrected, but the central approach remains valid.
- **NIT:** A precise wording or evidence correction that does not change implementation.

For each finding, give a short title, severity, exact evidence, why it matters, and a concrete correction. Do not manufacture findings to make the review look useful. If the contract holds up, say so.

## Result

Lead with **Ready** or **Not ready** and the decisive reason. Then provide:

1. numbered findings in priority order;
2. a short **Verified** list for important claims that survived review; and
3. explicit coverage gaps or unverified sources.

`conceptual-review` tests whether technical reasoning follows from its premises. Contract Review tests whether a concrete implementation contract is accurate, complete, and executable.
