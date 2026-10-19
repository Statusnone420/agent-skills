---
name: conceptual-review
description: Checks whether a plan, technical claim, or implementation spec holds up before work starts. Use when asked to sanity-check reasoning or review a spec. Not for code diffs.
---

# Conceptual Review

Decide whether reasoning or an implementation spec holds up before anyone builds on it. Stay read-only unless the user separately asks for edits.

## Start with evidence

- Retrieve cheap evidence first: repository state, tests, compiler or typechecker output, docs, logs, benchmarks, configuration, and runtime behavior. Reasoning starts where evidence ends; never reason instead of looking.
- Honor the requested revision, branch, scope, and read limits. When a spec is bound to a commit, read that commit, not the working tree.
- Treat every quotation, number, repository claim, and cited precedent as something to verify.
- Label each material premise as observed, inferred, assumed, or unknown. An unavailable source is a coverage gap, not confirmation.

## Pick the mode

- **Reasoning mode** for a decision, claim, or conclusion.
- **Spec mode** for an implementation contract, plan, or brief that an implementer will follow.

Use both when a spec rests on a contested claim.

## Reasoning mode

1. State the decision or claim.
2. List the premises it depends on, labeled as above.
3. Check that the evidence supports the conclusion without skipped steps, circular support, or more certainty than the premises allow.
4. Look for premises that cannot all be true.
5. Name the weakest important link.
6. Give the strongest credible counterargument or competing explanation. No strawmen.
7. Ask whether another decision handles the key uncertainty better, including reversibility when it matters.
8. Recommend the smallest correction: keep, modify, investigate one named unknown, or switch.

## Spec mode

Check what could make the implementation or its acceptance wrong:

1. **Outcome:** behavior, exclusions, and prerequisites agree with each other.
2. **Sources:** quotations, ranges, protocol rules, formulas, and external facts match their primary sources.
3. **Arithmetic:** counts, boundaries, matrices, and totals recompute exactly.
4. **Coverage:** every affected caller, test, interface, invariant, compatibility promise, and doc sentence is accounted for. Run a bounded search beyond the paths the spec names, without drifting into unrelated architecture review.
5. **Acceptance power:** each required test can fail for the defect it targets. Controls are meaningful, and negative cases have observable failures.
6. **Execution clarity:** file scope, order, edge and failure behavior, and completion proof leave nothing material to guess.
7. **Scope:** precedents and future work do not quietly justify more than the present evidence requires.

Rate findings with the repository's severity terms, or:

- **BLOCKING:** can produce a wrong implementation, a false pass, or unavoidable guesswork.
- **AMEND:** a concrete gap or ambiguity; the approach still stands.
- **NIT:** a wording or evidence fix that does not change the implementation.

## Output

- Lead with the verdict. Reasoning mode: **The reasoning holds up**, or what breaks it. Spec mode: **Ready** or **Not ready**, with the decisive reason.
- Reasoning mode then gives only what matters: key assumptions, weakest link, best counterargument, and recommendation.
- Spec mode then gives numbered findings in priority order (title, severity, exact evidence, why it matters, concrete fix) and a short **Verified** list of important claims that survived.
- End with confidence (high, medium, or low), the evidence most likely to change the verdict, and any coverage gaps or unverified sources.

## Rules

- Raise only points that could change the decision. A clean verdict is valid; never manufacture findings.
- Do not invent probabilities or scores the evidence cannot support.
- Ask the user only when a missing decision or requirement blocks the review. Fetch available facts yourself.
- This review does not authorize implementation, edits, or other consequential action.
- For interface and seam design, recommend `$codebase-design` instead of redoing its method.

Grounding: [Anthropic and Redwood Research's Conceptual Reasoning Index work](https://alignment.anthropic.com/2026/conceptual-reasoning-index/), adapted as a developer workflow. This skill does not implement CRI or its benchmarks.
