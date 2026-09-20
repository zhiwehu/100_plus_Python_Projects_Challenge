"""Create a folder of dummy files to practice organizing (project 016).

    python3 make_sample_files.py [target-folder]

Default target: ./sample-files
The files contain tiny text placeholders, not real media.
"""

import sys
from pathlib import Path

SAMPLES = {
    "photo1.png": "fake image",
    "photo2.JPG": "fake image",
    "notes.txt": "shopping list",
    "report.pdf": "fake pdf",
    "slides.pptx": "fake slides",
    "data.csv": "a,b,c\n1,2,3\n",
    "song.mp3": "fake audio",
    "clip.mp4": "fake video",
    "backup.zip": "fake archive",
    "script.py": "print('hello')\n",
    "app.js": "console.log('hello')\n",
    "mystery.xyz": "no clue",
}


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("sample-files")
    if target.exists():
        print(f"{target} already exists - remove it first")
        return 1
    target.mkdir()
    for name, content in SAMPLES.items():
        (target / name).write_text(content, encoding="utf-8")
    print(f"created {len(SAMPLES)} sample files in {target}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
