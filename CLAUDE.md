# dot-claude

Personal Claude Code configuration — custom CLAUDE.md, skills, and agents, with a CLI tool to manage artifacts across multiple repos.

## Repository Structure

```
my-claude/CLAUDE.md    # Global CLAUDE.md (symlinked to ~/.claude/CLAUDE.md)
my-skills/             # Custom skills (artifact source)
my-agents/             # Custom agents (artifact source)
src/dot_claude/        # CLI tool source code
  cli.py               # Click CLI entry point and subcommands
  config.py            # XDG paths, TOML config parsing, init
  repos.py             # Git clone/pull, artifact scanning
  deploy.py            # Symlink creation/removal, install status
tests/                 # Test suite (pytest)
```

## CLI Tool (dot-claude)

Manages Claude Code skills and agents artifacts from multiple git repos via symlinks.

### Setup
```bash
uvx dot-claude init     # Create config at $XDG_CONFIG_HOME/dot-claude/dot-claude.toml
# Edit config to add repos, then:
uvx dot-claude update   # Clone/pull all configured repos
```

### Commands
```bash
uvx dot-claude add <name> [-g]   # Symlink artifact (-g = user scope, default = project scope)
uvx dot-claude remove <name> [-g] # Remove symlink
uvx dot-claude list [-g]          # List all available artifacts with install status
uvx dot-claude update              # Clone new / pull existing repos
```

### Config ($XDG_CONFIG_HOME/dot-claude/dot-claude.toml)
```toml
[[repos]]
name = "dot-claude"
url = "https://github.com/user/dot-claude.git"
skills = "my-skills"  # optional, default: "skills"
agents = "my-agents"  # optional, default: "agents"

[[repos]]
name = "external-skills"
url = "https://github.com/user/external-skills.git"
```

## Deployment

Artifacts are deployed by the CLI tool via symlinks:
- User scope: `~/.claude/skills/*`, `~/.claude/agents/*`
- Project scope: `./.claude/skills/*`, `./.claude/agents/*`
- `my-claude/CLAUDE.md` -> `~/.claude/CLAUDE.md` (manual symlink)

## Rules (MUST follow — no exceptions)
- All instruction content MUST be written in English; user-facing communication preferences are defined in CLAUDE.md
- After any change that affects project structure, files, deployment, or rules, you MUST update this CLAUDE.md to reflect the current state. A task is NOT complete until this file is accurate.
