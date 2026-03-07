# Daily Report Generation Guide

This guide covers two independent report modes: **Morning Report** (interactive) and **Evening Report** (single output).

---

## Unified Error Handling Principles

All data collection steps share the following rules:

| Situation | Handling |
|-----------|---------|
| Query failure | Mark the section as "unavailable", ask whether to continue |
| No data | Note "none" and proceed to the next step |

---

## Morning Report

**Trigger condition**: Statements where the user expresses intent to "start work"

Trigger examples: "I'm starting work", "start work", "morning report", etc.

### Interactive Flow

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

**⚠️ Key behavior**: After outputting Jira tickets, **stop and wait** — do not automatically proceed to Step 2.

---

#### Step 2: Display Things Todos

**Trigger**: User indicates Jira is handled (e.g., "done", "next", "continue", "todos", or any forward signal)

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

Morning workflow complete.

---

### Standalone Requests

Each step can also be triggered independently:
- "show my Jira tickets" → execute Step 1 only (does not start Morning workflow)
- "show my todos" → execute Step 2 only

---

## Evening Report

**Trigger condition**: Statements where the user expresses intent to "wrap up for the day"

Trigger examples: "I'm done for the day", "wrapping up", "heading out", "evening report", etc.

### Execution Flow

1. Use `get_periodic_note(period="daily")` to read today's DailyNote
   (Actual path format: `DailyNote/YYYY/MM/YYYY-MM-DD.md`)
2. Summarize key information (meetings, completed work, work in progress, pending items)
3. Output Evening Report

**If DailyNote does not exist**: Notify the user "Today's DailyNote does not exist, unable to generate Evening Report", and ask whether to manually provide today's work summary

**Content handling**:
- Summarize key information (meetings, decisions, progress, todos)
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

---

## ⚠️ Reports are not automatically appended to notes

After generation, **output is shown to the user only**. Appending to notes is only performed when the user explicitly requests it (e.g., "add the report to today's note").

---

## FAQ

| Question | Answer |
|----------|--------|
| Ticket has no due date? | Show "none" in the table |
| Include completed tickets? | No, JQL already excludes `statusCategory not in (Done)` |
| Report requested multiple times in the same day? | Regenerate; appending to notes requires explicit user request |
| Can Morning Report skip Step 1? | Yes, the user can directly request Todos |
| Note contains drafts or sensitive content? | Summarize only publicly relevant parts, or ask the user whether to include |
