#!/usr/bin/env python3
from __future__ import annotations

import argparse
import filecmp
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the oral-exam trainer template into a vault.")
    parser.add_argument("target", type=Path)
    parser.add_argument("--template", type=Path, default=Path(__file__).resolve().parents[1] / "assets" / "trainer-template")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    if not args.template.is_dir():
        raise SystemExit(f"Template not found: {args.template}")
    args.target.mkdir(parents=True, exist_ok=True)

    copied = skipped = identical = 0
    for source in sorted(path for path in args.template.rglob("*") if path.is_file()):
        relative = source.relative_to(args.template)
        if any(part == "__pycache__" for part in relative.parts):
            continue
        target = args.target / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if filecmp.cmp(source, target, shallow=False):
                identical += 1
                continue
            if not args.overwrite:
                skipped += 1
                continue
        shutil.copy2(source, target)
        copied += 1

    print(f"template: {args.template}")
    print(f"target: {args.target}")
    print(f"copied: {copied}")
    print(f"identical: {identical}")
    print(f"skipped existing: {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
