## 1. Rewrite Spec

- [x] 1.1 Replace `openspec/specs/deployment/spec.md` with the new intent-driven spec (apply delta from change artifacts)

## 2. Remove Legacy Features

- [x] 2.1 Remove `--sync` flag and related argument parsing
- [x] 2.2 Remove `--undeploy` flag, argument parsing, and `do_undeploy` function
- [x] 2.3 Remove `--force` flag, argument parsing, and force-overwrite logic in conflict handling
- [x] 2.4 Remove symlink detection and removal logic from `do_copy`

## 3. Manifest Support

- [x] 3.1 Write tests for manifest read/write (TDD: create before implementation)
- [x] 3.2 Implement manifest write — after successful deploy, write `.deploy-manifest.json` to target with list of deployed file paths
- [x] 3.3 Implement manifest read — load previous manifest from target if it exists
- [x] 3.4 Skip manifest write on `--dry-run`

## 4. Manifest-based Cleanup

- [x] 4.1 Write tests for cleanup logic (TDD: stale file removal, preserve unmanaged, empty dir removal, first deploy)
- [x] 4.2 Implement cleanup — diff previous manifest against current source, delete stale files
- [x] 4.3 Implement empty directory removal after cleanup
- [x] 4.4 Skip cleanup when no previous manifest exists (first deploy)
- [x] 4.5 Support `--dry-run` for cleanup actions (print `delete <rel_path>`)

## 5. Simplify Conflict Detection

- [x] 5.1 Update conflict detection to always abort on type conflicts (remove force-overwrite path)
- [x] 5.2 Update tests for new conflict behavior

## 6. Update Existing Tests

- [x] 6.1 Remove tests for `--sync`, `--undeploy`, `--force`, and symlink handling
- [x] 6.2 Update deploy tests to verify manifest is created after deploy
- [x] 6.3 Update dry-run tests to verify manifest is NOT created
- [x] 6.4 Add integration test: deploy, remove a file from source, deploy again — verify stale file is cleaned up

## 7. Documentation

- [x] 7.1 Update README.md to reflect new CLI surface (remove `--sync`, `--undeploy` references)
- [x] 7.2 Update deploy script docstring
