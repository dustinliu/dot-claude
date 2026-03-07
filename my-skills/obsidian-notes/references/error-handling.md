# Error Handling and Troubleshooting Guide

## Common Issues Quick Reference

| Problem | Cause | Solution |
|---------|-------|---------|
| File not found (404) | Typo or wrong path | See **404 Fallback** below |
| YAML error | Indentation / colon formatting | Reference the `assets/project.md` template; use space indentation |
| File already exists | Name conflict | Ask the user: overwrite / rename / cancel |
| No search results | Keyword mismatch | Simplify the search term, try a partial name; or use `search(query)` to search content |
| `search()` returns 400 | Unsupported query syntax | See **search() 400 Fallback** below |
| API timeout | Network latency | Wait 3–5 seconds and auto-retry; provide a manual link on failure |

---

## 404 Fallback — File Not Found

> **Scope**: This fallback applies only when the **goal is to read** a note. For write/patch/append operations, do NOT run this fallback first — just attempt the write operation directly (see patch_note 400 fallback below if that fails).

When `read_note(path)` returns a 404 error:

1. Call `list_files(parent_dir)` on the parent directory to see what actually exists.
2. Look for close matches (different capitalisation, hyphen vs space, date format).
3. If a close match is found → read that file and inform the user of the actual path used.
4. If no match → tell the user the note does not exist and offer to create it or list alternatives.

```
read_note("Work/Projects/API-Gateway/API-Gateway.md")  → 404
  → list_files("Work/Projects/API-Gateway/")
  → Found: "API-Gateway-Migration.md"
  → read_note("Work/Projects/API-Gateway/API-Gateway-Migration.md")
  → Inform user: "Found note at the corrected path …"
```

---

## search() 400 Fallback — Bad Search Request

When `search(query)` returns a 400 error (unsupported syntax or Omnisearch not available):

1. **First try**: rewrite the query as a Dataview DQL query and call `search_query(dql)`.
   ```
   search_query('TABLE file.mtime FROM "" WHERE contains(file.name, "kubernetes")')
   ```
2. **If DQL also fails**: fall back to manual content scan —
   - Call `list_files(dir)` on each likely top-level directory (e.g. `Work/`, `Dev/`, their subdirectories).
   - For **every** `.md` file returned, call `read_note(path)` to read its content and check whether it contains the search keyword.
   - Do not stop after checking filenames — filenames rarely include the topic keyword; the content will.
   - Collect all matching notes, then summarise findings (title + vault-relative path) to the user.

```
search("kubernetes") → 400
  → search_query('TABLE FROM "" WHERE contains(file.name, "kubernetes")') → empty
  → list_files("Work/") → [Work/Yahoo/Infrastructure/, Work/Projects/, ...]
  → list_files("Work/Yahoo/Infrastructure/") → [Omega Cli.md, Omega Usage.md, ...]
  → read_note("Work/Yahoo/Infrastructure/Omega Cli.md") → contains "kubectl" → MATCH
  → read_note("Work/Yahoo/Infrastructure/Omega Usage.md") → contains ".k8s" → MATCH
  → ... (continue for all files in likely dirs)
  → Report: "Found 2 notes mentioning Kubernetes: ..."
```

Avoid using `Grep` or filesystem tools to search vault content — always prefer MCP tools.

---

## patch_note() 400 Fallback — Section Not Found or API Error

When `patch_note(path, content, heading)` returns a 400 error (heading not found, or "No 'Target-Type' header" API error):

1. Call `read_note(path)` to retrieve the **full current content** of the note.
2. If the note exists:
   - If the heading already exists: the patch_note call may have had an API issue — retry once.
   - If the heading does not exist: append the new section to the appropriate place in the note content.
   - Construct the complete updated content string (existing content + new section).
   - Call `create_note(path, updated_content)` to write the updated note.
3. If the note does not exist (404): create a new note with `create_note(path, content)`.
4. **Do NOT call `create_note` with only the new section content** — this overwrites all existing note content.

```
patch_note("Work/Projects/Wuxian/Wuxian.md", "...", "Deployment Checklist") → 400
  → read_note("Work/Projects/Wuxian/Wuxian.md")
  → Got existing content: "# Wuxian\n## Overview\n...\n## Status\n..."
  → Construct updated content: existing content + "\n## Deployment Checklist\n..."
  → create_note("Work/Projects/Wuxian/Wuxian.md", full_updated_content)
  → Note updated with all existing sections preserved
```

---

## Edge Case Handling

| Situation | Handling |
|-----------|---------|
| **Incomplete information** | List the missing items; ask whether to proceed |
| **Data conflict** | Priority order: Obsidian > Jira > logs; remind the user to sync |
| **Partial success** | Mark which steps succeeded/failed; ask whether to retry the failed parts |

---

## Validation Checklist

- [ ] **Path is correct**: file is at the expected location (confirm with `list_files(parent_dir)`)
- [ ] **Frontmatter is valid**: YAML has no indentation errors (confirm with `read_note(path)`)
- [ ] **Date format**: YYYY-MM-DD
- [ ] **Result is non-empty**: has actual content, or clearly explains why there is no result
- [ ] **Data source is clear**: user knows where the information came from

**Validation method**: use `read_note(path)` to read the file content → confirm key sections → notify the user of the result

---

## Recovery Strategies

- **Auto-recover**: API timeout, file lock → wait 3–5 seconds and retry
- **Requires user decision**: no search results, corrupted file, file already exists → notify and provide alternatives

---

## Escalate to User

Situations that require a user decision:

- **Confirmation** — deletion / overwrite confirmation
- **Data conflict** — inconsistency across multiple sources
- **Risk of data loss** — any operation that may lose data
- **Ambiguity** — unable to determine user intent

---

**Last updated**: 2026-03-07
