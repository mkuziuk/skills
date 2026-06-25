---
name: research-pipeline
description: Use for structured, source-grounded research workflows where an AI agent should clarify an objective, split it into bounded research tasks, gather evidence, optionally coordinate delegated researcher or reviewer passes when the user explicitly allows subagents, and produce an executive summary with confidence, risks, and next questions.
---

# Research Pipeline

Use this skill to run a visible research workflow that turns a broad question into bounded tasks, evidence memos, review, and an executive summary.

## Controls

Recognize these user controls when present:

- `artifact root: <path>`: write the run bundle at the requested relative or absolute path.
- `mode: research | design-review | literature-review | decision-support`: adapt task wording and review criteria to the selected mode.
- `no subagents`: complete the workflow sequentially in the current session.
- `subagents ok`: delegated researcher or reviewer passes are allowed when useful.

If the user does not provide an artifact root, choose a contextual default and announce it before writing:

- Projectless chat or scratch workspace: `work/<task-slug>/`
- Target repo or project workspace: `research/<task-slug>/`

Use a short lowercase slug derived from the objective. Keep all workflow artifacts inside the chosen root.

## Workflow

1. Clarify only when missing details would materially change the research direction, source universe, or decision criteria.
2. Read `references/run-bundle.md` before writing artifacts.
3. Write `manifest.md` and `brief.md` in the artifact root with the objective, assumptions, mode, task list, and success criteria.
4. Split the work into 3-10 bounded research tasks unless the request is narrow enough for fewer.
5. If the user explicitly allowed subagents, read `references/roles.md` and delegate only self-contained researcher or reviewer tasks. Otherwise, produce the same memo structure sequentially.
6. Gather evidence with available file inspection, local context, and web sources when current or external information is needed. Keep important claims traceable to sources.
7. Write one memo per task under `agents/<task-id>.md`.
8. Write `review.md` with evidence quality, disagreements, gaps, confidence, and decision-relevant findings.
9. Write `executive-summary.md` as the final artifact and summarize it in chat with links or paths.

## Evidence Rules

- Separate evidence from inference.
- Preserve source title, URL or local path, date or year when available, and the claim each source supports.
- Mark weak, indirect, stale, inaccessible, contradictory, or low-specificity evidence.
- Do not invent citations, source metadata, URLs, quotes, dates, authors, venues, or results.
- If a delegated pass fails or returns empty output, record the failure in `review.md` and do not hide the gap.

## Executive Summary

End with `executive-summary.md`, not a handoff to another phase. Include:

- concise answer;
- most important evidence;
- confidence level and why;
- risks, disagreements, and gaps;
- decision implications;
- recommended next questions or validation steps.
