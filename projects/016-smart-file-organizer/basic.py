"""Smart File Organizer - Basic version (project 016).

Scans a folder and moves its top-level files into category
subfolders (images/, documents/, ...).

Standard library only.

    python3 basic.py <folder>
"""

import shutil
import sys
from pathlib import Path

# extension (lowercase) -> category folder name
CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"},
    "documents": {".pdf", ".docx", ".txt", ".md", ".csv", ".xlsx"},
    "videos": {".mp4", ".mov", ".avi", ".mkv"},
    "audio": {".mp3", ".wav", ".flac"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
}

OTHER = "other"


def category_of(path):
    """Return the category name for a file, based on its extension."""
    ext = path.suffix.lower()
    for name, exts in CATEGORIES.items():
        if ext in exts:
            return name
    return OTHER


def organize(folder):
    """Move every top-level file in *folder* into its category subfolder."""
    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue  # skip subfolders
        if path.name.startswith("."):
            continue  # skip hidden files like .DS_Store
        target_dir = folder / category_of(path)
        target_dir.mkdir(exist_ok=True)
        shutil.move(str(path), target_dir / path.name)
        print("moved %s -> %s/" % (path.name, category_of(path)))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 basic.py <folder>")
        sys.exit(1)
    organize(Path(sys.argv[1]))
