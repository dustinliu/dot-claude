"""Interactive TUI prompts for scope and item selection."""

from __future__ import annotations

from pathlib import Path

import questionary

from dot_claude.inventory import Item, ItemType


def prompt_scope(cwd: Path) -> str | None:
    """Prompt user to select deployment scope.

    Returns:
        "user" or "project", or None if cancelled.
    """
    choices = [
        questionary.Choice(title="User (~/.claude/)", value="user"),
        questionary.Choice(title=f"Project ({cwd}/.claude/)", value="project"),
    ]
    return questionary.select("Select scope:", choices=choices).ask()


def prompt_items(items: list[Item], pre_selected: list[str]) -> list[str] | None:
    """Prompt user to select skills/agents to install.

    Args:
        items: Available items from inventory.
        pre_selected: Item keys to pre-check.

    Returns:
        List of selected item keys, or None if cancelled.
    """
    pre_set = set(pre_selected)
    choices: list[questionary.Choice | questionary.Separator] = []

    skills = [i for i in items if i.item_type == ItemType.SKILL]
    agents = [i for i in items if i.item_type == ItemType.AGENT]

    if skills:
        choices.append(questionary.Separator("── Skills ──"))
        for item in skills:
            choices.append(
                questionary.Choice(
                    title=item.name,
                    value=item.key,
                    checked=item.key in pre_set,
                )
            )

    if agents:
        choices.append(questionary.Separator("── Agents ──"))
        for item in agents:
            choices.append(
                questionary.Choice(
                    title=item.name,
                    value=item.key,
                    checked=item.key in pre_set,
                )
            )

    return questionary.checkbox("Select items to install:", choices=choices).ask()
