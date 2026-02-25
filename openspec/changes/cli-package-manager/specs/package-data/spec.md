## ADDED Requirements

### Requirement: Skills and agents bundled as package data

The Python package SHALL include the `claude/` directory contents (skills, agents, CLAUDE.md) as package data, accessible at runtime without a local repo checkout.

#### Scenario: Access skill from installed package

- **WHEN** the CLI is installed via `uv tool install` and runs `dot-claude add`
- **THEN** it can read all skill and agent files from the installed package data

#### Scenario: Package data matches repo content

- **WHEN** the package is installed from a specific git commit
- **THEN** the bundled skills/agents match the content of `claude/` at that commit

### Requirement: Inventory enumeration from package data

The tool SHALL enumerate all available skills and agents from the bundled package data to populate the TUI item list.

#### Scenario: Enumerate skills

- **WHEN** the package data contains `claude/skills/git-commit/SKILL.md` and `claude/skills/leading-change/SKILL.md`
- **THEN** the inventory returns two skills: `git-commit` and `leading-change`

#### Scenario: Enumerate agents

- **WHEN** the package data contains `claude/agents/code-explorer.md` and `claude/agents/code-reviewer.md`
- **THEN** the inventory returns two agents: `code-explorer` and `code-reviewer`

#### Scenario: Enumerate both types

- **WHEN** the inventory is queried
- **THEN** it returns a combined list with type annotations (skill or agent) for each item
