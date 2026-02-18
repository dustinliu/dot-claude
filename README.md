# dot-claude

## Project Overview

`dot-claude` is a repository for maintaining and documenting Claude Code configurations and guidance files. It serves as a centralized source for:

- **Agents** — role-specific prompts (e.g. code-explorer, code-architect, code-reviewer)
- **Skills** — reusable task instructions and templates (e.g. git-commit)
- **CLAUDE.md** — workspace rules and conventions under `claude/.claude/`

The `claude/` tree is deployed via GNU Stow so that `~/.claude/` is linked to this repo.

## Directory Structure

```
.
├── claude/                           # Deployed via Stow → ~/.claude
│   └── .claude/
│       ├── CLAUDE.md                 # Workspace rules for Claude Code
│       ├── agents/                   # code-explorer, code-architect, code-reviewer, etc.
│       └── skills/                   # e.g. git-commit/
├── .editorconfig
├── .gitignore
├── .python-version
├── CLAUDE.md                         # Root workspace rules (references README)
├── LICENSE
├── README.md
├── pyproject.toml                    # Python deps (e.g. PyYAML for skill tooling)
└── uv.lock
```

## Deployment

This project uses **GNU Stow** to deploy the `claude/` package into your home directory. Running Stow creates a symlink so that `~/.claude` points at this repo’s `claude/.claude/` (the package name `claude` becomes the link name under `$HOME`).

### GNU Stow usage

```bash
# Deploy: link ~/.claude → <repo>/claude/.claude
stow -t $HOME claude
```

