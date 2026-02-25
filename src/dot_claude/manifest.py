"""Read and write deploy manifests."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

MANIFEST_NAME = ".deploy-manifest.json"


@dataclass
class Manifest:
    scope: str
    items: list[str]
    files: set[Path] | list[Path] = field(default_factory=set)

    def __post_init__(self) -> None:
        if isinstance(self.files, list):
            self.files = set(self.files)


def write_manifest(dest: Path, manifest: Manifest) -> None:
    """Write a manifest to the target directory."""
    manifest_path = dest / MANIFEST_NAME
    data = {
        "scope": manifest.scope,
        "items": sorted(manifest.items),
        "files": sorted(str(p) for p in manifest.files),
    }
    manifest_path.write_text(json.dumps(data, indent=2) + "\n")


def delete_manifest(dest: Path) -> None:
    """Remove the manifest file from the target directory."""
    manifest_path = dest / MANIFEST_NAME
    if manifest_path.exists():
        manifest_path.unlink()


def read_manifest(dest: Path) -> Manifest | None:
    """Read a manifest from the target directory. Returns None if no manifest exists."""
    manifest_path = dest / MANIFEST_NAME
    if not manifest_path.exists():
        return None

    data = json.loads(manifest_path.read_text())
    files = {Path(f) for f in data.get("files", [])}

    if "scope" in data and "items" in data:
        return Manifest(scope=data["scope"], items=data["items"], files=files)

    # Legacy format: only "files" array, no scope or items
    items = _infer_items_from_files(files)
    return Manifest(scope="user", items=items, files=files)


def _infer_items_from_files(files: set[Path]) -> list[str]:
    """Infer item keys from file paths (for legacy manifest compat)."""
    items: set[str] = set()
    for f in files:
        parts = f.parts
        if len(parts) >= 2 and parts[0] == "skills":
            items.add(f"skills/{parts[1]}")
        elif len(parts) >= 2 and parts[0] == "agents":
            items.add(f"agents/{Path(parts[1]).stem}")
        # CLAUDE.md and other top-level files are not items
    return sorted(items)
