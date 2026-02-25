# dot-claude

User manual for Claude Code configurations. Use this repo to install, update, and manage your Claude Code agents and skills.

## What you get

- **Agents** — role-specific prompts (e.g. code-explorer, code-architect, code-reviewer)
- **Skills** — reusable task instructions (e.g. git-commit)
- **Rules** — workspace conventions Claude Code follows

The `claude/` tree in this repo is **deployed** to `~/.claude/`. Claude Code reads from `~/.claude/`, not from this repo. Deploy after cloning or pulling to apply changes.

## Quick start

1. Clone the repo (or ensure it’s up to date).
2. From the repo root, run:
   ```bash
   uv run deploy
   ```
   This copies the `claude/` tree into `~/.claude/` (merge semantics: your existing files there, e.g. `settings.local.json`, are kept). Files removed from the repo are automatically cleaned up from the target on the next deploy.

## Deployment commands

| Command | Description |
|--------|-------------|
| `uv run deploy` | Deploy to `~/.claude` (default home) |
| `uv run deploy --target /path/to/home` | Deploy so that files go to `DIR/.claude` (or set `DOT_CLAUDE_HOME`) |
| `uv run deploy --dry-run` | Show what would be copied/deleted, no writes |

If the target has a **file** where the repo has a **directory** (or the reverse), the script reports a conflict and exits.

## Requirements

- [uv](https://docs.astral.sh/uv/) (Python package runner). The project uses `pyproject.toml` and runs the deploy script via `uv run deploy`.

For development and contributing, see **CLAUDE.md** in this repo.
