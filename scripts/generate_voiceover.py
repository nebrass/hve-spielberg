#!/usr/bin/env python3
"""
hve-spielberg — Voiceover Generation Pipeline
Generates timed voiceover using ElevenLabs TTS, assembles with silence
padding, pads to VIDEO_DURATION, and verifies timing via transcript.

Usage:
    python3 generate_voiceover.py

Environment:
    ELEVENLABS_API_KEY   — Required. ElevenLabs API key.
                           (ELEVEN_LABS_API_KEY also accepted for back-compat.)

Configuration (edit below):
    VOICE_ID         — ElevenLabs voice ID
    VIDEO_DURATION   — Total video duration in seconds
    sections         — List of (start_time, text) tuples

Pitfalls handled (each one a real failure mode you'd otherwise hit silently):
  - ffmpeg concat resolves relative paths to the concat-list's location, not
    cwd. Always use absolute paths in concat lists.
  - Voiceover must be padded to VIDEO_DURATION (`apad=whole_dur=N`). Otherwise
    HyperFrames render finds no audio for the trailing frames.
  - ElevenLabs Matilda runs space-separated capital letters together as a
    phonetic blob ("H V E" → "Sage V E"). Write acronyms phonetically:
    "Aitch Vee Ee" for HVE, "A I" for AI, etc.
  - Transcript JSON from `hyperframes transcribe` is a flat list of word
    segments; from standalone `whisper --output_format json` it's a dict
    with a "segments" key. Handle both.
  - Word count is a poor proxy for spoken duration — comma density inflates
    the duration significantly (a 22-word sentence with 5 commas can be 15s;
    the same idea in 26 commaless words takes 10s). When budgets are tight,
    drop commas before dropping words.
  - Whisper tiny-model timestamps drift ±0.5s. For precise gap analysis use
    `ffmpeg silencedetect` (see workflows/phase-5-audio.md).
"""

import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# ─── Configuration ────────────────────────────────────────────────────────────

API_KEY = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVEN_LABS_API_KEY")
if not API_KEY:
    print("Error: ELEVENLABS_API_KEY not set")
    sys.exit(1)

# Voice IDs:
#   Matilda: XrExE9yKIg1WjnnlVkGX  — Warm, confident female
#   Rachel:  21m00Tcm4TlvDq8ikWAM  — Calm, clear female
#   Daniel:  onwK4e9ZLuTAKqWW03F9  — Authoritative male
#   Josh:    TxGEqnHWrfWFTfGW9XjX  — Friendly male
VOICE_ID = "XrExE9yKIg1WjnnlVkGX"  # Matilda (default)

VIDEO_DURATION = 60  # seconds

# (start_time_seconds, text_to_speak)
sections = [
    (1.0, "Your opening hook goes here."),
    (6.0, "Describe the problem your audience faces."),
    (16.0, "Introduce your solution."),
    (21.0, "Walk through the key features."),
    (46.0, "Share the results and impact."),
    (53.0, "Your call to action."),
]

# ─── ElevenLabs TTS ──────────────────────────────────────────────────────────

ELEVENLABS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

VOICE_SETTINGS = {
    "stability": 0.65,
    "similarity_boost": 0.85,
    "style": 0.2,
    "use_speaker_boost": True,
}


def generate_section(text: str, output_path: str) -> bool:
    """Generate a single voiceover section via ElevenLabs."""
    response = requests.post(
        ELEVENLABS_URL,
        headers={
            "xi-api-key": API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": VOICE_SETTINGS,
        },
        timeout=30,
    )

    if response.status_code != 200:
        print(f"  ElevenLabs error {response.status_code}: {response.text[:200]}")
        return False

    with open(output_path, "wb") as f:
        f.write(response.content)

    return True


def get_audio_duration(path: str) -> float:
    """Get duration of an audio file in seconds using ffprobe.

    Surfaces a clear error on the two common failure modes (ffprobe missing
    or input file empty/corrupt) instead of crashing with a generic
    ValueError from float("").
    """
    try:
        result = subprocess.run(
            ["ffprobe", "-i", path, "-show_entries", "format=duration",
             "-v", "quiet", "-of", "csv=p=0"],
            capture_output=True, text=True, check=True,
        )
    except FileNotFoundError:
        raise RuntimeError("ffprobe not installed — install ffmpeg")
    out = result.stdout.strip()
    if not out:
        raise RuntimeError(f"ffprobe returned empty duration for {path} "
                           "(file may be 0 bytes or corrupt)")
    return float(out)


