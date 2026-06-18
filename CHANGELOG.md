# Changelog

All notable changes to the **hve-spielberg** skill are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **Phase 5 music mix now sits the soundtrack under the voice as a ducked bed.**
  The static `volume=0.22` blend in `workflows/phase-5-audio.md` is replaced with:
  music normalized to a known base (`loudnorm I=-30`), EQ space carved for speech
  (`highpass=100` + `-3 dB @ 2.5 kHz`), and **sidechain ducking** keyed off the
  voiceover so the music dips under speech and breathes back in the gaps. Mastered
  with a peak limiter (`alimiter`, ~-1 dBFS) while the voiceover's -16 LUFS
  normalization carries loudness — a dynamic `loudnorm` master was rejected
  because it rides gain and reverses the duck. `aresample` guards keep
  mismatched-rate sources working through `amix`. `example/README.md` updated to
  match.

### Fixed

- **True-peak ceiling breach in the audio master.** The old `alimiter=limit=0.95`
  could leave the final mix above the -1 dBTP target (measured true peak -0.3 dBTP); the
  new master lands well under it (~-3.8 dBTP). The Step 5.3a clip-audio re-master is
  aligned to the same ceiling.

## [0.0.3] - 2026-06-08

Added a professional, skill-driven asciinema + agg CLI recording path so
terminal scenes can be captured autonomously — no user keyboard required.
The prior Phase 2 path treated asciinema as a one-line user-side note;
this release wires it as a first-class capture source on par with Chrome
DevTools screenshots and screencast clips.

### Added

- **Autonomous asciinema recording.** The skill drives `asciinema rec
  --command "<cmd>"` itself via its Bash tool: PTY-isolated, env-scrubbed
  (`env -i HOME=$HOME PATH=$PATH SHELL=/bin/bash PS1='$ '`), and bounded
  by `timeout Ns` so runaway / non-terminating commands can't stall the
  phase. The user never opens a terminal. `agg` then renders the cast to
  MP4 in the same autonomous sequence.
- `patterns/cli-terminal-capture.md` — end-to-end guide: when to use the
  asciinema path vs. the authored-terminal fallback, install per OS,
  autonomous recording sequence, edge cases (long-running commands,
  piped input, secrets-without-leaking, PTY allocation fallback to
  `script -qc`), agg theme→palette pairing, quality gate, troubleshooting.
- `templates/scene-terminal-clip.html` — Layer-A clip-scene archetype that
  wraps the agg-rendered MP4 in a macOS-style window for brand parity
  with browser-mockup scenes. Animates the `.term-frame` wrapper only
  (respects the no-`<video>`-dimension-tween rule).
- `templates/storyboard.md` — new `Capture: terminal-clip` value plus
  required `Command:` and `Record timeout:` fields so storyboards carry
  the inputs the autonomous path needs.
- README "Updating" section documenting how to pull the latest skill
  version (carried over from Unreleased).

### Changed

