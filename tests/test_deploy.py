"""Tests for scripts/deploy.py."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from scripts.deploy import (
    check_conflicts,
    do_copy,
    do_sync,
    do_undeploy,
    enumerate_source,
)


# ---------------------------------------------------------------------------
# enumerate_source
# ---------------------------------------------------------------------------


class TestEnumerateSource:
    def test_empty_dir(self, tmp_path: Path):
        files, dirs = enumerate_source(tmp_path)
        assert files == set()
        assert dirs == set()

    def test_nonexistent_dir(self, tmp_path: Path):
        files, dirs = enumerate_source(tmp_path / "nope")
        assert files == set()
        assert dirs == set()

    def test_flat_files(self, tmp_path: Path):
        (tmp_path / "a.txt").write_text("a")
        (tmp_path / "b.txt").write_text("b")
        files, dirs = enumerate_source(tmp_path)
        assert files == {Path("a.txt"), Path("b.txt")}
        assert dirs == set()

    def test_nested_dirs(self, tmp_path: Path):
        (tmp_path / "d1").mkdir()
        (tmp_path / "d1" / "f1.txt").write_text("f1")
        (tmp_path / "d1" / "d2").mkdir()
        (tmp_path / "d1" / "d2" / "f2.txt").write_text("f2")
        files, dirs = enumerate_source(tmp_path)
        assert files == {Path("d1/f1.txt"), Path("d1/d2/f2.txt")}
        assert dirs == {Path("d1"), Path("d1/d2")}

    def test_dot_not_in_dirs(self, tmp_path: Path):
        """Path('.') should never appear in the dirs set."""
        (tmp_path / "x.txt").write_text("x")
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub" / "y.txt").write_text("y")
        _, dirs = enumerate_source(tmp_path)
        assert Path(".") not in dirs


# ---------------------------------------------------------------------------
# check_conflicts
# ---------------------------------------------------------------------------


class TestCheckConflicts:
    def test_no_conflict_when_dest_empty(self, tmp_path: Path):
        result = check_conflicts(tmp_path, {Path("a.txt")}, set())
        assert result == []

    def test_no_conflict_when_types_match(self, tmp_path: Path):
        (tmp_path / "a.txt").write_text("existing")
        (tmp_path / "sub").mkdir()
        result = check_conflicts(tmp_path, {Path("a.txt")}, {Path("sub")})
        assert result == []

    def test_file_vs_dir_conflict(self, tmp_path: Path):
        # Source has "x" as a dir, but dest has "x" as a file
        (tmp_path / "x").write_text("i am a file")
        result = check_conflicts(tmp_path, set(), {Path("x")})
        assert result == [Path("x")]

    def test_dir_vs_file_conflict(self, tmp_path: Path):
        # Source has "x" as a file, but dest has "x" as a dir
        (tmp_path / "x").mkdir()
        result = check_conflicts(tmp_path, {Path("x")}, set())
        assert result == [Path("x")]


# ---------------------------------------------------------------------------
# do_copy
# ---------------------------------------------------------------------------


class TestDoCopy:
    def test_copies_files(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "a.txt").write_text("hello")
        dest = tmp_path / "dest"
        dest.mkdir()

        do_copy(src, dest, {Path("a.txt")}, dry_run=False)
        assert (dest / "a.txt").read_text() == "hello"

    def test_merge_preserves_existing(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "new.txt").write_text("new")
        dest = tmp_path / "dest"
        dest.mkdir()
        (dest / "existing.txt").write_text("keep me")

        do_copy(src, dest, {Path("new.txt")}, dry_run=False)
        assert (dest / "new.txt").read_text() == "new"
        assert (dest / "existing.txt").read_text() == "keep me"

    def test_creates_parent_dirs(self, tmp_path: Path):
        src = tmp_path / "src"
        (src / "d1" / "d2").mkdir(parents=True)
        (src / "d1" / "d2" / "f.txt").write_text("deep")
        dest = tmp_path / "dest"
        dest.mkdir()

        do_copy(src, dest, {Path("d1/d2/f.txt")}, dry_run=False)
        assert (dest / "d1" / "d2" / "f.txt").read_text() == "deep"

    def test_removes_symlink_in_path(self, tmp_path: Path):
        src = tmp_path / "src"
        (src / "sub").mkdir(parents=True)
        (src / "sub" / "f.txt").write_text("real")
        dest = tmp_path / "dest"
        dest.mkdir()
        # Create a symlink where a directory should be
        target = tmp_path / "elsewhere"
        target.mkdir()
        os.symlink(target, dest / "sub")

        do_copy(src, dest, {Path("sub/f.txt")}, dry_run=False)
        assert not (dest / "sub").is_symlink()
        assert (dest / "sub" / "f.txt").read_text() == "real"

    def test_dry_run_does_not_write(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "a.txt").write_text("hello")
        dest = tmp_path / "dest"
        dest.mkdir()

        do_copy(src, dest, {Path("a.txt")}, dry_run=True)
        assert not (dest / "a.txt").exists()


# ---------------------------------------------------------------------------
# do_sync
# ---------------------------------------------------------------------------


class TestDoSync:
    def test_removes_stale_file(self, tmp_path: Path):
        dest = tmp_path / "dest"
        (dest / "sub").mkdir(parents=True)
        (dest / "sub" / "keep.txt").write_text("keep")
        (dest / "sub" / "stale.txt").write_text("stale")

        source_files = {Path("sub/keep.txt")}
        source_dirs = {Path("sub")}
        do_sync(dest, source_files, source_dirs, dry_run=False)

        assert (dest / "sub" / "keep.txt").exists()
        assert not (dest / "sub" / "stale.txt").exists()

    def test_removes_stale_dir(self, tmp_path: Path):
        dest = tmp_path / "dest"
        (dest / "sub").mkdir(parents=True)
        (dest / "sub" / "old_dir").mkdir()
        (dest / "sub" / "old_dir" / "f.txt").write_text("gone")

        source_files: set[Path] = set()
        source_dirs = {Path("sub")}
        do_sync(dest, source_files, source_dirs, dry_run=False)

        assert not (dest / "sub" / "old_dir").exists()

    def test_preserves_owned_paths(self, tmp_path: Path):
        dest = tmp_path / "dest"
        (dest / "sub").mkdir(parents=True)
        (dest / "sub" / "a.txt").write_text("a")
        (dest / "sub" / "b.txt").write_text("b")

        source_files = {Path("sub/a.txt"), Path("sub/b.txt")}
        source_dirs = {Path("sub")}
        do_sync(dest, source_files, source_dirs, dry_run=False)

        assert (dest / "sub" / "a.txt").exists()
        assert (dest / "sub" / "b.txt").exists()

    def test_preserves_dir_with_owned_children(self, tmp_path: Path):
        """A dir not in source_dirs but containing owned files should be kept."""
        dest = tmp_path / "dest"
        (dest / "parent" / "child").mkdir(parents=True)
        (dest / "parent" / "child" / "f.txt").write_text("owned")

        source_files = {Path("parent/child/f.txt")}
        source_dirs = {Path("parent"), Path("parent/child")}
        do_sync(dest, source_files, source_dirs, dry_run=False)

        assert (dest / "parent" / "child" / "f.txt").exists()

    def test_dry_run_does_not_delete(self, tmp_path: Path):
        dest = tmp_path / "dest"
        (dest / "sub").mkdir(parents=True)
        (dest / "sub" / "stale.txt").write_text("stale")

        source_dirs = {Path("sub")}
        do_sync(dest, set(), source_dirs, dry_run=True)

        assert (dest / "sub" / "stale.txt").exists()

    def test_skips_nonexistent_dest_dir(self, tmp_path: Path):
        dest = tmp_path / "dest"
        dest.mkdir()
        # source_dirs references a dir that doesn't exist in dest — should not error
        do_sync(dest, set(), {Path("nonexistent")}, dry_run=False)


# ---------------------------------------------------------------------------
# do_undeploy
# ---------------------------------------------------------------------------


class TestDoUndeploy:
    def test_removes_source_owned_files(self, tmp_path: Path):
        dest = tmp_path / "dest"
        dest.mkdir()
        (dest / "a.txt").write_text("a")
        (dest / "b.txt").write_text("b")

        do_undeploy(dest, {Path("a.txt")}, set(), dry_run=False)
        assert not (dest / "a.txt").exists()
        assert (dest / "b.txt").exists()

    def test_removes_source_owned_dirs(self, tmp_path: Path):
        dest = tmp_path / "dest"
        (dest / "sub").mkdir(parents=True)
        (dest / "sub" / "f.txt").write_text("f")

        do_undeploy(dest, {Path("sub/f.txt")}, {Path("sub")}, dry_run=False)
        assert not (dest / "sub").exists()

    def test_leaves_non_source_paths(self, tmp_path: Path):
        dest = tmp_path / "dest"
        dest.mkdir()
        (dest / "mine.txt").write_text("mine")

        do_undeploy(dest, {Path("other.txt")}, set(), dry_run=False)
        assert (dest / "mine.txt").exists()

    def test_dry_run_does_not_delete(self, tmp_path: Path):
        dest = tmp_path / "dest"
        dest.mkdir()
        (dest / "a.txt").write_text("a")

        do_undeploy(dest, {Path("a.txt")}, set(), dry_run=True)
        assert (dest / "a.txt").exists()
