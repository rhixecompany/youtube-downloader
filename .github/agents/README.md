# Agent Context — youtube-downloader

This directory holds the agent-specific context files for this repo.

## Source of truth

| File | Purpose |
|---|---|
| `AGENTS.md` (repo root) | Workspace-wide agent rules + youtube-downloader overrides |
| `docs/scope/scope.md` | Living scope (8 features, Tracer Bullet, GA tier, design-md) |
| `docs/ai-agents-inventory.md` | Installed agent inventory (live-detected) |
| `copilot-instructions.md` (repo root) | Copilot adapter |
| `.cursorrules` (repo root) | Cursor Agent adapter |

## Workflow tier

- Project default: **GA** (`/check verify` → `/test` → `/check review` → `/document`)
- Per-feature overrides: none set (inherit GA)

## Design tokens

`/design-md` covers CLI output formatting (log colors, file naming patterns, subtitle format labels, spacing for multi-line output). The design spec lives at `docs/design.md` (to be created by `/design-md`).

## Next step recommendation

For each planned feature (`design.md`, output customization, tooling`): `/architect <feature>` to capture the spec, then `/develop <feature>` to build with milestone rollup, then follow the GA verification chain.
