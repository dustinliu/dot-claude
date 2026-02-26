## Why

The CLI has two UX issues that create confusion and friction:
1. The `add`/`remove` success messages display the parent `.claude/` directory instead of the full target path (e.g., `.claude/skills/my-skill`), making it unclear where the artifact was actually installed.
2. Running `add`/`remove` without `-g` silently defaults to project scope. Users who intend to install globally may not realize they need `-g`, and there is no way to explicitly request project scope in a non-interactive context (scripts).

## What Changes

- Fix `add` and `remove` success messages to display the full symlink target path (including `skills/<name>` or `agents/<name>.md` subdirectory).
- Add `-p` / `--project` flag to `add` and `remove` commands for explicit project-scope targeting.
- When neither `-g` nor `-p` is specified on `add` or `remove`, display an interactive TUI prompt (via InquirerPy) letting the user select between project and user scope.
- `list` command is unchanged — it already shows both scopes by default.

## Capabilities

### New Capabilities
- `scope-selection`: Interactive TUI scope selector and explicit `-p` flag for `add` and `remove` commands

### Modified Capabilities
- `artifact-deployment`: Success messages for `add` and `remove` must display the full target path instead of just the scope directory
- `cli-commands`: `add` and `remove` gain `-p` flag and interactive scope selection when no scope flag is provided

## Impact

- **Code**: `cli.py` (flag definitions, scope resolution, message formatting), `deploy.py` (`create_symlink` return value)
- **Tests**: `test_cli.py` (new tests for `-p` flag, TUI prompt, updated message assertions), `test_deploy.py` (updated return type)
- **Dependencies**: No new dependencies (InquirerPy already in use)
- **User-facing**: CLI help text changes; behavior change when running `add`/`remove` without flags (was silent default, now interactive prompt)
