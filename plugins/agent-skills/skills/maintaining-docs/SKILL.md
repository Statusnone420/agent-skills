---
name: maintaining-docs
description: Writes or updates repository docs from verified evidence with the smallest complete edit. Use when a change makes docs stale or the user asks for docs work. Not for doc lookup.
---

# Maintaining Docs

Make the smallest complete documentation change that helps the intended reader and stays true to the repository. If the user asked only for a diagnosis or a proposal, stay read-only. This skill never authorizes commits, pushes, publishing, deployment, or unrelated changes.

## Establish the change

- Read the repository's instructions, its documentation entry point and current-truth routes, the target documents, and the evidence for the change.
- For a code change, check changed paths and a path-limited diff before searching broadly. Verify claims against code, tests, configuration, runtime behavior, or confirmed intent.
- Separate verified fact, inference, unresolved intent, and future work. Never document a plan as current behavior.
- Name the reader and the job the document must help them do. Use Diátaxis categories when they clarify that need; do not reorganize a library just to fit the framework.

## Make the smallest complete edit

- Fix the existing canonical page before adding another explanation of the same fact.
- Create one focused page only when the repository has no home for the information.
- Fold repeated explanations into one maintained anchor instead of moving the same volume elsewhere.
- Update the docs map or navigation when a route is added, moved, renamed, or removed.
- Edit the generator or canonical source, not a generated copy, when the repository has one.
- Keep local terminology, structure, formatting, and authority conventions unless the user asked to change them.
- Do not add documentation state, receipts, finding IDs, readiness scores, hidden policy, or automatic update machinery.

## Structural changes

Before a move, merge, archive, or removal, show the exact affected files and the resulting tree. Identify current-only or untracked material and the recovery source for anything destructive. Wait for explicit approval unless that exact destructive set was already authorized. Preserve unrelated dirty and untracked work, and never rewrite Git history as part of documentation work.

## Verify

Run the repository's documentation check when one exists. Otherwise verify changed links, anchors, navigation entries, and referenced paths directly. Review the final diff for:

- claims that exceed the evidence;
- duplicated or contradictory guidance;
- edits outside the requested scope;
- generated files changed instead of their source; and
- routes the edit made stale.

Report checks that were unavailable or skipped. Do not claim the whole documentation set is correct from a focused change.

## Result

Lead with what changed for the reader. Name the files changed, the evidence used, the verification results, and any unresolved gap or owner decision.
