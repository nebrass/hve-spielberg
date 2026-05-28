# Code Review — `migrate/hyperframes`

**Reviewer:** GitHub Copilot (code-reviewer mode)  
**Date:** 2026-05-27  
**Commit:** `df8f5e5` — `feat(skill): migrate from Remotion to HyperFrames`  
**Scope:** 46 files changed: +4,531 / −378

---

## Summary

This branch migrates the rendering engine from Remotion (React/JSX) to HyperFrames (HTML + GSAP + headless Chromium), adds 10 vendored brand design-system presets, a self-promo example project, and three new pattern documents. The migration is well-engineered, security-clean, and ships a working end-to-end example (`example/out/final.mp4`). No critical security issues. Main findings are documentation/design-consistency contradictions, not code defects.

**Verdict:** Block merge on P0 items 1–3. Fix P1 items 4–7 in the same PR. Open follow-up issues for P2/P3.

---

## Architecture & Feature Summary

| Area | Change | Quality |
|---|---|---|
| Engine | Remotion → HyperFrames; phase contract updated in `SKILL.md` | Coherent. File-presence contract holds across `SKILL.md`, both `CLAUDE.md` files, and the workflows. |
| Visual identity | 3-strategy picker (vendored brand / HF style / screenshot derivation) in `workflows/phase-1-storytelling.md` | Strongest part of the diff. Path A → Path C falls back gracefully. |
| Vendored brands | 10 new `design-systems/<slug>/DESIGN.md` files, each ~70–110 lines | Genuinely brand-specific. `CONTRIBUTING.md` codifies the bar (motion-section fail-state test). |
| Patterns | 3 new files: `anti-slop.md`, `marker-highlight.md`, `transition-catalog.md`. `INDEX.md` is the wayfinding map. | Detailed and useful. Inconsistencies with the example and with `metallic-swoosh.md` flagged below. |
| Audio | Switched to `npx hyperframes transcribe` (preferred) + standalone Whisper (fallback) + ElevenLabs phonetic-spelling rule + `apad=whole_dur=N`. | Real bugfixes from prior surface; documented well in the docstring of `scripts/generate_voiceover.py`. |
| Example | A self-promo built end-to-end by this skill, 60s @ 1920×1080. `example/out/final.mp4` is the deliverable. | Demonstrates every phase. Mostly self-consistent — a few documentation contradictions called out below. |

---

## Critical (P0) — Must Fix Before Merging

### 1. `patterns/metallic-swoosh.md` ships an example that HyperFrames lint will reject

**File:** `patterns/metallic-swoosh.md` lines 24–30

Both overlapping scene clips share `data-track-index="1"`:

```html
<div data-composition-id="scene-01" ... data-start="0" data-duration="5.4" data-track-index="1" ...></div>
<div data-composition-id="scene-02" ... data-start="5" data-duration="5"   data-track-index="1" ...></div>
```

This directly violates the **hard rule** stated three other places in this PR:

- `workflows/phase-4-production.md` lines 146–150 — *"Track indices must be UNIQUE for overlapping scenes — HyperFrames rejects same-track overlap."*
- `patterns/transition-catalog.md` line 57 — same hard rule.
- `example/index.html` lines 41–65 — uses unique indices 1/2/3/4/5 correctly.

A user copy-pasting the metallic-swoosh sample will hit a lint failure on the first run.

**Fix:**

```html
<div data-composition-id="scene-01" ... data-track-index="1" ...></div>
<div data-composition-id="scene-02" ... data-track-index="2" ...></div>
```

---

### 2. `patterns/metallic-swoosh.md` contradicts the documented crossfade rule

**File:** `patterns/metallic-swoosh.md` lines 70–71

The same file uses **dual-direction crossfade**:

```js
root.to('[data-composition-id="scene-01"]', { opacity: 0, ... }, 5);  // outgoing → 0
root.to('[data-composition-id="scene-02"]', { opacity: 1, ... }, 5);  // incoming → 1
```

But `transition-catalog.md` line 59 and `workflows/phase-4-production.md` lines 185–188 both state:

