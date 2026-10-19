<div align="center">

<img src="assets/plugins/agent-skills/plugin-icon.png" width="96" alt="Agent Skills icon">

# Agent Skills

**One suite. Nine focused skills. Codex and Claude Code.**

`Codex` · `Claude Code` · Windows and macOS

</div>

---

Agent Skills is Statusnone's versioned skill suite for codebase design, debugging, reviews,
documentation, plain-English answers, frontend design, and subagent coordination. It ships as one
plugin, `agent-skills`, from the `statusnone-agent-skills` marketplace. Every skill is a peer inside
that plugin; there are no sub-plugins.

## The skills

| | Skill | What it does | Loads |
|---|---|---|---|
| <img src="skills/codebase-design/assets/icon.png" width="36" alt=""> | `codebase-design` | Designs deep modules: small interfaces, real seams, tests at the interface. | On its own |
| <img src="skills/conceptual-review/assets/icon.png" width="36" alt=""> | `conceptual-review` | Checks a plan, technical claim, or implementation spec before work starts. | On its own |
| <img src="skills/concise/assets/icon.png" width="36" alt=""> | `concise` | Gives the shortest complete reply without dropping facts or next steps. | On its own |
| <img src="skills/diagnosing-bugs/assets/icon.png" width="36" alt=""> | `diagnosing-bugs` | Finds root causes of hard bugs, flaky tests, and performance regressions. | On its own |
| <img src="skills/english/assets/icon.png" width="36" alt=""> | `english` | Explains technical text or the current situation in plain English, without acting. | Manual only |
| <img src="skills/frontend-design/assets/icon.png" width="36" alt=""> | `frontend-design` | Gives web interfaces a distinctive, deliberate visual direction. | On its own |
| <img src="skills/maintaining-docs/assets/icon.png" width="36" alt=""> | `maintaining-docs` | Updates repository docs from verified evidence. | On its own |
| <img src="skills/orchestrate/assets/icon.png" width="36" alt=""> | `orchestrate` | Runs focused subagents while the parent keeps decisions and final checks. | Manual only |
| <img src="skills/repository-docs/assets/icon.png" width="36" alt=""> | `repository-docs` | Finds and loads the repository guidance a task needs. | On its own |

