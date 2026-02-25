# dot-claude (developer)

Development and maintenance repository for Claude Code configurations. This file is for **developers** working in this repo. For installation and usage, see **README.md**.

## ⚠️ Important

**Claude Code should NOT directly read the `claude/` directory in this repo.**

- This repo is the **source** — develop and maintain agents, skills, and rules here.
- Run `uv run deploy` to copy the `claude/` tree to `~/.claude/`.
- Claude Code reads from `~/.claude/` or `./.claude/`(the deployed location).

Changes only take effect after deployment.

## Directory structure

```
.
├── claude/                           # Deployed → ~/.claude
│   ├── CLAUDE.md                     # Workspace rules for Claude Code
│   ├── agents/                       # claude code subagents
│   └── skills/                       # claude code skills
├── scripts/
│   └── deploy.py                     # Deploy/undeploy script
├── .editorconfig
├── .gitignore
├── .python-version
├── CLAUDE.md                         # This file (repo dev rules)
├── LICENSE
├── README.md                         # User manual
├── pyproject.toml                    # Python deps, uv run deploy
├── skills-lock.json                  # Tracks external skills (gitignored)
└── uv.lock
```

## Development workflow

1. Edit agents, skills, or files under `claude/` in this repo.
2. Run `uv run deploy` (or `--dry-run`) to test deployment.
3. After changing Python in `scripts/`, run [Ruff](https://docs.astral.sh/ruff/):
   ```bash
   uv run ruff format scripts/
   uv run ruff check scripts/
   ```
4. Run tests: `uv run pytest`
5. Do NOT run deploy immediately after editing — only run `uv run deploy` **after a git commit** has been made.

## External skills (`skills-lock.json`)

`skills-lock.json` is maintained by `npx skills` (the skills CLI) to track externally sourced skills installed from GitHub (e.g. `obra/superpowers`). It records each skill's source repo, type, and content hash so the CLI can detect updates.

- **Not checked in** — the file is gitignored since it varies per machine.
- **Do not edit manually** — use `npx skills` to add, update, or remove external skills.

## User-facing docs

Deployment commands, options, and requirements are in **README.md** (user manual).
