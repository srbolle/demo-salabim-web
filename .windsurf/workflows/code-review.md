---
description: Code review staged changes or a specific area of the codebase. Use when the user wants a code review, asks to review staged changes, or wants feedback on a specific feature's code.
---

# Code Review

## Context

When invoked, start by gathering context:
- Run `git diff --cached` to see staged changes
- Run `git log --oneline -10` to see recent commits

## Arguments

Parse the user's request as follows:

- **Feature** (optional): A description of what part of the codebase to review (e.g. "voting functionality", "authentication", "API endpoints"). When provided, find and review all files related to this feature. When empty/omitted, review staged changes instead.

## Instructions

### Determine what to review

1. **If a feature is specified** — use search tools to find all files related to the described feature. Read those files and review them as existing code.
2. **If no feature is specified and there are staged changes** — review the staged diff.
3. **If no feature is specified and there are NO staged changes** — tell the user: "Nothing to review. Either stage changes with `git add` or specify a feature to review, e.g. 'review the voting functionality'." Then stop.

### Perform the review

Read surrounding source files as needed to understand context. Organize findings by file, then by severity.

### Severity levels

1. **🔴 Critical** — Bugs, security vulnerabilities, data loss risks, or crashes. Must be fixed.
2. **🟠 Error** — Logic errors, missing error handling, broken edge cases. Very likely to cause problems.
3. **🟡 Warning** — Code smells, performance concerns, potential edge cases, maintainability issues.
4. **🔵 Suggestion** — Better approaches, readability improvements, idiomatic alternatives.
5. **⚪ Nitpick** — Style, naming, formatting, minor preferences. Totally optional.

### Output format

Group findings by severity. Each severity level that has findings should be its own heading (e.g. `## 🔴 Critical`, `## 🟠 Error`, etc.). Within each severity heading, list the findings. For each finding, include:
- The file and line reference
- A concise description of the issue
- A suggested fix or alternative (when applicable)

Omit severity headings that have no findings.

End with a `## Summary` section: overall assessment, whether changes look good to merge (or code looks healthy), and a count of findings per severity level.
