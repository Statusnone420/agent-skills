---
name: superpowers
description: Run a compact, adaptive build, test, and verification workflow.
disable-model-invocation: true
---

# Superpowers

Use this skill only after explicit invocation. Apply lightweight discipline without making every task ceremonial: choose the smallest workflow that fits the risk, preserve room for creative exploration, and require evidence before completion claims.

User instructions, repository instructions, and safety constraints outrank this skill.

## Activation boundary

- Do not activate this skill from topic, intent, or keyword similarity. Generic requests to build, fix, test, plan, brainstorm, or debug are not activation.
- Do not make this skill a bootstrap that runs at session start.
- Do not automatically invoke or impose other process skills because Superpowers is active. Use another skill only when separately requested, explicitly selected, or required by repository instructions.

## Choose the smallest effective mode

Classify the request before acting. Start small and escalate only when evidence or risk demands it.

| Mode | Use when | Minimum shape |
|---|---|---|
| Quick | The change is clear, local, reversible, and low-risk | Inspect context, make the smallest change, run a focused check |
| Focused | Behavior changes, bugs, several files, or meaningful regression risk | Read relevant callers/tests, state acceptance criteria, implement, verify |
| Deep | Requirements or architecture are ambiguous, or the change is high-impact, security-sensitive, data-destructive, or long-lived | Compact brainstorming, a recommendation, approval at consequential boundaries, then a short plan |

Do not choose Deep merely because a task is new. Downgrade when exploration resolves uncertainty; escalate when implementation reveals material risk.

## Core loop

### 1. Establish the contract

- Read the most specific repository instructions, relevant docs/config, callers, types, and tests before editing. Check working-tree status/diff when the workspace is a repository.
- Preserve existing user changes. Do not clean, reset, or rewrite unrelated work.
- Turn the request into observable acceptance criteria and name the command or observation that will prove each criterion.
- Ask one focused question only when an unresolved choice would materially change intent, behavior, architecture, security, cost, data, or an irreversible action. Otherwise make the safest reversible assumption and state it.
- For review, explanation, and diagnosis requests, stay read-only unless implementation is explicitly requested.

### 2. Explore and design just enough

- Follow existing patterns before inventing abstractions, dependencies, or project structure.
- For Deep work, ask only decision-changing questions, present a compact recommendation, and explore alternatives only when the trade-off matters. Do not require a design document, staged approvals, or a long questionnaire by default.
- Prefer a thin, testable slice and YAGNI. Keep speculative improvements out of scope.

### 3. Implement the smallest complete change

- Keep the diff scoped, readable, and compatible with existing public contracts unless the request changes them.
- Fix root causes rather than masking symptoms. Do not swallow errors, weaken types, bypass security, or add silent fallbacks.
- Remove only code made unused by this change. Leave unrelated cleanup alone.

### 4. Use TDD where it buys confidence

Use RED-GREEN-REFACTOR for new or changed behavior, bug fixes, and code with meaningful failure modes when the project has a usable test harness:

1. Write the smallest behavior-focused test or regression reproducer.
2. Run it and confirm it fails for the expected reason when a new test is being added.
3. Write the minimal implementation.
4. Run the focused test, then the relevant broader suite.
5. Refactor only while tests remain green.

Do not force ceremonial tests for documentation, comments, formatting, configuration-only changes, generated/vendor code, throwaway prototypes, or mechanical edits already covered by stronger checks. If test-first is impractical, state why, add the smallest meaningful check available, and compensate with direct verification.

### 5. Debug with evidence

For failures or unexpected behavior:

1. Read the complete error and reproduce the symptom when practical.
2. Inspect recent changes, working examples, dependencies, and data flow.
3. State one falsifiable root-cause hypothesis.
4. Test it with the smallest diagnostic or change.
5. Add a regression test when the issue is a behavior bug, then verify the fix and nearby behavior.

Do not stack guesses. After two failed fix attempts, stop and reassess the hypothesis or architecture before trying another patch.

## Optional isolation and delegation

- Do not create a worktree by default. Use one when the user asks, parallel changes would conflict, the change is risky or long-lived, or the host explicitly requires isolation. Detect existing isolation first and never nest a worktree without a reason.
- Do not delegate by default. Use a subagent only when the task is genuinely independent, parallelizable, or benefits from an independent review. Never let parallel agents edit the same files. Give each agent the relevant task context, inspect its diff and claims yourself, and run verification independently.
- Do not impose a fixed multi-agent review loop, mandatory commits, or a branch-finish menu. Choose the lightest review that matches risk.

## Completion gate

Before saying work is complete, fixed, correct, or passing:

1. Re-read the acceptance criteria.
2. Run fresh, relevant proof: focused tests and the broader suite as appropriate; also run the repository's prescribed lint, typecheck, build, or smoke check when they apply.
3. Inspect the final diff and status for scope, missing files, debug code, generated churn, secrets, and unintended changes. Use `git diff --check` when in Git.
4. Compare observed output to each criterion. Separate pre-existing failures from failures caused by the change.
5. Report the exact checks and results, remaining risk, and anything not verified.

No fresh evidence means no completion claim. Do not commit, merge, push, deploy, delete data, or publish without explicit authorization.

## Working style

- Lead with one clear recommendation.
- Keep plans, questions, reviews, and status updates proportional to the task.
- Preserve creativity: use constraints to improve decisions, not to manufacture ceremony.
- Stop at a verified, useful increment; offer the next consequential choice only when the user needs to make it.
