# dot-claude

Development guide for the dot-claude CLI tool. For installation, usage, and configuration, see [README.md](README.md).

## Rules (**MUST follow — no exceptions**)

Read these rules FIRST. Every task MUST comply with ALL rules below. Do NOT skip or defer any of them.

1. All instruction content MUST be written in English; user-facing communication preferences are defined in the user's global CLAUDE.md.
2. README.md is the user manual (installation, usage, commands, configuration, artifact format). CLAUDE.md is for development only (architecture, code structure, testing, contribution rules). User-facing documentation MUST NOT be placed in CLAUDE.md; development-only content MUST NOT be placed in README.md.
3. After any change that affects project structure, files, deployment, or rules, you MUST update this CLAUDE.md to reflect the current state. If the change affects user-facing behavior (commands, flags, configuration, artifact format, scopes), you MUST also update README.md. A task is NOT complete until all affected documentation is accurate.
4. Follow TDD (Test-Driven Development) — do NOT skip any step of the red-green-refactor cycle:
   - **Red**: write a failing test first, run it to confirm it fails.
   - **Green**: write the minimum production code to make the test pass, run it to confirm it passes.
   - **Refactor**: clean up while keeping all tests green.
   Do NOT write production code without a corresponding test.

## Repository Structure

```
my-skills/             # Custom skills (artifact source)
my-agents/             # Custom agents (artifact source)
src/dot_claude/        # CLI tool source code
  cli.py               # Click CLI entry point and subcommands
  config.py            # XDG paths, TOML config parsing, init
  repos.py             # Git clone/pull, artifact scanning
  deploy.py            # Symlink creation/removal, install status
tests/                 # Test suite (pytest)
  test_cli.py          # CLI command tests (CliRunner, end-to-end)
  test_config.py       # Config parsing and init tests
  test_repos.py        # Repo clone/pull/scan tests
  test_deploy.py       # Symlink creation/removal/status tests
```

## Architecture

### Module Responsibilities

| Module | Role |
|---|---|
| `cli.py` | Click command definitions, user-facing I/O, argument parsing. Delegates all logic to other modules. |
| `config.py` | XDG path resolution, TOML config loading/validation, `RepoEntry` dataclass, config file generation. |
| `repos.py` | Git clone/pull operations, artifact discovery (`Artifact` dataclass). Skills = subdirectories, agents = `.md` files. |
| `deploy.py` | Symlink creation/removal, install status detection. Enforces safety (no overwrite, symlink-only removal). |

### Data Flow

```
CLI command
  → config.py: load_config() → list[RepoEntry]
  → repos.py:  update_repos() / scan_artifacts() → list[Artifact]
  → deploy.py: create_symlink() / remove_symlink() / detect_install_status()
```

### Key Design Decisions

- **Symlinks over copies**: artifacts are symlinked so that `update` (git pull) immediately propagates changes without re-deploying.
- **XDG compliance**: config and cache directories follow the XDG Base Directory Specification.
- **No implicit side effects**: `add` refuses to overwrite existing paths; `remove` refuses to delete non-symlink files.

## Testing

```bash
uv run pytest              # Run all tests
uv run pytest -x           # Stop on first failure
uv run pytest tests/test_cli.py  # Run a specific module
```

### Test File Mapping

| Test file | Source file |
|---|---|
| `test_cli.py` | `src/dot_claude/cli.py` |
| `test_config.py` | `src/dot_claude/config.py` |
| `test_repos.py` | `src/dot_claude/repos.py` |
| `test_deploy.py` | `src/dot_claude/deploy.py` |

### Test Conventions

- **CLI tests**: use `click.testing.CliRunner` to invoke commands.
- **Isolation**: use `tmp_path` for filesystem, `monkeypatch.setenv` for XDG overrides, and `unittest.mock.patch` for subprocess/external calls.
- **Fixture `mock_env`**: creates an isolated XDG environment with a pre-configured repo and cached artifacts for end-to-end CLI tests.