**On its own** means the agent loads the skill when a request matches its description. You can also
call it by name. **Manual only** means the skill runs only when you call it: `orchestrate` starts
subagents, which cost time and tokens, and `english` refuses tool use, which would stop real work if
it fired by itself. Grok Build is an exception when Claude Code also has the plugin; see
[Grok Build CLI](#grok-build-cli).

## Calling a skill

| Host | Call it by name | Manual-only setting |
|---|---|---|
| **Claude Code** | `/agent-skills:english`, or `/english` when no other command uses that name | `disable-model-invocation: true` |
| **Codex** | `$agent-skills:english`. Plain `$english` does not find a plugin skill. | `allow_implicit_invocation: false` |

The catalog in `tools/build_adapters.py` sets each skill's mode, and tests check that the generated
Codex and Claude Code settings match it. Delegation never expands the user's authorization,
repository scope, or allowed side effects.

Both `orchestrate` variants keep the user's selected parent model, explicit subagent choices,
authorization, and final verification in the parent. Model roles are not tied to fixed releases.
When a requested choice is unavailable, the agent reports the limitation instead of silently
substituting. The Claude Code variant contains no Codex model names or custom agent framework.

## Load the skills

**Checked** means we ran it here on Windows with the host version named, or this repository's own
checks, a host's CLI help, or a host's validator confirmed it. Each label says which. **Docs** means
it comes from the host's documentation but was not run end to end here.
**Unverified** means it is our best reading and still needs a real test.

### Claude Code (terminal, IDE, and the Code tab in Claude Desktop)

```sh
claude plugin marketplace add Statusnone420/agent-skills
claude plugin install agent-skills@statusnone-agent-skills
```

In a session on Claude Code 2.1.275 or later, one line works too:
`/plugin install agent-skills --marketplace Statusnone420/agent-skills`. Update with
`claude plugin marketplace update statusnone-agent-skills`, then
`claude plugin update agent-skills@statusnone-agent-skills`. Call a skill with
`/agent-skills:english`. **Checked** on Claude Code 2.1.302: the two install commands,
`/agent-skills:english`, `/english`, and `diagnosing-bugs` loading on its own. `english` and
`orchestrate` were not among the skills the model could call. Strict plugin validation passes. The
update commands and the one-line install are checked by command name only.

### Claude on the web and Claude Desktop chat

Zip one folder from `skills/`, such as `skills/concise/`, so that the zip holds that folder with its
`SKILL.md`. Upload it in **Customize → Skills** and switch it on. Upload from `skills/`, not
`adapters/`: uploads reject the `disable-model-invocation` line in the Claude Code copies, so
uploaded skills can always load on their own. Skip `english` and `orchestrate` there. **Docs.**
Claude Desktop chat uses the skills on your claude.ai account. **Unverified.**

### Codex (CLI and the Codex app)

```sh
codex plugin marketplace add Statusnone420/agent-skills
codex plugin add agent-skills@statusnone-agent-skills
```

You can also install from `/plugins` in a session. Start a new session after installing, and refresh
later with `codex plugin marketplace upgrade`. Call a skill with `$agent-skills:english`; plain
`$english` does not find it. **Checked** on Codex CLI 0.162.1: `codex plugin add`, the upgrade,
`$agent-skills:english`, and `diagnosing-bugs` loading on its own. Codex lists only the seven
automatic skills to the model, so `english` and `orchestrate` did not load on their own.
`codex plugin marketplace add` is checked by CLI help, and every skill passes `quick_validate.py`.
**Unverified:** `/plugins` and the Codex app. The IDE extension does not support plugins. **Docs.**

### ChatGPT

Eligible Business, Enterprise, Healthcare, and Edu workspaces can add skills in **Plugins → Plugin
Directory → Skills → Create → Upload from your computer**. Upload a zipped folder from `skills/`.
**Docs**; the zip format is **Unverified**. Workspace admins can also import this repository's Codex
marketplace. **Docs.** On other plans, use Codex.

### Grok Build CLI

```sh
grok plugin marketplace add Statusnone420/agent-skills
grok plugin install agent-skills --trust
grok plugin enable agent-skills
```

Grok reads the Claude Code marketplace, so it needs no separate copy. If Claude Code already has the
marketplace, Grok sees it too and the first line fails with "already configured"; skip it. Plugins
start disabled. `grok plugin enable` lists `agent-skills` under `[plugins] enabled` in
`~/.grok/config.toml`; the Plugins tab works too. Call a skill with `/agent-skills:english`.
**Checked** on Grok 1.0.52 with Claude Code installed: install, enable, `/agent-skills:english`, and
`diagnosing-bugs` loading on its own. `grok plugin validate` accepts the plugin. **Docs:** the
Plugins tab. **Unverified:** Grok without Claude Code.

When Claude Code also has `agent-skills` installed, Grok loads the skills from Claude Code's copy of
this repository at `plugins/agent-skills/`. That is the Codex copy, which has no
`disable-model-invocation` line, so `english` and `orchestrate` can load on their own in Grok.
**Checked** on Grok 1.0.52. Whether Grok honors that line without Claude Code is **Unverified**.

### Cursor and Cursor Grok Bots

- **Cursor agents**, including Grok models in Cursor: copy the folders in
  `adapters/claude/plugins/agent-skills/skills/` to `~/.cursor/skills/` for every project, or to
  `.cursor/skills/` for one. Use these copies because Cursor honors their
  `disable-model-invocation` line. **Docs.**
- **Cursor Grok Bots** (the separate Grok Bot app): Cursor documents no skill-folder or plugin
  import. Paste a skill's `SKILL.md` into the Bot and ask it to save it as a skill. **Unverified.**

## Upgrading from the four plugins

Until October 2026 this repository shipped four plugins: Engineering Workflows, Communication Tools,
Agent Control, and Frontend Design. `agent-skills` replaces all four. Hosts keep installed copies of
the old plugins until you remove them.

Claude Code:

```sh
claude plugin marketplace update statusnone-agent-skills
claude plugin uninstall engineering-workflows@statusnone-agent-skills
claude plugin uninstall communication-tools@statusnone-agent-skills
claude plugin uninstall agent-control@statusnone-agent-skills
claude plugin uninstall frontend-design@statusnone-agent-skills
claude plugin install agent-skills@statusnone-agent-skills
```

New installs on Claude Code 2.1.275 or later can use one line in a session:
`/plugin install agent-skills --marketplace Statusnone420/agent-skills`.

Codex, removing only the old plugins you have:

```sh
codex plugin marketplace upgrade
codex plugin remove engineering-workflows@statusnone-agent-skills
codex plugin remove communication-tools@statusnone-agent-skills
codex plugin remove agent-control@statusnone-agent-skills
codex plugin remove frontend-design@statusnone-agent-skills
codex plugin add agent-skills@statusnone-agent-skills
```

Then start a new session. **Checked** on Codex CLI 0.162.1: these steps replaced all four old
plugins with `agent-skills` 1.1.0.

## Distribution model

```mermaid
flowchart LR
    S["Canonical skills<br/>skills/"] --> B["Catalog and builder<br/>tools/build_adapters.py"]
    B --> C["Codex plugin<br/>plugins/agent-skills/"]
    B --> A["Claude Code plugin<br/>adapters/claude/plugins/agent-skills/"]
    B --> M["Marketplaces<br/>.agents/plugins/ · .claude-plugin/"]
```

`skills/` is the only canonical workflow source. Suite metadata and each skill's invocation mode
live in one catalog at the top of `tools/build_adapters.py`. Host copies, plugin manifests, and both
marketplace files are generated and must never be edited by hand. Mac uses the same packages and
needs no separate adapter.

## Repository map

| Path | Role |
|---|---|
| `skills/` | Canonical skill instructions, assets, and host variants. |
| `tools/build_adapters.py` | Suite catalog and the builder for every generated file. |
| `plugins/agent-skills/` | Generated Codex plugin. |
| `adapters/claude/plugins/agent-skills/` | Generated Claude Code plugin. |
| `assets/plugins/agent-skills/` | Suite artwork. |
| `assets/retired-skills/` | Preserved artwork from retired skills. |
| `assets/retired-plugins/` | Preserved artwork from the four retired plugins. |
| `assets/retired-hosts/` | Preserved artwork from retired adapters, with SHA-256 fingerprints. |
| `.agents/plugins/marketplace.json` | Generated Codex marketplace. |
| `.claude-plugin/marketplace.json` | Generated Claude Code marketplace. |

## Rebuild and verify

Edit skills under `skills/` and suite metadata in the catalog in `tools/build_adapters.py`, then
run:

```sh
python3 tools/build_adapters.py
python3 tools/build_adapters.py --check
python3 -m unittest discover -s tests -v
claude plugin validate . --strict
```

The verification suite rebuilds every generated file in a temporary folder and compares it byte for
byte with the committed copy. It also checks the one-suite layout, each skill's invocation setting,
a "Use when" trigger line in every description, text files under 16 KB, host-specific
orchestration, attribution, the absence of workflow hooks, and preserved artwork. Also validate all
canonical and generated Codex skills with Codex's `quick_validate.py`, and the Claude plugin with
`claude plugin validate PATH --strict`. Windows can use `python` in place of `python3`; set
`PYTHONUTF8=1` for validators that use the platform's default text encoding.

## Retired

- **Skills, October 2026:** `superpowers` (its stop-after-two-failed-fixes rule moved into
  `diagnosing-bugs`), `contract-review` (merged into `conceptual-review` as spec mode),
  `domain-modeling`, `comment-discipline` (now a short rule for personal agent instructions),
  `grill-me`, and `tdd`. Their icons are in `assets/retired-skills/`.
- **Plugins, October 2026:** Engineering Workflows, Communication Tools, Agent Control, and Frontend
  Design, replaced by `agent-skills`. The Engineering Workflows icon became the suite icon; the other
  three are in `assets/retired-plugins/`.
- **Hosts, September 2026:** the Cursor/Grok Bot and ZCode adapters. Their artwork is in
  `assets/retired-hosts/`.

## Releases and installed copies

Version `1.1.0` refreshes `frontend-design` and adds the load instructions above. Version `1.0.0` was
the first `agent-skills` release. Repository updates and installed plugin caches are separate. After an approved release, refresh the marketplace and update the installed plugin
through each host's plugin manager. Restart the host or use a fresh session, then verify the
selected skill path and contents. Do not edit cached skills by hand. Each Windows or Mac
installation must be checked separately; passing repository checks on one machine does not
establish runtime acceptance on the other.

## Attribution and licensing

See [ORIGIN.md](ORIGIN.md), [NOTICE.md](NOTICE.md), and [LICENSE](LICENSE). Most of this repository is
MIT licensed. `skills/frontend-design/` is an Apache-2.0 adaptation and keeps its own `LICENSE.txt`,
so the plugin manifests declare `MIT AND Apache-2.0`. Third-party inspirations and adaptations are
attributed without implying endorsement.
