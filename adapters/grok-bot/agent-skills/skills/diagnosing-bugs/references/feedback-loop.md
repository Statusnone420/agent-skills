# Building a tight feedback loop

Try the smallest useful option first:

1. Failing unit, integration, or end-to-end test.
2. HTTP or command-line script with a precise assertion.
3. Browser automation that checks the DOM, console, or network.
4. Replay of a captured request, trace, payload, or event log.
5. Minimal harness with controlled dependencies.
6. Property or fuzz loop for intermittent wrong output.
7. Differential run against a known-good version or configuration.
8. Automated bisection across commits, versions, or datasets.
9. Human-in-the-loop script based on `scripts/hitl-loop.template.sh`.

A useful loop is:

- **Specific:** It detects the user's exact symptom.
- **Deterministic:** It returns the same verdict, or raises a flaky failure to a useful reproduction rate.
- **Fast:** Prefer seconds.
- **Agent-runnable:** It can run unattended when possible.

Tighten setup time, assertions, randomness, clock behavior, filesystem state, and network dependencies.

If no loop is possible, stop. State what was tried and request the missing environment, a redacted artifact, or authorization for temporary instrumentation. Do not guess from code alone.
