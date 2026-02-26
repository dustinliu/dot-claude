"""Tests for CLI commands."""

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from click.testing import CliRunner

from dot_claude.cli import main


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_env(tmp_path, monkeypatch):
    """Set up isolated XDG dirs and a fake cached repo."""
    config_home = tmp_path / "config"
    cache_home = tmp_path / "cache"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_home))
    monkeypatch.setenv("XDG_CACHE_HOME", str(cache_home))

    # Create config with one repo
    cfg_dir = config_home / "dot-claude"
    cfg_dir.mkdir(parents=True)
    (cfg_dir / "dot-claude.toml").write_text(
        '[[repos]]\nname = "test-repo"\n'
        'url = "https://github.com/test/repo.git"\n'
    )

    # Create fake cached repo with artifacts
    repo_dir = cache_home / "dot-claude" / "test-repo"
    (repo_dir / "skills" / "my-skill").mkdir(parents=True)
    (repo_dir / "skills" / "my-skill" / "SKILL.md").write_text("content")
    (repo_dir / "agents").mkdir(parents=True)
    (repo_dir / "agents" / "my-agent.md").write_text("content")

    return tmp_path


class TestInitCommand:
    """dot-claude init"""

    def test_creates_config(self, runner, tmp_path, monkeypatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
        result = runner.invoke(main, ["init"])
        assert result.exit_code == 0
        assert (tmp_path / "config" / "dot-claude" / "dot-claude.toml").exists()

    def test_refuses_overwrite(self, runner, mock_env):
        result = runner.invoke(main, ["init"])
        assert result.exit_code != 0
        assert "already exists" in result.output


class TestUpdateCommand:
    """dot-claude update"""

    def test_update_calls_update_repos(self, runner, mock_env):
        with patch("dot_claude.cli.update_repos", return_value=[]) as mock_update:
            result = runner.invoke(main, ["update"])
            assert result.exit_code == 0
            mock_update.assert_called_once()

    def test_update_reports_errors(self, runner, mock_env):
        with patch("dot_claude.cli.update_repos", return_value=["repo-a: network error"]):
            result = runner.invoke(main, ["update"])
            assert "repo-a" in result.output


class TestListCommand:
    """dot-claude list"""

    def test_list_shows_artifacts(self, runner, mock_env):
        result = runner.invoke(main, ["list"])
        assert result.exit_code == 0
        assert "my-skill" in result.output
        assert "my-agent" in result.output
        assert "test-repo" in result.output

    def test_list_shows_install_status(self, runner, mock_env, monkeypatch):
        fake_home = mock_env / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: fake_home)
        # Install a skill to user scope first
        result = runner.invoke(main, ["add", "-g", "my-skill"])
        assert result.exit_code == 0
        result = runner.invoke(main, ["list"])
        assert "[user]" in result.output

    def test_list_g_hides_project_status(self, runner, mock_env, monkeypatch):
        """list -g should only show user-scope install status."""
        fake_home = mock_env / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: fake_home)
        project_dir = mock_env / "project"
        project_dir.mkdir()
        monkeypatch.chdir(project_dir)
        # Install skill to project scope
        result = runner.invoke(main, ["add", "-p", "my-skill"])
        assert result.exit_code == 0
        # list without -g shows [project]
        result = runner.invoke(main, ["list"])
        assert "[project]" in result.output
        # list with -g should NOT show [project]
        result = runner.invoke(main, ["list", "-g"])
        assert "[project]" not in result.output

    def test_list_columns_aligned(self, runner, mock_env):
        result = runner.invoke(main, ["list"])
        lines = [l for l in result.output.splitlines() if "my-" in l]
        # All repo names should start at the same column
        positions = set()
        for line in lines:
            idx = line.index("test-repo")
            positions.add(idx)
        assert len(positions) == 1  # All aligned


class TestAddCommand:
    """dot-claude add"""

    def test_add_to_project_scope(self, runner, mock_env, monkeypatch):
        project_dir = mock_env / "project"
        project_dir.mkdir()
        monkeypatch.chdir(project_dir)
        result = runner.invoke(main, ["add", "-p", "my-skill"])
        assert result.exit_code == 0
        assert (project_dir / ".claude" / "skills" / "my-skill").is_symlink()
        assert "skills/my-skill" in result.output

    def test_add_to_user_scope(self, runner, mock_env, monkeypatch):
        fake_home = mock_env / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: fake_home)
        result = runner.invoke(main, ["add", "-g", "my-skill"])
        assert result.exit_code == 0
        assert (fake_home / ".claude" / "skills" / "my-skill").is_symlink()
        assert "skills/my-skill" in result.output

    def test_add_unknown_artifact(self, runner, mock_env):
        result = runner.invoke(main, ["add", "-p", "nonexistent"])
        assert result.exit_code != 0
        assert "not found" in result.output

    def test_add_agent(self, runner, mock_env, monkeypatch):
        project_dir = mock_env / "project"
        project_dir.mkdir()
        monkeypatch.chdir(project_dir)
        result = runner.invoke(main, ["add", "-p", "my-agent"])
        assert result.exit_code == 0
        assert (project_dir / ".claude" / "agents" / "my-agent.md").is_symlink()
        assert "agents/my-agent.md" in result.output

    def test_add_without_flags_shows_tui(self, runner, mock_env, monkeypatch):
        project_dir = mock_env / "project"
        project_dir.mkdir()
        monkeypatch.chdir(project_dir)
        with patch("dot_claude.cli.inquirer") as mock_inq:
            mock_inq.select.return_value.execute.return_value = f"Project ({project_dir / '.claude'})"
            result = runner.invoke(main, ["add", "my-skill"])
            assert result.exit_code == 0
            mock_inq.select.assert_called_once()
            assert (project_dir / ".claude" / "skills" / "my-skill").is_symlink()

    def test_add_without_flags_tui_user_scope(self, runner, mock_env, monkeypatch):
        fake_home = mock_env / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: fake_home)
        with patch("dot_claude.cli.inquirer") as mock_inq:
            mock_inq.select.return_value.execute.return_value = f"User ({fake_home / '.claude'})"
            result = runner.invoke(main, ["add", "my-skill"])
            assert result.exit_code == 0
            mock_inq.select.assert_called_once()
            assert (fake_home / ".claude" / "skills" / "my-skill").is_symlink()

    def test_add_mutually_exclusive_flags(self, runner, mock_env):
        result = runner.invoke(main, ["add", "-g", "-p", "my-skill"])
        assert result.exit_code != 0
        assert "mutually exclusive" in result.output