> *"Only fade the INCOMING scene's opacity 0→1. Don't simultaneously fade the outgoing scene 1→0 — that lets the body color contribute to the composite during the crossfade."*

**Fix (pick one):**

- Switch the example to incoming-only and let the shine handle the visual hand-off, **or**
- Add an explicit note: *"The swoosh's shine overlay is opaque at the midpoint, so dual-direction crossfade is acceptable here — the body never reaches the composite. Do not generalize this pattern."*

---

### 3. Example contradicts its own brand spec on marker highlights

**Files:** `example/DESIGN.md` line 69, `design-systems/vercel/DESIGN.md` line 69, `example/scenes/00-hero.html` lines 7–13 & 85, `example/storyboard.md` lines 22–23

The example's `DESIGN.md` (copied verbatim from the Vercel brand spec) lists *"marker highlights"* under the Vercel **Avoid** list:

> `Avoid | Soft crossfades over 0.5s, swoosh transitions, marker highlights, anything ornamental`

But `example/scenes/00-hero.html` renders a marker-highlight bar on *"This whole video."* using `#ff5b4f` (Vercel ship-red), with the sweep explicitly choreographed in the timeline. The storyboard describes the highlight as the scene's main visual move.

This is a high-visibility self-contradiction in the canonical demo.

**Fix (pick one):**

| Resolution | Cost |
|---|---|
| Remove the marker-highlight from `scenes/00-hero.html` | Loses the scene's strongest emphasis cue |
| Edit `design-systems/vercel/DESIGN.md` (and the copy in `example/`) to allow marker-highlight on a single ship-red emphasis word per video | Aligns the brand spec with the proven-good example |
| Add a documented exception in `example/DESIGN.md` only | Keeps the global Vercel spec strict; example is acknowledged as an opinionated case |

Option 2 reads as most honest — the example successfully uses the technique, so the rule was overly strict.

---

## High (P1) — Should Fix Before Merging

### 4. `example/voiceover.py` silently swallows `ffmpeg` failures in `_make_silence`

**File:** `example/voiceover.py` lines 123–130

```python
def _make_silence(duration_s: float) -> str:
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i",
        "anullsrc=r=44100:cl=mono", "-t", str(duration_s), path,
    ], capture_output=True)              # ← no check=True
    return path
```

If `ffmpeg` is missing or fails, the function returns a path to a zero-byte MP3 and the subsequent `concat` produces a near-silent file. The canonical `scripts/generate_voiceover.py` lines 137–142 has `check=True`. The example diverges.

**Fix:** Add `check=True`.

---

### 5. `scripts/generate_voiceover.py` leaks temp files on partial failure

**File:** `scripts/generate_voiceover.py` lines 172–173

The script creates many temp files (`_make_silence` calls + the concat-list `NamedTemporaryFile`) and only cleans up the concat-list on the success path. If any `subprocess.run(..., check=True)` raises `CalledProcessError`, all temp MP3s and the concat list are leaked to `/tmp`. This is mild on macOS (OS cleans `/tmp`), but on long-running CI or Linux servers without `tmpwatch`, leakage accumulates across runs.

**Fix:** Wrap the temp creation block in `try / finally` and call `os.unlink()` for each tracked path. Track silence files in a list returned from `_make_silence`.

---

### 6. `scripts/search_music.py` doesn't catch `URLError`

**File:** `scripts/search_music.py` lines 66–69

```python
except urllib.error.HTTPError as e:
    print(f"Freesound API error: HTTP {e.code} {e.reason}", file=sys.stderr)
    return 2
```

`urllib.error.HTTPError` is a subclass of `URLError`, but `URLError` itself (DNS failure, connection refused, TLS errors, socket timeout) is not caught. A user without network connectivity gets a Python traceback.

**Fix:**

```python
except urllib.error.HTTPError as e:
    print(f"Freesound API error: HTTP {e.code} {e.reason}", file=sys.stderr)
    return 2
except urllib.error.URLError as e:
    print(f"Freesound API error: {e.reason}", file=sys.stderr)
    return 2
```

`URLError` must follow `HTTPError` in the chain since `HTTPError` is the subclass.

---

