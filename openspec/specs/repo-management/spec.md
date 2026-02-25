## Requirements

### Requirement: Clone repos to XDG cache
The system SHALL clone configured repos to `$XDG_CACHE_HOME/dot-claude/<repo-name>/`.

#### Scenario: Clone new repo
- **WHEN** `update` is run and a repo URL is configured but not yet cloned
- **THEN** system runs `git clone <url>` into `$XDG_CACHE_HOME/dot-claude/<repo-name>/`

#### Scenario: XDG_CACHE_HOME not set
- **WHEN** `$XDG_CACHE_HOME` environment variable is not set
- **THEN** system falls back to `~/.cache/dot-claude/`

### Requirement: Pull existing repos
The system SHALL pull the latest changes for repos that are already cloned.

#### Scenario: Pull existing repo
- **WHEN** `update` is run and a repo already exists in cache
- **THEN** system runs `git pull` in the cached repo directory

#### Scenario: Pull fails
- **WHEN** `git pull` fails for a repo (network error, merge conflict, etc.)
- **THEN** system displays the error and continues updating remaining repos

### Requirement: Scan repos for artifacts
The system SHALL scan each repo for available skills and agents based on directory structure.

#### Scenario: Scan with default directories
- **WHEN** a repo config has no `skills` or `agents` override
- **THEN** system scans `skills/` for skill directories and `agents/` for agent files

#### Scenario: Scan with custom directories
- **WHEN** a repo config specifies `skills = "my-skills"` and/or `agents = "my-agents"`
- **THEN** system scans the specified directories instead of the defaults

#### Scenario: Identify skills
- **WHEN** scanning a skills directory
- **THEN** each subdirectory is treated as a skill artifact (named by directory name)

#### Scenario: Identify agents
- **WHEN** scanning an agents directory
- **THEN** each `.md` file is treated as an agent artifact (named by filename without extension)

#### Scenario: Missing directories
- **WHEN** a repo does not have the expected skills or agents directory
- **THEN** system skips that directory silently (a repo may provide only skills, only agents, or both)