class TestAddConflict:
    """dot-claude add with name conflict across repos."""

    def test_prompts_for_repo_selection(self, runner, tmp_path, monkeypatch):
        config_home = tmp_path / "config"
        cache_home = tmp_path / "cache"
        monkeypatch.setenv("XDG_CONFIG_HOME", str(config_home))
        monkeypatch.setenv("XDG_CACHE_HOME", str(cache_home))

        # Config with two repos
        cfg_dir = config_home / "dot-claude"
        cfg_dir.mkdir(parents=True)
        (cfg_dir / "dot-claude.toml").write_text(
            '[[repos]]\nname = "repo-a"\nurl = "https://github.com/a.git"\n\n'
            '[[repos]]\nname = "repo-b"\nurl = "https://github.com/b.git"\n'
        )

        # Both repos have same skill
        for repo_name in ["repo-a", "repo-b"]:
            d = cache_home / "dot-claude" / repo_name / "skills" / "shared-skill"
            d.mkdir(parents=True)
            (d / "SKILL.md").write_text("content")

        project_dir = tmp_path / "project"
        project_dir.mkdir()
        monkeypatch.chdir(project_dir)

        # Mock inquirerpy to select first repo
        with patch("dot_claude.cli.inquirer") as mock_inq:
            mock_inq.select.return_value.execute.return_value = "repo-a"
            result = runner.invoke(main, ["add", "-p", "shared-skill"])
            assert result.exit_code == 0
            mock_inq.select.assert_called_once()


class TestRemoveCommand:
    """dot-claude remove"""

    def test_remove_from_project_scope(self, runner, mock_env, monkeypatch):
        project_dir = mock_env / "project"
        project_dir.mkdir()
        monkeypatch.chdir(project_dir)
        runner.invoke(main, ["add", "-p", "my-skill"])
        result = runner.invoke(main, ["remove", "-p", "my-skill"])
        assert result.exit_code == 0
        assert "skills/my-skill" in result.output
        assert not (project_dir / ".claude" / "skills" / "my-skill").exists()

    def test_remove_not_installed(self, runner, mock_env, monkeypatch):
        project_dir = mock_env / "project"
        project_dir.mkdir()
        monkeypatch.chdir(project_dir)
        result = runner.invoke(main, ["remove", "-p", "nonexistent"])
        assert result.exit_code != 0
        assert "not installed" in result.output

    def test_remove_from_user_scope(self, runner, mock_env, monkeypatch):
        fake_home = mock_env / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: fake_home)
        runner.invoke(main, ["add", "-g", "my-skill"])
        result = runner.invoke(main, ["remove", "-g", "my-skill"])
        assert result.exit_code == 0
        assert "skills/my-skill" in result.output
        assert not (fake_home / ".claude" / "skills" / "my-skill").exists()

    def test_remove_without_flags_shows_tui(self, runner, mock_env, monkeypatch):
        project_dir = mock_env / "project"
        project_dir.mkdir()
        monkeypatch.chdir(project_dir)
        runner.invoke(main, ["add", "-p", "my-skill"])
        with patch("dot_claude.cli.inquirer") as mock_inq:
            mock_inq.select.return_value.execute.return_value = f"Project ({project_dir / '.claude'})"
            result = runner.invoke(main, ["remove", "my-skill"])
            assert result.exit_code == 0
            mock_inq.select.assert_called_once()
            assert not (project_dir / ".claude" / "skills" / "my-skill").exists()

    def test_remove_without_flags_tui_user_scope(self, runner, mock_env, monkeypatch):
        fake_home = mock_env / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: fake_home)
        runner.invoke(main, ["add", "-g", "my-skill"])
        with patch("dot_claude.cli.inquirer") as mock_inq:
            mock_inq.select.return_value.execute.return_value = f"User ({fake_home / '.claude'})"
            result = runner.invoke(main, ["remove", "my-skill"])
            assert result.exit_code == 0
            mock_inq.select.assert_called_once()
            assert not (fake_home / ".claude" / "skills" / "my-skill").exists()

    def test_remove_mutually_exclusive_flags(self, runner, mock_env, monkeypatch):
        project_dir = mock_env / "project"
        project_dir.mkdir()
        monkeypatch.chdir(project_dir)
        result = runner.invoke(main, ["remove", "-g", "-p", "my-skill"])
        assert result.exit_code != 0
        assert "mutually exclusive" in result.output
