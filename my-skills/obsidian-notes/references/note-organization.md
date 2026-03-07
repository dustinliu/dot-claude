# Note Organization Standards

Quick navigation: [Creation Process](#new-note-creation-process) | [Naming Conventions](#naming-conventions) | [Tags](#tag-classification-system) | [Q&A](#frequently-asked-questions)

---

## Directory Structure

### Top-Level Categories

```
Work/              # Work-related (projects, meetings, Yahoo items)
Dev/               # Development and technical (languages, tools, systems)
Games/             # Gaming content (guides, notes)
Personal/          # Personal matters (learning, hobbies)
Travel/            # Travel-related (guides, trip reports)
DailyNote/         # Daily notes (automatically managed)
```

### Depth Limits

- **General notes**: max 3 levels `Level1/Level2/Level3/file.md`
- **Project notes**: exception allows 4 levels `Work/Projects/[ProjectName]/[ProjectName].md` (related notes can be placed freely inside the project directory)
- **Meeting records**: exception allows 4 levels `Work/Meetings/YYYY/MM/file.md`
- **Exceeding the limit**: use tags instead of additional levels

### Special Note Types (with templates)

| Type | Path | Template |
|------|------|----------|
| **Project** | `Work/Projects/[ProjectName]/[ProjectName].md` | `assets/project.md` |
| **Meeting** | `Work/Meetings/YYYY/MM/[title] YYYY-MM-DD.md` | `assets/meeting.md` |
| **DailyNote** | `DailyNote/YYYY/MM/YYYY-MM-DD.md` | Use periodic note MCP tools |

### Free Organization

Except for project and meeting notes, all other notes are organized freely under the top-level categories, with a maximum depth of 3 levels and no special structural restrictions:

```
Dev/DevOps/Kubernetes-Ingress.md
Games/Hades/Story-Notes.md
Personal/Learning/Python-Tips.md
Work/Yahoo-Project/Q1-Roadmap.md
```

---

## Naming Conventions

### General Rules

- **English preferred**: easier to search
- **Capitalize first letter**: `Kubernetes-Ingress.md`
- **Meeting record exception**: `[Title] YYYY-MM-DD.md` (e.g., `Security-Review 2026-02-15.md`)
- **Avoid overly long names**: < 50 characters

### Directory Naming

- **English preferred**: easier to search
- **Capitalize first letter**: `Languages/`, `Tools/`
- **Singular form**: `Keyboard/` not `Keyboards/`
- **Parent directories must be in English**: avoid `Work/Work/...`

---

## Frontmatter Standards

### Required Fields (all notes)

```yaml
---
title: Note Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [category-tag, topic-tag, status-tag]
---
```

### Type-Specific Fields (by note type)

| Type | Additional Fields |
|------|------------------|
| **Project** | `jira: "PROJ-123"` / `status: active\|on-hold\|completed` |
| **Meeting** | `date: YYYY-MM-DD` / `attendees: [Name1, Name2]` / `project: "[[Link]]"` / `status: draft\|reviewed` |

---

## Tag Classification System

### 1. Category Tag (optional, 1 tag; can be omitted if directory already categorizes)

| Tag | Purpose |
|-----|---------|
| `work` | Work-related (projects, meetings) |
| `technical` | Technical documentation |
| `gaming` | Gaming content |
| `personal` | Personal matters |
| `travel` | Travel-related |
| `reference` | Pure reference material |

### 2. Topic Tag (optional, multiple allowed)

Common: `infrastructure`, `security`, `migration`, `deployment`, `database`, `documentation`, `development`, `system-admin`, `planning`, `performance`

### 3. Status Tag (optional, 1 tag)

- `active` — In progress
- `on-hold` — Paused
- `completed` — Completed
- `draft` — Draft
- `deprecated` — Deprecated

### 4. Priority Tag (optional, for GTD)

- `urgent` — Urgent matters
- `important` — Important but not urgent
- `routine` — Routine work

### Tag Examples

```yaml
# Project note
tags: [infrastructure, active]

# Technical documentation
tags: [kubernetes, deployment, documentation]

# Game guide
tags: [hades, reference]
```

---

## New Note Creation Process

### Decision Tree

```
1. Is it a project or meeting?
   ├─ Yes → Use the corresponding template (assets/project.md or assets/meeting.md)
   └─ No  → Create freely (choose top-level category + freely organize sub-levels)
   ↓
2. Set Frontmatter: title, created, updated, tags
   ↓
3. Create the note with `create_note(path, content)` (vault-relative path)
   ↓
4. Verify with `read_note(path)` to confirm the file was created
```

### Creation Checklist

- [ ] **Type determined**: project, meeting, or free note?
- [ ] **Path is reasonable**: max 3 levels deep (projects and meetings allow 4 levels as exceptions)
- [ ] **Filename is clear**: English preferred, capitalize first letter, meeting notes include date
- [ ] **Frontmatter complete**: title, created, updated, tags
- [ ] **Tags valid**: at least 1 category tag
- [ ] **Template used**: use corresponding template for projects/meetings; create freely for others
- [ ] **Verified**: `read_note(path)` to confirm file exists and YAML is valid

---

## Frequently Asked Questions

### Q1: Which directory should a note go in?

**A**:
- **Project notes**: `Work/Projects/[ProjectName]/[ProjectName].md`
- **Meeting records**: `Work/Meetings/YYYY/MM/[title] YYYY-MM-DD.md`
- **Other notes**: choose an appropriate top-level category (Work/Dev/Games/Personal/Travel/GTD/DailyNote), organize sub-levels freely, max 3 levels

### Q2: How do I decide on frontmatter fields?

**A**: All notes require `title`, `created`, `updated`, `tags`.
- **Projects/Meetings**: add type-specific fields (jira, date, attendees, etc.)
- **Free notes**: the basic 4 fields are sufficient

### Q3: What if the directory exceeds 3 levels?

**A**: Use tags instead. For example, `Dev/Tools/Terminal/tmux.md` + tag `multiplexer`, rather than a 6-level directory structure.

### Q4: Can Chinese filenames be used?

**A**: Yes, but parent directories must be in English. OK: `Games/RogueGames/隻狼.md` Not OK: `Work/工作/專案.md`

### Q5: Do all existing notes need to be updated?

**A**: Not required. Check notes when you edit them. Do a quarterly review of important notes.

---

## Real-World Scenario Examples

### Scenario 1: Creating a Project Note

**Request**: "Create a project note for the API Gateway migration, Jira is TWECP-300"

**Steps**:
1. Path (vault-relative): `Work/Projects/API-Gateway-Migration/API-Gateway-Migration.md`
2. Use: `assets/project.md`
3. Tool: `create_note("Work/Projects/API-Gateway-Migration/API-Gateway-Migration.md", content)`
4. Frontmatter:
```yaml
title: API Gateway Migration
jira: "TWECP-300"
space: TWECP
created: 2026-02-15
updated: 2026-02-15
status: active
tags: [work, infrastructure, migration, active]
```

### Scenario 2: Creating a Meeting Record

**Request**: "Record the Security Review meeting, attendees are Dustin and Jim"

**Steps**:
1. Path (vault-relative): `Work/Meetings/2026/02/Security-Review 2026-02-15.md`
2. Use: `assets/meeting.md`
3. Tool: `create_note("Work/Meetings/2026/02/Security-Review 2026-02-15.md", content)`
4. Frontmatter:
```yaml
title: Security Review
date: 2026-02-15
attendees: [Dustin Liu, Jim Lin]
project: "[[PCI Compliance]]"
status: draft
created: 2026-02-15
updated: 2026-02-15
tags: [work, security]
```

### Scenario 3: Free Note

**Request**: "Record Kubernetes Ingress configuration methods" or "Record notes on the Hades story"

**Steps**:
1. Choose top-level category: `Dev/` or `Games/`
2. Freely organize sub-levels (max 3 levels): `Dev/Deployment/Kubernetes-Ingress.md` or `Games/Hades/Story-Notes.md`
3. Basic Frontmatter (only required fields):
```yaml
title: [Note Title]
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [category-tag, topic-tag, ...]
```
**Note**: Free notes have no special restrictions; organize freely

---

## Changelog

**Last updated**: 2026-02-23
**Maintainer**: Secretary Assistant
