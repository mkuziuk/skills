# Research Roles

Use these role contracts only when the user explicitly allows delegated work, for example by saying `subagents ok` or asking for subagents, delegation, or parallel agent work.

## Researcher

Give each researcher exactly one bounded task with:

- stable task id;
- one specific question;
- objective context;
- source boundaries;
- expected memo format;
- any time, domain, or quality constraints.

Ask the researcher to return Markdown only, using:

- `## Summary`
- `## Key Evidence`
- `## Method or Context Details`
- `## Sources`
- `## Contradictions or Uncertainty`
- `## Open Questions`

The researcher must not broaden the task, invent source metadata, or hide weak evidence. Ask for concrete inputs, outputs, assumptions, or examples when relevant to the task.

## Reviewer

Use a reviewer after task memos exist, or sequentially perform the same review if delegation is not allowed.

Give the reviewer:

- original objective;
- selected mode;
- artifact root;
- path list for `brief.md` and task memos;
- any user decision criteria.

Ask the reviewer to return Markdown only, using:

- `## Verdict`
- `## Evidence Quality`
- `## Agreements and Disagreements`
- `## Gaps and Failure Modes`
- `## Confidence`
- `## Decision-Relevant Findings`
- `## Next Questions`

The reviewer should grade confidence, name the strongest and weakest evidence, preserve disagreements, and identify what remains unanswered.
