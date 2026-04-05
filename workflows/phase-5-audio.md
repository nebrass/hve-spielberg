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

### Pixabay Music API (if PIXABAY_API_KEY set)

Derive mood keywords from the storytelling phase (e.g., "corporate upbeat ambient"):

```bash
curl -s "https://pixabay.com/api/music/?key=${PIXABAY_API_KEY}&q=corporate+upbeat&category=background&per_page=5" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for hit in data.get('hits', []):
    print(f\"  {hit['id']}: {hit['title']} ({hit['duration']}s) — {hit['url']}\")
    print(f\"    Download: {hit['audio']}\")
"
```

Present options to user, download selected track:
```bash
curl -sL "<selected-audio-url>" -o background-music.mp3
```

### User-Provided (fallback)

If no PIXABAY_API_KEY or user prefers own music:

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
# Adjust st= in afade to (duration - 3) for fade out
ffmpeg -y -i voiceover-normalized.mp3 -i background-music.mp3 \
  -filter_complex "[1:a]volume=0.10,afade=t=in:st=0:d=2,afade=t=out:st=${FADE_OUT_START}:d=3[music];[0:a][music]amix=inputs=2:duration=first" \
  voiceover-with-music.mp3
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
