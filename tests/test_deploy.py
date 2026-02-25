"""Tests for artifact deployment: symlink creation, removal, status detection."""

import os
from pathlib import Path

import pytest

from dot_claude.repos import Artifact
from dot_claude.deploy import (
    create_symlink,
    remove_symlink,
    detect_install_status,
    DeployError,
)


def _skill(tmp_path, name="my-skill", repo_name="test-repo"):
    """Helper: create a fake skill artifact source."""
    source = tmp_path / "source" / name
    source.mkdir(parents=True)
    (source / "SKILL.md").write_text("content")
    return Artifact(name=name, kind="skill", repo_name=repo_name, source_path=source)


def _agent(tmp_path, name="my-agent", repo_name="test-repo"):
    """Helper: create a fake agent artifact source."""
    source = tmp_path / "source" / f"{name}.md"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("content")
    return Artifact(name=name, kind="agent", repo_name=repo_name, source_path=source)


class TestCreateSymlink:
    """Symlink creation for skills and agents."""

    def test_symlink_skill_to_target(self, tmp_path):
        artifact = _skill(tmp_path)
        target_dir = tmp_path / "target"
        create_symlink(artifact, target_dir)
        link = target_dir / "skills" / "my-skill"
        assert link.is_symlink()
        assert link.resolve() == artifact.source_path.resolve()

    def test_symlink_agent_to_target(self, tmp_path):
        artifact = _agent(tmp_path)
        target_dir = tmp_path / "target"
        create_symlink(artifact, target_dir)
        link = target_dir / "agents" / "my-agent.md"
        assert link.is_symlink()
        assert link.resolve() == artifact.source_path.resolve()

    def test_creates_target_directory(self, tmp_path):
        artifact = _skill(tmp_path)
        target_dir = tmp_path / "deep" / "target"
        create_symlink(artifact, target_dir)
        assert (target_dir / "skills").is_dir()

    def test_refuses_overwrite_existing(self, tmp_path):
        artifact = _skill(tmp_path)
        target_dir = tmp_path / "target"
        (target_dir / "skills" / "my-skill").mkdir(parents=True)
        with pytest.raises(DeployError, match="already installed"):
            create_symlink(artifact, target_dir)


class TestRemoveSymlink:
    """Symlink removal with safety checks."""

    def test_removes_skill_symlink(self, tmp_path):
        artifact = _skill(tmp_path)
        target_dir = tmp_path / "target"
        create_symlink(artifact, target_dir)
        remove_symlink("my-skill", "skill", target_dir)
        assert not (target_dir / "skills" / "my-skill").exists()

    def test_removes_agent_symlink(self, tmp_path):
        artifact = _agent(tmp_path)
        target_dir = tmp_path / "target"
        create_symlink(artifact, target_dir)
        remove_symlink("my-agent", "agent", target_dir)
        assert not (target_dir / "agents" / "my-agent.md").exists()

    def test_warns_on_regular_file(self, tmp_path):
        target_dir = tmp_path / "target"
        (target_dir / "skills" / "my-skill").mkdir(parents=True)
        with pytest.raises(DeployError, match="not a managed symlink"):
            remove_symlink("my-skill", "skill", target_dir)

    def test_error_when_not_installed(self, tmp_path):
        target_dir = tmp_path / "target"
        target_dir.mkdir()
        with pytest.raises(DeployError, match="not installed"):
            remove_symlink("nonexistent", "skill", target_dir)


class TestDetectInstallStatus:
    """Detect whether an artifact is installed and in which scope."""

    def test_detects_user_scope_skill(self, tmp_path):
        artifact = _skill(tmp_path)
        user_dir = tmp_path / "user"
        project_dir = tmp_path / "project"
        create_symlink(artifact, user_dir)
        status = detect_install_status("my-skill", "skill", user_dir, project_dir)
        assert status == "user"

    def test_detects_project_scope_skill(self, tmp_path):
        artifact = _skill(tmp_path)
        user_dir = tmp_path / "user"
        project_dir = tmp_path / "project"
        create_symlink(artifact, project_dir)
        status = detect_install_status("my-skill", "skill", user_dir, project_dir)
        assert status == "project"

    def test_not_installed(self, tmp_path):
        user_dir = tmp_path / "user"
        project_dir = tmp_path / "project"
        status = detect_install_status("missing", "skill", user_dir, project_dir)
        assert status is None

    def test_broken_symlink_treated_as_not_installed(self, tmp_path):
        user_dir = tmp_path / "user"
        project_dir = tmp_path / "project"
        (user_dir / "skills").mkdir(parents=True)
        link = user_dir / "skills" / "broken"
        link.symlink_to("/nonexistent/path")
        status = detect_install_status("broken", "skill", user_dir, project_dir)
        assert status is None

    def test_detects_agent_status(self, tmp_path):
        artifact = _agent(tmp_path)
        user_dir = tmp_path / "user"
        project_dir = tmp_path / "project"
        create_symlink(artifact, user_dir)
        status = detect_install_status("my-agent", "agent", user_dir, project_dir)
        assert status == "user"
