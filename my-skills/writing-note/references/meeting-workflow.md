# Meeting Records Workflow

Complete rules and workflows for managing and querying meeting records.

---

## Structure

**Path**: `Meetings/YYYY/MM/[Title] YYYY-MM-DD.md`
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
Glob("~/Documents/obsidian/My Note/Meetings/YYYY/MM/*.md") → for each file:
  Read(full_path) → extract status → if reviewed? → (yes) show title only : (no) show full content
```

---

## Common Operations

| Operation | Tool | Steps |
|-----------|------|-------|
| **Query meetings** | `Glob` + `Read` | 1. `Glob("~/Documents/obsidian/My Note/Meetings/YYYY/MM/*.md")` 2. `Read` each file 3. Filter by status |
| **Create meeting** | `Write` | 1. Fill out `assets/meeting.md` template 2. `Write` to full path |
| **Update status** | `Edit` | Edit the YAML frontmatter `status:` field directly |
| **Add content** | `Read` + `Write`/`Edit` | Follow the Note Update Workflow in SKILL.md — read, integrate, overwrite |
| **Search meetings** | `Grep` | `Grep(pattern, "~/Documents/obsidian/My Note/Meetings")` |

**Update status example**:
```yaml
# Before
status: draft

# After (via Edit — update the frontmatter status field)
status: reviewed
```

---

## Scenario Examples

### Scenario 1: Review meetings on a specific date
**Request**: "review meetings from 2026-02-09"
**Flow**: `Glob("~/Documents/obsidian/My Note/Meetings/2026/02/*.md")` → filter filenames containing `2026-02-09` → `Read(full_path)` → display by status

### Scenario 2: Query all meetings for a project
**Request**: "meeting records for ProjectX"
**Flow**: `Grep("project: ProjectX", "~/Documents/obsidian/My Note/Meetings")` → `Read(full_path)` each matching file → display sorted by date

---

## Quick Reference

| User request | Core tools | Key steps |
|-------------|-----------|-----------|
| Review meetings | `Glob` + `Read` | List directory, read each file, filter by status |
| Create meeting | `Write` | Fill in template, specify full filesystem path, write file |
| Update status | `Edit` | Edit frontmatter `status:` field in the file |
| Query specific meeting | `Glob` + `Read` | List directory, read matching file |
| Search keywords | `Grep` | Search content across meetings directory |

---

## Prohibited Operations

1. Do not manage meeting records in DailyNote — manage only under `Meetings/`
2. Do not mix multiple sources — single source of truth: `Meetings/`
3. Do not ignore the status field — it determines display behavior (values: `draft` or `reviewed`)
4. Do not omit frontmatter fields when creating — this affects subsequent queries and display

---

## Verification Checklist

When querying or operating on meeting records, ensure:

- [ ] Correct directory path is used (`Meetings/YYYY/MM/`)
- [ ] Display method is determined by the status field
- [ ] Reviewed status shows title only, no content output
- [ ] File changes are verified after modification (re-read with `Read`)
- [ ] Frontmatter fields remain complete
- [ ] Date format is consistent (YYYY-MM-DD)
