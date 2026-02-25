"""Tests for dot_claude.installer."""

from __future__ import annotations

from pathlib import Path

from dot_claude.installer import install, remove_files
from dot_claude.manifest import read_manifest


def _make_data_root(tmp_path: Path) -> Path:
    """Create a fake data root with skills and agents."""
    data = tmp_path / "data"
    (data / "skills" / "git-commit").mkdir(parents=True)
    (data / "skills" / "git-commit" / "SKILL.md").write_text("git-commit skill")
    (data / "skills" / "leading-change").mkdir(parents=True)
    (data / "skills" / "leading-change" / "SKILL.md").write_text("leading-change skill")
    (data / "agents").mkdir(parents=True)
    (data / "agents" / "code-explorer.md").write_text("code-explorer agent")
    (data / "agents" / "code-reviewer.md").write_text("code-reviewer agent")
    (data / "CLAUDE.md").write_text("workspace rules")
    return data


class TestInstall:
    def test_copies_selected_skill(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "dest"
        dest.mkdir()

        install(
            data_root=data,
            dest=dest,
            selected_items=["skills/git-commit"],
            scope="project",
        )

        assert (dest / "skills" / "git-commit" / "SKILL.md").read_text() == "git-commit skill"

    def test_copies_selected_agent(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "dest"
        dest.mkdir()

        install(
            data_root=data,
            dest=dest,
            selected_items=["agents/code-explorer"],
            scope="project",
        )

        assert (dest / "agents" / "code-explorer.md").read_text() == "code-explorer agent"

    def test_only_copies_selected_items(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "dest"
        dest.mkdir()

        install(
            data_root=data,
            dest=dest,
            selected_items=["skills/git-commit"],
            scope="project",
        )

        assert (dest / "skills" / "git-commit" / "SKILL.md").exists()
        assert not (dest / "skills" / "leading-change").exists()
        assert not (dest / "agents").exists()

    def test_overwrites_existing_files(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "dest"
        (dest / "skills" / "git-commit").mkdir(parents=True)
        (dest / "skills" / "git-commit" / "SKILL.md").write_text("old content")

        install(
            data_root=data,
            dest=dest,
            selected_items=["skills/git-commit"],
            scope="project",
        )

        assert (dest / "skills" / "git-commit" / "SKILL.md").read_text() == "git-commit skill"

    def test_creates_parent_dirs(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "dest"
        dest.mkdir()

        install(
            data_root=data,
            dest=dest,
            selected_items=["skills/git-commit"],
            scope="project",
        )

        assert (dest / "skills" / "git-commit").is_dir()

    def test_creates_dest_dir_if_missing(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "dest"  # not created

        install(
            data_root=data,
            dest=dest,
            selected_items=["skills/git-commit"],
            scope="project",
        )

        assert dest.is_dir()
        assert (dest / "skills" / "git-commit" / "SKILL.md").exists()

    def test_auto_deploys_claude_md_for_user_scope(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "dest"
        dest.mkdir()

        install(
            data_root=data,
            dest=dest,
            selected_items=["skills/git-commit"],
            scope="user",
        )

        assert (dest / "CLAUDE.md").read_text() == "workspace rules"

    def test_excludes_claude_md_for_project_scope(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "dest"
        dest.mkdir()

        install(
            data_root=data,
            dest=dest,
            selected_items=["skills/git-commit"],
            scope="project",
        )

        assert not (dest / "CLAUDE.md").exists()

    def test_writes_manifest(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "dest"
        dest.mkdir()

        install(
            data_root=data,
            dest=dest,
            selected_items=["skills/git-commit", "agents/code-explorer"],
            scope="user",
        )

        manifest = read_manifest(dest)
        assert manifest is not None
        assert manifest.scope == "user"
        assert "skills/git-commit" in manifest.items
        assert "agents/code-explorer" in manifest.items

    def test_cleans_up_deselected_items(self, tmp_path: Path):
        """Items from previous manifest that are no longer selected get removed."""
        data = _make_data_root(tmp_path)
        dest = tmp_path / "dest"
        dest.mkdir()

        # First install: two skills
        install(
            data_root=data,
            dest=dest,
            selected_items=["skills/git-commit", "skills/leading-change"],
            scope="project",
        )
        assert (dest / "skills" / "leading-change" / "SKILL.md").exists()

        # Second install: only one skill
        install(data_root=data, dest=dest, selected_items=["skills/git-commit"], scope="project")
        assert (dest / "skills" / "git-commit" / "SKILL.md").exists()
        assert not (dest / "skills" / "leading-change" / "SKILL.md").exists()

    def test_removes_empty_dirs_after_cleanup(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "dest"
        dest.mkdir()

        install(data_root=data, dest=dest, selected_items=["skills/git-commit"], scope="project")
        install(data_root=data, dest=dest, selected_items=[], scope="project")

        assert not (dest / "skills" / "git-commit").exists()

    def test_removes_manifest_when_last_item_removed(self, tmp_path: Path):
        """When all items are deselected, the manifest file should be deleted."""
        data = _make_data_root(tmp_path)
        dest = tmp_path / "dest"
        dest.mkdir()

        install(data_root=data, dest=dest, selected_items=["skills/git-commit"], scope="project")
        assert read_manifest(dest) is not None

        install(data_root=data, dest=dest, selected_items=[], scope="project")
        assert read_manifest(dest) is None
        assert not (dest / ".deploy-manifest.json").exists()

    def test_preserves_non_manifest_files(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "dest"
        dest.mkdir()
        (dest / "settings.local.json").write_text("{}")
        (dest / "skills" / "external").mkdir(parents=True)
        (dest / "skills" / "external" / "SKILL.md").write_text("external")

        install(data_root=data, dest=dest, selected_items=["skills/git-commit"], scope="project")

        assert (dest / "settings.local.json").read_text() == "{}"
        assert (dest / "skills" / "external" / "SKILL.md").read_text() == "external"


class TestRemoveFiles:
    def test_removes_files(self, tmp_path: Path):
        (tmp_path / "skills" / "old").mkdir(parents=True)
        (tmp_path / "skills" / "old" / "SKILL.md").write_text("old")

        remove_files(tmp_path, {Path("skills/old/SKILL.md")})

        assert not (tmp_path / "skills" / "old" / "SKILL.md").exists()

    def test_removes_empty_parent_dirs(self, tmp_path: Path):
        (tmp_path / "skills" / "old").mkdir(parents=True)
        (tmp_path / "skills" / "old" / "SKILL.md").write_text("old")

        remove_files(tmp_path, {Path("skills/old/SKILL.md")})

        assert not (tmp_path / "skills" / "old").exists()

    def test_preserves_non_empty_parent_dirs(self, tmp_path: Path):
        (tmp_path / "skills" / "keep").mkdir(parents=True)
        (tmp_path / "skills" / "keep" / "SKILL.md").write_text("keep")
        (tmp_path / "skills" / "old").mkdir(parents=True)
        (tmp_path / "skills" / "old" / "SKILL.md").write_text("old")

        remove_files(tmp_path, {Path("skills/old/SKILL.md")})

        assert not (tmp_path / "skills" / "old").exists()
        assert (tmp_path / "skills" / "keep" / "SKILL.md").exists()
        assert (tmp_path / "skills").exists()

    def test_ignores_already_missing_files(self, tmp_path: Path):
        # Should not raise
        remove_files(tmp_path, {Path("nonexistent/file.md")})
