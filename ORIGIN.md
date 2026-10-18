# Origin and modifications

## Matt Pocock engineering workflows

The Engineering Workflows plugin was adapted from
[`mattpocock/skills`](https://github.com/mattpocock/skills) at commit
`84fdeffd12f2ee307994d1eb6feb48173b6e0502`.

Upstream paths used:

- `skills/productivity/grill-me`
- `skills/productivity/grilling`
- `skills/engineering/grill-with-docs`
- `skills/engineering/domain-modeling`
- `skills/engineering/diagnosing-bugs`
- `skills/engineering/tdd`
- `skills/engineering/codebase-design`

Statusnone modifications include explicit-only invocation, separate generated host adapters,
local-file composition for manual-only dependencies, marketplace packaging, original artwork, and
distribution validation. The public `grilling` and `grill-with-docs` entrypoints were consolidated
into `grill-me`; their original artwork is preserved under `assets/retired-skills/`.

## Frontend Design

`skills/frontend-design/` is a Statusnone-maintained Codex and Claude Code adaptation of Anthropic's
[`frontend-design`](https://github.com/anthropics/skills/tree/main/skills/frontend-design) skill.
The upstream work is licensed under Apache License 2.0. Its complete license is retained at
`skills/frontend-design/LICENSE.txt` and is copied into each generated adapter.

Statusnone modifications include Codex-oriented wording and workflow refinements, explicit-only host
metadata, plugin packaging, and original artwork.

## Superpowers

`skills/superpowers/` is Statusnone's compact personal workflow. Its name and adaptive development
discipline were inspired by Jesse Vincent's
[`obra/superpowers`](https://github.com/obra/superpowers), which is MIT licensed. This repository does
not redistribute that project's complete suite, automatic bootstrap, hooks, or installation system.

## Other personal skills

The remaining Communication Tools and Agent Control skills originated in Statusnone's personal Codex
workflow library and were consolidated here for versioned maintenance and private backup.

`orchestrate` grew from the former Luna delegation route. Its Codex edition now selects from the
current session's models and effort levels. Claude Code receives a native variant that uses its
own subagent controls. The former `ask-pro` and `claude-handoff` skills are not part of the active
catalog. Historical skill artwork remains under `assets/retired-skills/`.

Cursor/Grok Bot and ZCode distributions were retired in September 2026. Their packaged artwork
is preserved unchanged under `assets/retired-hosts/`; canonical artwork remains in its original
locations.

`comment-discipline` is a Statusnone-native workflow for preventing comment-backed engineering shortcuts.

`contract-review`, `repository-docs`, and `maintaining-docs` are Statusnone-native compact workflows.
They distill observed contract-review practice and the useful evidence, routing, and maintenance ideas
from Statusnone's Diátaxis Docs project. They do not redistribute its checker, lifecycle system,
operational state, or release machinery.

This repository is unofficial. It is not affiliated with or endorsed by Matt Pocock, Anthropic, or
Jesse Vincent.
