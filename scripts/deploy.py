"""
Deploy the claude/ tree to ~/.claude/ (or a custom target).
Copies source files using merge semantics and automatically cleans up
stale files from prior deploys using a manifest.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

# Repo root: scripts/deploy.py -> repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_TREE = REPO_ROOT / "claude"

MANIFEST_NAME = ".deploy-manifest.json"


def _target_home(args: argparse.Namespace) -> Path:
    raw = args.target or os.environ.get("DOT_CLAUDE_HOME")
    if raw is None:
        return Path.home()
    p = Path(raw).expanduser().resolve()
    if not p.is_dir():
        raise SystemExit(f"Target directory does not exist: {p}")
    return p


def _dest_dir(args: argparse.Namespace) -> Path:
    return _target_home(args) / ".claude"


def enumerate_source(source: Path) -> tuple[set[Path], set[Path]]:
    """Return (relative_file_paths, relative_dir_paths). Paths are relative to source."""
    files: set[Path] = set()
    dirs: set[Path] = set()
    if not source.is_dir():
        return files, dirs
    for root, dnames, fnames in source.walk():
        root_path = Path(root)
        rel_root = root_path.relative_to(source) if root_path != source else Path(".")
        if rel_root != Path("."):
            dirs.add(rel_root)
        for f in fnames:
            if rel_root == Path("."):
                files.add(Path(f))
            else:
                files.add(rel_root / f)
    return files, dirs


def check_conflicts(
    dest: Path,
    source_files: set[Path],
    source_dirs: set[Path],
) -> list[Path]:
    """Check for file/dir type conflicts. Returns list of conflicting relative paths."""
    conflicts: list[Path] = []
    all_source_paths = source_files | source_dirs
    for rel in all_source_paths:
        dest_path = dest / rel
        if not dest_path.exists():
            continue
        src_is_file = rel in source_files
        dest_is_file = dest_path.is_file()
        if src_is_file != dest_is_file:
            conflicts.append(rel)
    return conflicts


def do_copy(
    source: Path,
    dest: Path,
    source_files: set[Path],
    dry_run: bool,
) -> None:
    """Copy source tree into dest (merge)."""
    for rel in source_files:
        src_path = source / rel
        dest_path = dest / rel
        if dry_run:
            print(f"  copy {rel}")
            continue
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dest_path)


def write_manifest(dest: Path, source_files: set[Path]) -> None:
    """Write manifest recording deployed file paths."""
    manifest_path = dest / MANIFEST_NAME
    data = {"files": sorted(str(p) for p in source_files)}
    manifest_path.write_text(json.dumps(data, indent=2) + "\n")


def read_manifest(dest: Path) -> set[Path]:
    """Read previous manifest. Returns empty set if no manifest exists."""
    manifest_path = dest / MANIFEST_NAME
    if not manifest_path.exists():
        return set()
    data = json.loads(manifest_path.read_text())
    return {Path(f) for f in data.get("files", [])}


def do_cleanup(
    dest: Path,
    previous_files: set[Path],
    current_files: set[Path],
    dry_run: bool,
) -> None:
    """Remove stale files from dest that were in previous manifest but not in current source."""
    stale = previous_files - current_files
    for rel in sorted(stale):
        dest_path = dest / rel
        if not dest_path.exists():
            continue
        if dry_run:
            print(f"  delete {rel}")
            continue
        dest_path.unlink()

    # Remove empty parent directories left behind (deepest first)
    dirs_to_check: set[Path] = set()
    for rel in stale:
        parent = rel.parent
        while parent != Path("."):
            dirs_to_check.add(parent)
            parent = parent.parent

    for d in sorted(dirs_to_check, key=lambda p: -len(p.parts)):
        dest_d = dest / d
        if dest_d.is_dir() and not any(dest_d.iterdir()):
            if not dry_run:
                dest_d.rmdir()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deploy claude/ to ~/.claude/ (copy with merge semantics).",
    )
    parser.add_argument(
        "--target",
        metavar="DIR",
        help="Target home directory (default: $HOME). Dest is DIR/.claude",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print what would be done, do not modify filesystem.",
    )
    args = parser.parse_args()

    if not SOURCE_TREE.is_dir():
        print("Source tree not found:", SOURCE_TREE, file=sys.stderr)
        sys.exit(1)

    try:
        dest = _dest_dir(args)
    except SystemExit as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    source_files, source_dirs = enumerate_source(SOURCE_TREE)
    if not source_files and not source_dirs:
        print("Source tree is empty.", file=sys.stderr)
        sys.exit(1)

    # Conflict check — always abort on type mismatch
    conflicts = check_conflicts(dest, source_files, source_dirs)
    if conflicts:
        print("Conflicts (target type differs from source):", file=sys.stderr)
        for c in conflicts:
            print(f"  {c}", file=sys.stderr)
        sys.exit(1)

    # Read previous manifest for cleanup
    previous_files = read_manifest(dest)

    if args.dry_run:
        print("Deploy (dry-run):")
        do_copy(SOURCE_TREE, dest, source_files, dry_run=True)
        if previous_files:
            do_cleanup(dest, previous_files, source_files, dry_run=True)
        return

    dest.mkdir(parents=True, exist_ok=True)
    do_copy(SOURCE_TREE, dest, source_files, dry_run=False)
    if previous_files:
        do_cleanup(dest, previous_files, source_files, dry_run=False)
    write_manifest(dest, source_files)
    print("Deployed to", dest)


if __name__ == "__main__":
    main()
