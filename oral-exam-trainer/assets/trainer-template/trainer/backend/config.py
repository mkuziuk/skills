from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


DEFAULT_CONFIG: dict[str, Any] = {
    "app_title": "Oral Exam Trainer",
    "subtitle": "Self-check dashboard for oral exam prep",
    "question_count": None,
    "default_answer_version": "light",
    "answer_versions": {
        "light": {"label": "Light", "root": "light-answers"},
        "complete": {"label": "Complete", "root": "complete-answers"},
    },
    "required_sections": [
        "Main idea",
        "Minimum answer",
        "Formulas / scheme",
        "Diagram",
        "Examiner follow-ups",
        "Common mistakes",
    ],
    "preferred_section_order": {
        "light": [
            "Main idea",
            "Minimum answer",
            "Formulas / scheme",
            "Diagram",
            "Examiner follow-ups",
            "Common mistakes",
        ]
    },
    "progress_path": "trainer/data/progress.json",
}


def load_config(vault_root: Path) -> dict[str, Any]:
    config = deepcopy(DEFAULT_CONFIG)
    path = vault_root / "trainer.config.json"
    if path.exists():
        merge(config, json.loads(path.read_text(encoding="utf-8")))
    return config


def merge(target: dict[str, Any], source: dict[str, Any]) -> None:
    for key, value in source.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            merge(target[key], value)
        else:
            target[key] = value
