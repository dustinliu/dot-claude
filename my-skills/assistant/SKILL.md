---
name: assistant
description: Use when the user starts or ends their work day (morning/evening report), wants a cross-system summary combining Jira + Things + Obsidian, or needs orchestration across multiple tools at once. For focused operations on notes, meetings, or projects, the respective sub-skills handle those. Always use for morning/evening work reports.
---

# Assistant

## Overview

Personal assistant role: manage Jira tickets, Things todos, maintain Obsidian notes, and produce daily work reports.

## Configuration

| Item | Value |
|------|-------|
| **Obsidian vault name** | `My Note` |
| **Jira cloudId** | `c07c0d37-d9c1-4795-8f63-ab7d6bcf3d2a` (ouryahoo.atlassian.net) |

## Sub-Skills

| Task | Skill |
|------|-------|
| Create / edit / search notes | `obsidian-notes` |
| Query / create / update projects | `project-management` |
| Query / create / update meetings | `meeting-records` |

## Daily Reports

Trigger only when user explicitly requests a report.

**Morning Report** (trigger: user expresses intent to start work, e.g. "I'm starting work"):

1. Fetch open Jira issues → if no issues, continue, else -> display → **wait for user**
2. After user responds → fetch today's Things todos → display

Each step can also be triggered independently.

**Evening Report** (trigger: user expresses intent to leave work, e.g. "I'm wrapping up"):

1. Read today's DailyNote: `get_periodic_note(period="daily")`
2. Output work summary (meetings, completed, in-progress, pending)

⚠️ Reports are NOT auto-appended to notes unless user explicitly requests it.

Full flow details → `references/daily-report-guide.md`

## File Output Rule

Temporary files or generated code → always place in `tmp/` under the project root, never in the root directory.
