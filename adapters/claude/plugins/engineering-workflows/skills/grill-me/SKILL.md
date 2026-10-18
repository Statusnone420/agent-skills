---
name: grill-me
description: Stress-test a plan, design, or decision through a structured interview.
disable-model-invocation: true
---

# Grill Me

Interview the user until the important decisions and assumptions are explicit. Treat the topic as a decision tree: settled choices reveal the next choices that depend on them.

## Run the interview

1. State the decision being tested and the intended outcome.
2. Build the current frontier: every question that can be answered now without depending on another open question.
3. Ask the whole frontier in one numbered round. Give your recommended answer for each question.
4. Wait for the user's answers.
5. Update the decision tree and repeat until no important branch remains open.

Use this format:

```text
Q1 - <short title>: <question and useful choices>

Recommendation: <your answer and brief reason>
```

Ask only decision-relevant questions. Do not add ceremony, repeat settled choices, or ask the user for facts you can safely inspect yourself. Use tools for available facts. Use a bounded read-only subagent only when the fact-finding is substantial and independent.

The decisions remain the user's. Separate facts, recommendations, and user choices.

Finish with a compact decision record:

- Settled decisions
- Remaining assumptions or risks
- Recommended next action

Do not implement the result until the user confirms the shared understanding or separately asks for implementation.

When the user wants decisions documented during the interview, also invoke `$domain-modeling`.
