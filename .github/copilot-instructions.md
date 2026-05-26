# Copilot Instructions — hve-spielberg

## What this repo is

This repo **is a Claude Code skill** (`hve-spielberg`), not a typical application. The "source" is prompt content (markdown) plus two Python helper scripts. There is no build system, no test suite, no lint config — the skill is consumed by future Claude Code sessions that invoke `/hve-spielberg <project-dir>`.

The renderer is **HyperFrames** (HTML + GSAP, rendered via headless Chromium). React/Remotion are **not** used.

Keep two scopes distinct when editing:

- **This repo** — the skill definition (`SKILL.md`, `workflows/`, `templates/`, `patterns/`, `scripts/`, `design-systems/`). Edits here change behavior for *all* users.
- **Generated video projects** — created by the skill at runtime in `{project-dir}/`. They contain `project-plan.md`, `context.md`, `storyboard.md`, `DESIGN.md`, `public/screenshots/`, `scenes/*.html`, `index.html` (root HyperFrames composition), `voiceover.mp3`, `out/final.mp4`. These do **not** live in this repo (except the canonical reference build under `example/`).

## Architecture

`SKILL.md` is the orchestrator prompt. It loads first, decides the entry mode (`new` / `continue` / `jump`), and dispatches to one of six phase workflows. Each phase has a user-approval checkpoint before advancing.

```
SKILL.md (orchestrator)
  ├─ workflows/phase-0-discovery.md     → produces context.md
  ├─ workflows/phase-1-storytelling.md  → produces storyboard.md
  ├─ workflows/phase-2-capture.md       → produces public/screenshots/ (via Chrome DevTools MCP)
  ├─ workflows/phase-3-design.md        → produces DESIGN.md + scenes/*.html (via hyperframes skill)
  ├─ workflows/phase-4-production.md    → produces root index.html composition (via hyperframes skill)
  └─ workflows/phase-5-audio.md         → produces voiceover.mp3 + background-music.mp3 + out/final.mp4
                                          (npx hyperframes render)
```

**Phase prerequisites are enforced in `jump` mode** — see `SKILL.md`. When editing workflows, preserve the file-presence contract:

- Phase 1 needs `context.md`
- Phase 2 needs `context.md` + `storyboard.md`
- Phase 3 needs `public/screenshots/`
- Phase 4 needs context + storyboard + `DESIGN.md` + `scenes/*.html`
- Phase 5 needs `index.html` (root composition) and passing `npx hyperframes lint|inspect|validate`

**External dependencies the skill calls out to:**

- `mcp__chrome-devtools__*` for app capture (Phase 2)
- The `hyperframes` Claude Code skill for HTML/GSAP authoring rules (Phases 3 + 4) — distinct from the `hyperframes` npm CLI
- The `gsap` skill (optional companion) for choreography reference
- `npx hyperframes` CLI for `init`, `lint`, `preview`, `inspect`, `validate`, `render`, plus `transcribe` (preferred timing verifier in Phase 5 — falls back to standalone Whisper) and `tts` (no-API-key fallback when `ELEVENLABS_API_KEY` is unset)
- `scripts/generate_voiceover.py` → ElevenLabs API + optional Whisper transcription (Phase 5)
- `scripts/search_music.py` → Freesound API for CC music (Phase 5)

`templates/` files are copied into generated projects. `patterns/` files are referenced for visual techniques. `patterns/INDEX.md` is the wayfinding map between local patterns and the deeper `hyperframes` skill references — read it before adding new pattern files. `patterns/metallic-swoosh.md` documents *why* clipPath transitions are banned (black-sliver artifacts).

`design-systems/<slug>/DESIGN.md` is the brand spec consumed by Phase 3 Path A — MIT-licensed, video-focused, authored by this skill. The canonical research source for new contributions is [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) (MIT, 73 brands, has a `npx getdesign add <slug>` CLI). The skill is **video-only** — it does not produce, render, or analyse web/UI artifacts.

## Working with the skill scripts

The Python scripts run inside generated video projects, not from this repo. They self-install `requests` via pip on first run.

```bash
# Voiceover generation (from inside a generated project)
ELEVENLABS_API_KEY=... python3 scripts/generate_voiceover.py

# Music search (from inside a generated project)
FREESOUND_API_KEY=... python3 scripts/search_music.py
```

Both `ELEVENLABS_API_KEY` and `ELEVEN_LABS_API_KEY` are accepted (back-compat).

There is no test/lint/build command for this repo. Validation of skill changes happens by running `/hve-spielberg <project-dir>` end-to-end in Claude Code; the canonical reference build is `example/` (run `example/voiceover.py` then `npx hyperframes render` to reproduce its `out/final.mp4`).

## Editing rules — DON'Ts that are easy to violate

These are enforced verbally in the `## DON'Ts` section of `SKILL.md`. If you modify workflows or patterns, do not reintroduce them:

- **No jitter** (shaking, vibrating motion).
- **No 360° scene spins.** Subtle `rotateY` ≤ 8° / `rotateZ` ≤ 4° on mockups only.
- **No 3D transforms in transitions.** 2D only (opacity, position, scale, gradient masks).
- **No clipPath transitions.** They cause anti-aliased black slivers; use crossfade + shine overlay (see `patterns/metallic-swoosh.md`).
- **No exit animations except on the closing scene.** The inter-scene transition owns the exit.
- **Never animate `display`, `visibility`, or call `.play()` inside a timeline.** Breaks HyperFrames' deterministic seek; use `opacity` + `pointer-events`.
- **Never animate `<img>` dimensions directly.** Wrap the `<img>` in a non-timed `<div>` and animate the wrapper's `transform`. Direct dimension tweens trigger layout recompute that breaks deterministic seek.
- **Never use `tl.from()` for opacity tweens with stagger.** GSAP records the END state at registration; if CSS rest is `opacity:0` the recorded end stays `opacity:0`. Always use `tl.fromTo(target, {opacity:0,...}, {opacity:1,...}, pos)`. See `patterns/visual-patterns.md` § "tl.from() stagger trap".

Anti-slop content rules (see `patterns/anti-slop.md`) also matter: no default Tailwind indigo/purple gradients (`#6366f1`, `#4f46e5`, etc.), no emoji as feature icons, no invented metrics, no lorem-ipsum filler.

## Common edits

- **Add a voice** → update both the `## ElevenLabs Voice IDs` table in `SKILL.md` and the `## Voices` table in `README.md` (the two tables must stay in sync).
- **Change phase logic** → edit the relevant `workflows/phase-N-*.md`; update the prerequisite list in `SKILL.md` if a new required file is introduced.
- **Adjust prerequisite checks** → the `## Prerequisites` block in `SKILL.md` (runs at skill entry).
- **Bump skill metadata** → frontmatter at top of `SKILL.md` (especially `allowed-tools` if a new MCP tool is needed).
- **Add a pattern file** → also register it in `patterns/INDEX.md` so phase workflows can find it.

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

Commits follow Conventional Commits (`feat`, `fix`, `docs`, `style`, `refactor`, `chore`). Recent history shows scoped forms like `feat(audio):`, `docs:`, `style(readme):`, `fix(readme):` — match the existing scope style. License is MIT.
