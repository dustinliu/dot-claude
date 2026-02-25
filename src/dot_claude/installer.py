"""Install and remove skills/agents to target directories."""

from __future__ import annotations

import shutil
from importlib.resources.abc import Traversable
from pathlib import Path

from dot_claude.inventory import list_items
from dot_claude.manifest import Manifest, delete_manifest, read_manifest, write_manifest


def install(
    data_root: Traversable,
    dest: Path,
    selected_items: list[str],
    scope: str,
) -> None:
    """Install selected items to the destination directory.

    Args:
        data_root: Root of the claude data directory (package data or filesystem path).
        dest: Target directory (e.g., ~/.claude/ or ./claude/).
        selected_items: List of item keys to install (e.g., ["skills/git-commit", "agents/code-explorer"]).
        scope: "user" or "project".
    """
    dest.mkdir(parents=True, exist_ok=True)

    # Read previous manifest for cleanup
    prev_manifest = read_manifest(dest)
    prev_files = prev_manifest.files if prev_manifest else set()

    # Determine files to deploy
    items = list_items(data_root)
    items_by_key = {item.key: item for item in items}

    current_files: set[Path] = set()
    for key in selected_items:
        item = items_by_key.get(key)
        if item is None:
            continue
        for rel_path in item.files:
            current_files.add(rel_path)

    # Auto-deploy CLAUDE.md for user scope
    if scope == "user":
        claude_md = data_root / "CLAUDE.md"
        if claude_md.is_file():
            current_files.add(Path("CLAUDE.md"))

    # Copy files
    for rel_path in current_files:
        src_path = data_root / str(rel_path)
        dest_path = dest / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        _copy_traversable(src_path, dest_path)

    # Cleanup deselected items
    stale_files = prev_files - current_files
    if stale_files:
        remove_files(dest, stale_files)

    # Write or remove manifest
    if selected_items:
        manifest = Manifest(scope=scope, items=list(selected_items), files=current_files)
        write_manifest(dest, manifest)
    else:
        delete_manifest(dest)


def remove_files(dest: Path, files: set[Path]) -> None:
    """Remove files from dest and clean up empty parent directories."""
    for rel in files:
        dest_path = dest / rel
        if dest_path.exists():
            dest_path.unlink()

    # Remove empty parent directories (deepest first)
    dirs_to_check: set[Path] = set()
    for rel in files:
        parent = rel.parent
        while parent != Path("."):
            dirs_to_check.add(parent)
            parent = parent.parent

    for d in sorted(dirs_to_check, key=lambda p: -len(p.parts)):
        dest_d = dest / d
        if dest_d.is_dir() and not any(dest_d.iterdir()):
            dest_d.rmdir()


def _copy_traversable(src: Traversable, dest_path: Path) -> None:
    """Copy a Traversable (package data or Path) to a filesystem path."""
    if isinstance(src, Path):
        shutil.copy2(src, dest_path)
    else:
        dest_path.write_text(src.read_text())
