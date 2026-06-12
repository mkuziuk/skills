# Trainer App Customization

The template is configured by `trainer.config.json` in the target vault.

## Core fields

```json
{
  "app_title": "Oral Exam Trainer",
  "subtitle": "Self-check dashboard for oral exam prep",
  "question_count": null,
  "default_answer_version": "light",
  "answer_versions": {
    "light": {"label": "Light", "root": "light-answers"},
    "complete": {"label": "Complete", "root": "complete-answers"}
  },
  "required_sections": ["Main idea", "Minimum answer", "Formulas / scheme", "Diagram"],
  "preferred_section_order": {
    "light": ["Main idea", "Minimum answer", "Formulas / scheme", "Diagram"]
  },
  "progress_path": "trainer/data/progress.json"
}
```

## Adaptation guidance

- Keep answer roots separate when the user wants concise and complete answers.
- Set `question_count` to an integer only when the expected count is known.
- Keep `progress_path` inside `trainer/data/` and ignored by git.
- If formulas or Mermaid diagrams are needed, run `npm install && npm run vendor`
  in the generated app to copy local browser assets into `trainer/frontend/vendor/`.
- Do not edit study-note content merely to work around frontend rendering. Fix
  the Markdown renderer unless a Mermaid block is syntactically invalid.
