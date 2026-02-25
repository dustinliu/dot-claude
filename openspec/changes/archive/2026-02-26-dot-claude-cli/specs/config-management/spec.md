## ADDED Requirements

### Requirement: XDG-compliant config location
The system SHALL store its config file at `$XDG_CONFIG_HOME/dot-claude/dot-claude.toml`.

#### Scenario: XDG_CONFIG_HOME set
- **WHEN** `$XDG_CONFIG_HOME` is set
- **THEN** system uses `$XDG_CONFIG_HOME/dot-claude/dot-claude.toml`

#### Scenario: XDG_CONFIG_HOME not set
- **WHEN** `$XDG_CONFIG_HOME` is not set
- **THEN** system falls back to `~/.config/dot-claude/dot-claude.toml`

### Requirement: Init generates commented example config
The `init` command SHALL generate a config file with commented examples that explain the format.

#### Scenario: Generated config content
- **WHEN** `init` is run and no config exists
- **THEN** the generated file contains commented TOML examples showing `[[repos]]` entries with `name`, `url`, `skills`, and `agents` fields

### Requirement: Parse TOML config
The system SHALL parse `dot-claude.toml` using Python's `tomllib` (stdlib).

#### Scenario: Valid config
- **WHEN** config contains valid `[[repos]]` entries with `name` and `url`
- **THEN** system loads all repo definitions

#### Scenario: Missing config file
- **WHEN** any command (except `init`) is run and no config file exists
- **THEN** system displays an error suggesting to run `dot-claude init` first

#### Scenario: Invalid TOML
- **WHEN** config file contains invalid TOML syntax
- **THEN** system displays a parse error with details

### Requirement: Repo entry fields
Each `[[repos]]` entry SHALL support the following fields:
- `name` (required): identifier for the repo
- `url` (required): git clone URL
- `skills` (optional, default: `"skills"`): directory name containing skills
- `agents` (optional, default: `"agents"`): directory name containing agents

#### Scenario: Minimal repo entry
- **WHEN** config contains `[[repos]]` with only `name` and `url`
- **THEN** system uses `"skills"` and `"agents"` as default directory names

#### Scenario: Custom directory names
- **WHEN** config contains `skills = "my-skills"` in a repo entry
- **THEN** system scans `my-skills/` instead of `skills/` for that repo

#### Scenario: Missing required field
- **WHEN** a `[[repos]]` entry is missing `name` or `url`
- **THEN** system displays a validation error identifying the incomplete entry
