---
name: conceptual-review
description: Test whether a technical conclusion follows from its evidence and assumptions.
---

# Conceptual Review

Check whether the reasoning actually holds up before building on it. Review reasoning that already exists; do not turn the review into an interview or implementation unless the user separately asks for that work.

## Start with evidence

Before reasoning conceptually, retrieve any evidence that can cheaply answer the question: repository state, tests, compiler or typechecker output, documentation, logs, benchmarks, runtime behavior, configuration, or other tool output.

If that evidence resolves the issue, use it. Conceptual review begins where empirical verification ends, remains incomplete, or still leaves a genuine judgment call. Prefer `evidence -> reasoning`, never reasoning instead of available evidence.

## Review the reasoning

1. State the actual decision, claim, or conclusion.
2. Identify the material premises it depends on.
3. Classify each material premise as observed evidence, reasonable inference, assumption, or unknown.
4. Check whether the evidence supports the conclusion without skipped steps, circular support, or stronger certainty than the premises allow.
5. Look for contradictions or assumptions that cannot all be true at once.
6. Identify the weakest important link in the reasoning.
7. Give the strongest credible counterargument or competing explanation. Do not use a strawman.
8. Consider whether another decision handles the important uncertainty better, including reversibility when it materially changes the choice.
9. Recommend the smallest meaningful correction: keep the reasoning, modify it, investigate one specific unknown, or choose the stronger alternative.
10. State confidence and name the evidence most likely to change the conclusion.

Surface only points that could change the decision. Do not manufacture criticism because the skill was invoked; a valid verdict is **The reasoning holds up.** Do not invent precise probabilities or scores when the evidence cannot support them.

Ask the user only when a genuinely missing decision or requirement prevents a useful review. Retrieve facts available from the environment yourself.

## Output

Default to a compact, actionable review:

- **Verdict:** one or two sentences.
- **Key assumptions:** only assumptions that materially affect the conclusion.
- **Weakest link:** the most consequential unsupported or uncertain step.
- **Best counterargument:** the strongest credible opposing case.
- **Recommendation:** keep, modify, investigate, or choose the better alternative.
- **Confidence:** high, medium, or low, plus the missing evidence most likely to change the verdict.

Omit headings that add no value. Take more space only when the decision genuinely requires it.

## Boundaries

- `$grill-me` resolves a design tree through an interactive interview. Conceptual Review normally assesses reasoning already present and returns a result.
- `$codebase-design` owns deep-module, interface, and seam design. Recommend it when that specialized analysis is needed rather than absorbing its method.
- `$concise` owns response compression. Conceptual Review owns the reasoning method; both may compose when explicitly invoked.
- This workflow reviews a decision. It does not authorize implementation, edits, or other consequential action.

Conceptual grounding: [Anthropic and Redwood Research's Conceptual Reasoning Index work](https://alignment.anthropic.com/2026/conceptual-reasoning-index/), adapted here as a developer workflow focused on argument quality, consistency, and judgment under uncertainty. This skill does not implement CRI or its benchmarks.
