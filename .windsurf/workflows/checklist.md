---
description: Convert the current plan, code review, or structured content in context into a persistent markdown checklist file. Use when the user wants to turn a plan or review into a trackable checklist.
---

# Checklist

## Your task

Convert the most recent structured content in this conversation (plan, code review, task list, implementation steps, etc.) into a markdown checklist file saved to the project.

## Instructions

### 1. Identify the content

Find the most recent plan, code review, implementation steps, or other structured content in the conversation.

### 2. Generate a name

Derive a short, descriptive kebab-case name from the content's topic (e.g., `auth-refactor`, `api-migration`). Save as `.windsurf/plans/<name>-checklist.md`.

### 3. Check for existing file

If the file already exists, ask whether to overwrite, rename, or cancel. Do NOT proceed without an answer.

### 4. Determine granularity

- **Plan from plan mode:** Keep text exactly as-is. Only add `- [ ]` to major sections.
- **Plan with clear large steps:** Add `- [ ]` at that level. Don't break down further.
- **Unstructured content:** Ask the user how to break it up before proceeding.

### 5. Convert to checklist

- Preserve original text exactly — no rewriting
- Only add `- [ ]` to top-level actionable sections
- Maintain heading hierarchy
- Leave sub-bullets/numbered lists as detail, not checkboxes

### 6. Add tracking header

```
<!-- CHECKLIST INSTRUCTIONS
IMPORTANT: When working on items in this checklist, you MUST check off each item
(change `- [ ]` to `- [x]`) AS SOON AS it is implemented/completed.
Do not wait until the end — check off each item immediately after finishing it.
This file is the source of truth for tracking progress.
-->
```

### 7. Write the file

Create `.windsurf/plans/` if needed, then save the checklist.

### 8. Confirm

Tell the user the file path and summary. Remind them items will be checked off as completed.
