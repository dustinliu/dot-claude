"""Tests for dot_claude.cli."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from dot_claude.cli import cli


def _make_data_root(tmp_path: Path) -> Path:
    data = tmp_path / "data"
    (data / "skills" / "git-commit").mkdir(parents=True)
    (data / "skills" / "git-commit" / "SKILL.md").write_text("git-commit skill")
    (data / "skills" / "leading-change").mkdir(parents=True)
    (data / "skills" / "leading-change" / "SKILL.md").write_text("leading-change skill")
    (data / "agents").mkdir(parents=True)
    (data / "agents" / "code-explorer.md").write_text("code-explorer agent")
    (data / "CLAUDE.md").write_text("workspace rules")
    return data


class TestAdd:
    def test_add_to_user_scope(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "home" / ".claude"

        with (
            patch("dot_claude.cli._get_data_root", return_value=data),
            patch("dot_claude.cli._get_user_dest", return_value=dest),
            patch("dot_claude.cli.prompt_scope", return_value="user"),
            patch("dot_claude.cli.prompt_items", return_value=["skills/git-commit"]),
        ):
            runner = CliRunner()
            result = runner.invoke(cli, ["add"])

        assert result.exit_code == 0
        assert (dest / "skills" / "git-commit" / "SKILL.md").exists()
        assert (dest / "CLAUDE.md").exists()

    def test_add_to_project_scope(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        dest = project_dir / ".claude"

        with (
            patch("dot_claude.cli._get_data_root", return_value=data),
            patch("dot_claude.cli._get_project_dest", return_value=dest),
            patch("dot_claude.cli.prompt_scope", return_value="project"),
            patch("dot_claude.cli.prompt_items", return_value=["skills/git-commit"]),
        ):
            runner = CliRunner()
            result = runner.invoke(cli, ["add"])

        assert result.exit_code == 0
        assert (dest / "skills" / "git-commit" / "SKILL.md").exists()
        assert not (dest / "CLAUDE.md").exists()

    def test_add_cancelled_at_scope(self, tmp_path: Path):
        data = _make_data_root(tmp_path)

        with (
            patch("dot_claude.cli._get_data_root", return_value=data),
            patch("dot_claude.cli.prompt_scope", return_value=None),
        ):
            runner = CliRunner()
            result = runner.invoke(cli, ["add"])

        assert result.exit_code == 0
        assert "Cancelled" in result.output

    def test_add_cancelled_at_items(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "home" / ".claude"

        with (
            patch("dot_claude.cli._get_data_root", return_value=data),
            patch("dot_claude.cli._get_user_dest", return_value=dest),
            patch("dot_claude.cli.prompt_scope", return_value="user"),
            patch("dot_claude.cli.prompt_items", return_value=None),
        ):
            runner = CliRunner()
            result = runner.invoke(cli, ["add"])

        assert result.exit_code == 0
        assert "Cancelled" in result.output

    def test_add_shows_deployed_message(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "home" / ".claude"

        with (
            patch("dot_claude.cli._get_data_root", return_value=data),
            patch("dot_claude.cli._get_user_dest", return_value=dest),
            patch("dot_claude.cli.prompt_scope", return_value="user"),
            patch("dot_claude.cli.prompt_items", return_value=["skills/git-commit"]),
        ):
            runner = CliRunner()
            result = runner.invoke(cli, ["add"])

        assert "Deployed" in result.output or "Installed" in result.output


class TestRemove:
    def test_remove_from_user_scope(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "home" / ".claude"

        # First install
        with (
            patch("dot_claude.cli._get_data_root", return_value=data),
            patch("dot_claude.cli._get_user_dest", return_value=dest),
            patch("dot_claude.cli.prompt_scope", return_value="user"),
            patch(
                "dot_claude.cli.prompt_items",
                return_value=["skills/git-commit", "skills/leading-change"],
            ),
        ):
            CliRunner().invoke(cli, ["add"])

        # Then remove one
        with (
            patch("dot_claude.cli._get_data_root", return_value=data),
            patch("dot_claude.cli._get_user_dest", return_value=dest),
            patch(
                "dot_claude.cli._get_project_dest", return_value=tmp_path / "no-project" / ".claude"
            ),
            patch("dot_claude.cli.prompt_scope", return_value="user"),
            patch("dot_claude.cli.prompt_items", return_value=["skills/git-commit"]),
        ):
            result = CliRunner().invoke(cli, ["remove"])

        assert result.exit_code == 0
        assert (dest / "skills" / "git-commit" / "SKILL.md").exists()
        assert not (dest / "skills" / "leading-change" / "SKILL.md").exists()


class TestList:
    def test_list_with_installed_items(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "home" / ".claude"

        # Install first
        with (
            patch("dot_claude.cli._get_data_root", return_value=data),
            patch("dot_claude.cli._get_user_dest", return_value=dest),
            patch("dot_claude.cli.prompt_scope", return_value="user"),
            patch("dot_claude.cli.prompt_items", return_value=["skills/git-commit"]),
        ):
            CliRunner().invoke(cli, ["add"])

        # Then list
        with (
            patch("dot_claude.cli._get_user_dest", return_value=dest),
            patch(
                "dot_claude.cli._get_project_dest", return_value=tmp_path / "no-project" / ".claude"
            ),
        ):
            result = CliRunner().invoke(cli, ["list"])

        assert result.exit_code == 0
        assert "git-commit" in result.output

    def test_list_with_no_items(self, tmp_path: Path):
        with (
            patch("dot_claude.cli._get_user_dest", return_value=tmp_path / "empty" / ".claude"),
            patch(
                "dot_claude.cli._get_project_dest", return_value=tmp_path / "no-project" / ".claude"
            ),
        ):
            result = CliRunner().invoke(cli, ["list"])

        assert result.exit_code == 0
        assert "Nothing installed" in result.output or "No items" in result.output


class TestUpdate:
    def test_update_redeploys_items(self, tmp_path: Path):
        data = _make_data_root(tmp_path)
        dest = tmp_path / "home" / ".claude"

        # Install first
        with (
            patch("dot_claude.cli._get_data_root", return_value=data),
            patch("dot_claude.cli._get_user_dest", return_value=dest),
            patch("dot_claude.cli.prompt_scope", return_value="user"),
            patch("dot_claude.cli.prompt_items", return_value=["skills/git-commit"]),
        ):
            CliRunner().invoke(cli, ["add"])

        # Modify the source data
        (data / "skills" / "git-commit" / "SKILL.md").write_text("updated content")

        # Update
        with (
            patch("dot_claude.cli._get_data_root", return_value=data),
            patch("dot_claude.cli._get_user_dest", return_value=dest),
            patch(
                "dot_claude.cli._get_project_dest", return_value=tmp_path / "no-project" / ".claude"
            ),
            patch("dot_claude.cli._upgrade_package"),
        ):
            result = CliRunner().invoke(cli, ["update"])

        assert result.exit_code == 0
        assert (dest / "skills" / "git-commit" / "SKILL.md").read_text() == "updated content"


class TestCliHelp:
    def test_main_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "add" in result.output
        assert "remove" in result.output
        assert "list" in result.output
        assert "update" in result.output

    def test_no_args_shows_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, [])
        assert result.exit_code == 0
