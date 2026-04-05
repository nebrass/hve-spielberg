#!/usr/bin/env python3
"""
hve-spielberg — Voiceover Generation Pipeline
Generates timed voiceover using ElevenLabs TTS, verifies with Whisper.

Usage:
    python3 generate_voiceover.py

Environment:
    ELEVEN_LABS_API_KEY  — Required. ElevenLabs API key.

Configuration (edit below):
    VOICE_ID         — ElevenLabs voice ID
    VIDEO_DURATION   — Total video duration in seconds
    sections         — List of (start_time, text) tuples
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

API_KEY = os.environ.get("ELEVEN_LABS_API_KEY")
if not API_KEY:
    print("Error: ELEVEN_LABS_API_KEY not set")
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
    """Get duration of an audio file in seconds using ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-i", path, "-show_entries", "format=duration",
         "-v", "quiet", "-of", "csv=p=0"],
        capture_output=True, text=True,
    )
    return float(result.stdout.strip())


# ─── Assembly ────────────────────────────────────────────────────────────────

def assemble_voiceover(section_files: list, output_path: str = "voiceover.mp3"):
    """Combine section audio files with silence gaps into final voiceover."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        concat_list = f.name

        for i, (start_time, audio_path) in enumerate(section_files):
            duration = get_audio_duration(audio_path)

            # Add silence before this section if needed
            if i == 0 and start_time > 0:
                silence = tempfile.mktemp(suffix=".mp3")
                subprocess.run([
                    "ffmpeg", "-y", "-f", "lavfi", "-i",
                    f"anullsrc=r=44100:cl=mono",
                    "-t", str(start_time), silence,
                ], capture_output=True)
                f.write(f"file '{silence}'\n")

            f.write(f"file '{audio_path}'\n")

            # Add silence gap to next section
            if i < len(section_files) - 1:
                next_start = section_files[i + 1][0]
                gap = next_start - start_time - duration
                if gap > 0:
                    silence = tempfile.mktemp(suffix=".mp3")
                    subprocess.run([
                        "ffmpeg", "-y", "-f", "lavfi", "-i",
                        f"anullsrc=r=44100:cl=mono",
                        "-t", str(gap), silence,
                    ], capture_output=True)
                    f.write(f"file '{silence}'\n")

    # Concatenate all parts
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list, "-c:a", "libmp3lame", "-q:a", "2",
        output_path,
    ], capture_output=True)

    os.unlink(concat_list)
    print(f"  Assembled: {output_path}")


# ─── Whisper Verification ────────────────────────────────────────────────────

def verify_with_whisper(voiceover_path: str) -> list:
    """Run Whisper on the voiceover and return timestamped segments."""
    try:
        result = subprocess.run(
            ["whisper", voiceover_path, "--model", "tiny",
             "--output_format", "json", "--output_dir", "."],
            capture_output=True, text=True, timeout=120,
        )
    except FileNotFoundError:
        print("  Whisper not installed — skipping verification")
        return []

    json_path = Path(voiceover_path).with_suffix(".json")
    if not json_path.exists():
        print("  Whisper output not found — skipping verification")
        return []

    with open(json_path) as f:
        data = json.load(f)

    return data.get("segments", [])


def check_overlaps(segments: list, sections: list) -> list:
    """Check if any Whisper segments overlap with scene boundaries."""
    overlaps = []
    for i, (start, text) in enumerate(sections[:-1]):
        next_start = sections[i + 1][0]
        # Find segments that cross into the next section
        for seg in segments:
            if seg["start"] < next_start and seg["end"] > next_start:
                overlaps.append({
                    "section": i,
                    "text": text[:50],
                    "segment_end": seg["end"],
                    "next_section_start": next_start,
                    "overlap_seconds": seg["end"] - next_start,
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

    # Step 3: Whisper verification
    print("\n[3/3] Verifying with Whisper...")
    segments = verify_with_whisper("voiceover.mp3")

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
