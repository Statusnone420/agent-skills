---
name: agent-skills
description: Use this when the user invokes one of the agent-skills by name (codebase-design, conceptual-review, concise, diagnosing-bugs, english, frontend-design, maintaining-docs, orchestrate, repository-docs).
---

# Agent Skills

Manual only. Run a sub-skill only when the user names it. If the user says agent-skills without a skill name, list the 9 sub-skills below and ask which one to run.

To run a sub-skill, read `skills/<name>/SKILL.md` next to this file and follow it. Open its helper files only when that skill says to.

## Sub-skills

- `codebase-design`: Designs deep modules with small interfaces, real seams, and interface-level tests. Use when shaping a module's API, restructuring code, or choosing test seams. Not for quick fixes.
- `conceptual-review`: Checks whether a plan, technical claim, or implementation spec holds up before work starts. Use when asked to sanity-check reasoning or review a spec. Not for code diffs.
- `concise`: Gives the shortest complete reply without dropping facts, caveats, permissions, or next steps. Use when the user asks for brevity, a TL;DR, or a tighter answer.
- `diagnosing-bugs`: Finds root causes of hard bugs, flaky tests, and performance regressions with a tight repro loop. Use when a bug resists a quick fix or will not reproduce. Not for obvious errors.
- `english`: Explains technical text or the current situation in plain English, without taking action. Use when the user is lost or asks what something means. Not for doing the work.
- `frontend-design`: Designs distinctive, accessible web interfaces instead of generic AI-looking defaults. Use when building or restyling a page, component, or app UI. Not for backend work.
- `maintaining-docs`: Writes or updates repository docs from verified evidence with the smallest complete edit. Use when a change makes docs stale or the user asks for docs work. Not for doc lookup.
- `orchestrate`: Runs focused subagents while the parent keeps decisions, integration, and final checks. Use when the user asks to delegate, parallelize, or fan out work.
- `repository-docs`: Finds and loads the repository guidance a task needs, without editing. Use when starting work in an unfamiliar repo or asked where its docs or rules live. Not for writing docs.

## Grok Bot translation

These skills were written for Codex and Claude Code. In Grok Bot, read them this way:

- **Subagents and sub-agents** (`orchestrate` and `skills/codebase-design/DESIGN-IT-TWICE.md`): use Grok Bot background workers or cloud agents, with the same rules. Give each one concrete output, let no two assignments overlap, and have the parent integrate and verify the results.
- **"The models and effort levels the current Codex session exposes"** (`orchestrate`): use the models Grok Bot offers. If the user named no model, ask which to use. Never choose Fast unless the user asks for it. Ignore `variants/claude.SKILL.md`, the Claude Code edition.
- **`$skill-name` references**, such as `$codebase-design`: run that sub-skill from this bundle.
- **Steps that edit code, run tests, or use Git:** do them in a cloud agent on the connected repository. Never commit, push, merge, or publish without the user's explicit approval.
- **"Do not use tools"** (`english`): answer from the conversation only, and take no actions in that reply.

Source: https://github.com/Statusnone420/agent-skills, version 1.1.0, fingerprint `ed08ad2b5cfc`. License: MIT AND Apache-2.0; see LICENSE, NOTICE.md, and ORIGIN.md next to this file.