### 7. SKILL.md frontmatter `updated` field is stale

**File:** `SKILL.md` line 13

`updated: "2026-04-05"` — but the commit landing this PR is dated 2026-05-26. If the field is meant to track meaningful skill changes, this migration is precisely the kind of change it should reflect.

**Fix:** Bump to the merge date.

---

## Medium (P2) — Recommended

### 8. `example/voiceover.py` advertises `voiceover.mp3` as the deliverable but `index.html` references `voiceover-with-music.mp3`

**Files:** `example/voiceover.py` lines 10–13, `example/index.html` line 36

The script docstring says:

```
Output:
    voiceover.mp3      — final concatenated voiceover (silence padding included)
```

But `index.html` wires `<audio src="voiceover-with-music.mp3">`. A user who only runs `python3 voiceover.py` then `npx hyperframes render` will get a video with no audio because the referenced file doesn't exist yet. The README documents the full mix recipe correctly (`example/README.md` lines 66–78), but the script's own docstring leaves this gap.

**Fix:** Add a note to the docstring:

```
Note:
    The root composition references voiceover-with-music.mp3, not voiceover.mp3.
    See ../example/README.md § "Reproducing the render" for the ffmpeg mix step.
```

---

### 9. `npx hyperframes lint` argument inconsistency between docs

| Doc | Form used |
|---|---|
| `example/README.md` line 67 | `npx hyperframes lint . --strict` |
| `workflows/phase-4-production.md` line 208 | `npx hyperframes lint index.html --strict` |
| `workflows/phase-5-audio.md` line 253 | `npx hyperframes lint` (no arg) |

All three probably work, but the inconsistency is jarring.

**Fix:** Pick one form (`.` is the most common HF convention) and apply everywhere.

---

### 10. README "Voices" table doesn't reference Kokoro fallback voices

Phase 5 fallback says *"54 voices across 8 languages"* but never names them or links to a list. A new user wanting to use the no-key path has no way to discover voice names without trial-and-error against `npx hyperframes tts --list`.

**Fix:** Either add a short link to the HF skill's `references/tts.md` (already referenced from `patterns/INDEX.md`), or document the most common 4–6 Kokoro voices alongside the ElevenLabs four.

---

### 11. Storyboard / voiceover timing drift in the canonical example

`example/storyboard.md` line 52 declares VO ends at *"~15.6s"* for Scene 1, but `example/voiceover.py` line 41 comments *"~18 words / ~7s"* — implying ~14.4s. The actual rendered MP4 may sit anywhere in 14–16s depending on ElevenLabs voice tuning.

**Fix:** Run `npx hyperframes transcribe` against the committed VO once and update the storyboard to the measured numbers.

---

### 12. Scene 4's missing 0.4s overlap is undocumented

`example/index.html` line 57: scene-04-cta has `data-duration="13"` ending exactly at composition end (60s). It doesn't follow the "extend 0.4s past nominal end" rule the file's own comment (lines 29–34) prescribes. That's correct for the *closing* scene (no successor to crossfade into), but a reader will wonder why scene 4 is "wrong."

**Fix:** Add an inline comment: `<!-- Closing scene — no successor, so no overlap extension; held final frame. -->`

---

## Low (P3) — Nits

### 13. Self-installing `requests` via `pip install` on import failure

**Files:** `scripts/generate_voiceover.py` lines 43–48, `example/voiceover.py` lines 28–33

```python
try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
```

Convenient but mildly surprising — in a CI environment or with system Python on modern macOS, the `pip install` will fail with a confusing error. Prefer at minimum logging the action so the user can spot it and `Ctrl-C`.

---

### 14. `patterns/visual-patterns.md` uses both `opacity` and `autoAlpha` inconsistently

The DON'Ts in `SKILL.md` lines 156–159 and `visual-patterns.md` lines 209–217 prescribe `autoAlpha`. The scene-entry catalog in the same file (lines 88–131) uses `opacity` instead. The example scenes all use `autoAlpha` consistently. The patterns file should match.

**Fix:** Replace `opacity` with `autoAlpha` in the four scene-entry catalog snippets, or add a note distinguishing when each is appropriate.

