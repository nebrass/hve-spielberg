# Project Plan — hve-spielberg promo

**Mode:** promo
**Aspect:** 16:9 1920×1080
**Visual identity strategy:** design-system
**Design system:** vercel
**HyperFrames style:** none
**Duration:** 60s
**Created:** 2026-05-26

This is **hve-spielberg's own promo video**, built by the pipeline it promotes. The video sells the skill; the rendered MP4 is the demo.

## Phase Tracker

| Phase | Status | Notes |
|-------|--------|-------|
| 0. Discovery | ✅ done | Subject is hve-spielberg itself — no external product brief needed |
| 1. Storytelling | ✅ done | 5-scene 60s promo arc with end-to-end-pipeline emphasis |
| 2. Capture | ⬜ skipped | Pipeline subject; no app to capture. Mockups hand-authored as HTML. |
| 3. Design | ✅ done | DESIGN.md seeded from `design-systems/vercel/DESIGN.md` |
| 4. Production | ✅ done | 5 scene templates + root index.html |
| 5. Audio & Render | 🟡 in-progress | Voiceover via ElevenLabs (Matilda), Whisper-verify via `npx hyperframes transcribe`, Freesound music, ffmpeg mix, `npx hyperframes render` |

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-26 | Promo mode, 60s | Long enough to show the 6-phase pipeline as a feature beat; short enough to ship as a launch asset |
| 2026-05-26 | 16:9 1920×1080 | Horizontal — web/embed default for the README |
| 2026-05-26 | Vercel design system | hve-spielberg is a developer tool; Geist + sharp black-on-white + flash-through-white transitions fit the "instant, engineered" voice we want |
| 2026-05-26 | Voice: Matilda | Warm-but-authoritative female — sells "the skill that thinks before it renders" better than the broadcast-tone alternatives |
| 2026-05-26 | End-to-end pipeline emphasis (not speed, not design thinking alone) | The 6-phase shape IS the differentiator — leading with it is the strongest hook |
