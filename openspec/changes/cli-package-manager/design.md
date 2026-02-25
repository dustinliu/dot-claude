## Context

Currently `dot-claude` is a local development repo with a `deploy.py` script that copies the entire `claude/` tree to `~/.claude/`. Users must clone the repo and run `uv run deploy` from within it. There is no selective installation, no project-scope support, and no way to use the tools without a local checkout.

The existing deployment spec (`openspec/specs/deployment/spec.md`) defines the core copy/cleanup/manifest mechanics which will be adapted rather than discarded.

## Goals / Non-Goals

**Goals:**
- Replace `deploy.py` with a `dot-claude` CLI tool installable via `uv tool install`
- Support both user scope (`~/.claude/`) and project scope (`$(pwd)/.claude/`)
- Interactive TUI wizard for scope and item selection
- Remember selections per scope in manifest
- Bundle skills/agents as Python package data (no local repo needed at runtime)
- TDD: all new functionality is test-driven

**Non-Goals:**
- Multi-repo support (only `dustinl/dot-claude` as source)
- Publishing to PyPI (install from GitHub is sufficient)
- Skill/agent version pinning or lockfiles
- Project-scope CLAUDE.md deployment
- Backward compatibility with the old `uv run deploy` entry point

## Decisions

### Decision 1: CLI framework — `click`

Use `click` for the CLI framework.

**Why**: click is the de facto standard for Python CLIs. It handles subcommands, argument parsing, help text, and testing (via `CliRunner`) out of the box. Lightweight and well-documented.

**Alternatives considered**:
- `argparse` (stdlib): Verbose for subcommands, no built-in test runner
- `typer`: Built on click, adds type hints magic — unnecessary complexity for this scope

### Decision 2: TUI library — `questionary`

Use `questionary` for interactive prompts (radio select for scope, checkbox for items).

**Why**: Simple API for exactly the prompt types we need (select, checkbox). Built on `prompt_toolkit`. No full-screen TUI overhead.

**Alternatives considered**:
- `rich` + `InquirerPy`: More features than needed, heavier dependency
- `textual`: Full TUI framework, overkill for a 2-step wizard
- Raw `prompt_toolkit`: Too low-level

### Decision 3: Package data via `importlib.resources`

Bundle the `claude/` directory as package data in the Python package. Access at runtime via `importlib.resources`.

**Why**: Standard Python mechanism. `uv tool install` handles packaging automatically. No git clone needed at runtime. Skills/agents version is always consistent with CLI version.

**Configuration in `pyproject.toml`**:
```toml
[tool.hatch.build.targets.wheel]
packages = ["src/dot_claude"]
```

### Decision 4: Manifest schema evolution

Extend `.deploy-manifest.json` to record scope and selected items:

```json
{
  "scope": "user",
  "items": ["skills/git-commit", "skills/leading-change", "agents/code-explorer"],
  "files": ["skills/git-commit/SKILL.md", "skills/leading-change/SKILL.md", "agents/code-explorer.md"]
}
```

- `items`: logical selections (for TUI defaults)
- `files`: actual deployed file paths (for cleanup)
- One manifest per scope per target directory

### Decision 5: Project scope uses cwd

Project scope always deploys to `$(pwd)/.claude/`. No `--target` flag needed for normal use. The CLI detects whether cwd is suitable (has `.git/` or `.claude/` already).

### Decision 6: CLAUDE.md auto-deploy to user scope

When deploying to user scope, `CLAUDE.md` is always included automatically — not shown in the TUI selection. When deploying to project scope, `CLAUDE.md` is excluded entirely.

### Decision 7: Module structure

Restructure from a single `scripts/deploy.py` to a proper Python package:

```
src/dot_claude/
├── __init__.py
├── cli.py            # click CLI entry point (add, update, remove, list)
├── tui.py            # questionary prompts (scope selection, item picking)
├── installer.py      # copy/cleanup/manifest logic (evolved from deploy.py)
├── inventory.py      # enumerate available skills/agents from package data
└── manifest.py       # manifest read/write/query
```

## Risks / Trade-offs

- **[Package data size]** → Minimal risk. Skills/agents are small markdown files. Total size well under 1MB.
- **[importlib.resources API differences]** → Use `importlib.resources.files()` (Python 3.9+). The project already requires Python 3.x via uv.
- **[Breaking change]** → Old `uv run deploy` stops working. Acceptable since this is a personal tool and the migration is a one-time switch. Document in README.
- **[TUI in non-interactive contexts]** → `questionary` falls back gracefully. Can add `--non-interactive` flag later if needed.
- **[Manifest migration]** → Old manifests lack `scope` and `items` fields. The installer should handle legacy manifests gracefully (treat as user-scope, full deploy).
