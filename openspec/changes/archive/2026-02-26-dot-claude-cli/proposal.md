## Why

Managing Claude Code artifacts (skills, agents) across multiple git repositories requires
manual symlink management, tracking which artifacts are installed where, and keeping
external repos up to date. A CLI tool automates this workflow, providing a single
interface to discover, install, and manage artifacts from any number of source repos.

## What Changes

- Add a uv Python project providing a `dot-claude` CLI, executable via `uvx dot-claude`
- `init` subcommand: creates config directory and generates a commented example config at `$XDG_CONFIG_HOME/dot-claude/dot-claude.toml`
- `update` subcommand: clones (first run) or pulls (subsequent runs) all configured repos to `$XDG_CACHE_HOME/dot-claude/`
- `add <name> [-g]` subcommand: symlinks an artifact to project scope (`./.claude/`) by default, or user scope (`~/.claude/`) with `-g` flag. When multiple repos provide the same artifact name, presents a TUI selector to choose the source repo.
- `remove <name> [-g]` subcommand: removes the symlink for an artifact
- `list [-g]` subcommand: lists all available artifacts from all repos with aligned columns showing artifact name, source repo, and install status (`[user]`, `[project]`, or `-`)
- Config file (`dot-claude.toml`) defines repos via `[[repos]]` entries with `name`, `url`, and optional `skills`/`agents` directory overrides (default: `skills/`, `agents/`)

## Capabilities

### New Capabilities
- `cli-commands`: CLI entry point, subcommand routing, and `-g` flag handling
- `repo-management`: Cloning, pulling, and scanning artifact repos based on config
- `artifact-deployment`: Symlink creation/removal for skills and agents to user or project scope
- `config-management`: XDG-compliant config initialization, parsing, and validation

### Modified Capabilities
_(none — this is a new tool)_

## Impact

- New `pyproject.toml` and Python source tree added to repository
- Requires `uv` for execution (`uvx dot-claude`)
- Creates directories under `$XDG_CONFIG_HOME/dot-claude/` and `$XDG_CACHE_HOME/dot-claude/`
- Creates symlinks in `~/.claude/` (user scope) and `./.claude/` (project scope)
