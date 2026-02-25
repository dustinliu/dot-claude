"""Tests for scripts/deploy.py."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.deploy import (
    check_conflicts,
    do_cleanup,
    do_copy,
    enumerate_source,
    read_manifest,
    write_manifest,
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

    def test_dry_run_does_not_write(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "a.txt").write_text("hello")
        dest = tmp_path / "dest"
        dest.mkdir()

        do_copy(src, dest, {Path("a.txt")}, dry_run=True)
        assert not (dest / "a.txt").exists()


# ---------------------------------------------------------------------------
# write_manifest / read_manifest
# ---------------------------------------------------------------------------


class TestManifest:
    def test_write_manifest_creates_file(self, tmp_path: Path):
        files = {Path("a.txt"), Path("sub/b.txt")}
        write_manifest(tmp_path, files)
        manifest_path = tmp_path / ".deploy-manifest.json"
        assert manifest_path.exists()
        data = json.loads(manifest_path.read_text())
        assert sorted(data["files"]) == ["a.txt", "sub/b.txt"]

    def test_write_manifest_overwrites_existing(self, tmp_path: Path):
        write_manifest(tmp_path, {Path("old.txt")})
        write_manifest(tmp_path, {Path("new.txt")})
        data = json.loads((tmp_path / ".deploy-manifest.json").read_text())
        assert data["files"] == ["new.txt"]

    def test_read_manifest_returns_files(self, tmp_path: Path):
        manifest = {"files": ["a.txt", "sub/b.txt"]}
        (tmp_path / ".deploy-manifest.json").write_text(json.dumps(manifest))
        result = read_manifest(tmp_path)
        assert result == {Path("a.txt"), Path("sub/b.txt")}

    def test_read_manifest_returns_empty_when_missing(self, tmp_path: Path):
        result = read_manifest(tmp_path)
        assert result == set()


# ---------------------------------------------------------------------------
# do_cleanup
# ---------------------------------------------------------------------------


class TestDoCleanup:
    def test_removes_stale_file(self, tmp_path: Path):
        dest = tmp_path / "dest"
        dest.mkdir()
        (dest / "skills" / "old-skill").mkdir(parents=True)
        (dest / "skills" / "old-skill" / "SKILL.md").write_text("old")

        previous = {Path("skills/old-skill/SKILL.md")}
        current = set()
        do_cleanup(dest, previous, current, dry_run=False)

        assert not (dest / "skills" / "old-skill" / "SKILL.md").exists()

    def test_removes_empty_dir_after_cleanup(self, tmp_path: Path):
        dest = tmp_path / "dest"
        dest.mkdir()
        (dest / "skills" / "old-skill").mkdir(parents=True)
        (dest / "skills" / "old-skill" / "SKILL.md").write_text("old")

        previous = {Path("skills/old-skill/SKILL.md")}
        current = set()
        do_cleanup(dest, previous, current, dry_run=False)

        assert not (dest / "skills" / "old-skill").exists()

    def test_preserves_unmanaged_files(self, tmp_path: Path):
        dest = tmp_path / "dest"
        dest.mkdir()
        (dest / "settings.local.json").write_text("{}")
        (dest / "skills" / "external-skill").mkdir(parents=True)
        (dest / "skills" / "external-skill" / "SKILL.md").write_text("ext")

        previous = {Path("skills/my-skill/SKILL.md")}
        current = set()
        do_cleanup(dest, previous, current, dry_run=False)

        assert (dest / "settings.local.json").exists()
        assert (dest / "skills" / "external-skill" / "SKILL.md").exists()

    def test_no_cleanup_on_first_deploy(self, tmp_path: Path):
        """When previous manifest is empty, nothing should be deleted."""
        dest = tmp_path / "dest"
        dest.mkdir()
        (dest / "existing.txt").write_text("keep")

        do_cleanup(dest, set(), {Path("new.txt")}, dry_run=False)

        assert (dest / "existing.txt").exists()

    def test_dry_run_does_not_delete(self, tmp_path: Path):
        dest = tmp_path / "dest"
        dest.mkdir()
        (dest / "stale.txt").write_text("stale")

        previous = {Path("stale.txt")}
        current = set()
        do_cleanup(dest, previous, current, dry_run=True)

        assert (dest / "stale.txt").exists()

    def test_does_not_remove_dir_if_still_has_content(self, tmp_path: Path):
        """If a dir still has other files after cleanup, don't remove it."""
        dest = tmp_path / "dest"
        (dest / "skills" / "my-skill").mkdir(parents=True)
        (dest / "skills" / "my-skill" / "SKILL.md").write_text("mine")
        (dest / "skills" / "external").mkdir(parents=True)
        (dest / "skills" / "external" / "SKILL.md").write_text("ext")
        (dest / "skills" / "old-skill").mkdir(parents=True)
        (dest / "skills" / "old-skill" / "SKILL.md").write_text("old")

        previous = {Path("skills/my-skill/SKILL.md"), Path("skills/old-skill/SKILL.md")}
        current = {Path("skills/my-skill/SKILL.md")}
        do_cleanup(dest, previous, current, dry_run=False)

        assert not (dest / "skills" / "old-skill").exists()
        assert (dest / "skills" / "my-skill" / "SKILL.md").exists()
        assert (dest / "skills" / "external" / "SKILL.md").exists()
        assert (dest / "skills").exists()


# ---------------------------------------------------------------------------
# Integration: deploy → remove from source → deploy again
# ---------------------------------------------------------------------------


class TestDeployIntegration:
    def test_stale_file_cleaned_on_second_deploy(self, tmp_path: Path):
        """Full cycle: deploy, remove a file from source, deploy again."""
        src = tmp_path / "src"
        dest = tmp_path / "dest"
        dest.mkdir()

        # First deploy: two skills
        (src / "skills" / "keep").mkdir(parents=True)
        (src / "skills" / "keep" / "SKILL.md").write_text("keep")
        (src / "skills" / "remove-me").mkdir(parents=True)
        (src / "skills" / "remove-me" / "SKILL.md").write_text("remove")

        source_files_v1 = {
            Path("skills/keep/SKILL.md"),
            Path("skills/remove-me/SKILL.md"),
        }
        do_copy(src, dest, source_files_v1, dry_run=False)
        write_manifest(dest, source_files_v1)

        assert (dest / "skills" / "remove-me" / "SKILL.md").exists()

        # Second deploy: remove-me is gone from source
        import shutil

        shutil.rmtree(src / "skills" / "remove-me")
        source_files_v2 = {Path("skills/keep/SKILL.md")}

        previous = read_manifest(dest)
        do_copy(src, dest, source_files_v2, dry_run=False)
        do_cleanup(dest, previous, source_files_v2, dry_run=False)
        write_manifest(dest, source_files_v2)

        assert (dest / "skills" / "keep" / "SKILL.md").exists()
        assert not (dest / "skills" / "remove-me").exists()

        # Verify manifest reflects current state
        final_manifest = read_manifest(dest)
        assert final_manifest == {Path("skills/keep/SKILL.md")}
