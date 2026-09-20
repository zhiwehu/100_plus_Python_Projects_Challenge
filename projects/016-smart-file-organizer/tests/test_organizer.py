"""Tests for the Smart File Organizer core logic (project 016).

No UI, camera, or external services needed - pure filesystem logic.

Run from the project folder:

    python3 -m pytest tests/ -v
"""
from pathlib import Path

import pytest

from main import CATEGORIES, OTHER, category_of, organize, unique_target


def touch(folder: Path, name: str, content: str = "x") -> Path:
    path = folder / name
    path.write_text(content, encoding="utf-8")
    return path


class TestCategoryOf:
    def test_image_extension(self):
        assert category_of(Path("photo.JPG")) == "images"

    def test_document_extension(self):
        assert category_of(Path("notes.pdf")) == "documents"

    def test_code_extension(self):
        assert category_of(Path("script.py")) == "code"

    def test_unknown_extension_is_other(self):
        assert category_of(Path("file.xyz123")) == "other"

    def test_no_extension_is_other(self):
        assert category_of(Path("Makefile")) == "other"

    def test_category_names_are_unique_and_not_other(self):
        assert len(set(CATEGORIES)) == len(CATEGORIES)
        assert OTHER not in CATEGORIES


class TestUniqueTarget:
    def test_returns_path_when_free(self, tmp_path):
        assert unique_target(tmp_path / "a.txt") == tmp_path / "a.txt"

    def test_adds_suffix_on_collision(self, tmp_path):
        touch(tmp_path, "a.txt")
        assert unique_target(tmp_path / "a.txt") == tmp_path / "a (1).txt"
        touch(tmp_path, "a (1).txt")
        assert unique_target(tmp_path / "a.txt") == tmp_path / "a (2).txt"


class TestOrganize:
    def test_moves_files_into_categories(self, tmp_path):
        touch(tmp_path, "cat.png")
        touch(tmp_path, "report.pdf")
        touch(tmp_path, "script.py")
        touch(tmp_path, "weird.bin")

        count = organize(tmp_path)

        assert count == 4
        assert (tmp_path / "images" / "cat.png").is_file()
        assert (tmp_path / "documents" / "report.pdf").is_file()
        assert (tmp_path / "code" / "script.py").is_file()
        assert (tmp_path / OTHER / "weird.bin").is_file()
        assert not (tmp_path / "cat.png").exists()  # original moved

    def test_dry_run_does_not_touch_files(self, tmp_path):
        src = touch(tmp_path, "cat.png")

        count = organize(tmp_path, dry_run=True)

        assert count == 1
        assert src.is_file()  # still where it was
        assert not (tmp_path / "images").exists()  # no folder created

    def test_copy_mode_keeps_source(self, tmp_path):
        src = touch(tmp_path, "song.mp3", "audio")

        count = organize(tmp_path, mode="copy")

        assert count == 1
        assert src.is_file()
        assert (tmp_path / "audio" / "song.mp3").is_file()

    def test_name_collision_renames_destination(self, tmp_path):
        touch(tmp_path, "a.txt")
        (tmp_path / "documents").mkdir()
        touch(tmp_path / "documents", "a.txt", "old")

        organize(tmp_path)

        assert (tmp_path / "documents" / "a (1).txt").is_file()
        assert (tmp_path / "documents" / "a.txt").read_text(encoding="utf-8") == "old"

    def test_hidden_files_are_skipped(self, tmp_path):
        touch(tmp_path, ".DS_Store")
        assert organize(tmp_path) == 0

    def test_non_recursive_ignores_subfolders(self, tmp_path):
        sub = tmp_path / "nested"
        sub.mkdir()
        touch(sub, "inner.txt")

        organize(tmp_path)

        assert (sub / "inner.txt").is_file()  # untouched

    def test_recursive_processes_subfolders_but_skips_category_dirs(self, tmp_path):
        sub = tmp_path / "nested"
        sub.mkdir()
        touch(sub, "inner.png")
        (tmp_path / "images").mkdir()
        touch(tmp_path / "images", "already.png")

        count = organize(tmp_path, recursive=True)

        assert count == 1  # only inner.png is new work
        assert (tmp_path / "images" / "inner.png").is_file()
        assert (tmp_path / "images" / "already.png").is_file()
        assert not (tmp_path / "images" / "images").exists()

    def test_missing_folder_raises(self, tmp_path):
        with pytest.raises(NotADirectoryError):
            organize(tmp_path / "nope")
