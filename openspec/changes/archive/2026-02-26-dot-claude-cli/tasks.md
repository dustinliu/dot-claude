## 1. Project Setup

- [x] 1.1 Initialize uv Python project with `pyproject.toml` (package name: `dot-claude`, entry point: `dot-claude`)
- [x] 1.2 Add dependencies: `click`, `InquirerPy`
- [x] 1.3 Create source module structure: `src/dot_claude/`

## 2. Config Management

- [x] 2.1 Implement XDG path resolution (`$XDG_CONFIG_HOME/dot-claude/`, `$XDG_CACHE_HOME/dot-claude/`) with fallbacks
- [x] 2.2 Implement TOML config parsing with `tomllib` (validate required fields: `name`, `url`)
- [x] 2.3 Implement `init` subcommand: create config directory and generate commented example config

## 3. Repo Management

- [x] 3.1 Implement repo clone logic (`git clone` to XDG cache directory)
- [x] 3.2 Implement repo pull logic (`git pull` on existing cached repos)
- [x] 3.3 Implement `update` subcommand: clone new repos, pull existing repos, report errors per-repo
- [x] 3.4 Implement artifact scanning: discover skills (subdirectories) and agents (`.md` files) from each repo

## 4. Artifact Deployment

- [x] 4.1 Implement symlink creation for skills (directory symlinks) and agents (file symlinks)
- [x] 4.2 Implement target directory creation (`~/.claude/skills/`, `./.claude/skills/`, etc.)
- [x] 4.3 Implement symlink removal with safety check (only remove symlinks, warn on regular files)
- [x] 4.4 Implement install status detection (check symlinks in both user and project scope, detect broken symlinks)

## 5. CLI Commands

- [x] 5.1 Implement `add <name> [-g]` subcommand with scope handling
- [x] 5.2 Implement TUI repo selector for name conflicts (InquirerPy list prompt)
- [x] 5.3 Implement `remove <name> [-g]` subcommand
- [x] 5.4 Implement `list [-g]` subcommand with aligned column output (artifact name, repo name, install status)

## 6. CLI Entry Point

- [x] 6.1 Wire up click group with all subcommands (`init`, `update`, `add`, `remove`, `list`)
- [x] 6.2 Configure `pyproject.toml` entry point for `uvx` execution
- [x] 6.3 Verify end-to-end: `uvx dot-claude init`, `update`, `add`, `list`, `remove`
