## ADDED Requirements

### Requirement: Persist selections in manifest

After a successful deploy, the tool SHALL write a manifest recording the selected items and scope to the target directory as `.deploy-manifest.json`.

#### Scenario: Manifest includes items and scope

- **WHEN** the user deploys `git-commit` and `leading-change` to user scope
- **THEN** `.deploy-manifest.json` in `~/.claude/` contains `"scope": "user"`, `"items": ["skills/git-commit", "skills/leading-change"]`, and `"files"` listing all deployed file paths

#### Scenario: Manifest updated on re-deploy

- **WHEN** the user runs `dot-claude add` again and changes their selection
- **THEN** the manifest is overwritten with the new selections

### Requirement: Restore selections from manifest

When the TUI item selection is shown, the tool SHALL read the existing manifest for the chosen scope and pre-check previously selected items.

#### Scenario: Pre-check from manifest

- **WHEN** a manifest exists with `items: ["skills/git-commit", "agents/code-explorer"]`
- **THEN** those two items are pre-checked in the TUI checkbox list

### Requirement: Cleanup deselected items

When items are deselected compared to the previous manifest, the tool SHALL remove the corresponding files from the target directory.

#### Scenario: Item deselected

- **WHEN** the previous manifest has `skills/git-commit` but the user deselects it
- **THEN** `skills/git-commit/SKILL.md` is deleted from the target and the manifest is updated

#### Scenario: Empty directories cleaned up

- **WHEN** removing a skill leaves its parent directory empty
- **THEN** the empty directory is also removed

### Requirement: Legacy manifest compatibility

The tool SHALL handle manifests from the old deploy system that lack `scope` and `items` fields.

#### Scenario: Old-format manifest

- **WHEN** a manifest contains only a `files` array (no `scope` or `items`)
- **THEN** the tool treats it as user scope and infers items from the file paths
