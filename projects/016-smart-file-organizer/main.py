"""Smart File Organizer - Better version (project 016).

Organizes a folder into category subfolders using only the standard
library. Adds a CLI (argparse), dry-run preview, copy mode, name
collision handling, logging, and type hints on top of the basic
implementation.

Examples:
    python3 main.py ~/Downloads --dry-run
    python3 main.py ~/Downloads --mode copy
    python3 main.py ~/Downloads --recursive -v
"""
from __future__ import annotations

import argparse
import logging
import shutil
import sys
from pathlib import Path
from typing import Iterable

# extension (lowercase) -> category folder name
CATEGORIES: dict[str, frozenset[str]] = {
    "images": frozenset(
        {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".heic", ".tiff"}
    ),
    "documents": frozenset(
        {".pdf", ".doc", ".docx", ".txt", ".md", ".csv", ".xls", ".xlsx", ".ppt", ".pptx"}
    ),
    "videos": frozenset({".mp4", ".mov", ".avi", ".mkv", ".webm"}),
    "audio": frozenset({".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"}),
    "archives": frozenset({".zip", ".rar", ".7z", ".tar", ".gz", ".dmg"}),
    "code": frozenset(
        {".py", ".js", ".ts", ".java", ".go", ".c", ".cpp", ".h", ".html", ".css", ".json", ".sh"}
    ),
}
OTHER = "other"
CATEGORY_DIRS = frozenset(CATEGORIES) | {OTHER}

log = logging.getLogger("organizer")


def category_of(path: Path) -> str:
    """Return the category name for *path*, based on its extension."""
    ext = path.suffix.lower()
    for name, exts in CATEGORIES.items():
        if ext in exts:
            return name
    return OTHER


def unique_target(path: Path) -> Path:
    """Return *path*, or a sibling with a `` (1)``, `` (2)``, ... suffix
    until the name is free."""
    if not path.exists():
        return path
    n = 1
    while True:
        candidate = path.with_name(f"{path.stem} ({n}){path.suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def iter_files(folder: Path, recursive: bool = False, include_hidden: bool = False) -> Iterable[Path]:
    """Yield the files to organize, sorted for stable output.

    Without *recursive*, only top-level files are considered. With
    *recursive*, files in subfolders are included too, except files that
    already live in a top-level category folder (no double processing).
    Hidden files (``.name``) are skipped unless *include_hidden*.
    """
    if recursive:
        known_dirs = {folder / name for name in CATEGORY_DIRS}
        for path in sorted(folder.rglob("*")):
            if not path.is_file() or path.parent in known_dirs:
                continue
            rel = path.relative_to(folder).parts
            if not include_hidden and any(part.startswith(".") for part in rel):
                continue
            yield path
    else:
        for path in sorted(folder.iterdir()):
            if path.is_file() and (include_hidden or not path.name.startswith(".")):
                yield path


def organize(
    folder: Path,
    mode: str = "move",
    dry_run: bool = False,
    recursive: bool = False,
) -> int:
    """Organize files in *folder* into category subfolders.

    Returns the number of files processed. Raises ``NotADirectoryError``
    if *folder* does not exist or is not a directory.
    """
    if not folder.is_dir():
        raise NotADirectoryError(f"not a directory: {folder}")

    processed = 0
    for src in iter_files(folder, recursive=recursive):
        cat = category_of(src)
        if dry_run:
            log.info("[dry-run] %s -> %s/", src.name, cat)
            processed += 1
            continue

        dest_dir = folder / cat
        dest_dir.mkdir(exist_ok=True)
        dest = unique_target(dest_dir / src.name)
        if mode == "copy":
            shutil.copy2(src, dest)
        else:
            shutil.move(str(src), dest)
        log.info("%-4s %s -> %s", mode, src.name, dest)
        processed += 1
    return processed


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Organize a folder into category subfolders."
    )
    parser.add_argument("folder", type=Path, help="folder to organize")
    parser.add_argument(
        "--mode",
        choices=("move", "copy"),
        default="move",
        help="move files (default) or copy them",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would happen without touching any file",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="also process files in subfolders (category folders are skipped)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="debug logging"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(message)s",
    )
    try:
        count = organize(
            args.folder,
            mode=args.mode,
            dry_run=args.dry_run,
            recursive=args.recursive,
        )
    except NotADirectoryError as exc:
        log.error("%s", exc)
        return 1
    log.info(
        "done: %d file(s) %s",
        count,
        "checked" if args.dry_run else args.mode,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
