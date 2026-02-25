# dot-claude

CLI tool for managing Claude Code skills and agents artifacts from multiple git repos via symlinks.

## What It Does

dot-claude lets you maintain a curated collection of Claude Code skills and agents across multiple git repositories, and install them into any project (or globally) with a single command. It clones your configured repos, discovers artifacts automatically, and deploys them as symlinks — keeping everything up to date with a simple `update`.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- git

## Getting Started

```bash
# 1. Create the config file
uvx dot-claude init

# 2. Edit the config to add your artifact repos
#    (see Configuration section below)

# 3. Clone all configured repos
uvx dot-claude update

# 4. See what's available
uvx dot-claude list

# 5. Install an artifact into the current project
uvx dot-claude add my-skill
```

## Commands

| Command | Description | Flags |
|---|---|---|
| `dot-claude init` | Create config directory and generate example config | — |
| `dot-claude update` | Clone new repos or pull latest changes for existing ones | — |
| `dot-claude list` | List all available artifacts with install status | `-g` show user scope only |
| `dot-claude add <name>` | Install an artifact by creating a symlink | `-g` install to user scope |
| `dot-claude remove <name>` | Remove an installed artifact symlink | `-g` remove from user scope |

## Configuration

Config file location: `$XDG_CONFIG_HOME/dot-claude/dot-claude.toml` (defaults to `~/.config/dot-claude/dot-claude.toml`).

```toml
[[repos]]
name = "my-artifacts"
url = "https://github.com/user/my-artifacts.git"
skills = "my-skills"  # optional, default: "skills"
agents = "my-agents"  # optional, default: "agents"

[[repos]]
name = "external-skills"
url = "https://github.com/user/external-skills.git"
```

### `[[repos]]` fields

| Field | Required | Default | Description |
|---|---|---|---|
| `name` | yes | — | Unique identifier for the repo (used as cache directory name) |
| `url` | yes | — | Git clone URL |
| `skills` | no | `"skills"` | Subdirectory in the repo containing skill artifacts |
| `agents` | no | `"agents"` | Subdirectory in the repo containing agent artifacts |

## Artifact Format

### Skills

A skill is a **subdirectory** inside the repo's skills directory. The directory name becomes the artifact name.

```
my-repo/
  skills/
    code-review/       # artifact name: "code-review"
      SKILL.md
      ...
    refactor/          # artifact name: "refactor"
      SKILL.md
      ...
```

Hidden directories (starting with `.`) are ignored.

### Agents

An agent is a **`.md` file** inside the repo's agents directory. The filename (without extension) becomes the artifact name.

```
my-repo/
  agents/
    architect.md       # artifact name: "architect"
    reviewer.md        # artifact name: "reviewer"
```

Hidden files (starting with `.`) are ignored.

## Scopes

Artifacts can be installed at two scopes:

| Scope | Flag | Target directory | Effect |
|---|---|---|---|
| **Project** (default) | — | `./.claude/skills/` or `./.claude/agents/` | Available only in the current project |
| **User** | `-g` | `~/.claude/skills/` or `~/.claude/agents/` | Available in all projects |

## How It Works

- **Repos are cached** under `$XDG_CACHE_HOME/dot-claude/` (defaults to `~/.cache/dot-claude/`). `update` runs `git clone` for new repos and `git pull` for existing ones.
- **Artifacts are deployed as symlinks** pointing from the target scope directory back to the cached repo. This means updates to the source repo (via `update`) are reflected immediately.
- **Safety**: `add` refuses to overwrite an existing file or symlink at the target path. `remove` refuses to delete anything that is not a managed symlink, preventing accidental deletion of manually created files.
- **Name conflicts**: if the same artifact name exists in multiple repos, `add` will prompt you to select which repo to use.

## License

[Apache License 2.0](LICENSE)
