---
name: oral-exam-trainer
description: Build reusable local oral-exam trainer apps from Markdown or Obsidian study material. Use when Codex needs to turn an exam question list, study notes, or a vault into an interactive self-check web app with answer reveal, light and complete answer versions, confidence ratings, dashboard queues, MathJax formulas, and Mermaid diagrams.
---

# Oral Exam Trainer

## Overview

Use this skill to create or adapt a local oral-exam trainer for a study vault.
The bundled template is a small FastAPI backend plus static frontend that reads
Markdown answer notes and stores personal ratings in a local ignored JSON file.

## Workflow

1. Inspect the user's sources:
   - question list: `.md`, `.txt`, `.csv`, or `.tsv`;
   - study notes or detailed vault;
   - preferred language, answer depth, and topic grouping if stated.
2. Generate answer-note stubs when the user has a question list:
   - run `scripts/questions_to_notes.py <question-list> --light-root <vault>/light-answers --complete-root <vault>/complete-answers`;
   - use `--overwrite` only when the user explicitly wants existing notes replaced.
3. Install the trainer template:
   - run `scripts/install_trainer_template.py <vault>`;
   - the script copies only missing files by default.
4. Fill or adapt answers:
   - write compact oral answers in `light-answers/`;
   - write fuller source-grounded answers in `complete-answers/`;
   - do not invent academic content from thin air unless the user requests draft answers.
5. Customize `trainer.config.json`:
   - set app title/subtitle;
   - set expected question count when known;
   - adjust answer version roots and labels if the vault uses different names.
6. Validate:
   - create/use a virtual environment;
   - install `requirements.txt`;
   - run `python -m trainer.backend.checks`;
   - run `node --check trainer/frontend/app.js` when Node is available.

## Notes

- Read `references/note-schema.md` before generating or editing answer notes.
- Read `references/app-customization.md` before changing the app template or config shape.
- Keep personal progress local: do not commit `trainer/data/progress.json`.
- Use Obsidian/Markdown math delimiters `$...$` and `$$...$$`; avoid `\(...\)` and `\[...\]`.
- Quote Mermaid labels containing brackets, pipes, or math-like text, for example `A["Waveform x[n]"]`.
