## MODIFIED Requirements

### Requirement: add subcommand
The system SHALL provide an `add <name>` subcommand that symlinks an artifact to the target scope, with scope determined by flags or interactive prompt.

#### Scenario: Add artifact with -g flag
- **WHEN** user runs `dot-claude add -g <name>`
- **THEN** system creates a symlink from the artifact source to `~/.claude/skills/<name>` or `~/.claude/agents/<name>.md`

#### Scenario: Add artifact with -p flag
- **WHEN** user runs `dot-claude add -p <name>`
- **THEN** system creates a symlink from the artifact source to `./.claude/skills/<name>` or `./.claude/agents/<name>.md`

#### Scenario: Add artifact without scope flag
- **WHEN** user runs `dot-claude add <name>` without `-g` or `-p`
- **THEN** system displays an interactive scope selector and creates the symlink in the selected scope

#### Scenario: Add artifact with conflicting flags
- **WHEN** user runs `dot-claude add -g -p <name>`
- **THEN** system displays an error that `-g` and `-p` are mutually exclusive

#### Scenario: Add artifact with name conflict
- **WHEN** user runs `dot-claude add <name>` and multiple repos provide an artifact with that name
- **THEN** system presents an interactive list selector showing repo names and waits for user to choose one

#### Scenario: Add unknown artifact
- **WHEN** user runs `dot-claude add <name>` and no repo provides an artifact with that name
- **THEN** system displays an error message indicating the artifact was not found

### Requirement: remove subcommand
The system SHALL provide a `remove <name>` subcommand that removes the symlink for an artifact, with scope determined by flags or interactive prompt.

#### Scenario: Remove artifact with -g flag
- **WHEN** user runs `dot-claude remove -g <name>`
- **THEN** system removes the symlink at `~/.claude/skills/<name>` or `~/.claude/agents/<name>.md`

#### Scenario: Remove artifact with -p flag
- **WHEN** user runs `dot-claude remove -p <name>`
- **THEN** system removes the symlink at `./.claude/skills/<name>` or `./.claude/agents/<name>.md`

#### Scenario: Remove artifact without scope flag
- **WHEN** user runs `dot-claude remove <name>` without `-g` or `-p`
- **THEN** system displays an interactive scope selector and removes the symlink from the selected scope

#### Scenario: Remove artifact with conflicting flags
- **WHEN** user runs `dot-claude remove -g -p <name>`
- **THEN** system displays an error that `-g` and `-p` are mutually exclusive

#### Scenario: Remove artifact that is not installed
- **WHEN** user runs `dot-claude remove <name>` and no symlink exists for that artifact in the target scope
- **THEN** system displays an error message indicating the artifact is not installed in that scope

### Requirement: Global flag
The `-g` flag SHALL be available on `add`, `remove`, and `list` subcommands to target user scope (`~/.claude/`) instead of project scope (`./.claude/`).

#### Scenario: Flag consistency
- **WHEN** user passes `-g` to `add`, `remove`, or `list`
- **THEN** the command operates on `~/.claude/` instead of `./.claude/`
