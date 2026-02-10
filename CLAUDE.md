# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`dot-claude` is a repository for maintaining and documenting Claude Code configurations and guidance files. It serves as a centralized source for:

## Directory Structure

```
.
├── claude/ # contains the configurations for the claude code agent
├── LICENSE
├── README.md
└── CLAUDE.md                   # This file
```

## Development Workflow

## Deployment

This project uses **GNU Stow** to deploy configurations via symlinks. The `claude/` directory structure mirrors the home directory layout, allowing Stow to create symlinks from the repository to `~/.` automatically.

### GNU Stow Usage

```bash
# Deploy all configurations from this repository
stow -t $HOME claude
```

