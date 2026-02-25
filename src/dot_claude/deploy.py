"""Artifact deployment: symlink creation, removal, status detection."""

from pathlib import Path

from dot_claude.repos import Artifact


class DeployError(Exception):
    """Raised when deployment operations fail."""


def _target_path(name: str, kind: str, scope_dir: Path) -> Path:
    """Return the target path for an artifact within a scope directory."""
    if kind == "skill":
        return scope_dir / "skills" / name
    return scope_dir / "agents" / f"{name}.md"


def create_symlink(artifact: Artifact, scope_dir: Path) -> None:
    """Create a symlink for an artifact in the target scope directory."""
    target = _target_path(artifact.name, artifact.kind, scope_dir)
    if target.exists() or target.is_symlink():
        raise DeployError(f"'{artifact.name}' is already installed at {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(artifact.source_path)


def remove_symlink(name: str, kind: str, scope_dir: Path) -> None:
    """Remove a symlink for an artifact. Refuses to delete non-symlink files."""
    target = _target_path(name, kind, scope_dir)
    if not target.exists() and not target.is_symlink():
        raise DeployError(f"'{name}' is not installed in {scope_dir}")
    if not target.is_symlink():
        raise DeployError(f"'{name}' at {target} is not a managed symlink")
    target.unlink()


def detect_install_status(
    name: str, kind: str, user_dir: Path, project_dir: Path | None = None
) -> str | None:
    """Check if an artifact is installed and return the scope ('user', 'project', or None)."""
    user_target = _target_path(name, kind, user_dir)
    if user_target.is_symlink() and user_target.exists():
        return "user"

    if project_dir is not None:
        project_target = _target_path(name, kind, project_dir)
        if project_target.is_symlink() and project_target.exists():
            return "project"

    return None
