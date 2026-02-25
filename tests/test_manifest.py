"""Tests for dot_claude.manifest."""

from __future__ import annotations

import json
from pathlib import Path

from dot_claude.manifest import Manifest, read_manifest, write_manifest


class TestWriteManifest:
    def test_writes_manifest_file(self, tmp_path: Path):
        manifest = Manifest(
            scope="user",
            items=["skills/git-commit", "skills/leading-change"],
            files=[Path("skills/git-commit/SKILL.md"), Path("skills/leading-change/SKILL.md")],
        )
        write_manifest(tmp_path, manifest)
        manifest_path = tmp_path / ".deploy-manifest.json"
        assert manifest_path.exists()

    def test_manifest_contains_scope(self, tmp_path: Path):
        manifest = Manifest(
            scope="user", items=["skills/git-commit"], files=[Path("skills/git-commit/SKILL.md")]
        )
        write_manifest(tmp_path, manifest)
        data = json.loads((tmp_path / ".deploy-manifest.json").read_text())
        assert data["scope"] == "user"

    def test_manifest_contains_items(self, tmp_path: Path):
        manifest = Manifest(
            scope="project",
            items=["skills/git-commit", "agents/code-explorer"],
            files=[Path("skills/git-commit/SKILL.md"), Path("agents/code-explorer.md")],
        )
        write_manifest(tmp_path, manifest)
        data = json.loads((tmp_path / ".deploy-manifest.json").read_text())
        assert data["items"] == ["agents/code-explorer", "skills/git-commit"]

    def test_manifest_contains_files(self, tmp_path: Path):
        manifest = Manifest(
            scope="user",
            items=["skills/git-commit"],
            files=[Path("skills/git-commit/SKILL.md"), Path("CLAUDE.md")],
        )
        write_manifest(tmp_path, manifest)
        data = json.loads((tmp_path / ".deploy-manifest.json").read_text())
        assert sorted(data["files"]) == ["CLAUDE.md", "skills/git-commit/SKILL.md"]

    def test_overwrites_existing_manifest(self, tmp_path: Path):
        m1 = Manifest(scope="user", items=["skills/old"], files=[Path("skills/old/SKILL.md")])
        write_manifest(tmp_path, m1)
        m2 = Manifest(scope="user", items=["skills/new"], files=[Path("skills/new/SKILL.md")])
        write_manifest(tmp_path, m2)
        data = json.loads((tmp_path / ".deploy-manifest.json").read_text())
        assert data["items"] == ["skills/new"]


class TestReadManifest:
    def test_reads_new_format(self, tmp_path: Path):
        data = {
            "scope": "user",
            "items": ["skills/git-commit"],
            "files": ["skills/git-commit/SKILL.md"],
        }
        (tmp_path / ".deploy-manifest.json").write_text(json.dumps(data))
        manifest = read_manifest(tmp_path)
        assert manifest.scope == "user"
        assert manifest.items == ["skills/git-commit"]
        assert manifest.files == {Path("skills/git-commit/SKILL.md")}

    def test_reads_legacy_format(self, tmp_path: Path):
        """Legacy manifest has only 'files', no 'scope' or 'items'."""
        data = {"files": ["skills/git-commit/SKILL.md", "agents/code-explorer.md", "CLAUDE.md"]}
        (tmp_path / ".deploy-manifest.json").write_text(json.dumps(data))
        manifest = read_manifest(tmp_path)
        assert manifest.scope == "user"
        assert "skills/git-commit" in manifest.items
        assert "agents/code-explorer" in manifest.items
        assert manifest.files == {
            Path("skills/git-commit/SKILL.md"),
            Path("agents/code-explorer.md"),
            Path("CLAUDE.md"),
        }

    def test_returns_none_when_missing(self, tmp_path: Path):
        manifest = read_manifest(tmp_path)
        assert manifest is None

    def test_files_returned_as_set(self, tmp_path: Path):
        data = {
            "scope": "project",
            "items": ["skills/a", "skills/b"],
            "files": ["skills/a/SKILL.md", "skills/b/SKILL.md"],
        }
        (tmp_path / ".deploy-manifest.json").write_text(json.dumps(data))
        manifest = read_manifest(tmp_path)
        assert isinstance(manifest.files, set)


class TestManifestDataclass:
    def test_manifest_creation(self):
        m = Manifest(scope="user", items=["skills/x"], files=[Path("skills/x/SKILL.md")])
        assert m.scope == "user"
        assert m.items == ["skills/x"]
