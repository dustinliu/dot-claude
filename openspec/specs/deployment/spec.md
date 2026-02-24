# Deployment

## Purpose

Deploy or undeploy the `claude/` source tree to a target `.claude/` directory using Stow-like merge semantics. The tool copies source files into the target, optionally syncs stale files, and supports undeployment — all with dry-run previews and conflict detection.

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

The tool SHALL detect type conflicts where a source file maps to an existing directory in the target (or vice versa). Non-existent target paths are not conflicts.

#### Scenario: No conflicts

- **WHEN** all source paths either do not exist in the target or have the same type (file vs directory)
- **THEN** an empty conflict list is returned

#### Scenario: File-vs-directory conflict

- **WHEN** a source path is a file but the corresponding target path is a directory
- **THEN** that path is included in the conflict list

#### Scenario: Directory-vs-file conflict

- **WHEN** a source path is a directory but the corresponding target path is a file
- **THEN** that path is included in the conflict list

#### Scenario: Non-existent target path

- **WHEN** a source path does not exist in the target at all
- **THEN** that path is not a conflict

### Requirement: Conflict Resolution

The tool SHALL either abort or force overwrite when conflicts are detected, based on the `--force` flag.

#### Scenario: Abort without --force

- **WHEN** conflicts exist and `--force` is not set
- **THEN** the tool prints the conflicting paths to stderr, advises using `--force`, and exits with code 1

#### Scenario: Overwrite with --force

- **WHEN** conflicts exist and `--force` is set
- **THEN** the tool prints the conflicting paths to stderr, prints a warning that it is overwriting, and proceeds with deployment

### Requirement: Deploy (Copy)

The tool SHALL copy all source files into the target directory using merge semantics. Existing files are overwritten. Parent directories are created as needed. Symlinks in the destination path MUST be removed before copying.

#### Scenario: Fresh deploy

- **WHEN** the target `.claude/` directory does not exist
- **THEN** the directory is created and all source files are copied into it preserving relative paths

#### Scenario: Merge into existing target

- **WHEN** the target already contains files not in the source
- **THEN** source files are copied (overwriting matching paths) and pre-existing non-source files are left untouched

#### Scenario: Overwrite existing file

- **WHEN** a source file already exists at the target path
- **THEN** the target file is overwritten with the source file, preserving metadata via `copy2`

#### Scenario: Symlink removal

- **WHEN** a symlink exists along the destination path (e.g. a leftover Stow symlink)
- **THEN** the symlink is removed before creating directories or copying the file

#### Scenario: Parent directory creation

- **WHEN** a source file is nested (e.g. `agents/foo/AGENT.md`) and intermediate directories do not exist in the target
- **THEN** all necessary parent directories are created

### Requirement: Sync

After copying, the tool SHALL remove files and directories from the target that are within source-managed directories but no longer present in the source. Directories MUST be processed depth-first. Paths that are ancestors of owned paths MUST be preserved.

#### Scenario: Remove stale file

- **WHEN** the target contains a file inside a source-managed directory that is not in the current source file set
- **THEN** that file is deleted

#### Scenario: Preserve files outside source directories

- **WHEN** the target contains files in directories that are not managed by the source
- **THEN** those files are left untouched

#### Scenario: Preserve ancestor directories

- **WHEN** a target directory is not in the source set but contains descendants that are in the source set
- **THEN** that directory is preserved

#### Scenario: Depth-first processing

- **WHEN** sync processes source directories
- **THEN** deeper directories are processed before shallower ones

#### Scenario: Remove stale directory

- **WHEN** the target contains a directory inside a source-managed directory that is not in the source set and has no owned descendants
- **THEN** that entire directory tree is removed

#### Scenario: No sync without --sync flag

- **WHEN** `--sync` is not provided
- **THEN** no stale files or directories are removed from the target

### Requirement: Undeploy

The tool SHALL remove from the target only the paths that exist in the source. Paths MUST be processed depth-first (deepest first). The tool MUST NOT copy anything during undeploy.

#### Scenario: Remove deployed files

- **WHEN** undeploy runs and source files exist in the target
- **THEN** those files are deleted from the target

#### Scenario: Remove deployed directories

- **WHEN** undeploy runs and source directories exist in the target with no non-source content
- **THEN** those directories are removed via `rmtree`

#### Scenario: Skip missing paths

- **WHEN** a source path does not exist in the target
- **THEN** that path is silently skipped

#### Scenario: Depth-first removal

- **WHEN** undeploy processes paths
- **THEN** deeper paths are removed before shallower ones

#### Scenario: No copy on undeploy

- **WHEN** `--undeploy` is specified
- **THEN** no files are copied — only removal is performed

#### Scenario: Preserve non-source paths

- **WHEN** the target contains files or directories not in the source
- **THEN** those paths are left untouched during undeploy

### Requirement: Dry Run

When `--dry-run` is specified, the tool SHALL print what would be done without modifying the filesystem. This MUST apply to deploy, sync, and undeploy operations.

#### Scenario: Dry-run deploy

- **WHEN** `--dry-run` is specified for a deploy operation
- **THEN** each file that would be copied is printed as `copy <rel_path>` and no files are written

#### Scenario: Dry-run deploy with sync

- **WHEN** `--dry-run` and `--sync` are both specified
- **THEN** files that would be copied are printed as `copy <rel_path>` and files that would be deleted are printed as `delete <rel_path>`, with no filesystem changes

#### Scenario: Dry-run undeploy

- **WHEN** `--dry-run` and `--undeploy` are both specified
- **THEN** each path that would be removed is printed as `delete <rel_path>` and no files are removed

### Requirement: CLI Interface

The tool SHALL be invoked via `uv run deploy` (mapped in `pyproject.toml`). It MUST accept `--target`, `--dry-run`, `--sync`, `--force`, and `--undeploy` flags.

#### Scenario: Default invocation

- **WHEN** the tool is invoked with no flags
- **THEN** it deploys the source tree to `$HOME/.claude/` and prints "Deployed to <path>"

#### Scenario: Help flag

- **WHEN** `--help` or `-h` is provided
- **THEN** usage information is displayed and the tool exits without performing any operation

#### Scenario: Success message

- **WHEN** a non-dry-run deploy completes successfully
- **THEN** the tool prints "Deployed to <dest>" where `<dest>` is the resolved `.claude/` path
