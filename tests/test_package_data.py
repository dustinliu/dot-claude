"""Tests that package data (skills/agents) is accessible via importlib.resources."""

from __future__ import annotations

from importlib import resources


def test_claude_directory_accessible():
    """Package data root 'claude' directory is accessible."""
    claude = resources.files("dot_claude") / "claude"
    assert claude.is_dir()


def test_skills_directory_accessible():
    """Skills directory exists and contains at least one skill."""
    skills = resources.files("dot_claude") / "claude" / "skills"
    assert skills.is_dir()
    skill_dirs = [p for p in skills.iterdir() if p.is_dir()]
    assert len(skill_dirs) > 0


def test_agents_directory_accessible():
    """Agents directory exists and contains at least one agent."""
    agents = resources.files("dot_claude") / "claude" / "agents"
    assert agents.is_dir()
    agent_files = [p for p in agents.iterdir() if p.name.endswith(".md")]
    assert len(agent_files) > 0


def test_skill_content_readable():
    """Can read the content of a skill SKILL.md file."""
    skill_md = resources.files("dot_claude") / "claude" / "skills" / "git-commit" / "SKILL.md"
    content = skill_md.read_text()
    assert len(content) > 0
    assert "---" in content  # frontmatter marker


def test_agent_content_readable():
    """Can read the content of an agent .md file."""
    agent_md = resources.files("dot_claude") / "claude" / "agents" / "code-explorer.md"
    content = agent_md.read_text()
    assert len(content) > 0
    assert "---" in content  # frontmatter marker


def test_claude_md_accessible():
    """CLAUDE.md is accessible as package data."""
    claude_md = resources.files("dot_claude") / "claude" / "CLAUDE.md"
    content = claude_md.read_text()
    assert len(content) > 0
