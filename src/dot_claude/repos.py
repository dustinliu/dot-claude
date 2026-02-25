"""Repo management: clone, pull, scan artifacts."""

import subprocess
from dataclasses import dataclass
from pathlib import Path

from dot_claude.config import RepoEntry


@dataclass
class Artifact:
    """A discovered skill or agent artifact."""

    name: str
    kind: str  # "skill" or "agent"
    repo_name: str
    source_path: Path


def clone_repo(repo: RepoEntry, cache: Path) -> None:
    """Clone a repo into the cache directory."""
    cache.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "clone", repo.url, str(cache / repo.name)],
        capture_output=True,
        text=True,
        check=True,
    )


def pull_repo(repo: RepoEntry, cache: Path) -> None:
    """Pull latest changes for a cached repo."""
    repo_dir = cache / repo.name
    subprocess.run(
        ["git", "pull"],
        cwd=str(repo_dir),
        capture_output=True,
        text=True,
        check=True,
    )


def update_repos(repos: list[RepoEntry], cache: Path) -> list[str]:
    """Clone new repos and pull existing ones. Returns list of error messages."""
    errors: list[str] = []
    for repo in repos:
        repo_dir = cache / repo.name
        try:
            if repo_dir.exists():
                pull_repo(repo, cache)
            else:
                clone_repo(repo, cache)
        except Exception as e:
            errors.append(f"{repo.name}: {e}")
    return errors


def scan_artifacts(repo: RepoEntry, cache: Path) -> list[Artifact]:
    """Scan a cached repo for available skills and agents."""
    repo_dir = cache / repo.name
    artifacts: list[Artifact] = []

    # Scan skills (subdirectories of the skills dir)
    skills_dir = repo_dir / repo.skills
    if skills_dir.is_dir():
        for entry in sorted(skills_dir.iterdir()):
            if entry.is_dir() and not entry.name.startswith("."):
                artifacts.append(
                    Artifact(
                        name=entry.name,
                        kind="skill",
                        repo_name=repo.name,
                        source_path=entry,
                    )
                )

    # Scan agents (.md files in the agents dir)
    agents_dir = repo_dir / repo.agents
    if agents_dir.is_dir():
        for entry in sorted(agents_dir.iterdir()):
            if entry.is_file() and entry.suffix == ".md" and not entry.name.startswith("."):
                artifacts.append(
                    Artifact(
                        name=entry.stem,
                        kind="agent",
                        repo_name=repo.name,
                        source_path=entry,
                    )
                )

    return artifacts
