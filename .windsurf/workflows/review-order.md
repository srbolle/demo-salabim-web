---
description: Prepare a structured, scannable review checklist for a branch or diff, grouped by feature change and applying the four-pass review order (Types, Data Flow, Business Logic, Edge Cases) within each feature. Use when the user asks to "prep a review", "review order", or wants a checklist to manually walk through changes.
---

# Review Order

## Arguments

Parse the user's request for a **base branch** to diff against. If none specified, default to `main`.

## Goal

Produce a **scannable map** of the changes between the base branch and `HEAD`, grouped by feature and following the four-pass review order (Types → Data Flow → Business Logic → Edge Cases) within each feature.

Every bullet needs a `file:line` so the user can click straight in. Keep prose minimal.

**Do not perform the review. Do not make suggestions. Do not flag things to verify. Do not propose fixes.**

Your job is purely descriptive: name the types, point at where data flows, state what the logic does, and point at where edge-case surfaces live.

## The review order

1. **Types and interfaces first.** Data shapes the code expects and produces.
2. **Data flow second.** Where data comes in, gets transformed, and goes out.
3. **Business logic third.** What the code does — methods, guards, branches.
4. **Edge cases last.** Locations where edge-case surfaces exist (branches, nullable values, external input, concurrent paths).

## Instructions

### 1. Get the diff
Run `git diff <base>...HEAD` and `git diff --name-status <base>...HEAD`. If no changes, tell the user and stop.

### 2. Read the changed files
Read enough to categorise each file. Skip auto-generated files.

### 3. Identify the feature changes
Group into distinct user-facing or behavioural changes. A feature is a coherent unit of behaviour, not a file or layer.

### 4. Output the map

```
## Feature: [short name]

One sentence describing the behaviour.

### 1. Types & Interfaces
- `path/file.php:12` — new `subscribers` BelongsToMany on `Idea`

### 2. Data Flow
- `path/controller.php:23` — entry: `POST /x` → invokable

### 3. Business Logic
- `path/observer.php:22` — short-circuit on `is_internal`

### 4. Edge Cases
- `path/observer.php:25` — `Auth::id()` is null in queue/console contexts
```

Omit a section if nothing fits.

## Rules

- **Every bullet has a `file:line`.**
- **One short clause per bullet.** Under ~15 words after the em-dash.
- **No suggestions, no advice, no questions.** State facts only.
- **No emojis.**
- **Description over prescription.**
- **Edge Cases name the surface, not the fix.**
- **Group by feature, not by review pass.**
- **Order features by blast radius.**
- **Skip auto-generated files.**
