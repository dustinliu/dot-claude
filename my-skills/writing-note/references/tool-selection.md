# Tool Selection Guide

## Vault Operations

All note operations use Obsidian MCP tools with **vault-relative paths** — no absolute path prefix needed.

```
# Correct
read_note("Work/Projects/API-Gateway/API-Gateway.md")
list_files("Work/Meetings/2026/02")

# Wrong
read_note("/Users/dustinl/Documents/obsidian/My Note/Work/Projects/...")
```

## Non-Vault File Operations

For files outside the vault (skill references, assets, system operations), use the standard file tools: `Read`, `Edit`, `Write`, `Glob`, `Grep`, `Bash`.

---

**Last updated**: 2026-03-10
