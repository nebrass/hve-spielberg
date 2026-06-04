# Example Project — hve-spielberg's own promo

This is **hve-spielberg's own promo video**, built by the pipeline it promotes.

▶ **[Watch on YouTube](https://www.youtube.com/watch?v=tIsQabrczRs)** — 60s, 1920×1080, H.264 + AAC stereo. The rendered `out/final.mp4` is not committed (regenerable binary); rebuild it locally with the steps below.

Every *input* artifact lives in this directory — it's the project's primary demo, not a staged sample. The rendered video is the one thing that isn't committed.

## What's here

| Path | Phase | What it is |
|---|---|---|
| `project-plan.md` | 0 | Mode (promo), aspect (16:9), design-system (vercel), phase tracker |
| `context.md` | 0 | Product brief — what hve-spielberg is, audience, goal of the video |
| `storyboard.md` | 1 | 5-scene 60s plan: Hook → How → Pipeline → Proof → CTA |
| `DESIGN.md` | 3 | Copied from `design-systems/vercel/DESIGN.md` |
| `scenes/00-hero.html` | 3 | Hook: *"One slash command. This whole video. Made in Claude Code."* with marker-sweep on "This whole video." |
| `scenes/01-how.html` | 3 | Terminal mockup showing `/hve-spielberg` + 4 checkmark lines + "Done in 14m 22s" |
| `scenes/02-pipeline.html` | 3 | 6-phase chip grid (numbered 1–6), each chip carries verb + method |
| `scenes/03-features.html` | 3 | 3 horizontal bands naming the tools that made *this* video |
| `scenes/04-cta.html` | 3 | `/hve-spielberg` install pill + wordmark + URL `github.com/nebrass/hve-spielberg` |
| `index.html` | 4 | Root 60s composition with 5 sub-comp loaders + incoming-only crossfade transitions |
| `voiceover.py` | 5 | ElevenLabs TTS (Matilda) + `npx hyperframes transcribe` verification + auto-pad to VIDEO_DURATION |
| `voiceover.mp3` | 5 | Generated 60s voiceover (5 sections with silence padding) — gitignored, regenerable |
| `background-music.mp3` | 5 | "Unpretentious Reveal" by SondreDrakensson (Freesound, CC-BY) — gitignored, fetch via Step 5.2 |
| `voiceover-with-music.mp3` | 5 | ffmpeg-mixed final audio with loudnorm + amix + alimiter — gitignored, regenerable |
| `out/final.mp4` | 5 | **The rendered video.** `npx hyperframes render` output — not committed; regenerable build artifact (watch the demo on YouTube, or regenerate with the steps below). |
| `CREDITS.md` | — | CC-BY attribution for the music track + voiceover provenance |

Only the source files (`.html`, `.md`, `.py`) are committed. The rendered `out/final.mp4` is not committed (not version-controlled — 3.4 MB of regenerable binary; the demo lives on YouTube), and the intermediate audio files (`voiceover.mp3`, `background-music.mp3`, `voiceover-with-music.mp3`, `vo_section_*.mp3`, `transcript.json`) are regenerable and `.gitignore`'d — see `example/.gitignore`.

## Reproducing the render

```bash
# 1. Set your API keys
export ELEVENLABS_API_KEY=<your-key>
export FREESOUND_API_KEY=<your-key>     # only needed if rebuilding music search

# 2. Regenerate the voiceover
python3 voiceover.py
#  → produces voiceover.mp3 + transcript.json
#  → ~$0.04 of ElevenLabs credits (5 sections, ~110 words)

# 3. (Optional) re-search Freesound for music; otherwise re-fetch the
#    same track used in the committed version:
curl -sL "https://cdn.freesound.org/previews/529/529380_6628165-hq.mp3" \
  -o background-music.mp3
#    See workflows/phase-5-audio.md § Step 5.2 for the search recipe.

# 4. Mix audio. `apad=whole_dur=60` is critical — without it the mix ends
#    where the voiceover ends (~58.5s), and HyperFrames render finds no
#    audio for the trailing frames of the 60s composition. voiceover.py
#    already pads, but the recipe pads again as a belt-and-suspenders guard
#    in case you brought your own voiceover.mp3.
ffmpeg -y -i voiceover.mp3 \
  -af "apad=whole_dur=60,loudnorm=I=-16:TP=-1.5:LRA=11" \
  voiceover-normalized.mp3
ffmpeg -y -i voiceover-normalized.mp3 -i background-music.mp3 \
  -filter_complex "
    [1:a]atrim=0:60,volume=0.22,afade=t=in:st=0:d=2,afade=t=out:st=57:d=3[music];
    [0:a][music]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,
                alimiter=limit=0.95[out]" \
  -map "[out]" -c:a libmp3lame -q:a 2 voiceover-with-music.mp3

# 5. Run quality gates + render
npx hyperframes doctor
npx hyperframes lint     .                 # operates on the project DIR (finds index.html)
npx hyperframes inspect  . --samples 12
npx hyperframes validate .
mkdir -p out
npx hyperframes render   . --output out/final.mp4 --quality high
```

Render time: ~20–30s on a 16-core machine with hardware GPU.

## What this example demonstrates

Every claim in the voiceover script maps to a real capability:

- **"Six phases"** → `SKILL.md` + `workflows/phase-0..5-*.md` (internal file naming is 0-based; viewer-facing labels are 1-based, see `patterns/anti-slop.md` § AI Tool Promo Specifics)
- **"Discover with design thinking"** → Phase 0 discovery workflow
- **"Capture via Chrome DevTools"** → Phase 2 uses `mcp__chrome-devtools__*`
- **"Design with brand DNA"** → Phase 3 Path A, this example uses `design-systems/vercel/DESIGN.md`
- **"GSAP at sub-second precision"** → every scene's GSAP timeline registered on `window.__timelines`, paused; HyperFrames drives playback frame-by-frame
- **"Render to deterministic MP4"** → `npx hyperframes render` (this video proves it works)

No invented metrics. No filler copy. No fictional product.

## Caveats

- **Voice pronunciation:** "hve-spielberg" is spoken as "Aitch Vee Ee Spielberg" (phonetic spelling) by ElevenLabs Matilda — space-separated capital letters render as a blob otherwise. See `workflows/phase-5-audio.md` § "Pronouncing acronyms".
- **Music attribution:** the chosen track is CC-BY, requiring attribution. See `CREDITS.md`. To swap for a different track, re-run the Freesound search in Phase 5.2.
- **`vo_section_NN.mp3` and `transcript.json` are debugging intermediates.** They're created by `voiceover.py` on every run, `.gitignore`'d, and safe to delete.
