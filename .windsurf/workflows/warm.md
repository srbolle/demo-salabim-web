---
description: Evaluate every dependency a branch pulls in — client or server, any language — against the WARM check (Worth it, Alive, Right-sized, Maintained securely). Diffs the branch against a base, finds newly added or upgraded direct dependencies across all manifests, and scores each one. Use when the user asks to "WARM check" a branch, vet new dependencies, or review what a PR adds to the dependency tree.
---

# WARM

## Arguments

Parse the user's request for a **base branch** to diff against. If none specified, default to `main`.

## Goal

Evaluate the dependencies this branch **pulls in** — added or upgraded since it diverged from the base — against the **WARM** check.

- **W**orth it? — could ~20 lines of your own code replace it?
- **A**live? — recent commits, active maintenance, real release cadence.
- **R**ight-sized? — are you pulling a whole library for one function?
- **M**aintained securely? — known vulnerabilities, unpatched issues.

Evaluate direct dependencies only. Mention transitive packages only under **M** when they carry a known advisory.

## Instructions

### 1. Find what the branch pulls in
Run `git diff --name-status <base>...HEAD` and identify changed dependency manifests (`package.json`, `composer.json`, `requirements*.txt`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.).

For each changed manifest, extract added dependencies and version bumps.

**Scope:**
- New direct dependencies → full WARM evaluation
- Version upgrades → evaluate only **A** and **M**
- Removed dependencies → ignore

If no manifests changed: `✅ No dependencies added or upgraded on this branch.` — stop.

### 2. Gather the facts
- **W**: search how the branch uses the dependency (import/require sites)
- **A**: check registry/repo for last release date and activity
- **R**: compare footprint against actual usage
- **M**: check for known advisories (use `npm audit`, `composer audit`, `pip-audit`, or web search)

If you can't verify something, mark it `?` — never fabricate.

### 3. Score and decide
Mark each letter: ✅ (fine), ⚠️ (concern), ❌ (problem), `?` (unknown).

Verdicts:
- **Keep** — no ❌, at most minor ⚠️
- **Reconsider** — ❌ on W or R
- **Patch/Pin** — ❌ on M only
- **Replace** — ❌ on A or multiple ❌s

### 4. Output the report

```
## `dayjs` — added to package.json (client)

- ✅ **Worth it** — date parsing used across 6 components
- ✅ **Alive** — last release 2 months ago
- ✅ **Right-sized** — 2KB, zero dependencies
- ✅ **Maintained securely** — no known advisories

**Verdict: Keep**
```

Order by concern: ❌ first, then ⚠️, then ✅.

End with: `N dependencies evaluated — X keep, Y reconsider, Z replace/patch.`

## Rules

- **Judge only what the branch pulls in.**
- **Direct dependencies get the full WARM.** Transitive only under M with advisories.
- **Cover client and server.** Label each with its manifest.
- **Language-agnostic.**
- **Don't fabricate facts.** Mark `?` if unverifiable.
- **One concern per bullet.**
- **Be specific and quantified.**
- **The verdict follows from the marks.**
- **No preamble.**
- **Don't change any files.** Evaluate and report only.
