---
name: diagnosing-bugs
description: Finds root causes of hard bugs, flaky tests, and performance regressions with a tight repro loop. Use when a bug resists a quick fix or will not reproduce. Not for obvious errors.
---

# Diagnosing Bugs

Build a fast, specific pass/fail signal before forming a strong theory. Redact secrets from commands, output, traces, and saved artifacts.

## Loop

1. **Reproduce.** Write one command that reaches the user's exact symptom and can fail on this bug. If no tight reproducer exists, read [references/feedback-loop.md](references/feedback-loop.md).
2. **Minimize.** Remove inputs, steps, callers, and configuration one at a time. Keep only what the failure needs.
3. **Hypothesize.** Write 3-5 ranked, falsifiable causes. For each, name the observation that would confirm or reject it.
4. **Probe.** Change one variable at a time. Prefer a debugger or focused instrumentation at boundaries. Tag temporary logs with a unique `[DEBUG-...]` prefix.
5. **Lock the fix.** Turn the smallest real reproduction into a failing regression test at the right public seam. Apply the smallest fix. Rerun the test and the original reproduction.
6. **Clean up.** Remove temporary instrumentation and harnesses. Report the cause, evidence, fix, and any remaining coverage gap.

## Rules

- After two failed fix attempts, stop. Recheck the hypothesis or the design before trying another patch. Do not stack guesses.
- For a performance regression, measure a baseline and profile or bisect before changing code. Logs alone are not a performance diagnosis.
- If no correct test seam exists, say so. After the fix, use `$codebase-design` to judge whether the missing seam needs structural work.
- Claim success only when the original symptom is gone and the regression check passes.