---

### 15. Scene 3 template ID mismatch

`example/scenes/03-features.html`: `<template id="scene-03-proof-template">` but `data-composition-id="scene-03-features"`. `data-composition-id` is the binding, so functionally correct, but the naming divergence is confusing.

---

## Security Review

| Concern | Verdict |
|---|---|
| API keys in env, not logged | ✅ Verified across both Python scripts. |
| Shell injection | ✅ All `subprocess` calls use list args, no `shell=True`. |
| URL injection (Freesound) | ✅ Uses `urllib.parse.urlencode` for query construction. |
| Path traversal | ✅ Inputs are local filenames; `os.path.abspath` used for the concat-list. No user-controlled paths flow into shell commands. |
| Prompt-injection from external content | ⚠️ `verify_transcript` parses arbitrary JSON from `npx hyperframes transcribe` and `whisper`. Both are trusted local tools, so low risk; no code is exec'd from the JSON content. |
| Auto-`pip install` of `requests` | ⚠️ See §13 above. Mild. |
| ElevenLabs API echoing `text` in error responses | ✅ Truncated to 200 chars before printing — limits log exposure of script content (not secrets). |
| Renderer XSS | N/A — HyperFrames runs author HTML in a controlled headless Chromium during render. No external content is injected into the page. |

No OWASP Top-10 issues for this project's threat model (local CLI skill, no servers, no user-supplied untrusted data flowing into shells or eval).

---

## Strengths — Worth Preserving

- **The dogfooding loop is real.** `example/` is the skill's own promo, built by the skill. The README's claim *"Every claim in the voiceover script maps to a real capability"* holds up under inspection. This is the single most valuable artifact in the PR.
- **`design-systems/CONTRIBUTING.md`** sets a high quality bar with the *"could this Motion section copy-paste cleanly into another brand's file?"* test. The 10 vendored brands pass this test individually — each has named brand-specific motion DNA, not just numbers.
- **`patterns/anti-slop.md` § AI Tool Promo Specifics** (dogfooding loop, show-don't-tell, 1-based phase numbering for viewer-facing content, CTA discipline) is unusually specific and reflects lessons learned from this exact production. Don't dilute it.
- **The `tl.from()` stagger trap documentation** (`patterns/visual-patterns.md` lines 40–80) is the kind of failure mode every team eventually hits. Codifying it here saves future debugging.
- **All 5 scene HTML files correctly use `tl.fromTo()` + `autoAlpha`** for stagger opacity — the canonical bug is avoided everywhere in practice.
- **Body bg white in root AND all scenes** — defense against the single-frame body-color flash documented in the transition catalog.
- **Overlapping scenes pattern correctly implemented** in `example/index.html` with unique track indices 1–5.
- **Audio element has required `id="audio-main"`** (HF lint requirement).
- **GSAP 3.14.2 pinned consistently** across all HTML files.
- **Phonetic spelling documented and applied** ("HVE" → "Aitch Vee Ee").
- **`apad=whole_dur=N` padding** for render safety.
- **API keys from env only** — never logged or hardcoded.
- **Absolute paths in ffmpeg concat lists** — documented pitfall avoided.
- **`tempfile.mkstemp` correctly used** (deprecated `mktemp` avoided).
- **The transcript-tolerant parsing** in `verify_transcript()` (handles both list and dict shapes from `hyperframes transcribe` vs `whisper`) is exactly the right defensive move for a tool boundary.
- **Design systems follow rigorous CONTRIBUTING.md quality bar.** Each brand has motion, palette, typography, and depth sections with fail-state-tested specificity.

---

## Recommended Action

| Priority | Items | Action |
|---|---|---|
| **P0 (Critical)** | #1, #2, #3 | Block merge. Fix in this PR. |
| **P1 (High)** | #4, #5, #6, #7 | Fix in this PR — small and prevents first-user pain. |
| **P2 (Medium)** | #8–#12 | Open follow-up issue(s). |
| **P3 (Low)** | #13–#15 | Backlog. |

After P0–P1 fixes, this is a strong, well-engineered migration. The `example/` artifact is the strongest validation a PR like this can carry.
