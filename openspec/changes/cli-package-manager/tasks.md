## 1. Project Restructure & Package Setup

- [x] 1.1 Create `src/dot_claude/` package directory with `__init__.py`
- [x] 1.2 Move `claude/` content into package data location and configure `pyproject.toml` for package data bundling
- [x] 1.3 Update `pyproject.toml`: change entry point from `deploy` to `dot-claude`, add `click` and `questionary` dependencies
- [x] 1.4 Write test: verify package data is accessible via `importlib.resources` (skills and agents are readable)

## 2. Inventory (enumerate available items from package data)

- [x] 2.1 Write tests for `inventory.py`: enumerate skills, enumerate agents, return combined list with type annotations
- [x] 2.2 Implement `inventory.py`: read package data, list skills (directories under `claude/skills/` containing `SKILL.md`) and agents (`.md` files under `claude/agents/`)

## 3. Manifest (read/write/query)

- [x] 3.1 Write tests for `manifest.py`: write new-format manifest, read new-format manifest, read legacy manifest (files-only), handle missing manifest
- [x] 3.2 Implement `manifest.py`: read/write `.deploy-manifest.json` with `scope`, `items`, and `files` fields; legacy compat for old format

## 4. Installer (copy/cleanup mechanics)

- [x] 4.1 Write tests for `installer.py`: selective copy (only chosen items), overwrite existing files, create parent dirs, cleanup deselected items, remove empty dirs, preserve non-manifest files
- [x] 4.2 Implement `installer.py`: selective copy from package data to target, manifest-based cleanup of deselected items, CLAUDE.md auto-deploy for user scope only

## 5. TUI (interactive wizard)

- [x] 5.1 Write tests for `tui.py`: scope selection returns chosen scope, item selection returns checked items, pre-check from manifest, cancellation handling
- [x] 5.2 Implement `tui.py`: scope select prompt (User / Project with cwd path), item checkbox prompt with Skills/Agents grouping, pre-check from manifest data

## 6. CLI Entry Point (click subcommands)

- [x] 6.1 Write tests for `cli.py add`: integrates TUI → installer → manifest write, CLAUDE.md auto-deploy on user scope, CLAUDE.md excluded on project scope
- [x] 6.2 Implement `cli.py add`: wire TUI scope + item selection → installer copy → manifest write
- [x] 6.3 Write tests for `cli.py remove`: TUI for deselection → remove files → update manifest, cleanup empty dirs
- [x] 6.4 Implement `cli.py remove`: wire TUI → installer cleanup → manifest update
- [x] 6.5 Write tests for `cli.py list`: display items grouped by scope, handle no manifests
- [x] 6.6 Implement `cli.py list`: read manifests from user scope + project scope (cwd), format output
- [x] 6.7 Write tests for `cli.py update`: upgrade package, re-deploy manifested items
- [x] 6.8 Implement `cli.py update`: run `uv tool upgrade dot-claude`, re-read package data, re-deploy all manifested items

## 7. Cleanup & Migration

- [x] 7.1 Remove old `scripts/deploy.py`
- [x] 7.2 Update existing tests: remove old deploy tests, ensure new test suite passes
- [x] 7.3 Update `README.md`: new installation instructions (`uv tool install`), new CLI usage docs