# ─── Assembly ────────────────────────────────────────────────────────────────

def _make_silence(duration_s: float) -> str:
    """Write a silence MP3 of `duration_s` seconds; return its absolute path."""
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i",
        "anullsrc=r=44100:cl=mono", "-t", str(duration_s), path,
    ], capture_output=True, check=True)
    return path


def assemble_voiceover(section_files: list, output_path: str = "voiceover.mp3"):
    """Combine section audio files with silence gaps into final voiceover.

    Two pitfalls this implementation handles:

    1. ffmpeg's concat demuxer resolves `file '...'` paths relative to the
       concat-list's location, NOT the cwd. The concat-list lives in /tmp,
       so relative paths like "vo_section_00.mp3" silently fail to resolve
       and produce a near-empty output. Use absolute paths everywhere.

    2. `tempfile.mktemp` is deprecated since Python 2.3 (race-prone). Use
       `mkstemp` instead — wrapped in `_make_silence` above.
    """
    silence_paths: list = []
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        concat_list = f.name

        for i, (start_time, audio_path) in enumerate(section_files):
            audio_abs = os.path.abspath(audio_path)
            duration = get_audio_duration(audio_abs)

            # Initial silence before the first section's start time
            if i == 0 and start_time > 0:
                sp = _make_silence(start_time)
                silence_paths.append(sp)
                f.write(f"file '{sp}'\n")

            f.write(f"file '{audio_abs}'\n")

            # Gap between this section and the next
            if i < len(section_files) - 1:
                next_start = section_files[i + 1][0]
                gap = next_start - start_time - duration
                if gap > 0:
                    sp = _make_silence(gap)
                    silence_paths.append(sp)
                    f.write(f"file '{sp}'\n")

    # Concatenate all parts. try/finally ensures the concat-list and every
    # silence tempfile is unlinked even if ffmpeg raises (unbounded /tmp
    # accumulation on CI otherwise).
    try:
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_list, "-c:a", "libmp3lame", "-q:a", "2",
            output_path,
        ], capture_output=True, check=True)
    finally:
        for p in [concat_list, *silence_paths]:
            try:
                os.unlink(p)
            except OSError:
                pass

    # Pad to exact VIDEO_DURATION so HyperFrames render finds audio for every
    # frame. Without this, a short voiceover ends early and the trailing
    # frames render with no audio (HyperFrames may even truncate the video).
    fd, padded = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", output_path,
            "-af", f"apad=whole_dur={VIDEO_DURATION}",
            "-c:a", "libmp3lame", "-q:a", "2", padded,
        ], capture_output=True, check=True)
        os.replace(padded, output_path)
    except Exception:
        try:
            os.unlink(padded)
        except OSError:
            pass
        raise

    final_dur = get_audio_duration(output_path)
    print(f"  Assembled + padded: {output_path} ({final_dur:.2f}s)")


# ─── Whisper Verification ────────────────────────────────────────────────────

def _load_segments(path: Path) -> list:
    """Read a transcript JSON file and normalize to a flat segment list.

    Robust to: UTF-8 transcripts on Windows (default cp1252 would crash),
    truncated/corrupt files written by a killed transcribe process, and
    both shapes (`[...]` vs `{"segments": [...]}`).
    """
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"  Could not parse {path}: {e}")
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("segments", []) or data.get("words", [])
    return []


