---
name: git-commit
description: 'Execute git commit with conventional commit message analysis, intelligent staging, and message generation. Use when user asks to commit changes, create a git commit, or mentions "/commit". Supports: (1) Auto-detecting type and scope from changes, (2) Generating conventional commit messages from diff, (3) Interactive commit with optional type/scope/description overrides, (4) Intelligent file staging for logical grouping'
license: MIT
allowed-tools: Bash
model: sonnet
---

# Git Commit with Conventional Commits

Create standardized git commits using Conventional Commits. Analyze the diff and follow the interactive confirmation workflow below.

## Workflow

1. **Analyze**: Run `git diff --staged` (or `git diff` if nothing staged) and `git status --porcelain`
2. **Stage**: Propose files to stage — **wait for user confirmation** before running `git add`
3. **Draft**: Generate commit message from the diff (type, scope, description)
4. **Commit**: Show the full commit command — **wait for user confirmation** before executing

## Grouping Changes

If the diff contains multiple unrelated changes, propose splitting into separate commits:

- Stage specific files per logical group: `git add path/to/file1 path/to/file2`
- Use `git add -p` for partial file staging
- One logical change per commit

## Interactive Confirmation (Required)

- Before `git add`: list intended files and wait for approval
- Before `git commit`: display the full command and wait for approval

Never stage or commit without explicit user approval.

## Co-Authored-By

Include in the commit footer using the current agent name and model name:

```
Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```
