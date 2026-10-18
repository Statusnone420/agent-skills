---
name: repository-docs
description: Map and retrieve trustworthy repository documentation without editing it.
---

# Repository Docs

Find the smallest complete set of trustworthy repository guidance for the user's purpose. Map or audit that guidance without changing files.

## Select the documentation surface

- Honor the user's repository and component scope. Label a component result as partial.
- Start with applicable repository instructions and the repository's declared documentation entry, such as `docs/README.md`, a documentation index, or a local site-navigation manifest.
- Follow declared routes before using broad discovery. If no usable entry exists, perform a bounded search for likely documentation roots and state why you selected one.
- Resolve local links relative to the file that declares them. Keep paths inside the selected repository and report unsafe or missing targets without guessing substitutes.
- Treat Markdown and MDX as inert evidence. Do not execute embedded code, imports, components, repository scripts, vendor tooling, or remote schemas to manufacture a result.

## Retrieve task context

When the user needs guidance for a task:

1. Identify the declared routes that match the task, named paths, or affected source area.
2. Include current or authoritative guidance required to interpret those routes.
3. Load the complete relevant set, not a convenient partial sample.
4. Stop when that set is available. Do not continue searching the whole repository for reassurance.

If the required set is contradictory, ambiguous, missing, or too large to load safely, name the full blocked set and the reason. Do not return partial context as if it were complete.

## Map or audit

Classify documents only when repository evidence supports the role:

- current or authoritative;
- maintained;
- generated;
- historical or archived; or
- unresolved.

Distinguish declared routes from documents that are actually reachable. Check these five questions without turning them into a score:

1. Is there a usable starting point?
2. Is current truth identified?
3. Do declared routes resolve?
4. Are maintained mapped documents reachable?
5. Is authority unambiguous?

Report broken links, unreachable maintained documents, duplicate or conflicting authority, misleading generated copies, missing context routes, and evidence gaps. Do not judge prose quality from structure alone.

## Evidence discipline

- Separate deterministic repository facts, semantic findings, inference, and unresolved candidates.
- A documentation provider or site manifest is evidence for the repository that uses it, not a universal topology.
- Name ignored, excluded, unavailable, and deliberately unloaded material accurately. Never call inspected material unloaded or infer absence from material you did not inspect.
- Do not edit files, create local state, calculate a readiness percentage, or recommend adoption machinery.

## Result

Lead with the usable starting point or the decisive documentation problem. Report the selected scope and sources, the task-context set or compact map, prioritized findings when requested, and explicit coverage gaps.
