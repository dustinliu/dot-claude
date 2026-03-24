# Meeting Records Workflow

Complete rules and workflows for managing and querying meeting records.

---

## Structure

**Path**: `Work/Meetings/YYYY/MM/[Title] YYYY-MM-DD.md`
**Naming**: `[Title] YYYY-MM-DD.md` (e.g., `Security-Review 2026-02-15.md`)

Detailed Frontmatter → see `assets/meeting.md`

---

## Core Query Rules

**Decision logic** (based on the `status` field):

| Status | Display | Purpose |
|--------|---------|---------|
| `reviewed` | Show only `[REVIEWED] Title` | Confirmed, skip content |
| `draft` | Full content + Frontmatter | Pending review, needs inspection |

**Operation flow**:
```
list_files("Work/Meetings/YYYY/MM") → for each file:
  read_note(path) → extract status → if reviewed? → (yes) show title only : (no) show full content
```

---

## Common Operations

| Operation | Tool | Steps |
|-----------|------|-------|
| **Query meetings** | `list_files` + `read_note` | 1. `list_files("Work/Meetings/YYYY/MM")` 2. `read_note` each file 3. Filter by status |
| **Create meeting** | `create_note` | 1. Fill out `assets/meeting.md` template 2. `create_note(path, content)` |
| **Update status** | `property_set` | `property_set(file, "status", "reviewed")` |
| **Add content** | `read_note` + rewrite | Follow the Note Update Workflow in SKILL.md — read, integrate, overwrite |
| **Search meetings** | `search` | `search("project: ProjectX")` or content keywords |

**Update status example**:
```yaml
# Before
status: draft

# After (via property_set)
status: reviewed
```

---

## Scenario Examples

### Scenario 1: Review meetings on a specific date
**Request**: "review meetings from 2026-02-09"
**Flow**: `list_files("Work/Meetings/2026/02")` → filter filenames containing `2026-02-09` → `read_note(path)` → display by status

### Scenario 2: Query all meetings for a project
**Request**: "meeting records for ProjectX"
**Flow**: `search("project: ProjectX")` → `read_note(path)` each matching file → display sorted by date

---

## Quick Reference

| User request | Core tools | Key steps |
|-------------|-----------|-----------|
| Review meetings | `list_files` + `read_note` | List directory, read each file, filter by status |
| Create meeting | `create_note` | Fill in template, specify vault-relative path, create note |
| Update status | `property_set` | Set frontmatter `status` field |
| Query specific meeting | `list_files` + `read_note` | List directory, read matching file |
| Search keywords | `search` | Search content across meetings |

---

## Prohibited Operations

1. Do not manage meeting records in DailyNote — manage only under `Work/Meetings/`
2. Do not mix multiple sources — single source of truth: `Work/Meetings/`
3. Do not ignore the status field — it determines display behavior (values: `draft` or `reviewed`)
4. Do not omit frontmatter fields when creating — this affects subsequent queries and display

---

## Verification Checklist

When querying or operating on meeting records, ensure:

- [ ] Correct directory path is used (`Work/Meetings/YYYY/MM/`)
- [ ] Display method is determined by the status field
- [ ] Reviewed status shows title only, no content output
- [ ] File changes are verified after modification (re-read with `read_note`)
- [ ] Frontmatter fields remain complete
- [ ] Date format is consistent (YYYY-MM-DD)
