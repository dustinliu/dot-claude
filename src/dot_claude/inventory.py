"""Enumerate available skills and agents from package data."""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path


class ItemType(enum.Enum):
    SKILL = "skill"
    AGENT = "agent"


@dataclass
class Item:
    name: str
    item_type: ItemType
    files: list[Path] = field(default_factory=list)

    @property
    def key(self) -> str:
        prefix = "skills" if self.item_type == ItemType.SKILL else "agents"
        return f"{prefix}/{self.name}"

    def __repr__(self) -> str:
        return f"Item(name={self.name!r}, type={self.item_type.value})"


def list_items(data_root: Traversable | None = None) -> list[Item]:
    """List all available skills and agents.

    Args:
        data_root: Path to the claude data directory. If None, uses package data.

    Returns:
        List of items sorted by type (skills first) then name.
    """
    if data_root is None:
        data_root = resources.files("dot_claude") / "claude"

    items: list[Item] = []

    # Enumerate skills
    skills_dir = data_root / "skills"
    if skills_dir.is_dir():
        for entry in sorted(skills_dir.iterdir(), key=lambda p: p.name):
            if not entry.is_dir():
                continue
            skill_md = entry / "SKILL.md"
            if skill_md.is_file():
                items.append(
                    Item(
                        name=entry.name,
                        item_type=ItemType.SKILL,
                        files=[Path("skills") / entry.name / "SKILL.md"],
                    )
                )

    # Enumerate agents
    agents_dir = data_root / "agents"
    if agents_dir.is_dir():
        for entry in sorted(agents_dir.iterdir(), key=lambda p: p.name):
            if not entry.is_file() or not entry.name.endswith(".md"):
                continue
            agent_name = entry.name.removesuffix(".md")
            items.append(
                Item(
                    name=agent_name,
                    item_type=ItemType.AGENT,
                    files=[Path("agents") / entry.name],
                )
            )

    return items
