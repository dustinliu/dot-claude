"""Tests for repo management: clone, pull, scan artifacts."""

from pathlib import Path
from unittest.mock import patch, call

import pytest

from dot_claude.config import RepoEntry
from dot_claude.repos import clone_repo, pull_repo, update_repos, scan_artifacts, Artifact


class TestCloneRepo:
    """Clone a repo to cache directory."""

    def test_clone_runs_git_clone(self, tmp_path):
        cache = tmp_path / "cache"
        repo = RepoEntry(name="my-repo", url="https://github.com/user/repo.git")
        with patch("dot_claude.repos.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            clone_repo(repo, cache)
            mock_run.assert_called_once_with(
                ["git", "clone", repo.url, str(cache / "my-repo")],
                capture_output=True,
                text=True,
                check=True,
            )

    def test_clone_creates_cache_dir(self, tmp_path):
        cache = tmp_path / "cache" / "deep"
        repo = RepoEntry(name="my-repo", url="https://github.com/user/repo.git")
        with patch("dot_claude.repos.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            clone_repo(repo, cache)
            assert cache.exists()


class TestPullRepo:
    """Pull latest changes for a cached repo."""

    def test_pull_runs_git_pull(self, tmp_path):
        repo_dir = tmp_path / "my-repo"
        repo_dir.mkdir()
        repo = RepoEntry(name="my-repo", url="https://github.com/user/repo.git")
        with patch("dot_claude.repos.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            pull_repo(repo, tmp_path)
            mock_run.assert_called_once_with(
                ["git", "pull"],
                cwd=str(repo_dir),
                capture_output=True,
                text=True,
                check=True,
            )


class TestUpdateRepos:
    """Update all repos: clone new, pull existing."""

    def test_clones_new_repo(self, tmp_path):
        repo = RepoEntry(name="new-repo", url="https://github.com/user/repo.git")
        with patch("dot_claude.repos.clone_repo") as mock_clone:
            update_repos([repo], tmp_path)
            mock_clone.assert_called_once_with(repo, tmp_path)

    def test_pulls_existing_repo(self, tmp_path):
        repo = RepoEntry(name="existing-repo", url="https://github.com/user/repo.git")
        (tmp_path / "existing-repo").mkdir()
        with patch("dot_claude.repos.pull_repo") as mock_pull:
            update_repos([repo], tmp_path)
            mock_pull.assert_called_once_with(repo, tmp_path)

    def test_reports_errors_per_repo(self, tmp_path):
        repo_a = RepoEntry(name="repo-a", url="https://github.com/a.git")
        repo_b = RepoEntry(name="repo-b", url="https://github.com/b.git")
        with patch("dot_claude.repos.clone_repo") as mock_clone:
            mock_clone.side_effect = [Exception("network error"), None]
            errors = update_repos([repo_a, repo_b], tmp_path)
            assert len(errors) == 1
            assert "repo-a" in errors[0]


def _make_repo(tmp_path, name="test-repo", skills_dir="skills", agents_dir="agents"):
    """Helper: create a fake cached repo with skills and agents."""
    repo_dir = tmp_path / name
    (repo_dir / skills_dir / "my-skill").mkdir(parents=True)
    (repo_dir / skills_dir / "my-skill" / "SKILL.md").write_text("skill content")
    (repo_dir / skills_dir / "other-skill").mkdir(parents=True)
    (repo_dir / agents_dir).mkdir(parents=True)
    (repo_dir / agents_dir / "my-agent.md").write_text("agent content")
    return repo_dir


class TestScanArtifacts:
    """Discover skills and agents from a cached repo."""

    def test_finds_skills(self, tmp_path):
        _make_repo(tmp_path)
        repo = RepoEntry(name="test-repo", url="https://example.com/repo.git")
        artifacts = scan_artifacts(repo, tmp_path)
        skills = [a for a in artifacts if a.kind == "skill"]
        assert len(skills) == 2
        names = {a.name for a in skills}
        assert names == {"my-skill", "other-skill"}

    def test_finds_agents(self, tmp_path):
        _make_repo(tmp_path)
        repo = RepoEntry(name="test-repo", url="https://example.com/repo.git")
        artifacts = scan_artifacts(repo, tmp_path)
        agents = [a for a in artifacts if a.kind == "agent"]
        assert len(agents) == 1
        assert agents[0].name == "my-agent"

    def test_custom_dirs(self, tmp_path):
        _make_repo(tmp_path, skills_dir="my-skills", agents_dir="my-agents")
        repo = RepoEntry(
            name="test-repo", url="https://example.com/repo.git",
            skills="my-skills", agents="my-agents",
        )
        artifacts = scan_artifacts(repo, tmp_path)
        assert len(artifacts) == 3  # 2 skills + 1 agent

    def test_missing_skills_dir(self, tmp_path):
        repo_dir = tmp_path / "test-repo"
        (repo_dir / "agents").mkdir(parents=True)
        (repo_dir / "agents" / "an-agent.md").write_text("content")
        repo = RepoEntry(name="test-repo", url="https://example.com/repo.git")
        artifacts = scan_artifacts(repo, tmp_path)
        assert len(artifacts) == 1
        assert artifacts[0].kind == "agent"

    def test_missing_agents_dir(self, tmp_path):
        repo_dir = tmp_path / "test-repo"
        (repo_dir / "skills" / "a-skill").mkdir(parents=True)
        repo = RepoEntry(name="test-repo", url="https://example.com/repo.git")
        artifacts = scan_artifacts(repo, tmp_path)
        assert len(artifacts) == 1
        assert artifacts[0].kind == "skill"

    def test_ignores_hidden_dirs(self, tmp_path):
        repo_dir = tmp_path / "test-repo"
        (repo_dir / "skills" / ".hidden").mkdir(parents=True)
        (repo_dir / "skills" / "visible").mkdir(parents=True)
        repo = RepoEntry(name="test-repo", url="https://example.com/repo.git")
        artifacts = scan_artifacts(repo, tmp_path)
        assert len(artifacts) == 1
        assert artifacts[0].name == "visible"

    def test_ignores_non_md_agent_files(self, tmp_path):
        repo_dir = tmp_path / "test-repo"
        (repo_dir / "agents").mkdir(parents=True)
        (repo_dir / "agents" / "valid.md").write_text("content")
        (repo_dir / "agents" / "invalid.txt").write_text("content")
        repo = RepoEntry(name="test-repo", url="https://example.com/repo.git")
        artifacts = scan_artifacts(repo, tmp_path)
        assert len(artifacts) == 1
        assert artifacts[0].name == "valid"

    def test_source_path_is_set(self, tmp_path):
        _make_repo(tmp_path)
        repo = RepoEntry(name="test-repo", url="https://example.com/repo.git")
        artifacts = scan_artifacts(repo, tmp_path)
        for a in artifacts:
            assert a.source_path.exists()