def verify_transcript(voiceover_path: str) -> list:
    """Transcribe the voiceover for timing verification.

    Prefers `npx hyperframes transcribe` (bundled with HyperFrames — no extra
    install required) and falls back to standalone `whisper` if available.

    Returns a flat list of word/segment dicts.

    Pitfalls handled:
      - subprocess.TimeoutExpired (slow npm fetch) — caught, not re-raised
      - Non-zero returncode with a stale transcript.json from a prior run
        in cwd would otherwise be loaded as the *current* result. We delete
        any stale candidate before invoking the transcriber, and only load
        files that exist *after* a successful (returncode == 0) run.
      - Truncated/corrupt JSON — `_load_segments` returns [] instead of
        crashing.
    """
    candidates = [
        Path("transcript.json"),
        Path(voiceover_path).with_suffix(".json"),
    ]

    # Clear stale outputs so a failed transcriber can't pollute this run.
    for c in candidates:
        if c.exists():
            try:
                c.unlink()
            except OSError:
                pass

    # First try: hyperframes transcribe (bundled)
    try:
        proc = subprocess.run(
            ["npx", "--yes", "hyperframes", "transcribe", voiceover_path,
             "--model", "tiny"],
            capture_output=True, text=True, timeout=300, check=False,
        )
        if proc.returncode == 0:
            for candidate in candidates:
                if candidate.exists():
                    segments = _load_segments(candidate)
                    if segments:
                        return segments
        else:
            print(f"  hyperframes transcribe exit {proc.returncode}: "
                  f"{proc.stderr[:200]}")
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"  hyperframes transcribe unavailable ({type(e).__name__}); "
              "trying whisper fallback")

    # Fallback: standalone whisper (requires `pip install openai-whisper`)
    try:
        proc = subprocess.run(
            ["whisper", voiceover_path, "--model", "tiny",
             "--output_format", "json", "--output_dir", "."],
            capture_output=True, text=True, timeout=180, check=False,
        )
        if proc.returncode != 0:
            print(f"  whisper exit {proc.returncode}: {proc.stderr[:200]}")
            return []
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"  Neither `hyperframes transcribe` nor `whisper` available "
              f"({type(e).__name__}) — skipping transcript verification")
        return []

    json_path = Path(voiceover_path).with_suffix(".json")
    if not json_path.exists():
        print("  Transcript output not found — skipping verification")
        return []
    return _load_segments(json_path)


def check_overlaps(segments: list, sections: list) -> list:
    """Check if any transcribed segments cross into the next section's window.

    NB: Whisper tiny-model timestamps drift ±0.5s. For accurate gap analysis
    use `ffmpeg silencedetect` (see workflows/phase-5-audio.md). This function
    tolerates 0.5s of drift before flagging an overlap.
    """
    overlaps = []
    for i in range(len(sections) - 1):
        _, text = sections[i]
        next_start = sections[i + 1][0]
        for seg in segments:
            seg_start = seg.get("start", seg.get("startTime", 0))
            seg_end = seg.get("end", seg.get("endTime", 0))
            if seg_start < next_start and seg_end > next_start + 0.5:
                overlaps.append({
                    "section": i,
                    "text": text[:50],
                    "segment_end": seg_end,
                    "next_section_start": next_start,
                    "overlap_seconds": seg_end - next_start,
                })
    return overlaps


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("hve-spielberg — Voiceover Generation")
    print("=" * 50)

    # Step 1: Generate each section
    print("\n[1/3] Generating voiceover sections...")
    section_files = []
    for i, (start, text) in enumerate(sections):
        print(f"  Section {i + 1}/{len(sections)}: \"{text[:60]}...\"")
        output = f"vo_section_{i:02d}.mp3"
        if generate_section(text, output):
            section_files.append((start, output))
            duration = get_audio_duration(output)
            print(f"    Duration: {duration:.1f}s (starts at {start}s)")
        else:
            print(f"    FAILED — skipping")

    if not section_files:
        print("No sections generated. Check API key and network.")
        sys.exit(1)

    # Step 2: Assemble
    print("\n[2/3] Assembling voiceover...")
    assemble_voiceover(section_files)

    # Step 3: Transcript verification (prefers `hyperframes transcribe`,
    # falls back to standalone `whisper`).
    print("\n[3/3] Verifying timing via transcript...")
    segments = verify_transcript("voiceover.mp3")

    if segments:
        overlaps = check_overlaps(segments, sections)
        if overlaps:
            print(f"\n  WARNING: {len(overlaps)} overlap(s) detected!")
            for o in overlaps:
                print(f"    Section {o['section']}: ends at {o['segment_end']:.1f}s, "
                      f"next starts at {o['next_section_start']:.1f}s "
                      f"(overlap: {o['overlap_seconds']:.1f}s)")
            print("\n  Fix: Shorten text or increase gaps, then re-run.")
        else:
            print("  No overlaps detected. Voiceover timing is clean.")
    else:
        print("  Whisper verification skipped.")

    print(f"\nDone! Output: voiceover.mp3")
    total_dur = get_audio_duration("voiceover.mp3")
    print(f"Total duration: {total_dur:.1f}s (video: {VIDEO_DURATION}s)")


if __name__ == "__main__":
    main()
