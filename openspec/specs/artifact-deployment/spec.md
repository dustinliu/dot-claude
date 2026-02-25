## Requirements

### Requirement: Symlink skills to target scope
The system SHALL create symlinks for skill artifacts from the cached repo to the target scope directory.

#### Scenario: Deploy skill to user scope
- **WHEN** user adds a skill with `-g` flag
- **THEN** system creates a symlink `~/.claude/skills/<name>` → `$XDG_CACHE_HOME/dot-claude/<repo>/<skills-dir>/<name>/`

#### Scenario: Deploy skill to project scope
- **WHEN** user adds a skill without `-g` flag
- **THEN** system creates a symlink `./.claude/skills/<name>` → `$XDG_CACHE_HOME/dot-claude/<repo>/<skills-dir>/<name>/`

### Requirement: Symlink agents to target scope
The system SHALL create symlinks for agent artifacts from the cached repo to the target scope directory.

#### Scenario: Deploy agent to user scope
- **WHEN** user adds an agent with `-g` flag
- **THEN** system creates a symlink `~/.claude/agents/<name>.md` → `$XDG_CACHE_HOME/dot-claude/<repo>/<agents-dir>/<name>.md`

#### Scenario: Deploy agent to project scope
- **WHEN** user adds an agent without `-g` flag
- **THEN** system creates a symlink `./.claude/agents/<name>.md` → `$XDG_CACHE_HOME/dot-claude/<repo>/<agents-dir>/<name>.md`

### Requirement: Create target directories
The system SHALL create target scope directories if they do not exist.

#### Scenario: Target directory missing
- **WHEN** user adds an artifact and `~/.claude/skills/` (or agents, or project scope equivalent) does not exist
- **THEN** system creates the directory before creating the symlink

### Requirement: Prevent overwrite of existing symlinks
The system SHALL not overwrite an existing symlink or file without user awareness.

#### Scenario: Artifact already installed
- **WHEN** user adds an artifact and a symlink or file already exists at the target path
- **THEN** system displays an error indicating the artifact is already installed

### Requirement: Remove symlinks
The system SHALL remove symlinks when the `remove` command is used.

#### Scenario: Remove existing symlink
- **WHEN** user removes an artifact that is installed as a symlink
- **THEN** system deletes the symlink (not the source file)

#### Scenario: Remove non-symlink file
- **WHEN** user removes an artifact but the target path is a regular file (not a symlink)
- **THEN** system displays a warning that the file is not a managed symlink and does not delete it

### Requirement: Detect install status
The system SHALL detect whether an artifact is installed and in which scope.

#### Scenario: Check user scope
- **WHEN** listing artifacts
- **THEN** system checks `~/.claude/skills/<name>` and `~/.claude/agents/<name>.md` for existing symlinks

#### Scenario: Check project scope
- **WHEN** listing artifacts (without `-g`)
- **THEN** system checks `./.claude/skills/<name>` and `./.claude/agents/<name>.md` for existing symlinks

#### Scenario: Broken symlink detection
- **WHEN** a symlink exists but its target no longer exists
- **THEN** system treats the artifact as not installed (broken symlink)
