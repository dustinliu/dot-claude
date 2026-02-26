## ADDED Requirements

### Requirement: Interactive scope selection
The system SHALL display an interactive TUI prompt to select scope when neither `-g` nor `-p` flag is provided on `add` or `remove` commands.

#### Scenario: No scope flag provided
- **WHEN** user runs `dot-claude add <name>` or `dot-claude remove <name>` without `-g` or `-p`
- **THEN** system displays an InquirerPy select prompt with choices "Project (./.claude/)" and "User (~/.claude/)"

#### Scenario: User selects project scope from prompt
- **WHEN** scope prompt is displayed and user selects "Project"
- **THEN** system operates on `./.claude/` directory

#### Scenario: User selects user scope from prompt
- **WHEN** scope prompt is displayed and user selects "User"
- **THEN** system operates on `~/.claude/` directory

### Requirement: Explicit project scope flag
The system SHALL accept `-p` / `--project` flag on `add` and `remove` commands to explicitly target project scope.

#### Scenario: Add with -p flag
- **WHEN** user runs `dot-claude add -p <name>`
- **THEN** system creates a symlink in `./.claude/` without prompting

#### Scenario: Remove with -p flag
- **WHEN** user runs `dot-claude remove -p <name>`
- **THEN** system removes the symlink from `./.claude/` without prompting

### Requirement: Mutual exclusivity of scope flags
The system SHALL reject commands where both `-g` and `-p` flags are provided.

#### Scenario: Both flags provided
- **WHEN** user runs `dot-claude add -g -p <name>` or `dot-claude remove -g -p <name>`
- **THEN** system displays an error message indicating the flags are mutually exclusive and does not proceed
