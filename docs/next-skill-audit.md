# Next skill audit

Status: proposed next task; the broader audit has not started.

Scope: the 15 personal skills for Codex and Claude Code on Windows and macOS. Review overlap with
installed third-party skills without changing those plugins. Cursor/Grok Bot and ZCode are retired.
Preserve all canonical and archived artwork and attribution.

## Evidence to collect

- For each machine and host, record the registered source, enabled state, installed version, and
  file comparison with the repository. Do not treat a Git push as an installation update.
- Inspect actual explicit invocations and skill reads over an agreed history window. Exclude
  catalog listings, quoted mentions, and audit activity. Label missing history as unknown usage.
- Compare each skill's purpose with current host capabilities, user instructions, neighboring
  skills, and installed alternatives. Check authorization, model selection, context cost, and
  whether the workflow improves the requested outcome.
- Classify each skill as keep, revise, consolidate, or retire from active distribution, with
  evidence and a proposed destination for any consolidated behavior.
- Check representative requests, including cases where the skill should not run. Static
  validation does not establish behavioral quality. Obtain explicit delegation authorization
  before using subagents for evaluations.

## Review checkpoint

Return the inventory, evidence limits, and proposed changes before editing workflows. Separate
installation fixes from instruction changes. Keep useful specialist behavior when consolidating.
Preserve artwork even when a skill is retired. Do not change marketplace registrations or publish
the next release without authorization.

The current patch removes fixed model rankings from `orchestrate`, retains separate Codex and
Claude variants, and narrows distribution to those two hosts. Mac runtime checks remain separate
from Windows validation and installation checks.
