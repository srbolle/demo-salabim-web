---
description: Triage a branch or diff by grouping changed files into feature areas, assigning each a risk tier (High/Medium/Low), and producing a scannable summary that helps decide where to spend review time. Use when the user asks to "triage" a branch, PR, or diff.
---

# Triage

## Arguments

Parse the user's request for a **base branch** to diff against. If none specified, default to `main`.

## Goal

Produce a **risk-ordered map** of the changes between the base branch and `HEAD`, grouped by feature area, so the user can decide where to spend their review time. This is a triage report — not a review.

**Do not perform the review. Do not make suggestions. Do not propose fixes.**

## Instructions

### 1. Get the diff
Run `git diff --name-status <base>...HEAD` for a file-level overview, then `git diff <base>...HEAD` to see the actual changes. If there are no changes, tell the user and stop.

### 2. Read the changed files
Read enough of each file to understand what feature area it belongs to and how risky it is.

### 3. Group by feature area
Group files by **what the code does**, not by file type. Good: "Authentication", "Notification Delivery". Bad: "Controllers", "PHP Files".

Each file appears in exactly one group. Keep group names short (2–4 words).

### 4. Assign a risk tier
**Always High** if the group:
- Touches authentication or authorization
- Mutates user data, payments, or billing
- Modifies permissions or access control
- Handles sensitive data (passwords, tokens, PII)

**Bump up one tier** if the group:
- Has complex conditionals or branching logic
- Interacts with external services or APIs
- Contains a large amount of generated code (100+ lines)

### 5. Identify auto-generated files
Auto-generated files go in a "Skip" section at the bottom (lockfiles, compiled assets, generated types).

### 6. Output the report

```
### ⚠️ High Risk

**[Feature Area Name]**
Reason: [one sentence explaining why this is high risk]
- path/to/file.php (added/modified)

### Medium Risk

**[Feature Area Name]**
Reason: [one sentence]
- path/to/file.php (added)

### Low Risk

**[Feature Area Name]**
- path/to/file.php (modified)

### Skip

**Auto-generated**
- path/to/generated/files... (auto-generated — skip)
```

End with: `X groups, Y high-risk files to focus on`.

## Rules

- **Group by feature area, not by file type.**
- **One group per file.**
- **Group names: 2–4 words.**
- **One-line reason per group** (High and Medium only).
- **Status suffix on each file**: `(added)`, `(modified)`, or `(deleted)`.
- **Order tiers from highest to lowest risk.**
- **Omit empty tier sections.**
- **No suggestions, no advice.** This is a triage map.
- **No emojis** other than ⚠️ on High Risk heading.
