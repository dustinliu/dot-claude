# Error Handling and Troubleshooting Guide

## Common Issues Quick Reference

| Problem | Cause | Solution |
|---------|-------|---------|
| File not found (404) | Typo or wrong path | Check the parent directory for close matches (capitalisation, hyphen vs space, date format) |
| YAML error | Indentation / colon formatting | Reference the `assets/project.md` template; use space indentation |
| File already exists | Name conflict | Ask the user: overwrite / rename / cancel |
| No search results | Keyword mismatch | Simplify the search term; try a manual content scan (see below) |
| API timeout | Network latency | Wait 3–5 seconds and auto-retry |

---

## Search Fallback

**Empty results** — `Grep` found nothing. The content may still exist:
1. Retry `Grep` with broader or alternative keywords / regex patterns
2. If still empty, do a targeted manual scan — `Glob` + `Read` in the most likely directories based on context (e.g. searching for a project → start with `~/Documents/obsidian/My Note/Projects/`). Stop as soon as matches are found; don't scan the entire vault.

---

## Edge Case Handling

| Situation | Handling |
|-----------|---------|
| **Incomplete information** | List the missing items; ask whether to proceed |
| **Data conflict** | Priority order: Obsidian > Jira > logs; remind the user to sync |
| **Partial success** | Mark which steps succeeded/failed; ask whether to retry the failed parts |

---

## Escalate to User

Situations that require a user decision:

- **Confirmation** — deletion / overwrite confirmation
- **Data conflict** — inconsistency across multiple sources
- **Risk of data loss** — any operation that may lose data
- **Ambiguity** — unable to determine user intent

---

**Last updated**: 2026-03-10
