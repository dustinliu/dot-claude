"""CLI entry point for dot-claude."""

from pathlib import Path

import click
from InquirerPy import inquirer

from dot_claude.config import (
    config_path,
    cache_dir,
    init_config,
    load_config,
    ConfigError,
)
from dot_claude.repos import update_repos, scan_artifacts, Artifact
from dot_claude.deploy import create_symlink, remove_symlink, detect_install_status, DeployError


def _load_all_artifacts() -> list[Artifact]:
    """Load config and scan all repos for artifacts."""
    cfg = config_path()
    repos = load_config(cfg)
    cache = cache_dir()
    artifacts: list[Artifact] = []
    for repo in repos:
        repo_dir = cache / repo.name
        if repo_dir.exists():
            artifacts.extend(scan_artifacts(repo, cache))
    return artifacts


def _resolve_scope(global_flag: bool, project_flag: bool) -> Path:
    """Return the target scope directory based on flags or interactive prompt."""
    if global_flag and project_flag:
        raise click.ClickException("Options -g and -p are mutually exclusive")
    if global_flag:
        return Path.home() / ".claude"
    if project_flag:
        return Path.cwd() / ".claude"
    # No flag — prompt user
    project_path = Path.cwd() / ".claude"
    user_path = Path.home() / ".claude"
    choices = [f"Project ({project_path})", f"User ({user_path})"]
    selected = inquirer.select(message="Select scope:", choices=choices).execute()
    if selected == choices[0]:
        return project_path
    return user_path


@click.group()
def main() -> None:
    """Manage Claude Code skills and agents artifacts."""


@main.command()
def init() -> None:
    """Create config directory and generate example config."""
    cfg = config_path()
    try:
        init_config(cfg)
        click.echo(f"Created {cfg}")
    except ConfigError as e:
        raise click.ClickException(str(e))


@main.command()
def update() -> None:
    """Clone or pull all configured repos."""
    cfg = config_path()
    try:
        repos = load_config(cfg)
    except ConfigError as e:
        raise click.ClickException(str(e))

    cache = cache_dir()
    errors = update_repos(repos, cache)

    if errors:
        for err in errors:
            click.echo(f"Error: {err}", err=True)
    else:
        click.echo("All repos up to date")


@main.command("list")
@click.option("-g", "global_scope", is_flag=True, help="Show user scope only")
def list_cmd(global_scope: bool) -> None:
    """List all available artifacts with install status."""
    try:
        artifacts = _load_all_artifacts()
    except ConfigError as e:
        raise click.ClickException(str(e))

    if not artifacts:
        click.echo("No artifacts found. Run 'dot-claude update' first.")
        return

    user_dir = Path.home() / ".claude"
    project_dir = None if global_scope else Path.cwd() / ".claude"

    skills = [a for a in artifacts if a.kind == "skill"]
    agents = [a for a in artifacts if a.kind == "agent"]

    # Calculate column widths
    all_names = [a.name for a in artifacts]
    all_repos = [a.repo_name for a in artifacts]
    name_width = max(len(n) for n in all_names) if all_names else 0
    repo_width = max(len(r) for r in all_repos) if all_repos else 0

    def _format_line(artifact: Artifact) -> str:
        status = detect_install_status(
            artifact.name, artifact.kind, user_dir, project_dir
        )
        status_str = f"[{status}]" if status else "-"
        return f"  {artifact.name:<{name_width}}  {artifact.repo_name:<{repo_width}}  {status_str}"

    if skills:
        click.echo("Skills:")
        for a in skills:
            click.echo(_format_line(a))
        click.echo()

    if agents:
        click.echo("Agents:")
        for a in agents:
            click.echo(_format_line(a))


@main.command()
@click.argument("name")
@click.option("-g", "global_scope", is_flag=True, help="Install to user scope (~/.claude/)")
@click.option("-p", "project_scope", is_flag=True, help="Install to project scope (./.claude/)")
def add(name: str, global_scope: bool, project_scope: bool) -> None:
    """Add an artifact by creating a symlink."""
    try:
        artifacts = _load_all_artifacts()
    except ConfigError as e:
        raise click.ClickException(str(e))

    matches = [a for a in artifacts if a.name == name]
    if not matches:
        raise click.ClickException(f"Artifact '{name}' not found in any repo")

    if len(matches) == 1:
        artifact = matches[0]
    else:
        # Multiple repos have same artifact — prompt for selection
        repo_names = [a.repo_name for a in matches]
        selected = inquirer.select(
            message=f"Multiple sources found for '{name}':",
            choices=repo_names,
        ).execute()
        artifact = next(a for a in matches if a.repo_name == selected)

    scope = _resolve_scope(global_scope, project_scope)
    try:
        target = create_symlink(artifact, scope)
        click.echo(f"Symlinked {name} to {target}")
    except DeployError as e:
        raise click.ClickException(str(e))


@main.command()
@click.argument("name")
@click.option("-g", "global_scope", is_flag=True, help="Remove from user scope (~/.claude/)")
@click.option("-p", "project_scope", is_flag=True, help="Remove from project scope (./.claude/)")
def remove(name: str, global_scope: bool, project_scope: bool) -> None:
    """Remove an artifact symlink."""
    scope = _resolve_scope(global_scope, project_scope)

    # Try skill first, then agent
    for kind in ("skill", "agent"):
        try:
            target = remove_symlink(name, kind, scope)
            click.echo(f"Removed {name} from {target}")
            return
        except DeployError:
            continue

    raise click.ClickException(f"'{name}' is not installed in {scope}")
