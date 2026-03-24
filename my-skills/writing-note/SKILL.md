---
name: writing-note
description: >-
  Use this skill to read, write, search, or modify files in the user's local
  Obsidian vault (markdown notes). This is the user's personal knowledge base
  stored as local files. Trigger whenever the request involves personal notes —
  including "save this to my notes", "幫我記", "幫我存", "daily note", "筆記",
  "幫我找...筆記", "我之前有存", "更新筆記", "meeting note", "project note", or
  appending entries to today's log. This skill is the default for any request to
  persist, retrieve, or edit personal knowledge when no external service (Jira,
  GitHub, Confluence, Linear, Things, Slack, email) is explicitly specified. Also
  trigger on any mention of "Obsidian", "vault", or "my notes".
argument-hint: [note-request]
model: sonnet
---

# Obsidian Notes

If `$ARGUMENTS` is provided, treat it as the user's note request and proceed directly without asking for clarification.

## Overview

Standard operations for reading, writing, and organizing notes in the Obsidian vault (Obsidian Flavored Markdown with YAML frontmatter and wikilinks). All vault operations use Obsidian MCP tools with vault-relative paths.

## Companion Skills

Obsidian supports more than plain markdown notes. Before proceeding, consider whether the user's request is better served by one of these formats:

| Skill | Format | When to use |
|-------|--------|-------------|
| `obsidian-markdown` | `.md` | **Always invoke** when creating or editing notes — ensures correct Obsidian Flavored Markdown (wikilinks, callouts, embeds, properties) |
| `obsidian-bases` | `.base` | User wants a database view, filtered table, card gallery, or summary of notes by properties |
| `json-canvas` | `.canvas` | User wants a visual layout — mind map, flowchart, project board, or spatial arrangement of ideas |

Invoke the relevant skill(s) before writing content so you follow the correct syntax.

## Note Placement

### Structured Types (fixed paths)

Project and meeting notes live at known, fixed locations so agents can quickly list and query them:

| Type | Path pattern |
|------|-------------|
| Project | `Work/Projects/[ProjectName]/[ProjectName].md` |
| Meeting | `Work/Meetings/YYYY/MM/[Title] YYYY-MM-DD.md` |
| DailyNote | *(plugin-managed)* — use `daily_read`, `daily_append`, `daily_prepend` |

Always create project and meeting notes at these paths. Read the corresponding reference file for the full workflow:
- Projects → `references/project-workflow.md`
- Meetings → `references/meeting-workflow.md`

### General Notes (dynamic discovery)

For all other notes, determine location dynamically based on the vault's existing structure and the note's content.

1. **Discover**: Use `list_files` to explore relevant areas of the vault. Understand the current folder structure and organizational patterns.
2. **Analyze**: Identify the note's topic and relationships to existing content.
3. **Match**: Find the best-fitting location within the existing structure:
   - Folders that already contain notes on the same topic or type
   - Naming and depth conventions used by neighboring files
4. **Decide**:
   - Existing location fits → use it, follow local naming conventions
   - No existing location fits → create a new path consistent with the vault's overall style; explain the choice
   - Restructuring needed → explain why and get user confirmation before moving files

**Principles**: Prefer existing structure over creating new folders. Observe local conventions — different vault areas may use different patterns. When content doesn't fit any existing category, create a new one but justify the deviation.

## Templates

| Type | Template |
|------|----------|
| Project | `assets/project.md` |
| Meeting | `assets/meeting.md` |
| DailyNote | *(plugin-managed)* — see [Structured Types](#structured-types-fixed-paths) |

## Note Creation Checklist

1. Determine note type (project / meeting / daily / general)
2. **Determine placement**:
   - Project or meeting → use the fixed path (see [Structured Types](#structured-types-fixed-paths))
   - General → follow the [dynamic discovery](#general-notes-dynamic-discovery) workflow
3. Select template if applicable
4. Create with `create_note(path, content)`
5. Verify frontmatter fields: `title`, `created`, `updated`, `tags`
6. Verify creation: `read_note(path)` to confirm file was created and YAML is valid

## Note Update Workflow

When the user asks to **update**, **add to**, or **modify** an existing note, do NOT blindly append new content to the end. Instead, follow this workflow:

1. **Read**: `read_note(path)` to get the full current content
2. **Analyze**: Identify the note's headings, sections, and organizational structure
3. **Integrate**: Compose the updated note by merging new content into the existing structure:
   - Place new content under the most relevant existing heading
   - Merge overlapping or duplicate information — keep the more complete or up-to-date version
   - Add a new section only when no existing heading fits; position it logically, not at the end by default
4. **Write**: Overwrite the note with the fully reorganized content
5. **Verify**: `read_note(path)` to confirm the result is well-structured

### When append IS appropriate

Use `append_note` only when the note is inherently chronological and the new content is a discrete new entry:

- **Daily notes**: adding log entries or timestamps
- **Meeting notes**: adding follow-up items after the meeting
- **The user explicitly says** "append", "add to the end", or "加在後面"

If unsure, default to the integrate workflow above.

## Reference Files

| File | When to read |
|------|-------------|
| `references/note-organization.md` | Naming, tag system, frontmatter standards |
| `references/error-handling.md` | File not found, YAML errors, search returns nothing |
| `references/meeting-workflow.md` | Any meeting note operation (create, query, update status) |
| `references/project-workflow.md` | Any project note operation (query, create, update, Jira integration) |
