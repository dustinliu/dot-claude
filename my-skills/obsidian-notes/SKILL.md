---
name: obsidian-notes
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
---

# Obsidian Notes

## Overview

Standard operations for reading, writing, and organizing notes in the Obsidian vault (Obsidian Flavored Markdown with YAML frontmatter and wikilinks). All vault operations use Obsidian MCP tools with vault-relative paths.

## Quick Operations

| Operation | Tool |
|-----------|------|
| Read a note | `read_note(path)` |
| List files in directory | `list_files(path)` |
| Search by content | `search(query)` |
| Search with Dataview DQL | `search_query(query)` |
| Create a note | `create_note(path, content)` |
| Edit a section | `patch_note(path, content, heading)` — attempt directly, no need to read first |
| Edit frontmatter | `patch_note(path, content)` (no heading) |
| Append to note | `append_note(path, content)` |
| DailyNote append | `append_periodic_note(period="daily", content=...)` |
| DailyNote section update | `patch_periodic_note(period="daily", heading=..., content=...)` |

## Directory Structure

Top-level categories: `Work/`, `Dev/`, `Games/`, `Personal/`, `Travel/`, `DailyNote/`

- Max depth: **3 levels** for general notes
- Exception: Projects and Meetings allow **4 levels**

## Special Note Types (use templates)

| Type | Path pattern | Template |
|------|-------------|----------|
| Project | `Work/Projects/[ProjectName]/[ProjectName].md` | `assets/project.md` |
| Meeting | `Work/Meetings/YYYY/MM/[title] YYYY-MM-DD.md` | `assets/meeting.md` |
| DailyNote | `DailyNote/YYYY/MM/YYYY-MM-DD.md` | Use `get_periodic_note`, `append_periodic_note`, `patch_periodic_note` |

## Note Creation Checklist

1. Determine note type (project / meeting / daily / general)
2. Select template if applicable
3. Create with `create_note(path, content)`
4. Verify frontmatter fields: `title`, `created`, `updated`, `tags`
5. Verify creation: `read_note(path)` to confirm file was created and YAML is valid

## Reference Files

| File | When to read |
|------|-------------|
| `references/note-organization.md` | Naming, tag system, frontmatter standards |
| `references/tool-selection.md` | Unsure which tool to use |
| `references/error-handling.md` | File not found, YAML errors, search returns nothing |
| `references/meeting-workflow.md` | Any meeting note operation (create, query, update status) |
| `references/project-workflow.md` | Any project note operation (query, create, update, Jira integration) |
