# dot-claude

Development and maintenance repository for Claude Code configurations.

## ⚠️ Important

**Claude Code should NOT directly read the `claude/` directory in this repo.**

Instead:
1. This repo is the **source** — develop and maintain agents, skills here
2. Run `uv run deploy` to copy the `claude/` tree to `~/.claude/`
3. Claude Code reads from `~/.claude/` (the deployed location)

Changes only take effect after deployment.

See @README.md for full project overview, directory structure, and deployment details.

