# Phase 5: Audio & Render

Generate voiceover, mix music, and render the final video.

## Step 5.1: Generate Voiceover

**The voiceover must match the visuals.** This is non-negotiable.

### Extract Scene Timings

Read the main composition file to extract exact scene timings and content. Build a timing table:

```
Scene              | Start | End  | Duration | Visual Content
-------------------|-------|------|----------|---------------
Hook               | 0s    | 5s   | 5s       | "Title text" + stat
Pain Point 1       | 5s    | 9s   | 4s       | "Pain title" + icon
...
```

### Write Aligned Script

For each scene, write voiceover text that:
- References what's visually on screen
- Starts 1s after scene start (buffer)
- Ends 0.5s before scene end (buffer)
- Matches the spoken stat to the visual stat

### Generate with ElevenLabs

Edit `scripts/generate_voiceover.py`:
- Set `VOICE_ID` to selected voice from Phase 1
- Set `sections` list with `(start_time, text)` pairs
- Set `VIDEO_DURATION` to match composition

```bash
python3 ${SKILL_DIR}/scripts/generate_voiceover.py
```

### Verify with Whisper (CRITICAL — do not skip!)

```bash
whisper voiceover.mp3 --model tiny --output_format srt
cat voiceover.srt
```

Compare Whisper timestamps against scene timings. If ANY overlap detected:

1. **Shorten text** — make it punchier, cut filler words
2. **Increase gaps** — push next section's start time 1-2s later
3. **Add pauses** — insert "..." in text
4. **Regenerate and verify again**

**Repeat until ZERO overlaps. Do NOT ask the user — just fix it.**

## Step 5.2: Background Music

### Freesound API (if FREESOUND_API_KEY set)

Freesound provides a real, public CC-licensed audio search API. Get a key at <https://freesound.org/apiv2/apply>. Authentication uses a `token` query parameter; previews require no OAuth2.

Derive mood/genre keywords from the storytelling phase (e.g., "cinematic corporate uplifting loop"). Filter by `duration` so you don't pick a 10-minute ambient drone for a 45s spot, and by `license` so you stay on safe ground (CC0 or CC-BY).

```bash
QUERY="cinematic corporate uplifting"
DURATION_S=42  # match your video duration

curl -sG "https://freesound.org/apiv2/search/text/" \
  --data-urlencode "query=${QUERY}" \
  --data-urlencode "filter=duration:[${DURATION_S} TO 180] license:(\"Creative Commons 0\" OR \"Attribution\")" \
  --data-urlencode "fields=id,name,duration,license,username,previews,url" \
  --data-urlencode "page_size=10" \
  --data-urlencode "token=${FREESOUND_API_KEY}" \
| python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in data.get('results', []):
    print(f\"  [{r['id']}] {r['name']} ({r['duration']:.1f}s) — {r['license']} by {r['username']}\")
    print(f\"      page:    {r['url']}\")
    print(f\"      preview: {r['previews']['preview-hq-mp3']}\")
"
```

Present results to the user. Each hit has a high-quality .mp3 preview URL (`previews.preview-hq-mp3`) usable directly as a soundtrack. Download the chosen track:

```bash
curl -sL "<selected-preview-hq-mp3-url>" -o background-music.mp3
```

**Attribution:** If the chosen track is CC-BY (not CC0), you must credit the author. Write `CREDITS.md` in the project root:

```
Background music: "<track name>" by <username> (Freesound, <license>)
URL: <track page URL>
```

Full-quality original downloads require OAuth2; previews are sufficient for video soundtracks.

### User-Provided (fallback)

If no FREESOUND_API_KEY or user prefers own music:

```json
{
  "questions": [{
    "question": "Background music?",
    "header": "Music",
    "options": [
      { "label": "I'll provide a file", "description": "Provide path to an MP3" },
      { "label": "No music", "description": "Voiceover only" }
    ],
    "multiSelect": false
  }]
}
```

## Step 5.3: Audio Mixing

### Normalize voiceover
```bash
ffmpeg -y -i voiceover.mp3 -af "loudnorm=I=-16:TP=-1.5:LRA=11" voiceover-normalized.mp3
```

### Mix music (if using background music)

```bash
# DURATION = video length in seconds; FADE_OUT_START = DURATION - 3
DURATION=42
FADE_OUT_START=39

ffmpeg -y -i voiceover-normalized.mp3 -i background-music.mp3 \
  -filter_complex "
    [1:a]atrim=0:${DURATION},
         volume=0.22,
         afade=t=in:st=0:d=2,
         afade=t=out:st=${FADE_OUT_START}:d=3[music];
    [0:a][music]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,
                alimiter=limit=0.95[out]" \
  -map "[out]" -c:a libmp3lame -q:a 2 \
  voiceover-with-music.mp3
```

**Critical:** `amix` defaults to `normalize=1`, which divides each input by the number of inputs (a hidden -6dB on every track). With music already attenuated to 0.22, that double-cut leaves music near-inaudible. Always pass `normalize=0` and rely on `alimiter` for peak control.

Validate with `ebur128`: integrated loudness should land around -16 LUFS, true peak under -0.5 dBFS.

```bash
ffmpeg -hide_banner -i voiceover-with-music.mp3 -af ebur128=peak=true -f null - 2>&1 | tail -16
```

## Step 5.4: Final Render

### Render video (high quality)
```bash
npx remotion render MainComposition out/video-hq.mp4 --image-format png --crf 1
```

### Combine video + audio
```bash
ffmpeg -y -i out/video-hq.mp4 -i voiceover-with-music.mp3 \
  -c:v copy -map 0:v:0 -map 1:a:0 \
  out/final.mp4
```

### Verify
```bash
ffprobe out/final.mp4 2>&1 | grep -E "Duration|Video|Audio"
```

## Output

- `out/final.mp4` — Final video with voiceover and music
- `voiceover.mp3` — Raw voiceover
- `voiceover.srt` — Whisper transcription (for subtitles)

## Checkpoint

> "Video rendered! Final deliverable: `out/final.mp4`
>
> Duration: [X]s | Resolution: 1920x1080 | Audio: voiceover + music
>
> Watch it and let me know if you'd like any adjustments."
