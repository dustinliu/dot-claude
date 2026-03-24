# Note Organization Standards

Quick navigation: [Naming](#naming-conventions) | [Frontmatter](#frontmatter-standards) | [Tags](#tag-classification-system)

---

## Naming Conventions

### File Names

- **English preferred**: easier to search
- **Capitalize first letter**: `Kubernetes-Ingress.md`
- **Meeting record convention**: `[Title] YYYY-MM-DD.md` (e.g., `Security-Review 2026-02-15.md`)
- **Avoid overly long names**: < 50 characters

### Directory Names

- **English preferred**: easier to search
- **Capitalize first letter**: `Languages/`, `Tools/`
- **Singular form**: `Keyboard/` not `Keyboards/`
- **Parent directories must be in English**: avoid mixing (e.g., `Work/工作/...`)

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

### Type-Specific Fields

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
