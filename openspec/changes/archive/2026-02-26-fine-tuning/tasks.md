## 1. Deploy functions return target path

- [x] 1.1 Change `create_symlink` in `deploy.py` to return `Path` (the resolved target) instead of `None`
- [x] 1.2 Change `remove_symlink` in `deploy.py` to return `Path` (the resolved target) instead of `None`
- [x] 1.3 Update `test_deploy.py` tests to assert the returned path for both `create_symlink` and `remove_symlink`

## 2. Scope resolution

- [x] 2.1 Replace `_scope_dir(global_flag)` with `_resolve_scope(global_flag, project_flag)` in `cli.py` — handle mutual exclusivity error, `-g`, `-p`, and TUI fallback via `inquirer.select()`
- [x] 2.2 Add `-p` / `--project` flag to `add` command
- [x] 2.3 Add `-p` / `--project` flag to `remove` command
- [x] 2.4 Wire `add` command to use `_resolve_scope()` and display full target path from `create_symlink` return value
- [x] 2.5 Wire `remove` command to use `_resolve_scope()` and display full target path from `remove_symlink` return value

## 3. CLI tests

- [x] 3.1 Update existing `add` tests in `test_cli.py` to assert full target path in success message (skills and agents)
- [x] 3.2 Update existing `remove` tests in `test_cli.py` to assert full target path in success message
- [x] 3.3 Add test for `add -p` flag (explicit project scope, no TUI prompt)
- [x] 3.4 Add test for `remove -p` flag (explicit project scope, no TUI prompt)
- [x] 3.5 Add test for `add` without flags (TUI prompt triggers and scope selection works)
- [x] 3.6 Add test for `remove` without flags (TUI prompt triggers and scope selection works)
- [x] 3.7 Add test for `-g -p` mutual exclusivity error on `add`
- [x] 3.8 Add test for `-g -p` mutual exclusivity error on `remove`

## 4. Documentation

- [x] 4.1 Update README.md with `-p` / `--project` flag and scope selection behavior for `add` and `remove`
