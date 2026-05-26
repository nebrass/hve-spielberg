# Product Context — hve-spielberg promo

## What it is

`hve-spielberg` is a Claude Code skill that produces product launch videos through a 6-phase pipeline: Discovery (design thinking) → Storytelling (narrative + storyboard) → Capture (Chrome DevTools screenshots) → Design (HyperFrames scene templates) → Production (composition + GSAP) → Audio & Render (ElevenLabs + Whisper + Freesound + headless-Chromium render).

## What this video is

A 60-second promo for hve-spielberg itself. **Built by hve-spielberg.** The video is both the demo and the marketing asset — every frame is evidence the pipeline works, not just description of what it would do.

## Audience

- Developers / indie hackers who ship products and need launch videos
- Open-source maintainers who want a real promo without hiring an agency
- Claude Code power users who want to see what an end-to-end skill looks like
- Marketing / DevRel people curious about AI-driven video production

## Goal

In 60 seconds, communicate three things:

1. **There's a real pipeline here** — not just a render endpoint. Six phases, in order.
2. **It thinks before it renders.** Discovery and storyboard are first-class; the AI doesn't skip to pixels.
3. **It's available now.** `/hve-spielberg my-project` in Claude Code.

If the viewer comes away thinking *"I'd actually try this"*, the video did its job.

## Brand intent

- **Visual identity:** Vercel design system — sharp black-on-white, Geist typography, flash-through-white transitions. Developer-tool voice. (See `design-systems/vercel/DESIGN.md`.)
- **Voice:** Matilda (ElevenLabs) — warm-but-authoritative female. "Reads like the docs were written by a senior engineer who actually likes the product."
- **Tone of script:** declarative, no marketing fluff, no "reimagine your workflow" filler. Concrete claims with verbs.

## Real product, real claims

Unlike the prior fictional "geist-y" example, this is **real**. Every claim in the script maps to a real capability:

- "Six phases, in order" — see `SKILL.md` and `workflows/phase-0..5-*.md`
- "Chrome DevTools captures your real product" — Phase 2 uses `mcp__chrome-devtools__*`
- "HyperFrames renders in headless Chrome" — Phase 4 produces `index.html`, Phase 5 runs `npx hyperframes render`
- "ElevenLabs speaks the script. Whisper verifies. Freesound scores it" — Phase 5 audio pipeline, end to end

No invented metrics. No `lorem ipsum`. Anything specific in the script is verifiable from the repo.

## Constraints

- 60 seconds total
- 16:9 1920×1080
- No real app screenshots — the "product" is a skill, not a UI. Scenes use typography + simulated terminal/CLI mockups.
- Must satisfy `patterns/anti-slop.md`: no Tailwind purple gradient hero, no emoji feature icons, no invented metrics, no filler copy.
