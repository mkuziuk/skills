from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


EMPTY_PROGRESS = {"questions": {}}


class ProgressStore:
    def __init__(self, path: Path):
        self.path = path

    def read(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"questions": {}}
        with self.path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if "questions" not in data or not isinstance(data["questions"], dict):
            return {"questions": {}}
        return data

    def write(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")

    def question_progress(self, number: int) -> dict[str, Any]:
        return self.read().get("questions", {}).get(str(number), {})

    def update_rating(self, number: int, rating: int, note: str | None = None) -> dict[str, Any]:
        data = self.read()
        questions = data.setdefault("questions", {})
        key = str(number)
        current = questions.setdefault(key, {})
        now = datetime.now(timezone.utc).isoformat()
        current["rating"] = rating
        current["review_count"] = int(current.get("review_count", 0)) + 1
        current["last_reviewed"] = now
        current.setdefault("history", []).append({"rating": rating, "reviewed_at": now})
        if note is not None:
            current["note"] = note
        self.write(data)
        return current
