## ADDED Requirements

### Requirement: Manifest Write

After a successful deploy, the tool SHALL write a manifest file (`.deploy-manifest.json`) to the target directory recording all file paths that were deployed.

#### Scenario: Manifest created on deploy

- **WHEN** deploy completes successfully
- **THEN** a `.deploy-manifest.json` file is written to the target directory containing a JSON object with a `files` array of all deployed relative file paths

#### Scenario: Manifest is overwritten on subsequent deploy

- **WHEN** a manifest already exists in the target directory
- **THEN** it is replaced with a new manifest reflecting the current deploy

#### Scenario: Manifest not written on dry-run

- **WHEN** `--dry-run` is specified
- **THEN** no manifest file is written or modified

### Requirement: Manifest-based Cleanup

After copying, the tool SHALL remove files from the target that were recorded in the previous manifest but are not in the current source. This ensures stale files from prior deploys are automatically cleaned up without touching files managed by other tools.

#### Scenario: Remove stale file from prior deploy

- **WHEN** the previous manifest lists `skills/old-skill/SKILL.md` but the current source does not contain it
- **THEN** `skills/old-skill/SKILL.md` is deleted from the target

#### Scenario: Remove empty directories after cleanup

- **WHEN** cleanup removes all files from a directory that was created by a prior deploy
- **THEN** the empty directory is also removed

#### Scenario: Preserve files not in manifest

- **WHEN** the target contains files that are not listed in the previous manifest (e.g. external skills, user settings)
- **THEN** those files are left untouched

#### Scenario: No manifest exists (first deploy)

- **WHEN** no `.deploy-manifest.json` exists in the target directory
- **THEN** no cleanup is performed; only copy and manifest creation occur

#### Scenario: Dry-run shows cleanup actions

- **WHEN** `--dry-run` is specified and stale files exist
- **THEN** files that would be deleted are printed as `delete <rel_path>` with no filesystem changes

## MODIFIED Requirements

### Requirement: Deploy (Copy)

The tool SHALL copy all source files into the target directory using merge semantics. Existing files are overwritten. Parent directories are created as needed.

#### Scenario: Fresh deploy

- **WHEN** the target `.claude/` directory does not exist
- **THEN** the directory is created and all source files are copied into it preserving relative paths

#### Scenario: Merge into existing target

- **WHEN** the target already contains files not in the source
- **THEN** source files are copied (overwriting matching paths) and pre-existing non-source files are left untouched

#### Scenario: Overwrite existing file

- **WHEN** a source file already exists at the target path
- **THEN** the target file is overwritten with the source file

#### Scenario: Parent directory creation

- **WHEN** a source file is nested (e.g. `agents/foo/AGENT.md`) and intermediate directories do not exist in the target
- **THEN** all necessary parent directories are created

### Requirement: Conflict Detection

The tool SHALL detect type conflicts where a source file maps to an existing directory in the target (or vice versa). When a conflict is detected, the tool MUST abort with an error. Non-existent target paths are not conflicts.

#### Scenario: No conflicts

- **WHEN** all source paths either do not exist in the target or have the same type (file vs directory)
- **THEN** deployment proceeds normally

#### Scenario: File-vs-directory conflict

- **WHEN** a source path is a file but the corresponding target path is a directory
- **THEN** the tool prints the conflicting path to stderr and exits with code 1

#### Scenario: Directory-vs-file conflict

- **WHEN** a source path is a directory but the corresponding target path is a file
- **THEN** the tool prints the conflicting path to stderr and exits with code 1

### Requirement: Dry Run

When `--dry-run` is specified, the tool SHALL print what would be done without modifying the filesystem. This MUST apply to both copy and cleanup operations.

#### Scenario: Dry-run deploy

- **WHEN** `--dry-run` is specified for a deploy operation
- **THEN** each file that would be copied is printed as `copy <rel_path>` and no files are written

#### Scenario: Dry-run cleanup

- **WHEN** `--dry-run` is specified and stale files from a previous manifest would be removed
- **THEN** files that would be deleted are printed as `delete <rel_path>`, with no filesystem changes

### Requirement: CLI Interface

The tool SHALL be invoked via `uv run deploy` (mapped in `pyproject.toml`). It MUST accept `--target` and `--dry-run` flags. The target MAY also be set via the `DOT_CLAUDE_HOME` environment variable.

#### Scenario: Default invocation

- **WHEN** the tool is invoked with no flags
- **THEN** it deploys the source tree to `$HOME/.claude/`, cleans up stale files from prior deploys, and prints "Deployed to <path>"

#### Scenario: Help flag

- **WHEN** `--help` or `-h` is provided
- **THEN** usage information is displayed and the tool exits without performing any operation

#### Scenario: Success message

- **WHEN** a non-dry-run deploy completes successfully
- **THEN** the tool prints "Deployed to <dest>" where `<dest>` is the resolved `.claude/` path

## REMOVED Requirements

### Requirement: Conflict Resolution
**Reason**: The `--force` flag allowed overwriting type conflicts. Type conflicts now always abort — they indicate an unexpected state that should be investigated manually.
**Migration**: Remove `--force` from any scripts. Resolve type conflicts manually before deploying.

### Requirement: Sync
**Reason**: Replaced by manifest-based cleanup which runs automatically on every deploy. The old sync used source-directory inference which could delete external files (e.g. skills installed by `npx skills`).
**Migration**: Remove `--sync` from any scripts. Cleanup is now automatic and safe by default.

### Requirement: Undeploy
**Reason**: No practical use case. The real need (removing a deleted skill from target) is handled by manifest-based cleanup automatically.
**Migration**: Remove `--undeploy` from any scripts. To fully remove deployed files, delete them manually from the target directory.
