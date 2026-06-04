# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This repo **is a Claude Code skill** (`hve-spielberg`), not a typical application. The "source" is prompt content (markdown) plus two Python helper scripts. There is no build system, no test suite, no lint config — the skill is consumed by future Claude Code sessions that invoke `/hve-spielberg <project-dir>`.

The renderer is **HyperFrames** (HTML + GSAP, rendered via headless Chromium). React/Remotion are no longer used.

Two things to keep distinct:

- **This repo** — the skill definition (`SKILL.md`, `workflows/`, `templates/`, `patterns/`, `scripts/`, `design-systems/`) plus the canonical demo (`example/`). Edits here change behavior for *all* users.
- **Generated video projects** — created by the skill at runtime in `{project-dir}/`. They contain `project-plan.md`, `context.md`, `storyboard.md`, `DESIGN.md`, `public/screenshots/`, `scenes/*.html`, `index.html` (root HyperFrames composition), `voiceover.mp3`, `out/final.mp4`. These do not live in this repo (except `example/`, which is *this skill's own* generated project, committed as the reference build).

## Architecture

`SKILL.md` is the orchestrator prompt. It loads first, decides the entry mode (`new` / `continue` / `jump`), and dispatches to one of six phase workflows. Each phase has a user-approval checkpoint before advancing.

```
SKILL.md (orchestrator)
  ├─ workflows/phase-0-discovery.md     → produces context.md
  ├─ workflows/phase-1-storytelling.md  → produces storyboard.md
  ├─ workflows/phase-2-capture.md       → produces public/screenshots/ (via Chrome DevTools MCP)
  ├─ workflows/phase-3-design.md        → produces DESIGN.md + scenes/*.html (via hyperframes skill)
  ├─ workflows/phase-4-production.md    → produces root index.html composition (via hyperframes skill)
  └─ workflows/phase-5-audio.md         → produces voiceover.mp3 + background-music.mp3 + out/final.mp4 (npx hyperframes render)
```

**Phase prerequisites are enforced in `jump` mode** — see `SKILL.md`. When editing workflows, preserve the file-presence contract:
- Phase 1 needs `context.md`
- Phase 2 needs `context.md` + `storyboard.md`
- Phase 3 needs capture artifacts (`public/screenshots/` and/or `public/clips/`)
- Phase 4 needs context + storyboard + `DESIGN.md` + `scenes/*.html`
- Phase 5 needs `index.html` (root composition) and passing `npx hyperframes lint|inspect|validate`
- Tutorial content mode prefers `public/clips/` but degrades to stills with a warning when clips are absent (warn-don't-block, spec §7.3); only missing captions is a hard check in tutorial mode

**External dependencies the skill calls out to:**
- `mcp__chrome-devtools__*` for app capture (Phase 2)
- The `hyperframes` skill for HTML/GSAP authoring rules (Phases 3 + 4)
- The `gsap` skill (optional companion) for choreography reference
- `npx hyperframes` CLI for `init`, `add` (pull catalog blocks, Phase 4), `lint`, `preview`, `inspect`, `validate`, `render`, `doctor` (render-environment diagnostics, Phase 5), `transcribe` (preferred voiceover-timing verifier in Phase 5; falls back to standalone Whisper if unavailable), and `tts` (used in Phase 5 as the no-API-key fallback when `ELEVENLABS_API_KEY` is unset)
- `mcp__chrome-devtools__screencast_*` + `resize_page` for Phase-2 web-clip capture (experimental, feature-detected — needs `--experimentalScreencast=true`; falls back to screenshots), and optional `asciinema`+`agg` for CLI clip recording (otherwise the authored-terminal path)
- `scripts/generate_voiceover.py` → ElevenLabs API + optional Whisper transcription (Phase 5)
- `scripts/search_music.py` → Freesound API for CC music (Phase 5)

`templates/` files are copied into generated projects. `patterns/` files are referenced for visual techniques — `metallic-swoosh.md` documents *why* clipPath transitions are banned (black-sliver artifacts).

## Working with the skill scripts

The Python scripts run inside generated video projects, not from this repo. They self-install `requests` via pip on first run.

```bash
# Voiceover generation (from inside a generated project)
ELEVENLABS_API_KEY=... python3 scripts/generate_voiceover.py

# Music search (from inside a generated project) — query is a required argument
FREESOUND_API_KEY=... python3 scripts/search_music.py "cinematic corporate uplifting"
```

Both `ELEVENLABS_API_KEY` and `ELEVEN_LABS_API_KEY` are accepted (back-compat).

## Editing rules — DON'Ts that are easy to violate

These are enforced verbally in the `## DON'Ts` section of `SKILL.md`. If you modify workflows or patterns, do not reintroduce them:

- **No jitter** (shaking, vibrating motion).
- **No 360° scene spins.** Subtle `rotateY` ≤ 8° / `rotateZ` ≤ 4° on mockups only.
- **No 3D transforms in transitions.** 2D only (opacity, position, scale, gradient masks).
- **No clipPath transitions.** They cause anti-aliased black slivers; use crossfade + shine overlay (see `patterns/metallic-swoosh.md`).
- **No exit animations except on the closing scene.** The inter-scene transition owns the exit.
- **Never animate `display`, `visibility`, or call `.play()` inside a timeline.** Breaks HyperFrames' deterministic seek; use `opacity` + `pointer-events`.
- **Never animate `<img>` dimensions directly.** Wrap the `<img>` in a non-timed `<div>` and animate the wrapper's `transform`. Direct dimension tweens trigger layout recompute that breaks deterministic seek.
- **Never use `tl.from()` for opacity tweens.** GSAP records the end-state at registration; if the CSS rest is `opacity:0` the recorded end is `opacity:0` (the tween goes nowhere), and under stagger later instances re-hide elements earlier ones revealed. Always use `tl.fromTo(target, {opacity:0,...}, {opacity:1,...}, pos)`.

## Common edits

- **Add a voice** → update both the `## ElevenLabs Voice IDs` table in `SKILL.md` and the `## Voices` table in `README.md` (the two tables must stay in sync).
- **Change phase logic** → edit the relevant `workflows/phase-N-*.md`; update the prerequisite list in `SKILL.md` if a new required file is introduced.
- **Adjust prerequisite checks** → the `## Prerequisites` block in `SKILL.md` (runs at skill entry).
- **Bump skill metadata** → frontmatter at top of `SKILL.md` (especially `allowed-tools` if a new MCP tool is needed).

## Installation paths users invoke

```bash
npx skills add nebrass/hve-spielberg                      # via Skills CLI
git clone https://github.com/nebrass/hve-spielberg.git \
  ~/.claude/skills/hve-spielberg                          # manual
cp -r ~/.claude/skills/hve-spielberg \
  my-project/.claude/skills/hve-spielberg                 # per-project copy
```

When testing skill changes locally, the global install path is `~/.claude/skills/hve-spielberg/`.

## Git / release conventions

Commits follow Conventional Commits (`feat`, `fix`, `docs`, `style`, `refactor`, `chore`). Recent history shows `feat(audio):`, `docs:`, `style(readme):`, `fix(readme):` — match the existing scope style. License is MIT.
