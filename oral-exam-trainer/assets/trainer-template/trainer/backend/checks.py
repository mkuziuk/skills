from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from .config import load_config
from .dashboard import build_dashboard
from .parser import answer_roots, find_question_files, parse_all_notes, validate_notes
from .progress import ProgressStore


def main() -> int:
    vault_root = Path(__file__).resolve().parents[2]
    config = load_config(vault_root)
    notes = parse_all_notes(vault_root, config)
    errors = validate_notes(notes, config)
    progress = ProgressStore(vault_root / config["progress_path"]).read()
    dashboard = build_dashboard(notes, progress)

    roots = answer_roots(config)
    for version, folder_name in roots.items():
        paths = find_question_files(vault_root / folder_name)
        if not paths:
            errors.append(f"No {version} answer notes found in {folder_name}")

    with TemporaryDirectory() as temp_dir:
        temp_progress = ProgressStore(Path(temp_dir) / "progress.json")
        updated = temp_progress.update_rating(notes[0].number if notes else 1, 4)
        reread = temp_progress.question_progress(notes[0].number if notes else 1)
        if updated["rating"] != 4 or reread.get("review_count") != 1:
            errors.append("Progress rating write/read check failed")

    if errors:
        print("Checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Checks passed:")
    print(f"- question notes: {dashboard['summary']['total_questions']}")
    print(f"- answer versions: {', '.join(roots)}")
    print(f"- topics: {len(dashboard['topic_coverage'])}")
    print(f"- suggested queue: {len(dashboard['suggested_queue'])}")
    print("- progress write/read: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
