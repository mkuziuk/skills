# Run Bundle

Use one artifact root per workflow. Keep every generated file for the workflow inside that root unless the user explicitly requests a different location.

## Root Selection

Respect `artifact root: <path>` exactly when it is safe to do so. If no root is given:

- Use `work/<task-slug>/` for projectless chats or scratch workspaces.
- Use `research/<task-slug>/` inside a target repo or project workspace.

Announce the chosen artifact root before writing files. Use lowercase slugs with letters, digits, and hyphens.

## Files

Create these files as the workflow progresses:

- `manifest.md`: objective, selected mode, artifact root, assumptions, source boundaries, stages, and status.
- `brief.md`: bounded tasks, success criteria, relevant context, and expected memo outputs.
- `agents/<task-id>.md`: one memo per research task, whether delegated or completed sequentially.
- `review.md`: evidence quality, disagreements, gaps, confidence, and decision-relevant findings.
- `executive-summary.md`: final concise answer, key evidence, confidence, risks, decision implications, and next questions.

## Task Memo Format

Each `agents/<task-id>.md` memo should use:

- `## Summary`
- `## Key Evidence`
- `## Method or Context Details`
- `## Sources`
- `## Contradictions or Uncertainty`
- `## Open Questions`

In `## Method or Context Details`, include concrete inputs, outputs, assumptions, or examples when they help the reader understand the finding.

## Review Format

Use these sections in `review.md`:

- `## Verdict`
- `## Evidence Quality`
- `## Agreements and Disagreements`
- `## Gaps and Failure Modes`
- `## Confidence`
- `## Decision-Relevant Findings`
- `## Next Questions`

Preserve uncertainty instead of smoothing it away.

## Executive Summary Format

Use these sections in `executive-summary.md`:

- `## Answer`
- `## Key Evidence`
- `## Confidence`
- `## Risks and Gaps`
- `## Decision Implications`
- `## Recommended Next Questions`
