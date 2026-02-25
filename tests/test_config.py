"""Tests for config module: XDG paths, TOML parsing, init."""

from pathlib import Path

import pytest

from dot_claude.config import (
    config_dir,
    cache_dir,
    config_path,
    load_config,
    init_config,
    ConfigError,
    RepoEntry,
)


class TestXdgPaths:
    """XDG path resolution with fallbacks."""

    def test_config_dir_uses_xdg_config_home(self, monkeypatch, tmp_path):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        assert config_dir() == tmp_path / "dot-claude"

    def test_config_dir_fallback_when_unset(self, monkeypatch):
        monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
        expected = Path.home() / ".config" / "dot-claude"
        assert config_dir() == expected

    def test_cache_dir_uses_xdg_cache_home(self, monkeypatch, tmp_path):
        monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
        assert cache_dir() == tmp_path / "dot-claude"

    def test_cache_dir_fallback_when_unset(self, monkeypatch):
        monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
        expected = Path.home() / ".cache" / "dot-claude"
        assert cache_dir() == expected


class TestConfigPath:
    """Config file path resolution."""

    def test_config_path_returns_toml_file(self, monkeypatch, tmp_path):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        assert config_path() == tmp_path / "dot-claude" / "dot-claude.toml"


class TestLoadConfig:
    """TOML config parsing and validation."""

    def test_load_valid_config(self, tmp_path):
        toml_file = tmp_path / "dot-claude.toml"
        toml_file.write_text(
            '[[repos]]\nname = "my-repo"\nurl = "https://github.com/user/repo.git"\n'
        )
        repos = load_config(toml_file)
        assert len(repos) == 1
        assert repos[0].name == "my-repo"
        assert repos[0].url == "https://github.com/user/repo.git"
        assert repos[0].skills == "skills"
        assert repos[0].agents == "agents"

    def test_load_config_with_custom_dirs(self, tmp_path):
        toml_file = tmp_path / "dot-claude.toml"
        toml_file.write_text(
            '[[repos]]\nname = "dot-claude"\n'
            'url = "https://github.com/user/dot-claude.git"\n'
            'skills = "my-skills"\nagents = "my-agents"\n'
        )
        repos = load_config(toml_file)
        assert repos[0].skills == "my-skills"
        assert repos[0].agents == "my-agents"

    def test_load_config_multiple_repos(self, tmp_path):
        toml_file = tmp_path / "dot-claude.toml"
        toml_file.write_text(
            '[[repos]]\nname = "repo-a"\nurl = "https://github.com/a.git"\n\n'
            '[[repos]]\nname = "repo-b"\nurl = "https://github.com/b.git"\n'
        )
        repos = load_config(toml_file)
        assert len(repos) == 2
        assert repos[0].name == "repo-a"
        assert repos[1].name == "repo-b"

    def test_load_config_missing_file(self, tmp_path):
        toml_file = tmp_path / "nonexistent.toml"
        with pytest.raises(ConfigError, match="not found"):
            load_config(toml_file)

    def test_load_config_invalid_toml(self, tmp_path):
        toml_file = tmp_path / "dot-claude.toml"
        toml_file.write_text("this is not valid toml [[[")
        with pytest.raises(ConfigError, match="parse"):
            load_config(toml_file)

    def test_load_config_missing_name(self, tmp_path):
        toml_file = tmp_path / "dot-claude.toml"
        toml_file.write_text('[[repos]]\nurl = "https://github.com/a.git"\n')
        with pytest.raises(ConfigError, match="name"):
            load_config(toml_file)

    def test_load_config_missing_url(self, tmp_path):
        toml_file = tmp_path / "dot-claude.toml"
        toml_file.write_text('[[repos]]\nname = "my-repo"\n')
        with pytest.raises(ConfigError, match="url"):
            load_config(toml_file)

    def test_load_config_no_repos(self, tmp_path):
        toml_file = tmp_path / "dot-claude.toml"
        toml_file.write_text("# empty config\n")
        repos = load_config(toml_file)
        assert repos == []


class TestInitConfig:
    """init_config creates config directory and example file."""

    def test_creates_config_file(self, tmp_path):
        cfg_path = tmp_path / "dot-claude" / "dot-claude.toml"
        init_config(cfg_path)
        assert cfg_path.exists()

    def test_creates_parent_directory(self, tmp_path):
        cfg_path = tmp_path / "dot-claude" / "dot-claude.toml"
        init_config(cfg_path)
        assert cfg_path.parent.is_dir()

    def test_generated_file_has_example_content(self, tmp_path):
        cfg_path = tmp_path / "dot-claude" / "dot-claude.toml"
        init_config(cfg_path)
        content = cfg_path.read_text()
        assert "[[repos]]" in content
        assert "name" in content
        assert "url" in content
        assert "skills" in content
        assert "agents" in content

    def test_generated_file_is_commented(self, tmp_path):
        cfg_path = tmp_path / "dot-claude" / "dot-claude.toml"
        init_config(cfg_path)
        content = cfg_path.read_text()
        assert content.startswith("#")

    def test_does_not_overwrite_existing(self, tmp_path):
        cfg_path = tmp_path / "dot-claude" / "dot-claude.toml"
        cfg_path.parent.mkdir(parents=True)
        cfg_path.write_text("existing content")
        with pytest.raises(ConfigError, match="already exists"):
            init_config(cfg_path)
