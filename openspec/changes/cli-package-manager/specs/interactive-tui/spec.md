## ADDED Requirements

### Requirement: Scope selection step

The TUI SHALL present a single-select prompt asking the user to choose between "User" and "Project" scope as the first step.

#### Scenario: Two scope options displayed

- **WHEN** the scope selection prompt is shown
- **THEN** two options are displayed: "User (~/.claude/)" and "Project (<cwd>/.claude/)" where `<cwd>` is the current working directory

#### Scenario: User selects scope

- **WHEN** the user selects a scope option
- **THEN** the wizard proceeds to the item selection step with the chosen scope

#### Scenario: User cancels scope selection

- **WHEN** the user presses Ctrl+C during scope selection
- **THEN** the wizard exits with no changes made

### Requirement: Item selection step

The TUI SHALL present a multi-select checkbox prompt listing all available skills and agents. Items are grouped by type (Skills, Agents) with visual section headers.

#### Scenario: Items listed with type grouping

- **WHEN** the item selection prompt is shown
- **THEN** all available skills are listed under a "Skills" heading and all available agents under an "Agents" heading

#### Scenario: Previous selections pre-checked

- **WHEN** a manifest exists for the chosen scope with previously selected items
- **THEN** those items are pre-checked in the checkbox list

#### Scenario: No previous selections

- **WHEN** no manifest exists for the chosen scope
- **THEN** all items are unchecked by default

#### Scenario: User confirms selection

- **WHEN** the user confirms their item selection
- **THEN** the wizard proceeds to deploy the selected items

#### Scenario: User cancels item selection

- **WHEN** the user presses Ctrl+C during item selection
- **THEN** the wizard exits with no changes made

### Requirement: Wizard-style sequential flow

The TUI MUST present one question at a time in sequential order: scope first, then items.

#### Scenario: Step order

- **WHEN** the user starts the add wizard
- **THEN** the scope question appears first; only after scope is answered does the item question appear
