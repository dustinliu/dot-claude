## Context

The `add` and `remove` commands in `cli.py` have two UX issues:

1. **Incorrect success message**: The message uses `scope` (a `.claude/` directory) instead of the full target path. The actual path (e.g., `.claude/skills/my-skill`) is computed inside `deploy.py:_target_path()` but never returned to the caller.

2. **No scope selection**: The `-g` flag is the only scope mechanism. Without it, the command silently defaults to project scope. There is no `-p` flag and no interactive prompt.

Current code flow:
```
cli.add() → _scope_dir(global_flag) → deploy.create_symlink(artifact, scope_dir)
                                        ↳ _target_path() computes full path internally
                                        ↳ returns None
           → click.echo(f"Symlinked {name} to {scope}/")  # BUG: scope, not full path
```

## Goals / Non-Goals

**Goals:**
- Success messages for `add` and `remove` display the full symlink target path
- `add` and `remove` support explicit `-p` / `--project` flag
- When neither `-g` nor `-p` is given, `add` and `remove` show an interactive scope selector
- Mutual exclusivity: `-g` and `-p` cannot be used together

**Non-Goals:**
- Changing `list` command behavior (already shows both scopes)
- Adding scope selection to `update` or `init` commands
- Changing the underlying symlink/deploy mechanics

## Decisions

### Decision 1: Return target path from deploy functions

`create_symlink` will return `Path` (the resolved target) instead of `None`. `remove_symlink` will also return `Path` so that the `remove` command can display the correct path.

**Rationale**: The target path is already computed internally via `_target_path()`. Returning it avoids exposing `_target_path()` as a public API or duplicating the kind-to-subdir mapping in `cli.py`.

**Alternative considered**: Export `_target_path()` as a public function for CLI to call directly. Rejected because it couples the CLI to deployment internals and duplicates the call site.

### Decision 2: Scope resolution with `_resolve_scope()`

Replace the current `_scope_dir(global_flag: bool)` with a new `_resolve_scope(global_flag: bool, project_flag: bool) -> Path` function in `cli.py`:

```
if global_flag and project_flag → ClickException (mutually exclusive)
if global_flag                  → ~/.claude
if project_flag                 → ./.claude
else                            → TUI prompt via InquirerPy
```

**Rationale**: Keeps scope logic in one place. The TUI is triggered only as a fallback when no explicit flag is given, so scripts can still use `-g` or `-p` for non-interactive operation.

### Decision 3: TUI prompt design

Use `inquirer.select()` (already a dependency) with two choices:

```
? Select scope:
> Project (./.claude/)
  User (~/.claude/)
```

Choices display the resolved paths so the user knows exactly where the artifact will go. Project scope is listed first as the default selection.

**Rationale**: Consistent with the existing TUI pattern used for artifact conflict resolution (repo selector). Two choices is simple enough that a select list is better than a raw text prompt.

### Decision 4: Flag definitions on `add` and `remove`

Both commands get:
- `-g` (existing) — user scope
- `-p` / `--project` — project scope

Click does not have built-in mutual exclusion for `is_flag` options. Validation will be done at the start of the command function body.

**Rationale**: Simpler than a Click callback or custom class. The error case (`-g -p` together) is rare and a clear error message is sufficient.

## Risks / Trade-offs

- **Behavior change for no-flag invocation**: Users who previously relied on silent project-scope default will now see a TUI prompt. → Acceptable because the old behavior was confusing and the TUI makes intent explicit. Users who want the old behavior can switch to `-p`.
- **Non-interactive environments**: Scripts piping to `dot-claude add` without flags will now hang on the TUI prompt. → Mitigated by `-p` flag. Could also detect non-TTY stdin and default to project scope, but this is a non-goal for now — prefer explicit flags in scripts.
