## ADDED Requirements

### Requirement: CLI entry point

The tool SHALL be invokable as `dot-claude` after installation via `uv tool install`. The entry point MUST be defined in `pyproject.toml`.

#### Scenario: Invoke after install

- **WHEN** the user runs `uv tool install git+https://github.com/dustinl/dot-claude` and then runs `dot-claude`
- **THEN** the CLI displays usage help with available subcommands

### Requirement: Add subcommand

The `dot-claude add` subcommand SHALL launch an interactive TUI wizard that guides the user through scope selection and item picking, then installs the selected items to the chosen scope.

#### Scenario: Add with interactive selection

- **WHEN** the user runs `dot-claude add`
- **THEN** the TUI wizard starts with scope selection, followed by item selection, then deploys selected items to the chosen scope

#### Scenario: Add to user scope

- **WHEN** the user selects "User" scope and picks `git-commit` and `code-explorer`
- **THEN** `skills/git-commit/SKILL.md` and `agents/code-explorer.md` are copied to `~/.claude/` and `CLAUDE.md` is auto-deployed

#### Scenario: Add to project scope

- **WHEN** the user selects "Project" scope and picks `git-commit`
- **THEN** `skills/git-commit/SKILL.md` is copied to `$(pwd)/.claude/` and `CLAUDE.md` is NOT deployed

### Requirement: Update subcommand

The `dot-claude update` subcommand SHALL upgrade the CLI package itself via uv, then re-deploy all previously installed items for every scope that has a manifest.

#### Scenario: Update with changes available

- **WHEN** the user runs `dot-claude update` and the GitHub repo has newer content
- **THEN** the CLI package is upgraded and all manifested items are re-deployed with the new content

#### Scenario: Update with no changes

- **WHEN** the user runs `dot-claude update` and the installed version is already latest
- **THEN** `uv tool upgrade` reports no changes, but all manifested items are still re-deployed and the tool prints the count of updated items (e.g., "Updated N item(s)."). If no manifests exist, the tool prints "Nothing to update."

### Requirement: Remove subcommand

The `dot-claude remove` subcommand SHALL remove previously installed items from a given scope. It MUST update the manifest after removal.

#### Scenario: Remove a skill

- **WHEN** the user runs `dot-claude remove` and deselects `git-commit` from user scope
- **THEN** `skills/git-commit/SKILL.md` is deleted from `~/.claude/`, empty parent directories are cleaned up, and the manifest is updated

#### Scenario: Remove last item from project scope

- **WHEN** the user removes the last installed item from project scope
- **THEN** all deployed files are removed, the manifest is removed, and empty directories are cleaned up

### Requirement: List subcommand

The `dot-claude list` subcommand SHALL display all installed items grouped by scope.

#### Scenario: List with items in both scopes

- **WHEN** the user runs `dot-claude list` and items are installed in both user and project scope
- **THEN** output shows items grouped under "User (~/.claude/)" and "Project (cwd/.claude/)" headings

#### Scenario: List with no items installed

- **WHEN** the user runs `dot-claude list` and no manifests exist
- **THEN** the tool prints a message indicating nothing is installed
