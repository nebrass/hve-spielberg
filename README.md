# hve-spielberg

**AI-powered video production pipeline for Claude Code and GitHub Copilot CLI.** From design thinking to final render — 6 automated phases that turn your app into a polished promo, showcase, or tutorial video.

```
/hve-spielberg
```

## Demo

[![Watch the 60-second promo](https://img.youtube.com/vi/tIsQabrczRs/maxresdefault.jpg)](https://www.youtube.com/watch?v=tIsQabrczRs)

▶ **[Watch the 60-second promo on YouTube](https://www.youtube.com/watch?v=tIsQabrczRs)** — 1920×1080, ElevenLabs voiceover (Matilda) + Freesound music. Regenerate locally via [`example/README.md`](example/README.md) § "Reproducing the render".


The promo above was built by hve-spielberg itself, end-to-end, using only what ships in this repo:

- Vercel design system (vendored at [`design-systems/vercel/DESIGN.md`](design-systems/vercel/DESIGN.md))
- Phase 3–4 HyperFrames composition ([`example/scenes/`](example/scenes/), [`example/index.html`](example/index.html))
- Phase 5 ElevenLabs voiceover (Matilda) + Freesound music (CC-BY) + ffmpeg mix
- `npx hyperframes render` → MP4 at 1920×1080, 30fps

Everything in [`example/`](example/) is the actual artifact — not a staged mock-up. To reproduce: run [`example/voiceover.py`](example/voiceover.py), then the normalize + music-mix ffmpeg steps in [`example/README.md`](example/README.md) to produce `voiceover-with-music.mp3` (the file `index.html` references — render is silent without it), then `npx hyperframes render`.

## What It Does

hve-spielberg is an agent skill (Claude Code / GitHub Copilot CLI) that orchestrates end-to-end video production:

1. **Understands your product** through design thinking (empathize, define, ideate)
2. **Builds a narrative** with scene storyboarding and emotional arc
3. **Captures your app** automatically via Chrome DevTools
4. **Authors HTML scene templates** matching your brand DNA — pick from [10 curated design systems](design-systems/) (Stripe, Linear, Apple, Notion, Vercel, Airbnb, GitHub, Cal, Arc, Bento), 8 HyperFrames named styles, or derive from screenshots
5. **Produces the video** in HyperFrames (HTML + GSAP, headless-Chromium rendered)
6. **Adds voiceover + music** with ElevenLabs TTS (or local Kokoro-82M fallback), `npx hyperframes transcribe` for timing verification, and Freesound music

### Three Modes

| Mode | Structure | Best For |
|------|-----------|----------|
| **Promo** | Hook → Pain → Solution → Features → CTA | Marketing, launches, ads |
| **Showcase** | Intro → Walkthrough → Highlights → Closer | Portfolio, demos, case studies |
| **Tutorial** | Cold Open → Step-by-Step Chapters → Recap | Walkthroughs, how-tos, onboarding |

## Pipeline

```
Phase 0: DISCOVERY         Phase 1: STORYTELLING       Phase 2: CAPTURE
├ Design thinking          ├ Narrative structure        ├ Chrome DevTools MCP
├ Codebase/feature scan    ├ Scene storyboard           ├ Auto-navigate app
├ Product context Q&A      ├ Emotional arc              ├ Screenshot key views
└ Goal/audience analysis   └ Script outline             └ Interaction states

Phase 3: DESIGN            Phase 4: PRODUCTION         Phase 5: AUDIO & RENDER
├ hyperframes skill        ├ HyperFrames root index     ├ ElevenLabs TTS
├ DESIGN.md (brand+motion) ├ Sub-composition wiring     ├ Whisper verification
├ Scene HTML templates     ├ GSAP transitions           ├ Freesound Music API
└ Per-scene preview        └ lint / inspect / validate  └ npx hyperframes render
```

Each phase has a user-approval checkpoint before proceeding to the next.

## Prerequisites

| Tool | Required | Installation |
|------|----------|-------------|
| Node.js 18+ | Yes | [nodejs.org](https://nodejs.org) |
| Python 3.10+ | Yes | [python.org](https://python.org) |
| ffmpeg | Yes | `brew install ffmpeg` / `apt install ffmpeg` |
| `chrome-headless-shell` | Yes | Used by `npx hyperframes render` for frame capture. System Chrome causes 120s render hangs. Install once: `npx puppeteer browsers install chrome-headless-shell` (one-time, ~170MB, cached). Verify with `npx hyperframes doctor`. |
| Chrome DevTools MCP | Yes | Configured in your agent's MCP settings (Claude Code or GitHub Copilot CLI) |
| `ELEVENLABS_API_KEY` | Recommended | [elevenlabs.io](https://elevenlabs.io) — higher-quality TTS. If unset, Phase 5 falls back to `npx hyperframes tts` (local Kokoro-82M, no key, lower quality). |
| `FREESOUND_API_KEY` | No | [freesound.org/apiv2/apply](https://freesound.org/apiv2/apply/) — enables CC music search |
| Whisper | Recommended | `pip install openai-whisper` — voiceover timing verification |
| `espeak-ng` | Optional | `brew install espeak-ng` / `apt install espeak-ng` — only needed for non-English voiceover via `hyperframes tts` fallback |
| `--experimentalScreencast` (chrome-devtools MCP) | No | Enables `screencast` web-clip capture; without it, web scenes fall back to screenshots. |
| `asciinema` + `agg` | No | Optional true terminal-clip recording for CLI scenes; without them, CLI scenes use the authored-terminal path. Install: `brew install asciinema agg` (macOS) · `apt install asciinema && cargo install --git https://github.com/asciinema/agg` (Debian/Ubuntu). See [`patterns/cli-terminal-capture.md`](patterns/cli-terminal-capture.md) for the full recording workflow. |

### Required Skills

hve-spielberg depends on two **companion agent skills** plus the **`hyperframes` npm package** (these are separate — the skills provide authoring prompts; the npm package provides the `hyperframes` CLI). Install the companion skills the same way as this skill — with `npx skills add` (see [Installation](#installation)), which auto-detects your agent and resolves the correct skills home for you:

| Dependency | Type | Purpose | Install |
|-----------|------|---------|---------|
| `hyperframes` skill | Agent skill | Authoring rules for HTML/GSAP compositions, sub-comps, transitions, captions | `npx skills add heygen-com/hyperframes` |
| `gsap` skill | Agent skill | Animation choreography reference (eases, timelines, stagger) | Recommended companion to the hyperframes skill |
| `hyperframes` npm package | CLI | `init`, `add` (pull catalog blocks, Phase 4), `lint`, `preview`, `inspect`, `validate`, `render`, `doctor` (render diagnostics), `transcribe` (Phase 5's preferred timing verifier, with standalone Whisper as fallback), `tts` (no-key fallback when `ELEVENLABS_API_KEY` is unset) | `npx hyperframes <command>` (auto-fetches; package: [`hyperframes`](https://www.npmjs.com/package/hyperframes), repo: [github.com/heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)) |

## Installation

The recommended install is the **[skills CLI](https://github.com/vercel-labs/skills)** — it auto-detects your agent (Claude Code, GitHub Copilot CLI) and installs into the skills home that agent actually scans, so you never hand-pick a path. The same install is discovered natively by OpenCode, Pi, Codex, and Cursor (see [below](#opencode-pi-codex--cursor-native-discovery)).

### Recommended: Skills CLI

```bash
# Project install — run from your project; writes to the agent's project skills home
npx skills add nebrass/hve-spielberg

# Global install (Claude Code is the default agent)
npx skills add nebrass/hve-spielberg --global

# Global install for GitHub Copilot CLI (~/.copilot/skills/)
npx skills add nebrass/hve-spielberg --agent github-copilot --global
```

In Copilot CLI, run `/skills` to confirm the skill is loaded.

### Fallback: manual git clone

If you can't run the CLI, clone the repo into your agent's skills home directly:

```bash
git clone https://github.com/nebrass/hve-spielberg.git ~/.claude/skills/hve-spielberg
# GitHub Copilot CLI: clone into ~/.copilot/skills/hve-spielberg instead
```

### OpenCode, Pi, Codex & Cursor (native discovery)

No plugin or manifest needed — these agents discover skills by directory convention and read the same Agent Skills `SKILL.md` format. The skills-CLI install above writes a `<name>/SKILL.md` subdir into a home each one scans, so they pick up hve-spielberg natively:

```bash
npx skills add nebrass/hve-spielberg            # project (.agents/skills/)
npx skills add nebrass/hve-spielberg --global   # global
```

- **OpenCode** — `.claude/skills/`, `~/.claude/skills/`, `.agents/skills/`, `~/.agents/skills/`, `.opencode/skills/`, `~/.config/opencode/skills/`. Docs: <https://opencode.ai/docs/skills/>.
- **Pi** — `~/.pi/agent/skills/`, `~/.agents/skills/` (global), `.pi/skills/`, `.agents/skills/` (project, after the project is *trusted*). Docs: <https://pi.dev/docs/latest/skills>.
- **Codex** — `$CWD/.agents/skills/`, `$REPO_ROOT/.agents/skills/`, `$HOME/.agents/skills/`, `/etc/codex/skills/`. Docs: <https://developers.openai.com/codex/skills>.
- **Cursor** — `.agents/skills/`, `.cursor/skills/`, `~/.agents/skills/`, `~/.cursor/skills/`, plus `.claude/skills/` and `.codex/skills/`. Docs: <https://cursor.com/docs/skills>.

Then ask for a video (e.g. "make a showcase video of this app") — the agent loads the skill on demand. Skill *loading* follows each agent's documented convention; a full Phase 0→5 run on these agents is **not yet verified** (end-to-end render is proven on Claude Code and GitHub Copilot CLI).

## Updating

Already installed an older version? Update to the latest `main`:

```bash
npx skills update hve-spielberg     # alias: upgrade · -g global · -p project · -y skip the scope prompt
```

Installed via a manual git clone instead? `cd` into the skills home you cloned to and run `git pull`.

Then **restart your agent** (Claude Code or GitHub Copilot CLI) so the updated `SKILL.md` reloads — skills are read at session start, so file changes don't apply mid-session. Run `npx skills list` to see what's installed and where.

## Quick Start

1. **Set API keys** (both optional but recommended):
   ```bash
   export ELEVENLABS_API_KEY=your_key_here    # Phase 5 falls back to local Kokoro TTS if unset
   export FREESOUND_API_KEY=your_key_here     # Phase 5 falls back to user-provided / no music if unset
   ```

2. **Start the skill:**
   ```
   /hve-spielberg
   ```
   On **Claude Code** this is a slash command. On **GitHub Copilot CLI**, invoke it by name or intent (e.g. "use hve-spielberg to make a promo video"); run `/skills` to confirm it's loaded. Append the same arguments either way (e.g. `--mode continue`).

3. **Follow the prompts.** Phase 0 → 5 is interactive; each phase has a user-approval checkpoint before advancing. The discovery questions include:
   - **Mode**: Promo, Showcase, or Tutorial
   - **Duration + theme + aspect ratio**: 30s/60s/90s, light/dark, 16:9/9:16/1:1/4:5
   - **Visual identity strategy**: pick a [vendored brand](design-systems/) (fastest), pick a HyperFrames named style (medium), or derive from screenshots (most adaptive)
   - **Voice**: Matilda / Rachel / Daniel / Josh (ElevenLabs), or any of 54 Kokoro voices
   - **Storyboard review** before Phase 2 capture
   - **Design review** after Phase 3 scene templates
   - **Composition preview** after Phase 4 root index.html
   - **Music search** after Phase 5 voiceover

4. **Get your video:**
   ```
   out/final.mp4  — chosen aspect (16:9 / 9:16 / 1:1 / 4:5), voiceover + music, H.264 + AAC
   ```

## Entry Modes

| Mode | Command | When |
|------|---------|------|
| `new` (default) | `/hve-spielberg` | Start a fresh video from scratch |
| `continue` | `/hve-spielberg --mode continue` | Resume where you left off |
| `jump` | `/hve-spielberg --mode jump --phase 3` | Jump to a specific phase (1–5) |

## Voices

| Voice | Style | Voice ID |
|-------|-------|----------|
| Matilda (default) | Warm, confident female | `XrExE9yKIg1WjnnlVkGX` |
| Rachel | Calm, clear female | `21m00Tcm4TlvDq8ikWAM` |
| Daniel | Authoritative male | `onwK4e9ZLuTAKqWW03F9` |
| Josh | Friendly, conversational male | `TxGEqnHWrfWFTfGW9XjX` |

**No-key fallback (Kokoro-82M):** when `ELEVENLABS_API_KEY` is unset, Phase 5 uses `npx hyperframes tts` — 54 local voices across 8 languages (e.g. `af_nova`, `af_heart`). List them with `npx hyperframes tts --list`; see the HyperFrames skill's `references/tts.md` for the full catalog.

## Music Strategy

No bundled audio files. Three-tier approach:

1. **Freesound API** — Search Creative Commons music by mood/genre, filter by duration and license, use the `preview-hq-mp3` URL directly (requires `FREESOUND_API_KEY`, free at [freesound.org/apiv2/apply](https://freesound.org/apiv2/apply/)). Attribute CC-BY tracks in `CREDITS.md`.
2. **User-provided** — Bring your own MP3 or URL
3. **No music** — Voiceover only

## Project Structure

When hve-spielberg creates a video project, it generates:

```
my-video-project/
├── project-plan.md           # Phase tracker + decision log
├── context.md                # Product context from Phase 0
├── storyboard.md             # Scene-by-scene plan from Phase 1
├── DESIGN.md                 # Design contract from Phase 3 (palette, type, motion)
├── public/
│   └── screenshots/          # App captures from Phase 2
├── scenes/                   # Phase 3 HyperFrames scene templates
│   ├── 00-title-card.html
│   ├── 01-pain-point.html
│   └── ...
├── index.html                # Phase 4 root HyperFrames composition
├── voiceover.mp3             # ElevenLabs TTS output
├── transcript.json           # `npx hyperframes transcribe` timing data
                              # (or voiceover.json if you used standalone whisper)
├── background-music.mp3      # Freesound or user-provided
├── voiceover-with-music.mp3  # Mixed track wired into index.html
└── out/
    └── final.mp4             # `npx hyperframes render` output
```

## Skill File Structure

```
hve-spielberg/
├── SKILL.md                       # Orchestrator entry point (read first)
├── CLAUDE.md                      # Codebase guide for agent sessions (Claude Code / Copilot CLI) editing this repo
├── workflows/                     # The 6-phase pipeline, one file per phase
│   ├── phase-0-discovery.md
│   ├── phase-1-storytelling.md
│   ├── phase-2-capture.md
│   ├── phase-3-design.md
│   ├── phase-4-production.md
│   └── phase-5-audio.md
├── templates/                     # Copied into each generated video project
│   ├── project-plan.md
│   ├── context.md
│   └── storyboard.md
├── patterns/                      # Animation + design reference
│   ├── INDEX.md                   # Wayfinding: situation → which file
│   ├── visual-patterns.md         # GSAP easing, scene entries, stagger trap
│   ├── metallic-swoosh.md         # Premium transition pattern
│   ├── marker-highlight.md        # 5 word-emphasis modes
│   ├── transition-catalog.md      # Mood-mapped transition reference
│   └── anti-slop.md               # Cardinal sins + AI Tool Promo specifics
├── design-systems/                # 10 vendored brand presets (Phase 1 Path A)
│   ├── README.md                  # Catalog + how to use
│   ├── CONTRIBUTING.md            # Quality bar for adding more brands
│   ├── stripe/DESIGN.md
│   ├── linear-app/DESIGN.md
│   ├── apple/DESIGN.md
│   └── …                          # notion, vercel, airbnb, github, cal, arc, bento
├── scripts/
│   └── generate_voiceover.py      # ElevenLabs TTS + transcript verification + auto-pad
├── example/                       # The skill's own promo, built by the skill itself
│   ├── (out/final.mp4)           # 60s rendered demo (1920×1080, 3.4 MB) — not committed; regenerable build artifact (demo on YouTube)
│   ├── voiceover.py               # Project-local script with the actual VO timing config
│   ├── index.html                 # Phase 4 root composition
│   ├── scenes/*.html              # Phase 3 scene templates
│   └── README.md                  # How to reproduce the render
└── .github/
    └── copilot-instructions.md    # Guide for Copilot reviewers
```

## FAQ

**Q: Can I use this without ElevenLabs?**
A: Yes — Phase 5 falls back to `npx hyperframes tts` (Kokoro-82M, runs locally, no API key). Quality is good but noticeably below ElevenLabs Multilingual v2. For non-English narration, install `espeak-ng`. ElevenLabs remains the default when `ELEVENLABS_API_KEY` is set.

**Q: Can I skip the screenshot capture phase?**
A: Yes — use `--mode jump --phase 3` to skip to design, or provide your own screenshots in `public/screenshots/`.

**Q: What video resolution/format does it output?**
A: 30fps MP4 (H.264 video + AAC audio) via `npx hyperframes render`. The canvas size is chosen in Phase 1:
  - 16:9 → 1920×1080 (default — horizontal, web, embeds)
  - 9:16 → 1080×1920 (vertical — TikTok, Reels, Shorts)
  - 1:1  → 1080×1080 (square — IG feed, LinkedIn)
  - 4:5  → 1080×1350 (portrait IG feed)

**Q: Can I edit the video after generation?**
A: Yes — the project is plain HTML + CSS + GSAP. Edit `index.html` or any `scenes/*.html` file directly. Run `npx hyperframes preview` for a scrubbable timeline UI, then `npx hyperframes render` to re-render.

**Q: Is Freesound music free to use commercially?**
A: It depends on the track. Freesound hosts a mix of CC0 (public domain — no attribution, commercial OK), CC-BY (commercial OK with attribution), and other Creative Commons variants. The Phase 5 search filters to CC0 / CC-BY by default. For CC-BY tracks, the workflow writes a `CREDITS.md` automatically. Always check each track's license on its Freesound page before commercial use.

## Credits

Fork of [promo-video](https://github.com/buildatscale-tv/claude-code-plugins/tree/main/plugins/promo-video) by buildatscale-tv, extended with design thinking, Chrome DevTools capture, HyperFrames composition (HTML + GSAP), and Freesound music search.

## License

MIT
