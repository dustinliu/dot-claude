# dot-claude

## Project Overview

`dot-claude` is a repository for maintaining and documenting Claude Code configurations and guidance files. It serves as a centralized source for:

- **Agents** — role-specific prompts (e.g. code-explorer, code-architect, code-reviewer)
- **Skills** — reusable task instructions and templates (e.g. git-commit)
- **CLAUDE.md** — workspace rules and conventions under `claude/`

The `claude/` tree is deployed by **copying** to `~/.claude/` via a Python script (Stow-like merge: only paths present in the repo are touched; files like `settings.local.json` in the target are left alone).

## Directory Structure

```
.
├── claude/                           # Deployed via script → ~/.claude
│   ├── CLAUDE.md                     # Workspace rules for Claude Code
│   ├── agents/                       # code-explorer, code-architect, code-reviewer, etc.
│   └── skills/                       # e.g. git-commit/
├── scripts/
│   └── deploy.py                     # Deploy/undeploy script
├── .editorconfig
├── .gitignore
├── .python-version
├── CLAUDE.md                         # Root workspace rules (references README)
├── LICENSE
├── README.md
├── pyproject.toml                    # Python deps and deploy entry point
└── uv.lock
```

## Deployment

Run the deploy script from the repo root. It **copies** the `claude/` tree into `~/.claude/` (merge only: existing files in the target that are not in the repo, e.g. `settings.local.json`, are preserved).

### Commands

```bash
# Deploy to ~/.claude (default)
uv run deploy

# Deploy to a custom directory (DIR/.claude)
uv run deploy --target /path/to/home
# or set DOT_CLAUDE_HOME

# Preview changes without writing
uv run deploy --dry-run

# After copy, remove from target any path that no longer exists in the repo (sync)
uv run deploy --sync

# Remove only repo-managed paths from the target (keeps e.g. settings.local.json)
uv run deploy --undeploy
```

If the target has a **file** where the repo has a **directory** (or the reverse), the script reports a conflict and exits unless you pass `--force`.

## Development

After changing Python code, run [Ruff](https://docs.astral.sh/ruff/) (format first, then check):

```bash
uv run ruff format scripts/
uv run ruff check scripts/
```

