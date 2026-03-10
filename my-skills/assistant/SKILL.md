---
name: assistant
description: Use when the user starts or ends their work day (morning/evening report), wants a cross-system summary combining Jira + Things + Obsidian, or needs orchestration across multiple tools at once. Always use for morning/evening work reports.
---

# Assistant

## Overview

Personal assistant role: manage Jira tickets, Things todos, maintain Obsidian notes, and produce daily work reports.

## Configuration

| Item | Value |
|------|-------|
| **Obsidian vault name** | `My Note` |
| **Jira cloudId** | `c07c0d37-d9c1-4795-8f63-ab7d6bcf3d2a` (ouryahoo.atlassian.net) |

---

## Error Handling

All data collection steps share the following rules:

| Situation | Handling |
|-----------|---------|
| Query failure | Mark the section as "unavailable", ask whether to continue |
| No data | Note "none" and proceed to the next step |

---

## Daily Reports

Trigger only when user explicitly requests a report.

---

### Morning Report

**Trigger**: User expresses intent to start work (e.g. "I'm starting work", "morning report")

Morning Report is **step-by-step interactive**, not a one-time output.

#### Step 1: Display Jira Tickets

**Tool**: `searchJiraIssuesUsingJql`

**JQL**:
```jql
assignee = currentUser() AND statusCategory not in (Done) ORDER BY updated DESC
```

**Display fields**: `key`, `summary`, `status`, `priority`, `duedate` (show "none" if no due date)

**Special handling**: More than 50 tickets → show only the latest 10, note total count

**Output template**:

```markdown
## Open Jira Tickets

| Key | Summary | Status | Priority | Due Date |
|-----|---------|--------|----------|----------|
| PROJ-123 | Task summary | In Progress | High | 2026-02-15 |

*X open tickets total*

---
Let me know when you're done, and I'll show today's Todos next.
```

⚠️ After outputting Jira tickets, **stop and wait** — do not automatically proceed to Step 2.

#### Step 2: Display Things Todos

**Trigger**: User indicates Jira is handled (e.g., "done", "next", "continue", "todos")

**Tool**: `get_today` (Things MCP)

**Display fields**: `title`, `notes`, `project`

**Output template**:

```markdown
## Today's Todos

| Task | Notes | Project |
|------|-------|---------|
| Finish documentation | See template | Project A |

*X tasks total*
```

Each step can also be triggered independently:
- "show my Jira tickets" → execute Step 1 only
- "show my todos" → execute Step 2 only

---

### Evening Report

**Trigger**: User expresses intent to wrap up (e.g. "I'm wrapping up", "heading out", "evening report")

#### Step 1: Review Things Inbox

1. Fetch all Inbox tasks: `get_inbox()`
2. Present each task one by one — ask the user how they want to handle it
3. Wait for user response before moving to the next task
4. Act on their decision (e.g. schedule, move to project, delete, keep in inbox)
5. Repeat until all inbox tasks are processed

#### Step 2: Daily Note Summary

1. Read today's DailyNote: `get_periodic_note(period="daily")`
   (Path format: `DailyNote/YYYY/MM/YYYY-MM-DD.md`)
2. If DailyNote does not exist: notify the user and ask whether to manually provide today's work summary
3. Summarize key information and output Evening Report

**Content handling**:
- Note is too long (>5000 characters) → summarize key sections, mark as "[Content condensed]"

**Output template**:

```markdown
# Evening Report - YYYY-MM-DD

**Generated at**: YYYY-MM-DD HH:MM

---

## Daily Note Summary

### Meeting Records
- [Time] [Title] - Decisions made

### Completed Work
- [Item]

### Work in Progress
- [Item]

### Pending Items
- [ ] [Item]

---

## Summary

- **Today's achievements**: [Key items completed]
- **Tomorrow's focus**: [Planned priorities]
```

⚠️ Reports are NOT auto-appended to notes unless user explicitly requests it.

---

## FAQ

| Question | Answer |
|----------|--------|
| Ticket has no due date? | Show "none" in the table |
| Include completed tickets? | No, JQL already excludes `statusCategory not in (Done)` |
| Report requested multiple times in the same day? | Regenerate; appending to notes requires explicit user request |
| Can Morning Report skip Step 1? | Yes, the user can directly request Todos |
| Note contains drafts or sensitive content? | Summarize only publicly relevant parts, or ask the user whether to include |
