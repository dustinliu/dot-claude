"""Tests for dot_claude.inventory."""

from __future__ import annotations

from pathlib import Path

from dot_claude.inventory import Item, ItemType, list_items


class TestListItems:
    def test_returns_skills(self, tmp_path: Path):
        (tmp_path / "skills" / "git-commit").mkdir(parents=True)
        (tmp_path / "skills" / "git-commit" / "SKILL.md").write_text("skill content")

        items = list_items(tmp_path)
        skills = [i for i in items if i.item_type == ItemType.SKILL]
        assert len(skills) == 1
        assert skills[0].name == "git-commit"

    def test_returns_agents(self, tmp_path: Path):
        (tmp_path / "agents").mkdir(parents=True)
        (tmp_path / "agents" / "code-explorer.md").write_text("agent content")

        items = list_items(tmp_path)
        agents = [i for i in items if i.item_type == ItemType.AGENT]
        assert len(agents) == 1
        assert agents[0].name == "code-explorer"

    def test_returns_combined_list(self, tmp_path: Path):
        (tmp_path / "skills" / "git-commit").mkdir(parents=True)
        (tmp_path / "skills" / "git-commit" / "SKILL.md").write_text("s")
        (tmp_path / "agents").mkdir(parents=True)
        (tmp_path / "agents" / "code-explorer.md").write_text("a")

        items = list_items(tmp_path)
        assert len(items) == 2

    def test_skill_without_skill_md_ignored(self, tmp_path: Path):
        """A directory under skills/ without SKILL.md is not a valid skill."""
        (tmp_path / "skills" / "broken").mkdir(parents=True)
        (tmp_path / "skills" / "broken" / "README.md").write_text("not a skill")

        items = list_items(tmp_path)
        assert len(items) == 0

    def test_agent_non_md_file_ignored(self, tmp_path: Path):
        """Non-.md files under agents/ are ignored."""
        (tmp_path / "agents").mkdir(parents=True)
        (tmp_path / "agents" / "notes.txt").write_text("not an agent")

        items = list_items(tmp_path)
        assert len(items) == 0

    def test_multiple_skills_and_agents(self, tmp_path: Path):
        for name in ["git-commit", "creating-todo", "leading-change"]:
            (tmp_path / "skills" / name).mkdir(parents=True)
            (tmp_path / "skills" / name / "SKILL.md").write_text("s")
        for name in ["code-explorer", "code-reviewer"]:
            (tmp_path / "agents").mkdir(parents=True, exist_ok=True)
            (tmp_path / "agents" / f"{name}.md").write_text("a")

        items = list_items(tmp_path)
        skills = [i for i in items if i.item_type == ItemType.SKILL]
        agents = [i for i in items if i.item_type == ItemType.AGENT]
        assert len(skills) == 3
        assert len(agents) == 2

    def test_empty_directory(self, tmp_path: Path):
        items = list_items(tmp_path)
        assert items == []

    def test_item_key_format(self, tmp_path: Path):
        """Item key is 'skills/<name>' for skills and 'agents/<name>' for agents."""
        (tmp_path / "skills" / "git-commit").mkdir(parents=True)
        (tmp_path / "skills" / "git-commit" / "SKILL.md").write_text("s")
        (tmp_path / "agents").mkdir(parents=True)
        (tmp_path / "agents" / "code-explorer.md").write_text("a")

        items = list_items(tmp_path)
        keys = {i.key for i in items}
        assert keys == {"skills/git-commit", "agents/code-explorer"}

    def test_item_files_for_skill(self, tmp_path: Path):
        """Skill item lists all files relative to the data root."""
        (tmp_path / "skills" / "git-commit").mkdir(parents=True)
        (tmp_path / "skills" / "git-commit" / "SKILL.md").write_text("s")

        items = list_items(tmp_path)
        assert items[0].files == [Path("skills/git-commit/SKILL.md")]

    def test_item_files_for_agent(self, tmp_path: Path):
        """Agent item lists the single .md file."""
        (tmp_path / "agents").mkdir(parents=True)
        (tmp_path / "agents" / "code-explorer.md").write_text("a")

        items = list_items(tmp_path)
        assert items[0].files == [Path("agents/code-explorer.md")]

    def test_items_sorted_by_type_then_name(self, tmp_path: Path):
        """Items are returned sorted: skills first, then agents, each alphabetical."""
        (tmp_path / "skills" / "zebra").mkdir(parents=True)
        (tmp_path / "skills" / "zebra" / "SKILL.md").write_text("s")
        (tmp_path / "skills" / "alpha").mkdir(parents=True)
        (tmp_path / "skills" / "alpha" / "SKILL.md").write_text("s")
        (tmp_path / "agents").mkdir(parents=True)
        (tmp_path / "agents" / "beta.md").write_text("a")

        items = list_items(tmp_path)
        names = [i.name for i in items]
        assert names == ["alpha", "zebra", "beta"]


class TestItem:
    def test_repr(self):
        item = Item(
            name="git-commit", item_type=ItemType.SKILL, files=[Path("skills/git-commit/SKILL.md")]
        )
        assert "git-commit" in repr(item)

    def test_key_property(self):
        skill = Item(name="git-commit", item_type=ItemType.SKILL, files=[])
        assert skill.key == "skills/git-commit"
        agent = Item(name="code-explorer", item_type=ItemType.AGENT, files=[])
        assert agent.key == "agents/code-explorer"
