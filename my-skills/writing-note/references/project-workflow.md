# Project Operations Complete Guide

Full workflow for querying, creating, and modifying projects, including intelligent modification rules.

---

## Core Decision Flow

```
User mentions a project
    ↓
Identify project name and operation type (query / create / modify)
    ↓
Look up in Projects/
    ├─ Exact match found → Read and respond (Scenario 1)
    ├─ Fuzzy or multiple matches → Ask user to confirm (Scenario 2)
    └─ Not found → Ask whether to create (Scenario 3)

If modifying → Determine location based on content type → Execute modification (Scenario 4)
If spanning multiple projects → Batch query and summarize (Scenario 5)
```

---

## Scenario 1: Explicit Project Name - Query

**Precondition**: User explicitly mentions a project name and the note exists

**Steps**:
1. `Read("~/Documents/obsidian/My Note/Projects/[ProjectName]/[ProjectName].md")`
2. Scan frontmatter (status, Jira, created/updated dates) and content
3. Extract progress, Jira tickets, deadlines
4. Respond to user

**Response format**: Status, last updated, related tickets, latest progress

---

## Scenario 2: Fuzzy or Multiple Matches

**Precondition**: Name is ambiguous or search returns multiple results

**Steps**:
1. `Glob("~/Documents/obsidian/My Note/Projects/**/*.md")` → scan available project directories
2. List all results (name + brief description)
3. Ask user to confirm
4. Execute Scenario 1

---

## Scenario 3: Project Does Not Exist - Create

**Precondition**: Note not found in `Projects/`

**Steps**:
1. Notify user that the project was not found
2. Ask whether to create it
3. If confirmed, collect required information: project name, short description, Jira code (optional)
4. Compose content from `assets/project.md` template, then `Write` to `~/Documents/obsidian/My Note/Projects/[ProjectName]/[ProjectName].md`
5. Verify: `Read` the file to confirm it was created
6. Notify user that creation is complete

---

## Scenario 4: Modify / Update Project - Intelligent Modification

**Precondition**: Project note exists and user requests a modification

### Core Principle

**Automatically determine the modification location based on content type** — no repeated clarifying questions needed. Instruction format:
```
"Add [content] to [ProjectName] project note"
```

### Content Type to Modification Location Mapping

| Content Type | Recognition Signals | Modification Location | How to Apply |
|---|---|---|---|
| **Progress update** | "completed", "in progress", "encountered", "already" | `Progress Tracking` section | Add new date block |
| **Time-related** | "deadline", "estimated", "delayed" | `Timeline` section | Update completion date or milestone |
| **Jira ticket** | "PROJ-123", "ticket", "issue" | `Related Jira Issues` section | Add new ticket list item |
| **Goal change** | "goal", "goals", "implement", "achieve" | `Goals` section | Add or update goal item |
| **Status change** | "completed", "on hold", "on-hold", "active" | frontmatter `status` field | Update field value |
| **Issues / Decisions** | "issue", "decision", "discovered", "meeting result" | `Notes` section | Add a note |

### Modification Execution Flow

```
1. Read("~/Documents/obsidian/My Note/Projects/[ProjectName]/[ProjectName].md")
   ↓
2. Determine content type and location based on content signals (see table above)
   ↓
3. Locate the corresponding section or frontmatter field
   ↓
4. Update the relevant section or frontmatter field using Edit
   ↓
5. Update frontmatter `updated: YYYY-MM-DD` using Edit
   ↓
6. Verify the modification succeeded (re-read with Read)
   ↓
7. Confirm completion: "Updated [ProjectName]: [location and brief summary]"
```

### Modification Location Details

#### Progress Tracking

**Recognition**: "completed", "in progress", "encountered", "already tested"

**How to apply**: Add a new date block

**Example**:
```
Instruction: "Completed the API authentication module, integration testing estimated to start next Monday"

Result:
### [Date: 2026-02-16]
- Completed API authentication module
- Ready for integration testing (Est. start: 2026-02-17)
```

---

#### Timeline

**Recognition**: "deadline", "estimated", "delayed", "next week", "end of month"

**How to apply**:
- Update `Target Completion` if it is an overall deadline
- Add to `Key Milestones` if it is a milestone

**Example**:
```
Instruction: "MVP must be completed by end of March"

Result (Timeline section):
- **Target Completion**: 2026-03-31
- **Key Milestones**:
  - MVP completion — 2026-03-31
```

---

#### Related Jira Issues

**Recognition**: `PROJ-123` format, "new ticket", "linked ticket"

**How to apply**: Add to the list in the correct format