- `SKILL.md` frontmatter — `description` broadened so Phase 2 reads as a
  multi-source step ("Chrome DevTools screenshots + screencast clips,
  asciinema terminal recording") instead of screenshots only;
  `allowed-tools` gains `Bash(asciinema:*), Bash(agg:*),
  Bash(timeout:*), Bash(ffprobe:*)`; prerequisites block prints an
  actionable per-OS install hint when asciinema/agg are missing.
- `workflows/phase-2-capture.md` — replaces the 3-line asciinema note
  with the full autonomous record → render → verify sequence,
  preconditions, and the edge-case matrix.
- `README.md` prerequisites table — concrete install commands and a link
  to the new pattern doc.
- `patterns/INDEX.md` and `CLAUDE.md` — register the new pattern doc and
  template so future editing sessions find them.

### Fixed

- **Clip `<video>` timing contract.** Clip scenes previously used a bare
  `<video>` and told authors *not* to add timing attributes. The runtime only
  frame-syncs videos carrying `data-start`, so with 2+ clip scenes footage
  cross-routed (one scene played another's footage, another played black)
  while `lint`/`inspect`/`validate` all passed green. Both clip templates and
  the phase-3/4 docs now mandate the explicit contract: `id` +
  `data-start="0"` + `data-duration` + `data-media-start` +
  `data-track-index="0"`. Also added to the central `## DON'Ts` list and as a
  carve-out in `patterns/transition-catalog.md`.
- **`Clip in/out` trim now lands in the scene** via `data-media-start`
  (= storyboard `Clip in`). Previously the trim was silently ignored — the
  video played from source `t=0` and desynced from Phase 5's clip-audio
  extraction (`CIN`).
- **Clips no longer blank during crossfades.** The inner video's
  `data-duration` is the scene loader's full crossfade-extended window (per
  `patterns/transition-catalog.md`), not the bare clip length — an
  expired track goes `visibility:hidden` mid-crossfade otherwise.
- **Phase 1 now surfaces `Capture: terminal-clip`** (with `Command:` /
  `Record timeout:`) so new-mode storyboards can actually trigger the
  autonomous asciinema path.
- **asciinema record env keeps `LANG`** (`LANG="${LANG:-C.UTF-8}"` through
  `env -i`) — asciinema 2.x aborts without a UTF-8 locale.
- **agg no longer passes `--cols`/`--rows`** — it reads the size from the
  cast header; the previous hardcoded `144×32` mismatched the recorded
  `175×32` and wrapped/letterboxed wide output. The intermediate GIF now goes
  to `$TMPDIR` instead of `public/clips/`, and the verify step reads
  `nb_frames` from the header instead of a full `-count_frames` decode.
- **`timeout` is feature-detected** (GNU coreutils; absent on stock macOS —
  install hint now says `brew install asciinema agg coreutils`), and the
  PTY-failure fallback documents both `script` syntaxes (GNU `-qc` vs
  BSD/macOS positional). `allowed-tools` gains `Bash(script:*)` and
  `mcp__chrome-devtools__emulate` (used for viewport + dark-mode emulation).
- **Dark-mode MutationObserver guidance inverted to the working order** —
  inject *after* `navigate_page` (navigation wipes the page's JS context;
  hydration re-renders don't navigate, so the observer survives them).
- **Mandatory hero-frame content check in Phase 4** (`inspect --at` scene
  midpoints, then read the PNGs) — the mechanical gates can't see wrong
  content; this is how the bare-`<video>` cross-route shipped unnoticed.

### Security

- **Subresource Integrity on the GSAP CDN tag.** Every `<script>` loading
  `gsap@3.14.2` from jsDelivr (4 templates, the phase-3/phase-4 skeletons, and
  all `example/` scenes) now carries `integrity="sha384-…" crossorigin="anonymous"`,
  so a tampered CDN response is rejected by the browser instead of executing in
  `preview`/render. `CLAUDE.md` documents the hash-recompute step required on any
  future GSAP version bump.

### Unchanged (by design)

- If `asciinema`/`agg` are missing, the skill silently falls back to the
  authored-terminal scene (`templates/scene-terminal.html`). No install
  prompts — the user is told once, then Phase 2 proceeds.

## [0.0.2] - 2026-06-04

Migrated the rendering engine from **Remotion** (React, server-rendered) to
**HyperFrames** (HTML + GSAP + headless Chromium) across the whole 6-phase
pipeline, then extended it with first-class video-clip capture and a new
tutorial content mode. Released via [PR #2](https://github.com/nebrass/hve-spielberg/pull/2).

### Changed

- **Rendering engine: Remotion → HyperFrames.** All six `workflows/phase-*.md`
  rewritten. New scene authoring model (sub-compositions + `data-composition-id`
  + GSAP timelines registered on `window.__timelines`) replaces Remotion JSX
  compositions. Phase contracts (the `continue`/`jump` detection logic,
  prerequisite lists, project-structure diagrams) updated end-to-end across
  `SKILL.md`, `CLAUDE.md`, and `.github/copilot-instructions.md`.
- Phase 2 capture contract generalized from "screenshots" to **capture
  artifacts** (`public/screenshots/` and/or `public/clips/`).
- `patterns/visual-patterns.md` fully rewritten for GSAP — adds the
  `tl.fromTo()` stagger-trap rule, `autoAlpha` guidance, and `tl.set` for
  late-entry elements.
- `patterns/metallic-swoosh.md` reworked as an inline root-timeline pattern
  (transitions straddle two scenes and can't be sub-comps).

### Added

- **Tutorial / walkthrough content mode** — a third mode beside promo and
  showcase: task-ordered chapters with a cold-open on the payoff, required
  baked captions, footage-time legibility punch-in for sub-24px UI text,
  a recap archetype (`templates/scene-recap.html`), a "Step N of M" / chapter
  overlay, and a ~90s segment cap. Warns-and-degrades to stills when clips are
  absent; missing captions is the only hard gate.
- **Video-clip capability** — real motion footage as a first-class,
  source-agnostic capture artifact:
  - _Capture target_ — clip-scene archetype `templates/scene-clip.html`
    ("Wiring S"): a muted `<video>` in a sub-composition, `currentTime`-synced
    by the runtime; footage-locked durations (`data-duration = (out - in) / speed`).
    Optional per-scene storyboard clip fields (`Capture`, `Clip`, `Clip in/out`,
    `Speed`, `Clip audio`, `Captions`).
  - _Capture sources_ — Chrome DevTools `screencast` for web (experimental,
    feature-detected, falls back to screenshots) and a dependency-free terminal
    path for CLI (`templates/scene-terminal.html`, with optional `asciinema`+`agg`),
    plus a footage quality gate (resolution/fps floor, one-clean-take review).
- **10 vendored brand design presets** in `design-systems/<slug>/DESIGN.md`
  (Stripe, Linear, Apple, Notion, Vercel, Airbnb, GitHub, Cal, Arc, Bento) —
  original MIT-licensed prose — plus `design-systems/CONTRIBUTING.md` codifying
  the quality bar.
- New pattern files: `patterns/INDEX.md` (wayfinding), `anti-slop.md`,
  `marker-highlight.md` (5 word-emphasis modes), `transition-catalog.md`.
- `example/` — a self-contained reference promo project built by the pipeline
  itself (storyboard, design seed, 5 scene HTMLs, `voiceover.py`,
  `example/README.md` reproduction guide).
- `CLAUDE.md` — codebase guide for future Claude Code sessions, and a top-level
  `.gitignore`.
- Opt-in clip-own audio mixed under a ducked voiceover (sidechain) in Phase 5,
  with an ffprobe gate proving it reaches `out/final.mp4`.
- CLI inventory entries `add` and `doctor`; `screencast_*` + `resize_page`
  added to `allowed-tools`.

### Fixed

- `scripts/generate_voiceover.py` hardening: absolute-path ffmpeg concat,
  list-or-dict transcript parser, `mktemp` → `mkstemp`, non-zero exit on a
  failed TTS section, guards for null word timestamps and ffprobe `N/A`
  durations, a mid-loop tempfile leak, word-level timestamps for overlap
  detection, and voiceover-overrun warnings.
- HyperFrames `lint`/`inspect`/`validate`/`render` gates take a project
  directory, not a file.
- `gsap.from()` → `tl.fromTo()` (the stagger trap) across workflows, patterns,
  and templates.
- Three rounds of Copilot review fixes plus a max-effort code-review pass
  (phase-contract, no-music audio path, audio element id, design-system refs,
  license posture, and example consistency).

### Removed

- The Remotion / React rendering path.
- The committed `example/out/final.mp4` binary (3.4 MB) — no longer tracked in
  git (regenerable build artifact; the demo lives on YouTube).

## [0.0.1] - 2026-04-28

Initial release of the hve-spielberg skill.

### Added

- 6-phase AI video production orchestrator (`SKILL.md`) with per-phase approval
  checkpoints and `new`/`continue`/`jump` entry modes: Discovery → Storytelling
  → Capture (Chrome DevTools screenshots) → Design → Production → Audio & Render
  (Remotion-based rendering).
- Promo and showcase content modes.
- ElevenLabs voiceover generation with Whisper timing verification
  (`scripts/generate_voiceover.py`).
- Freesound CC music search (`scripts/search_music.py`), switched over from an
  earlier Pixabay integration.
- README with install instructions and an MIT license.

[Unreleased]: https://github.com/nebrass/hve-spielberg/compare/v0.0.3...HEAD
[0.0.3]: https://github.com/nebrass/hve-spielberg/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/nebrass/hve-spielberg/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/nebrass/hve-spielberg/releases/tag/v0.0.1
