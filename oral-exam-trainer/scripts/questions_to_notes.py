#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path


DEFAULT_SECTIONS = [
    "Main idea",
    "Minimum answer",
    "Formulas / scheme",
    "Diagram",
    "Examiner follow-ups",
    "Common mistakes",
]


@dataclass(frozen=True)
class Question:
    number: int
    question: str
    topic: str
    title: str | None = None
    source: str | None = None


def main() -> int:
    parser = argparse.ArgumentParser(description="Create oral-exam answer stubs from a question list.")
    parser.add_argument("question_list", type=Path)
    parser.add_argument("--light-root", type=Path, default=Path("light-answers"))
    parser.add_argument("--complete-root", type=Path)
    parser.add_argument("--source-label", default=None)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    questions = load_questions(args.question_list)
    if not questions:
        raise SystemExit("No questions found.")

    source_label = args.source_label or args.question_list.name
    written = write_notes(questions, args.light_root, source_label, args.overwrite)
    complete_written = 0
    if args.complete_root:
        complete_written = write_notes(questions, args.complete_root, source_label, args.overwrite)

    print(f"questions: {len(questions)}")
    print(f"light notes written: {written}")
    if args.complete_root:
        print(f"complete notes written: {complete_written}")
    return 0


def load_questions(path: Path) -> list[Question]:
    suffix = path.suffix.lower()
    if suffix in {".csv", ".tsv"}:
        return load_table(path, delimiter="\t" if suffix == ".tsv" else ",")
    return load_text(path)


def load_table(path: Path, delimiter: str) -> list[Question]:
    rows = path.read_text(encoding="utf-8-sig").splitlines()
    sample = "\n".join(rows[:5])
    has_header = csv.Sniffer().has_header(sample) if sample else False
    questions: list[Question] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        if has_header:
            reader = csv.DictReader(handle, delimiter=delimiter)
            for index, row in enumerate(reader, start=1):
                question = first_present(row, ["question", "original_question", "prompt", "text"])
                if not question:
                    continue
                number = int(first_present(row, ["number", "no", "id"]) or index)
                topic = first_present(row, ["topic", "section", "category"]) or "Questions"
                title = first_present(row, ["title", "name"])
                source = first_present(row, ["source"])
                questions.append(Question(number, question.strip(), topic.strip(), title, source))
        else:
            reader = csv.reader(handle, delimiter=delimiter)
            for index, row in enumerate(reader, start=1):
                cells = [cell.strip() for cell in row if cell.strip()]
                if not cells:
                    continue
                questions.append(Question(index, cells[-1], cells[0] if len(cells) > 1 else "Questions"))
    return sorted(questions, key=lambda item: item.number)


def load_text(path: Path) -> list[Question]:
    questions: list[Question] = []
    current_topic = "Questions"
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        heading = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if heading:
            current_topic = heading.group(1)
            continue
        if line.startswith("```"):
            continue
        line = re.sub(r"^>\s*", "", line)
        line = re.sub(r"^[-*]\s+", "", line)
        line = re.sub(r"^\d{1,3}[.)-]\s+", "", line)
        if len(line) < 3:
            continue
        questions.append(Question(len(questions) + 1, line, current_topic))
    return questions


def first_present(row: dict[str, str | None], keys: list[str]) -> str | None:
    lowered = {key.lower().strip(): value for key, value in row.items() if key}
    for key in keys:
        value = lowered.get(key)
        if value and value.strip():
            return value.strip()
    return None


def write_notes(questions: list[Question], root: Path, source_label: str, overwrite: bool) -> int:
    topic_names: dict[str, str] = {}
    written = 0
    for question in questions:
        topic_dir = topic_names.setdefault(question.topic, topic_folder_name(len(topic_names) + 1, question.topic))
        title = question.title or title_from_question(question.question)
        path = root / topic_dir / f"{question.number:02d} - {safe_filename(title)}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not overwrite:
            continue
        path.write_text(note_text(question, title, source_label), encoding="utf-8")
        written += 1
    return written


def topic_folder_name(index: int, topic: str) -> str:
    topic = topic.strip()
    if re.match(r"^Topic \d{1,3} - ", topic):
        return topic
    return f"Topic {index:02d} - {safe_filename(topic, max_words=8)}"


def title_from_question(question: str) -> str:
    words = re.findall(r"[\wА-Яа-яЁё-]+", question, flags=re.UNICODE)
    return " ".join(words[:8]) or "Question"


def safe_filename(value: str, max_words: int = 10) -> str:
    words = re.findall(r"[A-Za-z0-9А-Яа-яЁё-]+", value, flags=re.UNICODE)[:max_words]
    return " ".join(words) if words else "Question"


def note_text(question: Question, title: str, source_label: str) -> str:
    sections = "\n\n".join(section_stub(section) for section in DEFAULT_SECTIONS)
    return f"""# {title}

Source: `{question.source or source_label}`, Question {question.number:02d}

Original question:

> {question.question}

{sections}
"""


def section_stub(section: str) -> str:
    if section == "Diagram":
        return """## Diagram

```mermaid
flowchart LR
    A[Question] --> B[Answer]
```"""
    return f"""## {section}

TODO"""


if __name__ == "__main__":
    raise SystemExit(main())
