---
name: orchestrate
description: Coordinate focused subagents for independent, context-isolating, or review work while the parent retains decisions and integration.
---

# Orchestrate

Delegate when bounded work can run independently, reduce parent context, or add a distinct review perspective. The parent keeps architecture, consequential decisions, integration, approvals, and final verification.

## Choose the smallest useful roster

- Keep the parent on the user's selected model and reasoning effort unless the user requests a change.
- Honor explicit subagent model and effort choices. Otherwise, choose from the models and supported effort levels exposed by the current Codex session. Do not infer availability or a permanent role from a model family name.
- Choose the least costly, fastest model that can reliably complete the assignment. Use lower effort for bounded mechanical work; increase capability or effort for ambiguity, interacting constraints, or consequential review. Do not assume minimum effort is always sufficient.
- Use the available model descriptions and task evidence to choose between efficient inspection, routine implementation, and demanding judgment. Do not invent model IDs, prices, agent types, or effort levels.
- If model selection is unavailable, use native inheritance. If an explicitly requested model or effort is unavailable, report the limitation and continue independent parent work; get approval before choosing a replacement.
- Use native read-only or write-capable agent controls appropriate to the authorized assignment.
- Keep urgent, tightly coupled, or consequential work in the parent.

## Delegate safely

1. Define one concrete output for each agent.
2. Start self-contained assignments without parent history. Include prior thread context only when the assignment needs it. Check whether history inheritance also fixes the model or effort; use a focused brief when a different model is required.
3. Permit edits, tests, or Git commands only when the user's request already authorizes that action.
4. Give write-capable agents distinct file or module ownership.
5. State that agents share the codebase, must preserve other edits, and must not revert work they do not own.
6. Prevent overlapping assignments and unnecessary child delegation.
7. Continue useful parent work while agents run.
8. Integrate findings yourself. Resolve conflicts against repository evidence and the user's decisions.

Keep the roster bounded. One agent is enough when one independent track exists.
If native subagents are unavailable, continue in the parent and state that limitation.
