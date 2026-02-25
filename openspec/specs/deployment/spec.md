# Deployment

## Purpose

Synchronize the `claude/` source tree to a target `.claude/` directory using merge semantics. The tool copies source files into the target, automatically cleans up stale files from prior deploys using a manifest, and supports dry-run previews. It never touches files it did not deploy.

## Requirements

### Requirement: Source Enumeration

The tool SHALL walk the `claude/` source tree and return all relative file paths and relative directory paths. The root directory itself (`.`) is excluded from the directory set.

#### Scenario: Nested tree

- **WHEN** the source tree contains files in nested subdirectories (e.g. `agents/foo/AGENT.md`, `skills/bar/SKILL.md`)
- **THEN** all files are returned as relative paths and all intermediate directories are included in the directory set

#### Scenario: Flat tree

- **WHEN** the source tree contains only files at the top level (e.g. `CLAUDE.md`)
- **THEN** all files are returned as relative paths and the directory set is empty

#### Scenario: Non-existent source

- **WHEN** the source directory does not exist
- **THEN** both the file set and directory set are empty

### Requirement: Target Resolution

The tool SHALL determine the target `.claude/` directory from CLI `--target`, the `DOT_CLAUDE_HOME` environment variable, or the user's home directory as default.

#### Scenario: Default target

- **WHEN** neither `--target` nor `DOT_CLAUDE_HOME` is set
- **THEN** the target directory is `$HOME/.claude`

#### Scenario: CLI --target flag

- **WHEN** `--target /tmp/test` is provided
- **THEN** the target directory is `/tmp/test/.claude`

#### Scenario: Environment variable

- **WHEN** `DOT_CLAUDE_HOME` is set to `/tmp/env-test` and `--target` is not provided
- **THEN** the target directory is `/tmp/env-test/.claude`

#### Scenario: CLI takes precedence over environment variable

- **WHEN** both `--target /tmp/cli` and `DOT_CLAUDE_HOME=/tmp/env` are set
- **THEN** the target directory is `/tmp/cli/.claude`

#### Scenario: Non-existent target directory

- **WHEN** the resolved target home directory does not exist
- **THEN** the tool exits with an error message indicating the directory does not exist

### Requirement: Pre-flight Validation

The tool MUST validate that the source tree exists and is non-empty before any operation.

#### Scenario: Missing source tree

- **WHEN** the `claude/` source directory does not exist
- **THEN** the tool prints an error to stderr and exits with code 1

#### Scenario: Empty source tree

- **WHEN** the `claude/` source directory exists but contains no files or subdirectories
- **THEN** the tool prints "Source tree is empty." to stderr and exits with code 1

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
