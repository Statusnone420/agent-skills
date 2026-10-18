---
name: comment-discipline
description: Prevent comments and workarounds from replacing durable engineering, or audit comment debt in a bounded code scope.
---

# Comment Discipline

Comments are not implementation. Prefer code that carries its behavior, constraints, and failure modes directly. A comment earns its place only when it preserves information that the code cannot express.

## Select the mode

- **Build mode:** While implementing an authorized change, prevent new comment debt and reject comment-backed shortcuts.
- **Audit mode:** When the user asks to review or clean comments, inspect only the named files, diff, or current task scope. Do not infer a repository-wide cleanup.

Invoking this skill does not authorize unrelated refactoring, broader cleanup, or changes outside the user's requested scope.

## Enforce the engineering gate

Before adding or keeping a comment that explains a workaround, fallback, suppression, special case, temporary path, or surprising branch:

1. Determine whether it records an external constraint or excuses a weakness in code we control.
2. For code we control, fix the root cause within the authorized scope. Prefer a real API, type, invariant, data model, or testable design over a comment-backed patch.
3. Do not complete the task by leaving a TODO, silent fallback, catch-all, duplicate path, compatibility shim, or "temporary" branch unless the product contract requires it and verification covers it.
4. When the root cause is outside the authorized scope or requires a consequential design decision, report the unresolved debt. Do not hide it behind a new comment.
5. When an external system, protocol, platform defect, or compatibility boundary is the real cause, keep the shortest useful `why` comment. Include a stable source or issue reference when one exists.

After a root-cause fix, remove the obsolete workaround and its comment. Do not preserve a comment that describes behavior which no longer exists.

## Keep comments exceptional

Do not add comments that narrate statements, restate names or types, announce sections, paraphrase tests, preserve deleted code, describe edit history, or explain syntax. Do not add decorative separators or prose that a clearer name or smaller unit makes unnecessary.

Preserve and maintain comments that have a concrete contract:

- legal notices, attribution, and generated-file markers;
- compiler, linter, formatter, coverage, build, and type-checker directives;
- public API documentation required by the language or repository;
- non-obvious invariants, security or concurrency reasoning, protocol rules, units, formulas, and external compatibility constraints;
- tracked TODOs that identify a real owner or issue and do not defer work required by the current task.

Treat comment-shaped directives as executable code. Never delete or rewrite one based only on its syntax.

## Audit existing comments

Use repository rules, nearby tests, types, call sites, and history when needed to classify each scoped comment:

- **Delete:** proven narration, decoration, obsolete prose, irrelevant text, or commented-out dead code.
- **Fix:** a comment that exposes an in-scope workaround, suppression, fallback, or design shortcut in code we control.
- **Keep:** a required contract or concise rationale that code cannot express.
- **Unresolved:** anything whose purpose or safety cannot be proved from available evidence.

Delete only high-confidence delete candidates. Fix root causes only when the user's request authorizes executable-code changes. Keep unresolved comments and report what evidence or decision is missing.

Never measure success by deletion count. A successful pass leaves less commentary, no hidden debt, and no weaker behavior.

## Verify

Review the final diff for scope and for comments that no longer match the code. Run the narrowest relevant formatter, lint, typecheck, build, and tests available for the changed behavior.

Report:

- root causes fixed instead of commented around;
- comments removed or shortened;
- required comments added or kept and why;
- unresolved debt and its blocker;
- verification performed and any coverage gap.
