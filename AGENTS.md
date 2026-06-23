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

## Native plugin manifests

For agents that load native plugins, per-agent manifests are provided at the repo root. Each points its skills source at `./` (the repo root holds `SKILL.md`), not `./skills/`:

- `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` — Claude Code (verified)
- `.codex-plugin/plugin.json` — Codex (experimental — manifest provided, not yet verified end-to-end)
- `.cursor-plugin/plugin.json` — Cursor (experimental — manifest provided, not yet verified end-to-end)

All manifests are MIT-licensed, matching this repository. End-to-end loading + render is currently proven on **Claude Code** and **GitHub Copilot CLI** only.

## Using the skill

Once installed, start it with `/hve-spielberg` (a slash command on Claude Code; invoke by name or intent on GitHub Copilot CLI — run `/skills` there to confirm it loaded). It runs a 6-phase video production pipeline — see [`SKILL.md`](SKILL.md) and [`README.md`](README.md).
