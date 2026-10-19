# Skill audit

Status: done in October 2026. This page records the outcome and the open follow-ups.

## Outcome

- One plugin, `agent-skills`, replaces the four plugins. Every skill is a peer inside it.
- Kept (9): `codebase-design`, `conceptual-review`, `concise`, `diagnosing-bugs`, `english`,
  `frontend-design`, `maintaining-docs`, `orchestrate`, and `repository-docs`.
- Merged: `contract-review` into `conceptual-review` as spec mode, and the stop-after-two-failed-fixes
  rule from `superpowers` into `diagnosing-bugs`.
- Retired: `superpowers`, `contract-review`, `domain-modeling`, `comment-discipline`, `grill-me`, and
  `tdd`. `comment-discipline` became a short rule for personal agent instructions.
- Invocation: skills load from their descriptions. `orchestrate` stays manual-only because it starts
  subagents, and `english` stays manual-only because it refuses tool use.
- Cursor/Grok Bot and ZCode stay retired. Grok Build reads the Claude Code marketplace directly, so
  it needs no separate adapter.

## Follow-ups

- Refresh `frontend-design` against the current upstream skill and WCAG 2.2 AA basics.
- Document how to load the suite in each host, and mark the steps that are not verified.
- After each release, check the installed copies on every Windows and Mac machine. Repository checks
  do not prove runtime behavior.
