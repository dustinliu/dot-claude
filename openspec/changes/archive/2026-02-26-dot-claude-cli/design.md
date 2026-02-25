## Context

This repository (`dot-claude`) maintains personal Claude Code configuration — custom
CLAUDE.md, skills, and agents. Artifacts live in `my-skills/`, `my-agents/`, and
`my-claude/` locally, plus external git repos that follow Claude Code's standard
`skills/` and `agents/` directory convention.

Currently, deploying artifacts to `~/.claude/` (user scope) or `./.claude/` (project
scope) is entirely manual. There is no tooling to discover available artifacts across
repos, track what is installed, or keep external repos up to date.

## Goals / Non-Goals

**Goals:**
- Single CLI to manage artifact lifecycle: discover, install, remove, update
- Support multiple source repos (local + external git repos)
- XDG-compliant config and cache directories
- Symlink-based deployment for both user and project scopes
- Executable from anywhere via `uvx dot-claude`

**Non-Goals:**
- Migration of existing copy-deployed artifacts (done manually)
- CLAUDE.md deployment (managed separately)
- Version pinning or lock files (always track repo HEAD)
- Publishing to PyPI (local/uvx usage only)

## Decisions

### 1. CLI framework: `click`
Use `click` for subcommand routing and argument parsing. It is mature, well-documented,
and handles the `-g` flag pattern cleanly. `argparse` is too verbose for this use case;
`typer` adds unnecessary pydantic dependency.

### 2. TUI library: `inquirer` (via `inquirerpy`)
Use `InquirerPy` for interactive prompts (repo selection when name conflicts arise).
Lightweight, supports list selection out of the box, no heavy TUI framework needed.

### 3. Config format: TOML at `$XDG_CONFIG_HOME/dot-claude/dot-claude.toml`
TOML is the Python ecosystem standard (`pyproject.toml`). Parse with `tomllib` (stdlib
since Python 3.11). Config lives outside the repo so it works when running via `uvx`
from any directory.

### 4. All repos defined via URL, cloned to XDG cache
Every source repo (including this one) is defined with a `url` field in config and
cloned to `$XDG_CACHE_HOME/dot-claude/<repo-name>/`. This eliminates the need for
hardcoded local paths that break when directories move. The `update` command handles
clone (first time) and pull (subsequent).

### 5. Directory override via `skills` and `agents` config keys
Repos default to scanning `skills/` and `agents/` directories. Config entries can
override with `skills = "my-skills"` and `agents = "my-agents"` for repos that use
non-standard directory names.

### 6. Scope via `-g` flag
Default scope is project (`./.claude/`). The `-g` flag switches to user scope
(`~/.claude/`). This applies to `add`, `remove`, and `list`.

### 7. Artifact type detection by directory
Skills live in a directory containing `SKILL.md` (or subdirectories of the skills dir).
Agents are `.md` files directly in the agents directory. No manifest needed — directory
structure is the source of truth.

## Risks / Trade-offs

- **[Symlink breakage]** → If cache directory is cleared, symlinks break. Mitigation:
  `update` re-clones missing repos; `list` can detect broken symlinks.
- **[Name collision across repos]** → Two repos providing same artifact name. Mitigation:
  `add` presents interactive selection; `list` shows source repo for each artifact.
- **[No offline support]** → `update` requires network. Mitigation: artifacts work from
  cache after initial clone; only `update` needs connectivity.
- **[Python version requirement]** → `tomllib` requires Python 3.11+. Mitigation: `uv`
  manages Python versions; can fall back to `tomli` backport if needed.
