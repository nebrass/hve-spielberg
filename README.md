# hve-spielberg

**AI-powered video production pipeline for Claude Code.** From design thinking to final render — 6 automated phases that turn your app into a polished promo or showcase video.

```
/hve-spielberg ./my-project
```

## What It Does

hve-spielberg is a Claude Code skill that orchestrates end-to-end video production:

1. **Understands your product** through design thinking (empathize, define, ideate)
2. **Builds a narrative** with scene storyboarding and emotional arc
3. **Captures your app** automatically via Chrome DevTools
4. **Designs branded components** matching your app's visual identity
5. **Produces the video** in Remotion (React-based motion graphics)
6. **Adds voiceover + music** with ElevenLabs TTS, Whisper verification, and Pixabay music

### Dual Mode

| Mode | Structure | Best For |
|------|-----------|----------|
| **Promo** | Hook → Pain → Solution → Features → CTA | Marketing, launches, ads |
| **Showcase** | Intro → Walkthrough → Highlights → Closer | Portfolio, demos, case studies |

## Pipeline

```
Phase 0: DISCOVERY         Phase 1: STORYTELLING       Phase 2: CAPTURE
├ Design thinking          ├ Narrative structure        ├ Chrome DevTools MCP
├ Codebase/feature scan    ├ Scene storyboard           ├ Auto-navigate app
├ Product context Q&A      ├ Emotional arc              ├ Screenshot key views
└ Goal/audience analysis   └ Script outline             └ Interaction states

Phase 3: DESIGN            Phase 4: PRODUCTION         Phase 5: AUDIO & RENDER
├ frontend-design skill    ├ Remotion scaffolding       ├ ElevenLabs TTS
├ Brand-matched components ├ remotion-best-practices    ├ Whisper verification
├ Scene templates          ├ Screenshot integration     ├ Pixabay Music API
└ Visual design brief      └ Animation + transitions    └ Final render + export
```

Each phase has a user-approval checkpoint before proceeding to the next.

## Prerequisites

| Tool | Required | Installation |
|------|----------|-------------|
| Node.js 18+ | Yes | [nodejs.org](https://nodejs.org) |
| Python 3.10+ | Yes | [python.org](https://python.org) |
| ffmpeg | Yes | `brew install ffmpeg` / `apt install ffmpeg` |
| Chrome DevTools MCP | Yes | Configured in Claude Code settings |
| `ELEVEN_LABS_API_KEY` | Yes | [elevenlabs.io](https://elevenlabs.io) — set as env var |
| `PIXABAY_API_KEY` | No | [pixabay.com/api](https://pixabay.com/api/docs/) — enables music search |
| Whisper | Recommended | `pip install openai-whisper` — voiceover timing verification |

### Required Skills

hve-spielberg depends on two other Claude Code skills:

| Skill | Purpose | Install |
|-------|---------|---------|
| `remotion-best-practices` | Remotion API patterns and constraints | `npx skills add remotion-dev/skills` |
| `frontend-design` | UI/UX component generation | Included with Claude Code superpowers |

## Installation

### Option 1: Skills CLI (Recommended)

```bash
npx skills add nebrass/hve-spielberg
```

### Option 2: Manual

```bash
git clone https://github.com/nebrass/hve-spielberg.git ~/.claude/skills/hve-spielberg
```

### Option 3: Git Submodule / Direct Copy

Copy the skill files directly into any project's `.claude/skills/` directory:

```bash
cp -r ~/.claude/skills/hve-spielberg ./my-project/.claude/skills/hve-spielberg
```

## Quick Start

1. **Set your API key:**
   ```bash
   export ELEVEN_LABS_API_KEY=your_key_here
   export PIXABAY_API_KEY=your_key_here  # optional, for music search
   ```

2. **Start the skill:**
   ```
   /hve-spielberg ./my-video-project
   ```

3. **Follow the prompts:**
   - Select video mode (Promo or Showcase)
   - Answer discovery questions about your product and audience
   - Review the storyboard
   - Provide your app URL for screenshot capture
   - Review branded design components
   - Preview the video composition
   - Choose a voice and background music

4. **Get your video:**
   ```
   out/final.mp4  — 1920x1080, voiceover + music
   ```

## Entry Modes

| Mode | Command | When |
|------|---------|------|
| `new` | `/hve-spielberg ./project` | Start a fresh video from scratch |
| `continue` | `/hve-spielberg ./project --mode continue` | Resume where you left off |
| `jump` | `/hve-spielberg ./project --mode jump --phase 3` | Jump to a specific phase |

## Voices

| Voice | Style | Voice ID |
|-------|-------|----------|
| Matilda (default) | Warm, confident female | `XrExE9yKIg1WjnnlVkGX` |
| Rachel | Calm, clear female | `21m00Tcm4TlvDq8ikWAM` |
| Daniel | Authoritative male | `onwK4e9ZLuTAKqWW03F9` |
| Josh | Friendly, conversational male | `TxGEqnHWrfWFTfGW9XjX` |

## Music Strategy

No bundled audio files. Three-tier approach:

1. **Pixabay Music API** — Search free royalty-free music by mood keywords (requires `PIXABAY_API_KEY`)
2. **User-provided** — Bring your own MP3 or URL
3. **No music** — Voiceover only

## Project Structure

When hve-spielberg creates a video project, it generates:

```
my-video-project/
├── project-plan.md           # Phase tracker + decision log
├── context.md                # Product context from Phase 0
├── storyboard.md             # Scene-by-scene plan from Phase 1
├── visual-brief.md           # Brand analysis from Phase 3
├── public/
│   └── screenshots/          # App captures from Phase 2
├── src/
│   ├── components/           # Branded Remotion components from Phase 3
│   └── ...                   # Video composition from Phase 4
├── voiceover.mp3             # ElevenLabs TTS output
├── voiceover.srt             # Whisper transcription (subtitles)
├── background-music.mp3      # Pixabay or user-provided
└── out/
    └── final.mp4             # Final rendered video
```

## Skill File Structure

```
hve-spielberg/
├── SKILL.md                  # Orchestrator entry point
├── workflows/
│   ├── phase-0-discovery.md
│   ├── phase-1-storytelling.md
│   ├── phase-2-capture.md
│   ├── phase-3-design.md
│   ├── phase-4-production.md
│   └── phase-5-audio.md
├── templates/
│   ├── project-plan.md
│   ├── context.md
│   └── storyboard.md
├── patterns/
│   ├── visual-patterns.md
│   └── metallic-swoosh.md
└── scripts/
    └── generate_voiceover.py
```

## FAQ

**Q: Can I use this without ElevenLabs?**
A: No, ElevenLabs is required for voiceover generation. You need an API key.

**Q: Can I skip the screenshot capture phase?**
A: Yes — use `--mode jump --phase 3` to skip to design, or provide your own screenshots in `public/screenshots/`.

**Q: What video resolution/format does it output?**
A: 1920x1080 (Full HD), 30fps, MP4 with H.264 video and MP3 audio.

**Q: Can I edit the video after generation?**
A: Yes — the Remotion project is fully editable. Run `npx remotion studio` to open the visual editor, tweak scenes, then re-render.

**Q: Is the Pixabay music free to use commercially?**
A: Yes — Pixabay content is released under their [Content License](https://pixabay.com/service/license-summary/) which allows commercial use without attribution.

## Credits

Fork of [promo-video](https://github.com/buildatscale-tv/claude-code-plugins/tree/main/plugins/promo-video) by buildatscale-tv, extended with design thinking, Chrome DevTools capture, frontend-design integration, and Pixabay music search.

## License

MIT
