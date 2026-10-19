---
name: orchestrate
description: Runs focused subagents while the parent keeps decisions, integration, and final checks. Use when the user asks to delegate, parallelize, or fan out work.
---

# Orchestrate

Delegate bounded work that can run independently, cut parent context, or add a distinct review. The parent keeps architecture, consequential decisions, integration, approvals, and final verification.

## Choose the smallest useful roster

- Keep the parent on the user's selected model and reasoning effort unless the user asks for a change.
- Honor explicit subagent model and effort choices. Otherwise choose from the models and effort levels the current Codex session exposes. Do not infer availability or a permanent role from a model family name.
- Pick the cheapest, fastest model that can reliably finish the assignment. Use lower effort for bounded mechanical work; raise capability or effort for ambiguity, interacting constraints, or consequential review. Minimum effort is not always enough.
- Use the session's model descriptions and the task's evidence to separate quick inspection, routine implementation, and demanding judgment. Do not invent model IDs, prices, agent types, or effort levels.
- If model selection is unavailable, use native inheritance. If an explicitly requested model or effort is unavailable, report it and continue independent parent work; get approval before choosing a replacement.
- Use native read-only or write-capable agent controls that match the authorized assignment.
- Keep urgent, tightly coupled, or consequential work in the parent.

## Delegate safely

1. Give each agent one concrete output.
2. Start self-contained assignments without parent history. Include prior thread context only when the assignment needs it. Check whether inheriting history also fixes the model or effort; use a focused brief when a different model is needed.
3. Allow edits, tests, or Git commands only when the user's request already authorizes them.
4. Give write-capable agents separate file or module ownership.
5. Tell agents that they share the codebase, must preserve other edits, and must not revert work they do not own.
6. Prevent overlapping assignments and unnecessary child delegation.
7. Keep doing useful parent work while agents run.
8. Integrate findings yourself. Resolve conflicts against repository evidence and the user's decisions.

One agent is enough when there is one independent track. Delegation never expands the user's authorization, repository scope, or allowed side effects. If native subagents are unavailable, continue in the parent and say so.
