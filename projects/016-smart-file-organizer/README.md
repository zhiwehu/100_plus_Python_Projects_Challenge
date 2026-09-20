# 016 · Smart File Organizer

> Your Downloads folder is a landfill. Sort it.

A small CLI tool that scans a folder and moves (or copies) its files into
category subfolders: `images/`, `documents/`, `audio/`, `code/`, ...

**Standard library only** — no third-party packages to run it.

## What are we building?

A command-line organizer with these rules:

1. Each top-level file in the target folder is classified by its extension.
2. The file is moved into `<folder>/<category>/`.
3. If the destination already has a file with the same name, the file is
   renamed `name (1).ext`, `name (2).ext`, ... — nothing is ever overwritten.
4. `--dry-run` previews the plan without touching anything.

## Requirements

- Classify files by extension into a fixed set of categories; unknown
  extensions go to `other/`.
- Work in `move` (default) or `copy` mode.
- Skip hidden files (`.DS_Store` and friends) and subfolders by default;
  `--recursive` processes subfolders but never re-processes category
  folders.
- Handle name collisions instead of overwriting.
- Be safe to point at a big folder: `--dry-run` first.

## What will we practice?

- `pathlib` — file paths as objects (`Path`, `suffix`, `with_name`)
- `shutil` — `move` / `copy2`
- `argparse` — a real CLI with flags and choices
- `logging` — structured output instead of `print`
- type hints — readable, checkable function signatures
- `pytest` + `tmp_path` — testing filesystem logic without touching real files
- exit codes — the CLI contract with the shell

## Basic implementation

The core idea fits in a few lines: a dictionary maps categories to
extension sets, a function looks up the extension, and a loop moves files.

```python
CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"},
    "documents": {".pdf", ".docx", ".txt", ".md", ".csv", ".xlsx"},
    "videos": {".mp4", ".mov", ".avi", ".mkv"},
    "audio": {".mp3", ".wav", ".flac"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
}
OTHER = "other"

def category_of(path):
    ext = path.suffix.lower()
    for name, exts in CATEGORIES.items():
        if ext in exts:
            return name
    return OTHER

def organize(folder):
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.name.startswith("."):
            continue
        target_dir = folder / category_of(path)
        target_dir.mkdir(exist_ok=True)
        shutil.move(str(path), target_dir / path.name)
```

Notes:

- `path.suffix.lower()` makes `PHOTO.JPG` and `photo.jpg` behave the same.
- `sorted()` gives a stable, predictable order for the log output.
- `mkdir(exist_ok=True)` is idempotent — safe to run twice.
- The full version with comments lives in [`basic.py`](basic.py). Run it:

  ```bash
  python3 basic.py <folder>
  ```

  The basic version has no dry-run and no collision handling — if
  `images/cat.png` already exists, `shutil.move` silently overwrites it.
  That's a real bug for a tool that touches your files, and the reason the
  next version exists.

## How to run

Everything is in this folder:

```bash
cd projects/016-smart-file-organizer

# 1. Create a practice folder with 12 dummy files
python3 make_sample_files.py

# 2. Preview first — never move real files blind
python3 main.py sample-files --dry-run

# 3. Organize for real
python3 main.py sample-files

# 4. Other useful invocations
python3 main.py sample-files --mode copy     # keep originals
python3 main.py ~/Downloads --recursive -v   # deep + debug output

# 5. Run the tests (only dependency needed, for development)
python3 -m pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

After step 3, `sample-files/` looks like this:

```text
sample-files/
├── archives/backup.zip
├── audio/song.mp3
├── code/app.js
├── code/script.py
├── documents/data.csv
├── documents/notes.txt
├── documents/report.pdf
├── documents/slides.pptx
├── images/photo1.png
├── images/photo2.JPG
├── other/mystery.xyz
└── videos/clip.mp4
```

## Exercises / ideas to extend it

1. **Date subfolders** — move files to `images/2026/09/` instead of
   `images/`, using the file's modified time.
2. **Undo log** — append every move to `organizer.log`; add `--undo` that
   reads the log backwards and puts files back.
3. **Custom categories** — load a JSON file mapping extensions to
   category names, so you can add `.obsidian` files to `documents`.
4. **Age filter** — with `--older-than 7`, only touch files modified more
   than a week ago.
5. **Prefix rename** — `--rename {category}_{name}` turns `cat.png` into
   `images_cat.png`, useful when flattening folders later.

## Better version

[`main.py`](main.py) is the production-shaped version. What changed and
why:

| Basic | Better | Why |
|---|---|---|
| `sys.argv` parsing by hand | `argparse` with `--mode`, `--dry-run`, `--recursive`, `-v` | free `--help`, validation, no index errors |
| overwrites on name collision | `unique_target()` appends ` (1)`, ` (2)`, ... | a file organizer must never destroy data |
| no preview | `--dry-run` | you can always look before you leap |
| `print` | `logging` | one place to control verbosity and format |
| no type hints | full type hints (`Path`, `str`, `int`) | readers (and the compiler, later) know the contract |
| monolithic script | `category_of` / `iter_files` / `organize` / `main` separated | each piece is unit-testable — that's what `tests/` exercises |
| always exits 0 | returns a proper exit code | the shell can tell success from failure |

## AI Upgrade (optional)

Where the basic approach genuinely fails: **a file with no extension, or a
wrong one.** `mystery.xyz` goes to `other/` forever.

A useful AI extension keeps the fast rule-based path for known extensions
and only calls a model for the leftovers:

1. For every file landing in `other/`, read the first few kilobytes.
2. Ask a local or cloud LLM: "Given this raw header, what kind of file is
   this? Answer with one word." (Many formats have stable magic bytes —
   the model just maps bytes to human names.)
3. Optionally, generate a better filename for files named like
   `Screenshot 2026-09-17 at 10.02.33.png`: summarize the content and
   rename to `team-offsite-notes.png`.

Keep it behind `--ai` so the default run stays instant and offline.

---

# 中文说明

一个命令行小工具：扫描文件夹，把顶层文件按扩展名归类到 `images/`、`documents/`、`audio/`、`code/` 等子文件夹。只依赖 Python 标准库。

- **basic.py** — 最简单的实现：扩展名 → 类别字典 + 一个移动循环。没有 dry-run，重名会覆盖，这正好是它的教学点。
- **main.py** — 工程版：`argparse` 命令行、`--dry-run` 预览、`move`/`copy` 两种模式、重名自动改名 ` (1).txt`、`logging`、类型提示、退出码。
- **tests/** — 用 pytest + `tmp_path` 测核心逻辑，不碰真实文件。
- **make_sample_files.py** — 一键生成 12 个假文件，放心练手。

练习：日期子文件夹、undo 日志、JSON 自定义类别、按文件年龄过滤、AI 识别无扩展名/错误扩展名的文件（见上面 AI Upgrade）。
