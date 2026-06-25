# Codex Skills

Custom global Codex skills from `~/.codex/skills`, excluding built-in `.system`
skills.

## Skills

- `research-pipeline`: structured, source-grounded research workflows that
  produce an executive summary.
- `frontend-skill`: guidance for visually strong landing pages, apps, prototypes,
  demos, and game UI.
- `jupyter-notebook`: templates and helpers for creating reproducible Jupyter
  notebooks for experiments and tutorials.
- `oral-exam-trainer`: a reusable local oral-exam trainer app template for
  Markdown or Obsidian study material.
- `security-threat-model`: repository-grounded AppSec threat modeling workflow
  and report template.

## Install

To install these skills into another Codex environment:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
rsync -a --exclude='.git' ./ "${CODEX_HOME:-$HOME/.codex}/skills/"
```
