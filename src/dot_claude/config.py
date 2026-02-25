"""Config management: XDG paths, TOML parsing, init."""

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

APP_NAME = "dot-claude"
CONFIG_FILENAME = "dot-claude.toml"


class ConfigError(Exception):
    """Raised when config loading or validation fails."""


@dataclass
class RepoEntry:
    """A single [[repos]] entry from the config."""

    name: str
    url: str
    skills: str = "skills"
    agents: str = "agents"


def config_dir() -> Path:
    """Return the config directory ($XDG_CONFIG_HOME/dot-claude/)."""
    base = os.environ.get("XDG_CONFIG_HOME", "")
    if base:
        return Path(base) / APP_NAME
    return Path.home() / ".config" / APP_NAME


def cache_dir() -> Path:
    """Return the cache directory ($XDG_CACHE_HOME/dot-claude/)."""
    base = os.environ.get("XDG_CACHE_HOME", "")
    if base:
        return Path(base) / APP_NAME
    return Path.home() / ".cache" / APP_NAME


def config_path() -> Path:
    """Return the full path to the config file."""
    return config_dir() / CONFIG_FILENAME


def load_config(path: Path) -> list[RepoEntry]:
    """Load and validate the TOML config file, returning repo entries."""
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")

    try:
        data = tomllib.loads(path.read_text())
    except tomllib.TOMLDecodeError as e:
        raise ConfigError(f"Failed to parse config: {e}") from e

    repos_raw = data.get("repos", [])
    repos: list[RepoEntry] = []
    for i, entry in enumerate(repos_raw):
        if "name" not in entry:
            raise ConfigError(f"repos[{i}]: missing required field 'name'")
        if "url" not in entry:
            raise ConfigError(f"repos[{i}]: missing required field 'url'")
        repos.append(
            RepoEntry(
                name=entry["name"],
                url=entry["url"],
                skills=entry.get("skills", "skills"),
                agents=entry.get("agents", "agents"),
            )
        )
    return repos


_EXAMPLE_CONFIG = """\
# dot-claude configuration
#
# Define artifact repositories below.
# Each repo provides skills and/or agents for Claude Code.
#
# [[repos]]
# name = "my-repo"
# url = "https://github.com/user/repo.git"
# skills = "my-skills"  # optional, default: "skills"
# agents = "my-agents"  # optional, default: "agents"
"""


def init_config(path: Path) -> None:
    """Create the config directory and generate a commented example config."""
    if path.exists():
        raise ConfigError(f"Config file already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_EXAMPLE_CONFIG)
