---
name: orchestrate
description: Runs Claude Code subagents while the parent keeps decisions, integration, and final checks. Use when the user asks to delegate, parallelize, or fan out work.
disable-model-invocation: true
---

# Orchestrate

Use Claude Code's native subagent controls for this task.

## Choose the roster

- Keep the parent on the user's selected model and effort unless the user asks for a change.
- Honor explicit subagent model and effort choices. Otherwise select a capable model through the controls the current Claude Code session exposes. Prefer lower cost and latency for bounded work; use more capable models for ambiguity or consequential review.
- Use supported Claude model aliases or exact IDs. Do not hard-code release numbers or assume that a built-in agent type always uses a particular model. When selection is unavailable, use native inheritance.
- Set effort only when the subagent controls support it for the selected model; otherwise keep the host's inherited behavior. Do not change global settings to force a per-task choice.
- If an explicitly requested model or effort is unavailable, or the host reports a substitution, say so and continue independent parent work; get approval before using a replacement.

## Delegate safely

- Delegate only work that can run independently. Start with the smallest useful roster and self-contained briefs that carry only the context each assignment needs.
- Give each subagent one concrete output and non-overlapping file ownership.
- Use native read-only or write-capable agent controls that match the authorized assignment. Preserve other edits and prevent unnecessary child delegation.
- Keep architecture, consequential decisions, integration, and final verification in the parent.
- Delegation never expands the user's authorization, repository scope, or allowed side effects.

If native subagents are unavailable, continue in the parent and say so.
