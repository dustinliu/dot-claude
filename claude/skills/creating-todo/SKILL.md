---
name: creating-todo
description: Use ONLY when the user explicitly mentions "Things" and wants to add a task to Things to-do list
allowed-tools: Bash, mcp__things__get_projects, mcp__things__add_todo, mcp__things__add_project, AskUserQuestion
---

# Creating Todo

Add current work as **exactly one** to-do item in Things, mapped to the correct Things project.

## Scope

- **One todo per invocation** — always create exactly one top-level todo
- Multiple related items go inside the **Notes** field of that todo (as a checklist or bullet list)
- Do NOT create multiple `mcp__things__add_todo` calls in a single invocation

## Workflow

### 1. Prepare task content

- If user provided a description → use it directly
- Otherwise → summarize current work from conversation context, confirm with user before continuing

### 2. Detect current project name

1. In a git repo (including worktrees) → `git worktree list --porcelain 2>/dev/null | head -1 | sed 's/^worktree //' | xargs basename`
2. Not in git → `basename "$PWD"`

### 3. Confirm Things project with user (always required)

Call `mcp__things__get_projects` to list all projects, then do a case-insensitive partial match.

**Always use `AskUserQuestion` to confirm the project with the user**, regardless of whether a match was found:

- Match found → ask: *"I found Things project 'X'. Is this the right project?"*
  - User says yes → proceed
  - User says no → ask: *"Which Things project should I add this to?"*
  - User gives a project name directly → use that name and proceed
- No match found → ask: *"Which Things project should I add this to?"*

Never proceed to step 4 without an explicit answer from the user.

### 4. Create project if needed

If the project name given in step 3 does not exist in Things, call `mcp__things__add_project` directly — no additional confirmation needed.

### 5. Add the to-do (requires confirmation)

Show the user the full details and ask for confirmation before submitting:

```
Title:   <title>
Notes:   <notes>   (if any)
Project: <project name>
```

*"Shall I add this to Things?"*

Only call `mcp__things__add_todo` with the project's UUID after user confirms. Pass only `title`, `notes`, and `list_id` — do not add `when`, `tags`, `deadline`, or any other fields unless the user explicitly requests them.

## Rules

- **Only activate** when the user explicitly mentions "Things"
- **One todo per invocation** — never call `mcp__things__add_todo` more than once
- **Always** confirm the Things project with the user via `AskUserQuestion` — even when a confident match is found
- **Never** add a to-do without showing details and waiting for approval
- **Never** pass extra fields (`when`, `tags`, `deadline`, etc.) to `mcp__things__add_todo` unless user explicitly requests them
