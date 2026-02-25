## ADDED Requirements

### Requirement: Project scope target resolution

When project scope is selected, the tool SHALL deploy to `$(pwd)/.claude/`.

#### Scenario: Deploy to cwd

- **WHEN** the user selects project scope and cwd is `/Users/dustinl/src/my-app`
- **THEN** items are deployed to `/Users/dustinl/src/my-app/.claude/`

#### Scenario: Create .claude directory if missing

- **WHEN** project scope is selected and `$(pwd)/.claude/` does not exist
- **THEN** the `.claude/` directory is created before deploying items

### Requirement: CLAUDE.md exclusion from project scope

The tool SHALL NOT deploy `CLAUDE.md` when deploying to project scope.

#### Scenario: CLAUDE.md excluded

- **WHEN** the user deploys items to project scope
- **THEN** `CLAUDE.md` is not included in the deployed files, regardless of item selection

### Requirement: User scope target resolution

When user scope is selected, the tool SHALL deploy to `~/.claude/`.

#### Scenario: Deploy to home

- **WHEN** the user selects user scope
- **THEN** items are deployed to `~/.claude/`

### Requirement: CLAUDE.md auto-deploy for user scope

The tool SHALL automatically deploy `CLAUDE.md` when deploying to user scope, without requiring user selection.

#### Scenario: CLAUDE.md auto-included

- **WHEN** the user deploys any items to user scope
- **THEN** `CLAUDE.md` is automatically copied to `~/.claude/CLAUDE.md` in addition to selected items