**Example**:
```
Instruction: "Add ticket TWECP-456 - Security audit"

Result:
- [TWECP-456] — Security audit and review
```

---

#### Frontmatter Status

**Recognition**: "project completed", "project on hold", "change to active"

**How to apply**: Update the `status` field (values: `active` | `on-hold` | `completed`)

**Example**:
```
Instruction: "The entire project is complete"

Result:
status: completed
```

---

#### Goals

**Recognition**: "add goal", "update goal", "want to achieve"

**How to apply**: Add to the `Goals` list

**Example**:
```
Instruction: "Add goal: support OAuth 2.0"

Result (Goals section):
- OAuth 2.0 support
```

---

#### Notes

**Recognition**: "issue", "discovered", "decision", "meeting", "important", "note"

**How to apply**: Append directly to the `Notes` section

**Example**:
```
Instruction: "Decided to delay v2 feature development and focus on stability first"

Result (Notes section):
**Decision**: Delay v2 feature development; prioritize core functionality stability
```

---

### Handling Ambiguity

#### Case 1: Content Spans Multiple Sections

**Example**: "Completed the authentication module, discovered a security vulnerability, deadline pushed to next month"

**Determination**:
1. "Completed" → `Progress Tracking`
2. "Security vulnerability" → `Notes`
3. "Deadline pushed" → `Timeline`

**Approach**: Modify all relevant sections in a single pass

---

#### Case 2: Implied Status Change

**Example**: "All work is done, the team can move on to the next project"

**Determination**: Implies `status: completed` + progress record

**Approach**: Update both status and Progress Tracking simultaneously

---

### Common Modification Scenario Examples

#### Scenario A: Daily Progress Report

```
Instruction: "Fixed the token refresh bug in the login flow, tests passed, add to Authentication project note"

Auto-determined: Progress update
Location: Progress Tracking
Modification:
### [Date: 2026-02-16]
- Fixed token refresh bug in login flow
- Testing passed
```

---

#### Scenario B: Deadline Change

```
Instruction: "MVP delayed to March 15, add to Infrastructure project note"

Auto-determined: Time-related + status info
Location: Timeline + possibly Notes (reason)
Modification:
Timeline:
- **Target Completion**: 2026-03-15

Notes:
Revised target completion to 2026-03-15 (originally 2026-03-01)
```

---

#### Scenario C: Add Jira Ticket

```
Instruction: "Link new ticket TWECP-789 - Database optimization"

Auto-determined: Jira ticket
Location: Related Jira Issues
Modification:
- [TWECP-789] — Database optimization
```

---

#### Scenario D: Project On Hold

```
Instruction: "Project on hold, waiting for client feedback"

Auto-determined: Status change + reason
Location: frontmatter + Notes
Modification:
status: on-hold

Notes:
On hold - awaiting client feedback on requirements
```

---

## Scenario 5: Query Across Multiple Projects

**Precondition**: Query involves information from multiple projects (e.g., "all active projects")

**Steps**:
1. `Glob("~/Documents/obsidian/My Note/Projects/**/*.md")` → get all project main notes
2. `Read(path)` for each project's main note
3. Filter by condition (e.g., `status: active` in frontmatter)
4. Compile results into a table

---

## Prohibited Operations

Do not search for project primary information in Things, DailyNote, or other directories — the single source of truth is `Projects/` (project-related todos may still be queried from Things)

Do not create duplicate project notes without confirmation

When modifying, do not assume the location of content — always refer to the content mapping table

---

## Workflow Summary

| Scenario | Verification Method |
|---|---|
| Scenario 1: Explicit name | Read file directly |
| Scenario 2: Fuzzy name | List results for user to confirm |
| Scenario 3: Project does not exist | Re-read after creation |
| Scenario 4: Modify / update | Re-read after modification |
| Scenario 5: Cross-project query | Review compiled results |

---

## FAQ

**Q: Project name has a different spelling?**
A: Use `Glob("~/Documents/obsidian/My Note/Projects/**/*.md")` to browse all projects, list results for user to confirm (see Scenario 2)

**Q: Jira and Obsidian information are inconsistent?**
A: Treat the Obsidian note as the primary source and notify the user of the discrepancy

**Q: Unsure where to apply a modification?**
A: Refer to the content type mapping table (see the mapping table in "Scenario 4")

**Q: Modification involves complex formatting?**
A: Use `Read` to examine the existing format, then follow the Note Update Workflow in SKILL.md to integrate changes

**Q: Multiple modifications to the same project on the same day?**
A: Update the `updated` timestamp on every modification; do not duplicate earlier edits
