"""
Deploy or undeploy the claude/ tree to ~/.claude/ (or a custom target).
Stow-like: merge only, only touch paths that exist in source; support --sync and --undeploy.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

# Repo root: scripts/deploy.py -> repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_TREE = REPO_ROOT / "claude"


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
    force: bool,
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
    if conflicts and not force:
        return conflicts
    return []


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


def do_sync(
    dest: Path,
    source_files: set[Path],
    source_dirs: set[Path],
    dry_run: bool,
) -> None:
    """Remove from dest any path under a source dir that is not in source."""
    # All paths we "own" (files or dirs in source)
    owned = source_files | source_dirs
    # For each source dir D, list dest/D and remove entries not in source
    for d in sorted(source_dirs, key=lambda p: -len(p.parts)):  # deeper first
        dest_d = dest / d
        if not dest_d.is_dir():
            continue
        for entry in list(dest_d.iterdir()):
            if d == Path("."):
                rel = Path(entry.name)
            else:
                rel = d / entry.name
            if rel in owned:
                continue
            # Check if any owned path is under rel (e.g. rel is "skills", we have "skills/git-commit")
            if any(
                len(p.parts) > len(rel.parts) and p.parts[: len(rel.parts)] == rel.parts
                for p in owned
            ):
                continue
            if dry_run:
                print(f"  delete {rel}")
            else:
                if entry.is_file():
                    entry.unlink()
                else:
                    shutil.rmtree(entry)


def do_undeploy(
    dest: Path,
    source_files: set[Path],
    source_dirs: set[Path],
    dry_run: bool,
) -> None:
    """Remove from dest only paths that exist in source (deepest first)."""
    all_paths = list(source_files | source_dirs)
    # Sort by depth descending so we delete files and deep dirs first
    all_paths.sort(key=lambda p: (-len(p.parts), str(p)))
    for rel in all_paths:
        dest_path = dest / rel
        if not dest_path.exists():
            continue
        if dry_run:
            print(f"  delete {rel}")
            continue
        if dest_path.is_file():
            dest_path.unlink()
        else:
            shutil.rmtree(dest_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deploy or undeploy claude/ to ~/.claude/ (copy, Stow-like merge).",
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
    parser.add_argument(
        "--sync",
        action="store_true",
        help="After copy, remove from target any path we own that is no longer in source.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite on conflict (target is file vs source dir or vice versa).",
    )
    parser.add_argument(
        "--undeploy",
        action="store_true",
        help="Remove from target only paths that exist in source; do not copy.",
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

    if args.undeploy:
        if args.dry_run:
            print("Undeploy (dry-run):")
        else:
            print("Undeploy:")
        do_undeploy(dest, source_files, source_dirs, args.dry_run)
        return

    # Deploy path: conflict check -> copy -> optional sync
    conflicts = check_conflicts(dest, source_files, source_dirs, args.force)
    if conflicts:
        print("Conflicts (target type differs from source):", file=sys.stderr)
        for c in conflicts:
            print(f"  {c}", file=sys.stderr)
        if not args.force:
            print("Use --force to overwrite.", file=sys.stderr)
            sys.exit(1)

    if args.dry_run:
        print("Deploy (dry-run):")
        do_copy(SOURCE_TREE, dest, source_files, dry_run=True)
        if args.sync:
            do_sync(dest, source_files, source_dirs, dry_run=True)
        return

    dest.mkdir(parents=True, exist_ok=True)
    do_copy(SOURCE_TREE, dest, source_files, dry_run=False)
    if args.sync:
        do_sync(dest, source_files, source_dirs, dry_run=False)
    print("Deployed to", dest)


if __name__ == "__main__":
    main()
