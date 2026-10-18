---
name: diagnosing-bugs
description: Diagnose hard bugs and performance regressions with a tight feedback loop.
disable-model-invocation: true
---

# Diagnosing Bugs

Build a fast, specific pass/fail signal before forming a strong theory. Redact secrets from commands, output, traces, and captured artifacts.

## Workflow

1. **Reproduce.** Create one command that reaches the user's exact symptom and can fail on this bug. Read [references/feedback-loop.md](references/feedback-loop.md) when no tight reproducer exists.
2. **Minimize.** Remove inputs, steps, callers, and configuration one at a time. Keep only what is required for the failure.
3. **Hypothesize.** Write 3-5 ranked, falsifiable causes. For each, state the observation that would support or reject it.
4. **Probe.** Change one variable at a time. Prefer a debugger or focused boundary instrumentation. Tag temporary logs with a unique `[DEBUG-...]` prefix.
5. **Lock the fix.** Turn the smallest real reproduction into a failing regression test at the correct public seam when one exists. Apply the smallest fix. Run the test and the original reproduction again.
6. **Clean up.** Remove temporary instrumentation and harnesses. State the cause, evidence, fix, and remaining coverage gap.

For a performance regression, measure a baseline and profile or bisect before changing code. Logs alone are not a performance diagnosis.

If no correct test seam exists, document that limitation. After the bug is fixed, use `$codebase-design` to assess whether the missing seam warrants structural work.

Do not claim success unless the original symptom is gone and the available regression check passes.
