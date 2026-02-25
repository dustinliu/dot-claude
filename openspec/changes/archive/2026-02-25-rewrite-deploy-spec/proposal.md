## Why

The current deployment spec was auto-generated from existing code, making it a behavior description rather than a true specification. It documents implementation details (symlink handling, Stow compatibility) that are no longer relevant, and misses the core intent of the tool. A rewrite is needed to define what the deploy tool SHOULD do — capturing design decisions, dropping legacy baggage, and introducing manifest-based sync.

## What Changes

- **Rewrite `openspec/specs/deployment/spec.md`** from scratch as an intent-driven spec
- **Drop legacy features**: `--sync` flag (sync becomes default), `--undeploy`, `--force`, symlink removal
- **Add manifest-based sync**: deploy records what it placed in a `.deploy-manifest.json` at the target; subsequent deploys use this to remove stale files without touching unmanaged files
- **Simplify CLI**: only `--target`, `--dry-run`, and `DOT_CLAUDE_HOME` env var remain
- **BREAKING**: `--sync`, `--undeploy`, and `--force` flags removed

## Capabilities

### New Capabilities

### Modified Capabilities
- `deployment`: Rewrite spec to be intent-driven. Drop legacy features (symlink handling, --sync flag, --undeploy, --force). Add manifest-based sync as default behavior. Simplify CLI surface.

## Impact

- `scripts/deploy.py`: Implementation will need to change to match the new spec (remove symlink logic, add manifest, remove flags)
- `openspec/specs/deployment/spec.md`: Complete rewrite
- CLI interface: Breaking change — `--sync`, `--undeploy`, `--force` flags removed
- Users who rely on `--undeploy` or `--sync` will need to adjust workflows
