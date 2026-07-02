---
description: Suggest tests worth writing for a feature using the ZOMBIES heuristic (Zero, One, Many, Boundaries, Interface, Exceptions, Simple scenarios). Pass a free-text feature description, or omit to use the current branch's diff.
---

# ZOMBIES

## Arguments

If the user provides a feature description, treat it as a **free-text feature description** (e.g. "sign-in code login flow", "image upload validation"). Locate the relevant code and tests using search tools.

If no feature is described, run `git diff main...HEAD` and use the diff as the feature scope.

## Goal

Identify the **most valuable tests to write** for the feature, using ZOMBIES as a thinking tool. The output is a list of test ideas the user can stub out themselves — **do not write or stub the tests**.

ZOMBIES stands for:

- **Z**ero — no inputs / empty state
- **O**ne — a single input / the happy path
- **M**any — multiple inputs, ordering, pagination, concurrency
- **B**oundaries — limits, off-by-one, min/max lengths, timing edges, type edges
- **I**nterface — the contract/shape of the public API (return types, status codes, redirects)
- **E**xceptions — invalid input, failures, expired/used/missing state, auth failures
- **S**imple scenarios — the common everyday usage paths a real user takes

**Skip categories that don't apply.** Only list tests that are genuinely worth writing — quality over coverage.

## Instructions

### 1. Locate the feature
- **With feature description**: search the codebase for files matching the description. Read the implementation files and the existing test file if one exists.
- **Without feature description**: run `git diff --name-status main...HEAD` and `git diff main...HEAD`, then read the changed implementation files. Skip auto-generated files.

### 2. Generate ZOMBIES suggestions
For each ZOMBIES letter, ask: *is there a test here that would catch a real bug or document real behaviour?* If yes, list it. If no, skip the letter.

**Cross-reference against existing tests.** Skip behaviours already fully covered. Keep partially-covered behaviours prefixed with `[partial]`.

Suggestion quality bar:
- **Specific, not generic.** "Test maximum email length (255 chars)" beats "Test boundaries".
- **Reference real values from the code** when possible.
- **One test per bullet.**
- **Phrase as a behaviour to verify**, not as a method name.

### 3. Output the report
Group by feature area first, then by ZOMBIES letter. Letters always appear in ZOMBIES order. Use this format:

```
## 🧟 [Feature Area]

**Boundaries**
- Email field rejects values longer than 255 chars (matches migration column)
- Sign-in code expires exactly at the 15-minute mark

**Exceptions**
- Expired code returns a validation error
- Already-used code cannot be redeemed twice

**Simple**
- Requesting a code emails the user and creates a `SignInCode` row
- [partial] valid code logs the user in — existing test asserts redirect but not code consumption
```

End with: `X test ideas.`

If nothing worth testing: `✅ Nothing worth writing tests for.`

## Rules

- **Don't stub the tests.** Ideas only.
- **Skip letters that don't apply.** No "(none)" placeholders.
- **Gaps only.** Skip already-covered behaviours.
- **Always preserve ZOMBIES order.**
- **Be specific.** Reference actual values from the code.
- **One behaviour per bullet.**
- **No implementation hints.**
- **Group by feature first, then by letter.**
- **No preamble.** Start with the first heading.
- **No closing advice** beyond the summary line.
