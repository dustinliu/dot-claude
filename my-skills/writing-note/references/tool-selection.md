# Tool Selection Guide

## Obsidian Vault Operations — Use MCP Tools

All note operations inside the Obsidian vault must use MCP tools. Paths are **vault-relative** (no absolute prefix needed).

```
What do you need to do?
├─ Read a note → read_note(path)
├─ Create a new note → create_note(path, content)
├─ Update a section → patch_note(path, content, heading=<section title>)
├─ Update frontmatter → patch_note(path, content)  [no heading argument]
├─ Append to note → append_note(path, content)
├─ List files in a directory → list_files(path)  [non-recursive, immediate children only]
├─ Search by content/keywords → search(query)
├─ Search with metadata/Dataview → search_query(query)  [DQL syntax]
└─ DailyNote operations
   ├─ Read today → get_periodic_note(period="daily")
   ├─ Append today → append_periodic_note(period="daily", content=...)
   └─ Update section → patch_periodic_note(period="daily", heading=..., content=...)
```

## MCP Tool Quick Reference

| Tool | Purpose | Notes |
|------|---------|-------|
| `read_note(path)` | Read note content | Vault-relative path |
| `create_note(path, content)` | Create a new note | Fails if file exists |
| `patch_note(path, content, heading)` | Update a specific section | heading = section title string |
| `patch_note(path, content)` | Update frontmatter | Omit heading argument |
| `append_note(path, content)` | Append to end of note | |
| `list_files(path)` | List immediate children | Non-recursive; use for directory listing |
| `search(query)` | Full-text search | Returns matching notes |
| `search_query(query)` | Dataview DQL search | e.g., `TABLE status FROM "Work/Projects"` |
| `get_periodic_note(period)` | Get periodic note | `period="daily"` for today's DailyNote |
| `append_periodic_note(period, content)` | Append to periodic note | |
| `patch_periodic_note(period, heading, content)` | Update section in periodic note | |

## Path Examples

```
# Correct — vault-relative paths
read_note("Work/Projects/API-Gateway/API-Gateway.md")
list_files("Work/Meetings/2026/02")
create_note("Dev/Tools/tmux.md", content)

# Wrong — absolute paths not needed
read_note("/Users/dustinl/Documents/obsidian/My Note/Work/Projects/...")
```

## Non-Vault File Operations

For files outside the vault (skill references, assets, system operations):

| What you need | Tool |
|--------------|------|
| Read a local file | `Read` |
| Edit a local file | `Edit` |
| Create a local file | `Write` |
| Find local files | `Glob` |
| Search local file content | `Grep` |
| Git / system commands | `Bash` |

---

**Last updated**: 2026-03-07
