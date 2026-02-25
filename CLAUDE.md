# dot-claude (developer)

Development and maintenance repository for Claude Code configurations. This file is for **developers** working in this repo. For installation and usage, see **README.md**.

## ⚠️ Important

- Skills, agents, and CLAUDE.md live in `src/dot_claude/claude/` — this is the **single source of truth** (bundled as package data).
- Use `dot-claude add/update/remove/list` CLI commands to deploy items to `~/.claude/` or `./.claude/`.
- Claude Code reads from `~/.claude/` or `./.claude/` (the deployed locations).

Changes only take effect after deployment.

## Directory structure

```
.
├── src/dot_claude/                   # Python package
│   ├── __init__.py
│   ├── claude/                       # Source of truth for skills/agents (package data)
│   │   ├── CLAUDE.md                 # Workspace rules for Claude Code
│   │   ├── agents/                   # Claude Code subagents
│   │   └── skills/                   # Claude Code skills
│   ├── cli.py                        # CLI entry point (dot-claude command)
│   ├── installer.py                  # Install/remove logic
│   ├── inventory.py                  # List available items from package data
│   ├── manifest.py                   # Deploy manifest read/write
│   └── tui.py                        # Interactive TUI (scope/item selection)
├── openspec/                         # OpenSpec artifacts (specs, changes, config)
├── tests/                            # pytest tests
├── .editorconfig
├── .gitignore
├── .python-version
├── CLAUDE.md                         # This file (repo dev rules)
├── LICENSE
├── README.md                         # User manual
├── pyproject.toml                    # Python project config (hatchling build)
├── skills-lock.json                  # Tracks external skills (gitignored)
└── uv.lock
```

## Development workflow

1. Edit agents, skills, or files under `src/dot_claude/claude/` in this repo.
2. After changing Python in `src/`, run [Ruff](https://docs.astral.sh/ruff/):
   ```bash
   uv run ruff format src/
   uv run ruff check src/
   ```
3. Run tests: `uv run pytest`
4. Test CLI locally: `uv run dot-claude add/update/remove/list`

## External skills (`skills-lock.json`)

`skills-lock.json` is maintained by `npx skills` (the skills CLI) to track externally sourced skills installed from GitHub (e.g. `obra/superpowers`). It records each skill's source repo, type, and content hash so the CLI can detect updates.

- **Not checked in** — the file is gitignored since it varies per machine.
- **Do not edit manually** — use `npx skills` to add, update, or remove external skills.

## User-facing docs

Deployment commands, options, and requirements are in **README.md** (user manual).
