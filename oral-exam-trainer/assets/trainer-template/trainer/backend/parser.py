from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import re


QUESTION_FILE_RE = re.compile(r"^(?P<number>\d{2,3}) - (?P<title>.+)\.md$")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
MERMAID_RE = re.compile(r"```mermaid\s*\n.*?\n```", re.DOTALL)
IMAGE_RE = re.compile(r"!\[[^\]]*]\(([^)]+)\)")


@dataclass(frozen=True)
class QuestionNote:
    number: int
    title: str
    topic: str
    path: str
    source: str | None
    original_question: str
    sections: dict[str, str]
    section_order: list[str]
    mermaid_count: int
    assets: list[str]

    def summary(self) -> dict[str, Any]:
        return {
            "number": self.number,
            "title": self.title,
            "topic": self.topic,
            "path": self.path,
            "source": self.source,
            "original_question": self.original_question,
            "mermaid_count": self.mermaid_count,
            "assets": self.assets,
        }

    def full(self) -> dict[str, Any]:
        data = self.summary()
        data["sections"] = self.sections
        data["section_order"] = self.section_order
        return data


@dataclass(frozen=True)
class QuestionRecord:
    number: int
    title: str
    topic: str
    path: str
    source: str | None
    original_question: str
    versions: dict[str, QuestionNote]

    def summary(self) -> dict[str, Any]:
        return {
            "number": self.number,
            "title": self.title,
            "topic": self.topic,
            "path": self.path,
            "source": self.source,
            "original_question": self.original_question,
            "answer_versions": list(self.versions),
        }

    def full(self) -> dict[str, Any]:
        data = self.summary()
        data["versions"] = {version: note.full() for version, note in self.versions.items()}
        return data


def answer_roots(config: dict[str, Any]) -> dict[str, str]:
    return {
        version: item["root"]
        for version, item in config.get("answer_versions", {}).items()
        if item.get("root")
    }


def find_question_files(answer_root: Path) -> list[Path]:
    files: list[Path] = []
    if not answer_root.exists():
        return files
    for path in answer_root.rglob("*.md"):
        if QUESTION_FILE_RE.match(path.name):
            files.append(path)
    return sorted(files, key=lambda path: int(path.name.split(" ", 1)[0]))


def parse_all_notes(vault_root: Path, config: dict[str, Any]) -> list[QuestionRecord]:
    notes_by_version: dict[str, dict[int, QuestionNote]] = {}
    for version, folder_name in answer_roots(config).items():
        answer_root = vault_root / folder_name
        notes_by_version[version] = {
            note.number: note
            for note in (parse_note(path, vault_root) for path in find_question_files(answer_root))
        }

    default_version = config.get("default_answer_version", "light")
    primary_notes = notes_by_version.get(default_version) or next(iter(notes_by_version.values()), {})
    records: list[QuestionRecord] = []
    for number in sorted(primary_notes):
        primary = primary_notes[number]
        versions = {
            version: notes[number]
            for version, notes in notes_by_version.items()
            if number in notes
        }
        records.append(
            QuestionRecord(
                number=number,
                title=primary.title,
                topic=primary.topic,
                path=primary.path,
                source=primary.source,
                original_question=primary.original_question,
                versions=versions,
            )
        )
    return records


def parse_note(path: Path, vault_root: Path) -> QuestionNote:
    match = QUESTION_FILE_RE.match(path.name)
    if not match:
        raise ValueError(f"Not a question note: {path}")

    text = path.read_text(encoding="utf-8")
    number = int(match.group("number"))
    title = extract_title(text) or match.group("title")
    sections = extract_sections(text)
    return QuestionNote(
        number=number,
        title=title,
        topic=path.parent.name,
        path=str(path.relative_to(vault_root)),
        source=extract_source(text),
        original_question=extract_original_question(text),
        sections=sections,
        section_order=list(sections),
        mermaid_count=len(MERMAID_RE.findall(text)),
        assets=extract_assets(text),
    )


def validate_notes(notes: list[QuestionRecord], config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = config.get("question_count")
    if expected is not None and len(notes) != int(expected):
        errors.append(f"Expected {expected} question notes, found {len(notes)}")
    if not notes:
        errors.append("No question notes found")

    numbers = [note.number for note in notes]
    if numbers != sorted(numbers):
        errors.append("Question notes are not sorted by number")
    if len(set(numbers)) != len(numbers):
        errors.append("Duplicate question numbers found")

    roots = answer_roots(config)
    default_version = config.get("default_answer_version", "light")
    required_sections = config.get("required_sections", [])
    for note in notes:
        missing_versions = [version for version in roots if version not in note.versions]
        if missing_versions:
            errors.append(f"Question {note.number:02d} missing versions: {', '.join(missing_versions)}")
        primary = note.versions.get(default_version) or next(iter(note.versions.values()), None)
        if not primary:
            continue
        if not primary.original_question:
            errors.append(f"Question {note.number:02d} has no original question")
        missing = [section for section in required_sections if section not in primary.sections]
        if missing:
            errors.append(f"Question {note.number:02d} missing sections: {', '.join(missing)}")
    return errors


def extract_title(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def extract_source(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("Source:"):
            return line.removeprefix("Source:").strip()
    return None


def extract_original_question(text: str) -> str:
    marker = "Original question:"
    start = text.find(marker)
    if start == -1:
        return ""
    rest = text[start + len(marker):]
    next_heading = re.search(r"^##\s+", rest, re.MULTILINE)
    block = rest[: next_heading.start()] if next_heading else rest
    lines = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(">"):
            stripped = stripped[1:].strip()
        lines.append(stripped)
    return " ".join(lines).strip()


def extract_sections(text: str) -> dict[str, str]:
    matches = list(HEADING_RE.finditer(text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        section_name = match.group(1).strip()
        section_start = match.end()
        section_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[section_name] = text[section_start:section_end].strip()
    return sections


def extract_assets(text: str) -> list[str]:
    assets: list[str] = []
    for match in IMAGE_RE.finditer(text):
        target = match.group(1).strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        assets.append(target)
    return assets
