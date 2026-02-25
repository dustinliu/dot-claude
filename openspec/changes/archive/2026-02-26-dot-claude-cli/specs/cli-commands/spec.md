## ADDED Requirements

### Requirement: CLI entry point
The system SHALL provide a CLI executable named `dot-claude` that can be invoked via `uvx dot-claude`.

#### Scenario: Invoke without subcommand
- **WHEN** user runs `dot-claude` with no arguments
- **THEN** system displays help text listing all available subcommands

### Requirement: init subcommand
The system SHALL provide an `init` subcommand that creates the config directory and generates a config file with commented examples.

#### Scenario: First-time init
- **WHEN** user runs `dot-claude init` and no config exists
- **THEN** system creates `$XDG_CONFIG_HOME/dot-claude/dot-claude.toml` with commented example content explaining the `[[repos]]` format

#### Scenario: Init when config already exists
- **WHEN** user runs `dot-claude init` and config file already exists
- **THEN** system informs user that config already exists and does not overwrite it

### Requirement: add subcommand
The system SHALL provide an `add <name>` subcommand that symlinks an artifact to the target scope.

#### Scenario: Add artifact to project scope
- **WHEN** user runs `dot-claude add <name>` without `-g` flag
- **THEN** system creates a symlink from the artifact source to `./.claude/skills/<name>` or `./.claude/agents/<name>`

#### Scenario: Add artifact to user scope
- **WHEN** user runs `dot-claude add -g <name>`
- **THEN** system creates a symlink from the artifact source to `~/.claude/skills/<name>` or `~/.claude/agents/<name>`

#### Scenario: Add artifact with name conflict
- **WHEN** user runs `dot-claude add <name>` and multiple repos provide an artifact with that name
- **THEN** system presents an interactive list selector showing repo names and waits for user to choose one

#### Scenario: Add unknown artifact
- **WHEN** user runs `dot-claude add <name>` and no repo provides an artifact with that name
- **THEN** system displays an error message indicating the artifact was not found

### Requirement: remove subcommand
The system SHALL provide a `remove <name>` subcommand that removes the symlink for an artifact.

#### Scenario: Remove artifact from project scope
- **WHEN** user runs `dot-claude remove <name>` without `-g` flag
- **THEN** system removes the symlink at `./.claude/skills/<name>` or `./.claude/agents/<name>`

#### Scenario: Remove artifact from user scope
- **WHEN** user runs `dot-claude remove -g <name>`
- **THEN** system removes the symlink at `~/.claude/skills/<name>` or `~/.claude/agents/<name>`

#### Scenario: Remove artifact that is not installed
- **WHEN** user runs `dot-claude remove <name>` and no symlink exists for that artifact in the target scope
- **THEN** system displays an error message indicating the artifact is not installed in that scope

### Requirement: list subcommand
The system SHALL provide a `list` subcommand that displays all available artifacts from all configured repos.

#### Scenario: List all artifacts
- **WHEN** user runs `dot-claude list`
- **THEN** system displays all available artifacts grouped by type (Skills, Agents) with columns for artifact name, source repo name, and install status (`[user]`, `[project]`, or `-`), with columns vertically aligned

#### Scenario: List with -g filter
- **WHEN** user runs `dot-claude list -g`
- **THEN** system displays all available artifacts but only shows user-scope install status

### Requirement: update subcommand
The system SHALL provide an `update` subcommand that clones or pulls all configured repos.

#### Scenario: First update for a repo
- **WHEN** user runs `dot-claude update` and a configured repo has not been cloned yet
- **THEN** system clones the repo to `$XDG_CACHE_HOME/dot-claude/<repo-name>/`

#### Scenario: Subsequent update
- **WHEN** user runs `dot-claude update` and a configured repo already exists in cache
- **THEN** system runs `git pull` in the cached repo directory

### Requirement: Global flag
The `-g` flag SHALL be available on `add`, `remove`, and `list` subcommands to target user scope (`~/.claude/`) instead of project scope (`./.claude/`).

#### Scenario: Flag consistency
- **WHEN** user passes `-g` to `add`, `remove`, or `list`
- **THEN** the command operates on `~/.claude/` instead of `./.claude/`
