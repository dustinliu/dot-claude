## Context

The deploy tool (`scripts/deploy.py`) copies the `claude/` source tree to `~/.claude/` so Claude Code can read it. The target directory is a shared space — it contains both repo-managed files and user/external files (e.g. `settings.local.json`, skills installed via `npx skills`).

The current implementation carries legacy features from a GNU Stow migration (symlink removal) and offers granular flags (`--sync`, `--undeploy`, `--force`) that add complexity without matching real usage patterns.

## Goals / Non-Goals

**Goals:**
- Deploy always produces a target that reflects the current source state (copy + cleanup)
- Only clean up files that THIS tool previously deployed (manifest-based tracking)
- Never touch files managed by other tools or the user
- Minimal CLI surface: `--target`, `--dry-run`, `DOT_CLAUDE_HOME`

**Non-Goals:**
- Multi-source deployment (multiple repos deploying to same target)
- Undeploy as a standalone operation
- Stow compatibility or symlink management
- Conflict auto-resolution (type mismatches are errors)

## Decisions

### Decision 1: Manifest-based cleanup instead of source-directory inference

**Choice**: Track deployed files in a `.deploy-manifest.json` at the target.

**Why not source-directory inference** (the old `--sync` approach): It treats everything under source-managed directories (e.g. `skills/`) as "ours", which would delete external skills installed by `npx skills` into the same directory.

**Why manifest**: A manifest records exactly which files we placed. On next deploy, we compare: files in the old manifest but not in the current source get deleted. Files we never placed are never touched.

**Trade-off**: Adds a state file. First deploy without a manifest just copies and creates the manifest — no cleanup on first run.

### Decision 2: Sync is always on, no opt-in flag

**Choice**: Every deploy automatically cleans up stale files.

**Rationale**: The only reason `--sync` was opt-in was caution. With manifest-based tracking, cleanup is safe by default — we only remove what we previously placed. No reason to make the user remember to pass a flag.

### Decision 3: Type conflicts are hard errors

**Choice**: If source has a file where target has a directory (or vice versa), abort with an error. No `--force` to override.

**Rationale**: This situation should not occur in normal usage. If it does, it signals something unexpected that the user should investigate manually rather than having the tool silently resolve.

### Decision 4: Drop symlink handling

**Choice**: Remove all symlink detection and removal logic.

**Rationale**: This was a migration path from GNU Stow. The migration is complete — no longer needed.

### Decision 5: Drop --undeploy

**Choice**: Remove the undeploy operation entirely.

**Rationale**: The real need was "I removed a skill from source, make it disappear from target" — which manifest-based sync handles automatically. A full undeploy (remove everything we deployed) has no practical use case.

## Risks / Trade-offs

- **[First deploy has no cleanup]** → Acceptable. First deploy just copies and writes manifest. Subsequent deploys have full cleanup. Users migrating from the old tool may have stale files after the first run — they can delete manually or run deploy twice (first creates manifest, second cleans based on it).
- **[Manifest corruption or deletion]** → Tool treats it as first deploy (copy only, write new manifest). No data loss, just one cycle without cleanup.
- **[Breaking CLI change]** → Users with scripts using `--sync`, `--undeploy`, or `--force` will get errors. Acceptable given the small user base.
