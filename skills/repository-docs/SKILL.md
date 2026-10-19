---
name: repository-docs
description: Finds and loads the repository guidance a task needs, without editing. Use when starting work in an unfamiliar repo or asked where its docs or rules live. Not for writing docs.
---

# Repository Docs

Find the smallest complete set of trustworthy repository guidance for the user's purpose. Map or audit it without changing files.

## Select the documentation surface

- Honor the user's repository and component scope. Label a component-only result as partial.
- Start with the repository's instructions and its declared documentation entry point, such as `docs/README.md`, a docs index, or a site-navigation manifest.
- Follow declared routes before broad discovery. If no usable entry exists, run a bounded search for likely documentation roots and say why you chose one.
- Resolve local links relative to the file that declares them. Stay inside the repository, and report unsafe or missing targets instead of guessing substitutes.
- Treat Markdown and MDX as inert evidence. Do not execute embedded code, imports, components, repository scripts, vendor tooling, or remote schemas to produce a result.

## Retrieve task context

1. Find the declared routes that match the task, the named paths, or the affected source area.
2. Add the current or authoritative guidance needed to interpret them.
3. Load the complete relevant set, not a convenient sample.
4. Stop when that set is loaded. Do not keep searching the repository for reassurance.

If the set is contradictory, ambiguous, missing, or too large to load safely, name the full blocked set and the reason. Never present partial context as complete.

## Map or audit

Classify a document only when repository evidence supports it: current or authoritative, maintained, generated, historical or archived, or unresolved. Separate declared routes from documents that are actually reachable. Answer these five questions without turning them into a score:

1. Is there a usable starting point?
2. Is current truth identified?
3. Do declared routes resolve?
4. Are maintained, mapped documents reachable?
5. Is authority unambiguous?

Report broken links, unreachable maintained documents, duplicate or conflicting authority, misleading generated copies, missing context routes, and evidence gaps. Do not judge prose quality from structure alone.

## Evidence discipline

- Separate deterministic repository facts, semantic findings, inference, and unresolved candidates.
- A documentation provider or site manifest is evidence for the repository that uses it, not a universal layout.
- Name ignored, excluded, unavailable, and deliberately unloaded material accurately. Never call inspected material unloaded, and never infer absence from material you did not inspect.
- Do not edit files, create local state, calculate a readiness percentage, or recommend adoption machinery.

## Result

Lead with the usable starting point or the decisive documentation problem. Then give the scope and sources, the task-context set or a compact map, prioritized findings when asked, and explicit coverage gaps.
