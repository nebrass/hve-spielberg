# Agent Skills

This repo ships the **hve-spielberg** agent skill via [vercel-labs/skills](https://github.com/vercel-labs/skills). `SKILL.md` lives at the repository **root** (a single-skill layout), so the skills CLI discovers it directly — there is no `skills/` wrapper.

## Install

```bash
# Project install — auto-detects your agent and writes to its project skills home
npx skills add nebrass/hve-spielberg

# Global install (Claude Code is the default agent)
npx skills add nebrass/hve-spielberg --global

# Global install for GitHub Copilot CLI (~/.copilot/skills/)
npx skills add nebrass/hve-spielberg --agent github-copilot --global
```

The CLI auto-detects which coding agents you have installed and resolves the correct scanned skills home for each — you never hand-pick a path.

## Plugin manifest

Only **Claude Code** reads a plugin manifest; it ships at the repo root and points its skills source at `./` (the repo root holds `SKILL.md`), not `./skills/`:

- `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` — Claude Code (verified)

MIT-licensed, matching this repository.

## Native skill discovery (no manifest)

**GitHub Copilot CLI**, **OpenCode**, **Pi**, **Codex**, and **Cursor** need no manifest — they discover skills by directory convention and read the same Agent Skills `SKILL.md` format. They scan overlapping homes, all of which `npx skills add nebrass/hve-spielberg` writes into (`.agents/skills/` for a project install, `~/.claude/skills/` etc. for global):

- **OpenCode** — `.claude/skills/`, `~/.claude/skills/`, `.agents/skills/`, `~/.agents/skills/`, `.opencode/skills/`, `~/.config/opencode/skills/`
- **Pi** — `~/.pi/agent/skills/`, `~/.agents/skills/`, `.pi/skills/`, project `.agents/skills/` (once trusted)
- **Codex** — `$CWD/.agents/skills/`, `$REPO_ROOT/.agents/skills/`, `$HOME/.agents/skills/`, `/etc/codex/skills/`
- **Cursor** — `.agents/skills/`, `.cursor/skills/`, `~/.agents/skills/`, `~/.cursor/skills/`, plus `.claude/skills/` and `.codex/skills/`

`npx skills add nebrass/hve-spielberg` installs a `<name>/SKILL.md` subdir into a scanned home, so all of these pick it up natively (see the agent sections in [`README.md`](README.md)). Skill loading follows each agent's documented convention; a full Phase 0→5 run on the non-verified agents is not yet confirmed (end-to-end render is proven on Claude Code and GitHub Copilot CLI).

## Using the skill

Once installed, start it with `/hve-spielberg` (a slash command on Claude Code; invoke by name or intent on GitHub Copilot CLI — run `/skills` there to confirm it loaded). It runs a 6-phase video production pipeline — see [`SKILL.md`](SKILL.md) and [`README.md`](README.md).
