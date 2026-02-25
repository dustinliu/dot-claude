"""CLI entry point for dot-claude."""

from __future__ import annotations

import subprocess
import sys
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path

import click

from dot_claude.installer import install
from dot_claude.inventory import list_items
from dot_claude.manifest import read_manifest
from dot_claude.tui import prompt_items, prompt_scope


def _get_data_root() -> Traversable:
    return resources.files("dot_claude") / "claude"


def _get_user_dest() -> Path:
    return Path.home() / ".claude"


def _get_project_dest() -> Path:
    return Path.cwd() / ".claude"


def _upgrade_package() -> None:
    subprocess.run(
        [sys.executable, "-m", "uv", "tool", "upgrade", "dot-claude"],
        check=True,
    )


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Manage Claude Code skills and agents."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
def add() -> None:
    """Add skills and agents to a scope."""
    data_root = _get_data_root()
    cwd = Path.cwd()

    scope = prompt_scope(cwd)
    if scope is None:
        click.echo("Cancelled.")
        return

    dest = _get_user_dest() if scope == "user" else _get_project_dest()

    items = list_items(data_root)
    manifest = read_manifest(dest)
    pre_selected = manifest.items if manifest else []

    selected = prompt_items(items, pre_selected)
    if selected is None:
        click.echo("Cancelled.")
        return

    install(data_root=data_root, dest=dest, selected_items=selected, scope=scope)

    item_count = len(selected)
    click.echo(f"Installed {item_count} item(s) to {dest}")


@cli.command()
def remove() -> None:
    """Remove skills and agents from a scope."""
    data_root = _get_data_root()
    cwd = Path.cwd()

    scope = prompt_scope(cwd)
    if scope is None:
        click.echo("Cancelled.")
        return

    dest = _get_user_dest() if scope == "user" else _get_project_dest()

    manifest = read_manifest(dest)
    if manifest is None:
        click.echo("Nothing installed in this scope.")
        return

    items = list_items(data_root)
    selected = prompt_items(items, manifest.items)
    if selected is None:
        click.echo("Cancelled.")
        return

    install(data_root=data_root, dest=dest, selected_items=selected, scope=scope)

    removed_count = len(set(manifest.items) - set(selected))
    click.echo(f"Removed {removed_count} item(s) from {dest}")


@cli.command("list")
def list_cmd() -> None:
    """List installed skills and agents."""
    user_dest = _get_user_dest()
    project_dest = _get_project_dest()

    user_manifest = read_manifest(user_dest)
    project_manifest = read_manifest(project_dest)

    if not user_manifest and not project_manifest:
        click.echo("Nothing installed.")
        return

    if user_manifest and user_manifest.items:
        click.echo(f"User ({user_dest}):")
        for item in sorted(user_manifest.items):
            click.echo(f"  {item}")

    if project_manifest and project_manifest.items:
        click.echo(f"Project ({project_dest}):")
        for item in sorted(project_manifest.items):
            click.echo(f"  {item}")


@cli.command()
def update() -> None:
    """Upgrade the package and re-deploy installed items."""
    _upgrade_package()

    data_root = _get_data_root()
    user_dest = _get_user_dest()
    project_dest = _get_project_dest()

    updated = 0
    for dest in [user_dest, project_dest]:
        manifest = read_manifest(dest)
        if manifest is None:
            continue
        install(
            data_root=data_root,
            dest=dest,
            selected_items=manifest.items,
            scope=manifest.scope,
        )
        updated += len(manifest.items)

    if updated:
        click.echo(f"Updated {updated} item(s).")
    else:
        click.echo("Nothing to update.")


def main() -> None:
    cli()
