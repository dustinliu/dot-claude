---
name: writing-note
description: >-
  Use this skill to read, write, search, or modify files in the user's local Obsidian vault
  (markdown notes). This is the user's personal knowledge base stored as local files. Trigger
  whenever the request involves personal notes — including "save this to my notes", "幫我記",
  "幫我存", "daily note", "筆記", "幫我找...筆記", "我之前有存", "更新筆記", "meeting note",
  "project note", or appending entries to today's log. This skill is the default for any request
  to persist, retrieve, or edit personal knowledge when no external service (Jira, GitHub,
  Confluence, Linear, Things, Slack, email) is explicitly specified. Also trigger on any mention
  of "Obsidian", "vault", or "my notes".
metadata:
  argument-hint: "[note-request]"
  model: sonnet
---

# Obsidian Notes

If `$ARGUMENTS` is provided, treat it as the user's note request and proceed directly without asking for clarification.

## Overview

Standard operations for reading, writing, and organizing notes in the Obsidian vault (Obsidian Flavored Markdown with YAML frontmatter and wikilinks). All vault operations access the filesystem directly using the Read, Write, Edit, Glob, and Grep tools.

## Vault Location

| Item | Value |
|------|-------|
| **Vault root** | `~/Documents/obsidian/My Note` |
| **Notes base** | `~/Documents/obsidian` (may contain multiple vaults) |

All paths in this skill are **vault-relative**. Prepend `~/Documents/obsidian/My Note/` to get the full filesystem path.

## Companion Skills

Obsidian supports more than plain markdown notes. Before proceeding, consider whether the user's request is better served by one of these formats:

| Skill | Format | When to use |
|-------|--------|-------------|
| `obsidian-markdown` | `.md` | **Always invoke** when creating or editing notes — ensures correct Obsidian Flavored Markdown (wikilinks, callouts, embeds, properties) |
| `obsidian-bases` | `.base` | a database view, filtered table, card gallery, or summary of notes by properties |
| `json-canvas` | `.canvas` | a visual layout — mind map, flowchart, project board, or spatial arrangement of ideas |

Invoke the relevant skill(s) before writing content so you follow the correct syntax.

## Note Placement

### Structured Types (fixed paths)

Three root directories have fixed, reserved path patterns — always use these exact locations:

| Type | Path pattern |
|------|-------------|
| Project | `Projects/[ProjectName]/[ProjectName].md` |
| Meeting | `Meetings/YYYY/MM/[Title] YYYY-MM-DD.md` |
| DailyNote | `DailyNote/YYYY/MM/YYYY-MM-DD.md` |

Always create project and meeting notes at these paths. Read the corresponding reference file for the full workflow:

- Projects → `references/project-workflow.md`
- Meetings → `references/meeting-workflow.md`

### General Notes (dynamic discovery)

For all other notes, **always** explore the vault's current structure before deciding on a location. Never assume where a note should go without checking first.

1. **Discover**: Use `Glob` (`~/Documents/obsidian/My Note/**/*.md`) to survey the vault. Build a picture of the existing top-level directories, sub-folders, and naming conventions.
1. **Analyze**: Identify the note's topic, type, and how it relates to existing content.
1. **Decide** on a path:
   - **Existing location fits** → place the note there; follow local naming conventions exactly.
   - **No existing location fits** → create a new path consistent with the vault's overall style; briefly explain the choice to the user.
   - **Restructuring needed** → explain why and get user confirmation before moving any files.

**Depth constraint**: Outside of `Projects/`, `Meetings/`, and `DailyNote/`, directory nesting must not exceed **3 levels** (e.g., `Area/Topic/SubTopic/note.md` is the maximum depth). Do not create deeper hierarchies.

**Principles**: Prefer existing structure over creating new folders. Observe local conventions — different vault areas may use different patterns. When content doesn't fit any existing category, create a new folder but justify the choice.

## Templates

| Type | Template |
|------|----------|
| Project | `assets/project.md` |
| Meeting | `assets/meeting.md` |
| DailyNote | *(plugin-managed)* — see [Structured Types](#structured-types-fixed-paths) |

## Note Creation Checklist

1. Determine note type (project / meeting / daily / general)
1. **Determine placement**:
   - Project or meeting → use the fixed path (see [Structured Types](#structured-types-fixed-paths))
   - General → follow the [dynamic discovery](#general-notes-dynamic-discovery) workflow
1. Select template if applicable
1. Create with `Write` at the full filesystem path
1. Verify frontmatter fields: `title`, `created`, `updated`, `tags`
1. Verify creation: `Read` the file to confirm it was created and YAML is valid

## Note Update Workflow

When the user asks to **update**, **add to**, or **modify** an existing note, do NOT blindly append new content to the end. Instead, follow this workflow:

1. **Read**: `Read` the file at its full filesystem path to get the full current content
1. **Analyze**: Identify the note's headings, sections, and organizational structure
1. **Integrate**: Compose the updated note by merging new content into the existing structure:
   - Place new content under the most relevant existing heading
   - Merge overlapping or duplicate information — keep the more complete or up-to-date version
   - Add a new section only when no existing heading fits; position it logically, not at the end by default
1. **Write**: Overwrite the note with `Write` (or use `Edit` for targeted changes)
1. **Verify**: `Read` the file again to confirm the result is well-structured

### When append IS appropriate

Use append only when the note is inherently chronological and the new content is a discrete new entry:

- **Daily notes**: adding log entries or timestamps
- **Meeting notes**: adding follow-up items after the meeting
- **The user explicitly says** "append", "add to the end", or "加在後面"

Use `Edit` to insert content at the correct position, or `Bash` (`echo >> file`) for a simple append to end of file.

If unsure, default to the integrate workflow above.

## Reference Files

| File | When to read |
|------|-------------|
| `references/note-organization.md` | Naming, tag system, frontmatter standards |
| `references/meeting-workflow.md` | Any meeting note operation (create, query, update status) |
| `references/project-workflow.md` | Any project note operation (query, create, update, Jira integration) |
