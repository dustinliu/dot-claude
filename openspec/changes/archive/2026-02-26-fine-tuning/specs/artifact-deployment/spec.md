## MODIFIED Requirements

### Requirement: Symlink skills to target scope
The system SHALL create symlinks for skill artifacts from the cached repo to the target scope directory and return the full target path.

#### Scenario: Deploy skill to user scope
- **WHEN** user adds a skill with `-g` flag
- **THEN** system creates a symlink `~/.claude/skills/<name>` → `$XDG_CACHE_HOME/dot-claude/<repo>/<skills-dir>/<name>/` and returns the full target path `~/.claude/skills/<name>`

#### Scenario: Deploy skill to project scope
- **WHEN** user adds a skill with `-p` flag or selects project scope from the TUI prompt
- **THEN** system creates a symlink `./.claude/skills/<name>` → `$XDG_CACHE_HOME/dot-claude/<repo>/<skills-dir>/<name>/` and returns the full target path `./.claude/skills/<name>`

### Requirement: Symlink agents to target scope
The system SHALL create symlinks for agent artifacts from the cached repo to the target scope directory and return the full target path.

#### Scenario: Deploy agent to user scope
- **WHEN** user adds an agent with `-g` flag
- **THEN** system creates a symlink `~/.claude/agents/<name>.md` → `$XDG_CACHE_HOME/dot-claude/<repo>/<agents-dir>/<name>.md` and returns the full target path `~/.claude/agents/<name>.md`

#### Scenario: Deploy agent to project scope
- **WHEN** user adds an agent with `-p` flag or selects project scope from the TUI prompt
- **THEN** system creates a symlink `./.claude/agents/<name>.md` → `$XDG_CACHE_HOME/dot-claude/<repo>/<agents-dir>/<name>.md` and returns the full target path `./.claude/agents/<name>.md`

### Requirement: Remove symlinks
The system SHALL remove symlinks when the `remove` command is used and return the full target path that was removed.

#### Scenario: Remove existing symlink
- **WHEN** user removes an artifact that is installed as a symlink
- **THEN** system deletes the symlink (not the source file) and returns the full target path that was removed

#### Scenario: Remove non-symlink file
- **WHEN** user removes an artifact but the target path is a regular file (not a symlink)
- **THEN** system displays a warning that the file is not a managed symlink and does not delete it

### Requirement: Display full target path in success messages
The system SHALL display the full symlink target path (including the `skills/` or `agents/` subdirectory) in success messages for `add` and `remove` commands.

#### Scenario: Add skill success message
- **WHEN** user successfully adds a skill named `my-skill` to project scope
- **THEN** system displays "Symlinked my-skill to ./.claude/skills/my-skill" (not "./.claude/")

#### Scenario: Add agent success message
- **WHEN** user successfully adds an agent named `my-agent` to user scope
- **THEN** system displays "Symlinked my-agent to ~/.claude/agents/my-agent.md" (not "~/.claude/")

#### Scenario: Remove success message
- **WHEN** user successfully removes an artifact named `my-skill` from project scope
- **THEN** system displays "Removed my-skill from ./.claude/skills/my-skill" (not "./.claude/")
