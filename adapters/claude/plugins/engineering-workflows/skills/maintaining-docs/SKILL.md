---
name: maintaining-docs
description: Create or update repository documentation from verified evidence.
disable-model-invocation: true
---

# Maintaining Docs

Make the smallest complete documentation change that helps the intended reader and remains true to the repository.

If the user asks only for diagnosis or a proposal, remain read-only. Selecting this workflow does not authorize commits, pushes, publication, deployment, or unrelated changes.

## Establish the change

- Read applicable repository instructions, the documentation entry and current-truth routes, the target documents, and the evidence for the requested change.
- For a code change, inspect changed path names and a path-limited diff before broad search. Verify claims against code, tests, configuration, runtime evidence, or confirmed intent.
- Separate verified fact, inference, unresolved intent, and future work. Do not publish a plan as current behavior.
- Identify the reader and the job the document must help them complete. Use Diátaxis categories when they clarify the reader's need; do not force four folders or reorganize a library merely to satisfy the framework.

## Choose the smallest complete edit

- Prefer correcting an existing canonical page over adding another explanation of the same fact.
- Create one focused page when the repository genuinely lacks a home for the information.
- Consolidate repeated explanation into a short maintained anchor instead of moving the same volume elsewhere.
- Update the documentation map or navigation when a route is added, moved, renamed, or removed.
- Edit a generator or canonical source instead of a generated copy when repository evidence identifies one.
- Preserve local terminology, structure, formatting, and authority conventions unless the user asked to change them.

Do not introduce documentation state, receipts, finding IDs, readiness scores, hidden policy, or automatic update machinery.

## Structural changes

For moves, merges, archives, or removals, first show the exact affected files and resulting tree. Identify current-only or untracked material and the recovery source for anything destructive. Wait for explicit approval when the exact destructive set was not already authorized.

Preserve unrelated dirty and untracked work. Do not rewrite Git history or use repository cleanup as part of documentation maintenance.

## Verify

Run the smallest relevant repository documentation check when one exists. Otherwise verify changed local links, anchors, navigation entries, and referenced paths directly. Review the final diff for:

- claims that exceed the evidence;
- duplicated or contradictory guidance;
- accidental edits outside the requested scope;
- generated files changed instead of their source; and
- stale routes caused by the edit.

Report checks that were unavailable or intentionally skipped. Do not claim the whole documentation set is correct from a focused change.

## Result

Lead with what changed for the reader. Name the files changed, the evidence used, verification results, and any unresolved documentation gap or owner decision.
