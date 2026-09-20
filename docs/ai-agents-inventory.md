# AI Agents Inventory — youtube-downloader

Repo: `youtube-downloader` (Python CLI YouTube downloader, Python 3.x + `yt-dlp`)
Workspace: `~/Desktop/SandBox/projects/youtube-downloader`
Branch: `clean-development`

## Installed agents (detected live)

| Agent | Root / CLI | System prompt / context |
|---|---|---|
| Hermes | `~/AppData/Local/hermes/` | `SOUL.md` + `memories/USER.md` + profile dirs |
| OpenCode | `~/.opencode/` | `opencode.json` + `~/.opencode/skills/` |
| Codex | `~/.codex/` | `~/.codex/agents/*.toml` + `~/.codex/config.toml` |
| Copilot | `.github/copilot-instructions.md` | `.github/agents/*.agent.md` |
| Cursor Agent | workspace `.cursorrules` | `.cursorrules` + `.cursor/rules/` |
| GitHub CLI (`gh`) | `gh` | n/a (tool, not agent) |

## Repo agent context

- Root agent file: `AGENTS.md` (workspace-wide rules + youtube-downloader overrides)
- Scope: `docs/scope/scope.md` (8 features, Tracer Bullet, GA tier, design-md included)
- Design tokens: `/design-md` covers CLI output formatting (colors, file naming, subtitle labels)
- Context adapters: `.cursorrules`, `copilot-instructions.md`

## Verification

- `docs/scope/scope.md` exists (5768 B, 95 lines) — verified
- `.github/agents/README.md` exists — verified
- `AGENTS.md` preserved (not overwritten) — verified (538 B)
- No secrets or `.env` contents exposed — verified (`.env` protected at workspace root and hermes home)
