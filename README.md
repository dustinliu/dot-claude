# dot-claude

CLI tool for managing Claude Code skills and agents. Install skills and agents to user scope (`~/.claude/`) or project scope (`./.claude/`) with an interactive TUI.

## What you get

- **Agents** — role-specific prompts (e.g. code-explorer, code-architect, code-reviewer)
- **Skills** — reusable task instructions (e.g. git-commit)
- **Rules** — workspace conventions Claude Code follows (`CLAUDE.md`, user scope only)

## Install

```bash
uv tool install git+https://github.com/dustinl/dot-claude
```

## Usage

### Add skills/agents

```bash
dot-claude add
```

Interactive wizard:
1. Select scope — **User** (`~/.claude/`) or **Project** (`<cwd>/.claude/`)
2. Select items — check/uncheck skills and agents to install

Selections are remembered per scope. Next time you run `add`, previous choices are pre-checked.

### Update

```bash
dot-claude update
```

Upgrades the CLI to the latest version from GitHub and re-deploys all previously installed items.

### Remove

```bash
dot-claude remove
```

Deselect items to remove from a scope.

### List installed

```bash
dot-claude list
```

Shows what's installed in user and project scope.

## How it works

- Skills and agents are bundled as package data inside the CLI tool
- `CLAUDE.md` is automatically deployed to user scope (never to project scope)
- A `.deploy-manifest.json` in each target directory tracks what was installed
- Files not managed by dot-claude (e.g. `settings.local.json`, external skills) are never touched

## Requirements

- [uv](https://docs.astral.sh/uv/) (Python package runner/installer)
