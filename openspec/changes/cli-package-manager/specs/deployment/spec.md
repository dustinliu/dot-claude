## MODIFIED Requirements

### Requirement: CLI Interface

The tool SHALL be invokable as `dot-claude` with subcommands `add`, `update`, `remove`, `list`. The old `uv run deploy` entry point is removed.

#### Scenario: Default invocation

- **WHEN** the tool is invoked as `dot-claude` with no subcommand
- **THEN** it displays usage help listing available subcommands

#### Scenario: Help flag

- **WHEN** `--help` or `-h` is provided
- **THEN** usage information is displayed and the tool exits without performing any operation

### Requirement: Target Resolution

The tool SHALL determine the target `.claude/` directory based on scope selection: user scope resolves to `~/.claude/`, project scope resolves to `$(pwd)/.claude/`.

#### Scenario: User scope target

- **WHEN** user scope is selected
- **THEN** the target directory is `$HOME/.claude`

#### Scenario: Project scope target

- **WHEN** project scope is selected and cwd is `/Users/dustinl/src/my-app`
- **THEN** the target directory is `/Users/dustinl/src/my-app/.claude`

### Requirement: Deploy (Copy)

The tool SHALL copy selected items (not the entire source tree) into the target directory using merge semantics. Existing files are overwritten. Parent directories are created as needed.

#### Scenario: Selective deploy

- **WHEN** the user selects `git-commit` and `code-explorer`
- **THEN** only `skills/git-commit/SKILL.md` and `agents/code-explorer.md` are copied to the target

#### Scenario: Overwrite existing file

- **WHEN** a selected item already exists at the target path
- **THEN** the target file is overwritten with the source content

#### Scenario: Parent directory creation

- **WHEN** a selected skill requires `skills/git-commit/` and the directory does not exist in the target
- **THEN** the directory is created before copying

### Requirement: Manifest-based Cleanup

After copying, the tool SHALL remove files from the target that were in the previous manifest but are no longer selected. This ensures deselected items are cleaned up.

#### Scenario: Remove deselected item

- **WHEN** the previous manifest lists `skills/old-skill/SKILL.md` but the user does not select `old-skill`
- **THEN** `skills/old-skill/SKILL.md` is deleted from the target

#### Scenario: Remove empty directories after cleanup

- **WHEN** cleanup removes all files from a directory
- **THEN** the empty directory is also removed

#### Scenario: Preserve files not in manifest

- **WHEN** the target contains files that are not listed in the previous manifest (e.g. external skills, user settings)
- **THEN** those files are left untouched

### Requirement: Manifest Write

After a successful deploy, the tool SHALL write a `.deploy-manifest.json` to the target directory recording scope, selected items, and deployed file paths.

#### Scenario: Manifest with new schema

- **WHEN** deploy completes successfully
- **THEN** `.deploy-manifest.json` contains `scope`, `items`, and `files` fields

## REMOVED Requirements

### Requirement: Source Enumeration

**Reason**: Replaced by inventory enumeration from package data. The tool no longer walks a local `claude/` source tree.
**Migration**: Use `inventory.py` to enumerate skills/agents from package data.

### Requirement: Pre-flight Validation

**Reason**: No longer applicable. The source is bundled package data, not a local directory that might be missing.
**Migration**: Package data availability is guaranteed by the Python packaging system.

### Requirement: Conflict Detection

**Reason**: Selective deployment eliminates the class of file-vs-directory conflicts. Items are well-structured (skills in subdirs, agents as files).
**Migration**: None needed.

### Requirement: Dry Run

**Reason**: The interactive TUI makes dry-run less necessary — users see and confirm their selections before deployment. Can be re-added later if needed.
**Migration**: None needed.
