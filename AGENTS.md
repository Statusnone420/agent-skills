# Repository rules

- Treat `skills/` as the only canonical workflow source.
- Regenerate adapters and marketplaces with `python3 tools/build_adapters.py`; never hand-edit generated files. Plugin metadata lives in its catalog.
- Ship one plugin, `agent-skills`, with every skill as a peer. Do not add plugin buckets.
- Skills load from their descriptions; only `orchestrate` and `english` are manual-only. Change that list only with approval.
- Support Codex and Claude Code on Windows and macOS. Do not add other host adapters or marketplaces without explicit approval.
- Keep Codex `orchestrate` aware of the current session's models and effort levels. Keep the Claude variant native to Claude Code and free of Codex model or role names.
- Preserve all artwork, including retired host, plugin, and skill artwork. Verify file hashes when moving it.
- Do not add hooks, automatic bootstrap, issue-tracker setup, commits, pushes, or publishing behavior to a workflow.
- Preserve the upstream MIT notice and `ORIGIN.md` attribution.
- Before release claims, also run Codex validation and strict Claude validation.
- Before every push, run `python3 tools/build_adapters.py --check` and `python3 -m unittest discover -s tests -v`. CI runs the same check on every pull request.
- Do not publish, push, or change marketplace registrations without the user's explicit approval.

## Code Review Rules

- P1: any break of the repository rules above, especially:
  - generated files that drift from `skills/` or the catalog, or were edited by hand
  - invocation settings that contradict the rules above
  - broken skill frontmatter
  - changed or removed MIT, `NOTICE.md`, or `ORIGIN.md` attribution
  - altered or deleted artwork
  - a skill that adds hooks, automatic bootstrap, commits, pushes, or publishing
- P2: broken links, docs that a change made stale, and missing tests for changed build or check logic.
- Low priority (mention it, don't block on it): wording and style in skill prose.
