from __future__ import annotations

from collections import defaultdict
from typing import Any

from .parser import QuestionRecord


def merge_note_progress(note: QuestionRecord, progress: dict[str, Any]) -> dict[str, Any]:
    data = note.summary()
    data["progress"] = progress.get("questions", {}).get(str(note.number), {})
    return data


def build_dashboard(notes: list[QuestionRecord], progress: dict[str, Any]) -> dict[str, Any]:
    merged = [merge_note_progress(note, progress) for note in notes]
    rated = [item for item in merged if item["progress"].get("rating")]
    ratings = [item["progress"]["rating"] for item in rated]
    average = round(sum(ratings) / len(ratings), 2) if ratings else None
    return {
        "summary": {
            "total_questions": len(notes),
            "rated_questions": len(rated),
            "unrated_questions": len(notes) - len(rated),
            "average_rating": average,
        },
        "suggested_queue": suggested_queue(merged),
        "weakest_questions": weakest_questions(merged),
        "topic_coverage": topic_coverage(merged),
    }


def suggested_queue(questions: list[dict[str, Any]], limit: int = 12) -> list[dict[str, Any]]:
    return sorted(questions, key=lambda item: queue_score(item))[:limit]


def weakest_questions(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(questions, key=lambda item: (item["progress"].get("rating") or 0, item["number"]))


def queue_score(item: dict[str, Any]) -> tuple[int, int, int]:
    progress = item.get("progress", {})
    rating = progress.get("rating")
    review_count = progress.get("review_count", 0)
    unrated = 0 if rating is None else 1
    return (unrated, rating or 0, review_count)


def topic_coverage(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for question in questions:
        grouped[question["topic"]].append(question)
    rows = []
    for topic, items in sorted(grouped.items()):
        rated = [item for item in items if item["progress"].get("rating")]
        ratings = [item["progress"]["rating"] for item in rated]
        rows.append(
            {
                "topic": topic,
                "total": len(items),
                "rated": len(rated),
                "coverage_percent": round(100 * len(rated) / len(items)) if items else 0,
                "average_rating": round(sum(ratings) / len(ratings), 2) if ratings else None,
                "weak_count": len([item for item in items if (item["progress"].get("rating") or 0) <= 2]),
            }
        )
    return rows
