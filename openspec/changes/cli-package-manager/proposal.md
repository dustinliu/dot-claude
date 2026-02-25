## Why

The current `deploy.py` only supports deploying the entire `claude/` source tree to `~/.claude/` (user scope). There is no way to selectively install skills/agents, no project-scope support (`./.claude/`), and the source must be a local checkout. This limits reusability across projects and makes it impossible to share project-specific skills via git.

## What Changes

- **BREAKING**: Replace the current `uv run deploy` script with a `dot-claude` CLI tool distributed as a Python package via `uv tool install`
- Add subcommands: `add`, `update`, `remove`, `list`
- `add`: Interactive TUI wizard — step 1: choose scope (user or project), step 2: select skills/agents to install. Selections are remembered in the manifest for next time.
- `update`: Upgrade the CLI itself via uv, then re-deploy all previously installed items from the updated package data
- `remove`: Remove installed skills/agents from a given scope
- `list`: Show what is installed in each scope
- Source of truth moves from local repo to GitHub — skills/agents are bundled as Python package data
- `CLAUDE.md` is always deployed to user scope automatically, never to project scope
- Project scope target is always `$(pwd)/.claude/`

## Capabilities

### New Capabilities

- `cli-commands`: Top-level CLI with subcommands (`add`, `update`, `remove`, `list`) replacing the old `deploy` entry point
- `interactive-tui`: Wizard-style terminal UI for scope selection and item picking (skills + agents in one list)
- `project-scope`: Deploy selected skills/agents to `$(pwd)/.claude/` for project-level use
- `selection-memory`: Remember per-scope item selections in the manifest so subsequent runs pre-check previous choices
- `package-data`: Bundle skills/agents as Python package data so the CLI can read them without a local repo checkout

### Modified Capabilities

- `deployment`: The deploy/copy/cleanup/manifest mechanics are reused but now driven by selective item lists instead of full-tree sync. Target resolution changes to support project scope via cwd. CLAUDE.md auto-deploys to user scope only.

## Impact

- `scripts/deploy.py` — major rewrite or replacement
- `pyproject.toml` — change entry point from `deploy` to `dot-claude`, add TUI dependency, configure package data
- `.deploy-manifest.json` — schema changes to record scope and selected items
- `README.md` — installation and usage docs need full rewrite
- Tests — existing deploy tests need updating for new CLI interface and TDD for new capabilities
