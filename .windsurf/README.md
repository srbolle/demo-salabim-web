# Cascade Customizations

This directory contains **Skills** and **Workflows** that customize [Cascade](https://docs.windsurf.com/windsurf/cascade) — the AI assistant in Windsurf.

Adapted from [unlearndev/skills](https://github.com/unlearndev/skills) (originally built for Claude Code).

## Skills (auto-invoked)

Skills are picked up automatically by Cascade when your prompt matches the skill's description. You can also invoke them explicitly with `@skill-name`.

| Skill | What it does |
|---|---|
| `spec-generator` | Turn a rough idea into a structured product specification (`spec.md`) |
| `feature-generator` | Expand a `spec.md` into a dependency-ordered `features.md`, or sync changes between the two |

## Workflows (manual `/command`)

Workflows are triggered explicitly via slash commands in Cascade.

| Command | What it does |
|---|---|
| `/code-review` | Review staged changes or a specific feature area, with severity-ranked findings |
| `/first-five` | Quick safety scan: Error Handling, Input Boundaries, External Calls, State Mutations, Assumed Dependencies |
| `/zombies` | Suggest tests worth writing using the ZOMBIES heuristic (Zero, One, Many, Boundaries, Interface, Exceptions, Simple) |
| `/triage` | Risk-tier map of branch changes grouped by feature area |
| `/review-order` | Four-pass review checklist (Types → Data Flow → Business Logic → Edge Cases) |
| `/warm` | Vet new dependencies: Worth it, Alive, Right-sized, Maintained securely |
| `/preflight` | Production pre-merge checklist (migrations, env vars, workers, etc.) |
| `/checklist` | Convert the current plan or review into a trackable markdown checklist |

## Structure

```
.windsurf/
├── skills/                          # Auto-invoked by Cascade
│   ├── spec-generator/SKILL.md
│   └── feature-generator/SKILL.md
└── workflows/                       # Manual via /slash-command
    ├── checklist.md
    ├── code-review.md
    ├── first-five.md
    ├── preflight.md
    ├── review-order.md
    ├── triage.md
    ├── warm.md
    └── zombies.md
```

## Skills vs Workflows

| | Skills | Workflows |
|---|---|---|
| **Invocation** | Automatic (model decides) or `@mention` | Manual only via `/command` |
| **Structure** | Folder with `SKILL.md` + optional resources | Single `.md` file |
| **Best for** | Tasks that should trigger contextually | Tasks you always invoke explicitly |
