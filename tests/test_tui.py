"""Tests for dot_claude.tui."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from dot_claude.inventory import Item, ItemType
from dot_claude.tui import prompt_items, prompt_scope


class TestPromptScope:
    def test_returns_user_scope(self):
        with patch("questionary.select") as mock_select:
            mock_select.return_value.ask.return_value = "user"
            result = prompt_scope(cwd=Path("/tmp/my-project"))
        assert result == "user"

    def test_returns_project_scope(self):
        with patch("questionary.select") as mock_select:
            mock_select.return_value.ask.return_value = "project"
            result = prompt_scope(cwd=Path("/tmp/my-project"))
        assert result == "project"

    def test_returns_none_on_cancel(self):
        with patch("questionary.select") as mock_select:
            mock_select.return_value.ask.return_value = None
            result = prompt_scope(cwd=Path("/tmp/my-project"))
        assert result is None

    def test_displays_cwd_in_project_option(self):
        with patch("questionary.select") as mock_select:
            mock_select.return_value.ask.return_value = "user"
            prompt_scope(cwd=Path("/tmp/my-project"))
            call_kwargs = mock_select.call_args
            choices = (
                call_kwargs[1]["choices"] if "choices" in call_kwargs[1] else call_kwargs[0][1]
            )
            labels = [c.title for c in choices]
            assert any("/tmp/my-project" in label for label in labels)


class TestPromptItems:
    def _make_items(self) -> list[Item]:
        return [
            Item(
                name="git-commit",
                item_type=ItemType.SKILL,
                files=[Path("skills/git-commit/SKILL.md")],
            ),
            Item(
                name="leading-change",
                item_type=ItemType.SKILL,
                files=[Path("skills/leading-change/SKILL.md")],
            ),
            Item(
                name="code-explorer",
                item_type=ItemType.AGENT,
                files=[Path("agents/code-explorer.md")],
            ),
        ]

    def test_returns_selected_items(self):
        items = self._make_items()
        with patch("questionary.checkbox") as mock_cb:
            mock_cb.return_value.ask.return_value = ["skills/git-commit"]
            result = prompt_items(items, pre_selected=[])
        assert result == ["skills/git-commit"]

    def test_returns_multiple_selected(self):
        items = self._make_items()
        with patch("questionary.checkbox") as mock_cb:
            mock_cb.return_value.ask.return_value = ["skills/git-commit", "agents/code-explorer"]
            result = prompt_items(items, pre_selected=[])
        assert result == ["skills/git-commit", "agents/code-explorer"]

    def test_pre_selected_items_passed_as_checked(self):
        items = self._make_items()
        with patch("questionary.checkbox") as mock_cb:
            mock_cb.return_value.ask.return_value = ["skills/git-commit"]
            prompt_items(items, pre_selected=["skills/git-commit"])
            call_kwargs = mock_cb.call_args
            choices = (
                call_kwargs[1]["choices"] if "choices" in call_kwargs[1] else call_kwargs[0][1]
            )
            checked_values = [c.value for c in choices if hasattr(c, "checked") and c.checked]
            assert "skills/git-commit" in checked_values

    def test_returns_none_on_cancel(self):
        items = self._make_items()
        with patch("questionary.checkbox") as mock_cb:
            mock_cb.return_value.ask.return_value = None
            result = prompt_items(items, pre_selected=[])
        assert result is None

    def test_returns_empty_list_when_none_selected(self):
        items = self._make_items()
        with patch("questionary.checkbox") as mock_cb:
            mock_cb.return_value.ask.return_value = []
            result = prompt_items(items, pre_selected=[])
        assert result == []
