# Storyboard — hve-spielberg promo

**Duration:** 60s | **Canvas:** 1920×1080 (16:9) | **Renderer:** HyperFrames
**Mode:** promo | **Theme:** light (Vercel-style)

5-scene end-to-end-pipeline emphasis. All times in seconds. Each scene maps 1:1 to a HyperFrames sub-composition under `scenes/`.

VO timing discipline (per `workflows/phase-5-audio.md`):
- VO starts ≥1.0s after scene start (entry buffer for visuals to land)
- VO ends ≥0.5s before scene end (tail buffer for breathing)
- Adjacent scenes OVERLAP during the 0.4s crossfade window (data-duration extends 0.4s past nominal end, next data-start moves 0.4s earlier)
- The VO end-times below are **nominal estimates** mirrored from `voiceover.py`'s per-section budget; rendered ElevenLabs durations vary ±0.5s. Verify with `npx hyperframes transcribe voiceover.mp3` and adjust if any section overruns its scene window.

---

### Scene 0: Hook (meta-conceit)

**Window:** 0s → 6.4s (incl. crossfade overlap)
**Scene file:** `scenes/00-hero.html`

**Visual:**
- Large headline in Geist 600 at 180px: "One slash command."
- Subtitle in Geist 400 at 56px below: marker-highlighted "This whole video." + " Made in Claude Code."
- Marker-sweep highlight on "This whole video." — Vercel ship-red `#ff5b4f` (`patterns/marker-highlight.md` § highlight mode)
- Canvas `#ffffff`, near-black text `#171717`

**Voiceover (1.0s → ~5.0s):**
> "One slash command. This whole video. Made in Claude Code."

**Animation:**
- Headline `tl.fromTo('#hl', {y:60, autoAlpha:0}, {y:0, autoAlpha:1, duration:0.7, ease:'expo.out'}, 0.3)`
- Subtitle `tl.fromTo('#sub', {y:24, autoAlpha:0}, {y:0, autoAlpha:1, duration:0.5, ease:'power2.out'}, 1.1)`
- Marker sweep on "This whole video.": `tl.to('#mh-this', { scaleX: 1, duration: 0.5, ease: 'power2.out' }, 1.8)`

**Transition to next:** crossfade 0.4s at 6s (incoming-only fade-in on scene 1)

---

### Scene 1: How (terminal mockup — visual proof)

**Window:** 6s → 16.4s (incl. crossfade overlaps both ends)
**Scene file:** `scenes/01-how.html`

**Visual:**
- A simulated terminal pane (dark `#0a0a0a` chrome on white canvas)
- Title bar: "claude code"
- Prompt line `$ /hve-spielberg` (no argument — matches the canonical CLI)
- 4 checkmark lines stream in with stagger:
  1. ✓ Interviewed about your product
  2. ✓ Picked the Vercel design system
  3. ✓ Captured your live app
  4. ✓ Rendered `final.mp4`
- Closing line: "Done in 14m 22s"

**Voiceover (7.4s → ~15.0s):**
> "Inside Claude Code. Slash Aitch Vee Ee Spielberg. It interviews you, picks a brand, captures your app, renders the video."

**Animation:**
- Terminal panel `tl.fromTo('#term', {y:40, autoAlpha:0}, {y:0, autoAlpha:1, duration:0.6, ease:'power3.out'}, 0.2)`
- Prompt line at 0.7s; 4 checkmarks stagger 0.55s apart starting at 1.3s
- "Done in 14m 22s" at 3.7s

**Transition to next:** crossfade 0.4s at 16s

---

### Scene 2: Pipeline (the 6 phases)

**Window:** 16s → 32.4s
**Scene file:** `scenes/02-pipeline.html`

**Visual:**
- Top headline in Geist 600 at 80px: "Six phases. In order."
- 6 phase chips in a 3×2 grid (`#ffffff` cards, Vercel shadow-as-border), numbered **1–6** (not 0–5; 1-based for viewer-facing content):
  - 1. **Discover the product** — using design thinking
  - 2. **Write the narrative** — promo or showcase, scene by scene
  - 3. **Capture the live app** — via Chrome DevTools, every viewport
  - 4. **Design the scenes** — brand DNA applied to HTML
  - 5. **Compose the timeline** — GSAP tweens, sub-second precision
  - 6. **Render the video** — headless Chrome, deterministic MP4

**Voiceover (17.4s → ~31.5s, ~14s):**
> "Six phases. Discover with design thinking. Storyboard the narrative. Capture via Chrome DevTools. Design with brand DNA. Compose with GSAP at sub-second precision. Render to deterministic MP4."

**Animation:**
- Headline `fromTo({y:30, autoAlpha:0} → {y:0, autoAlpha:1}, 0.5s, expo.out)` at 0.3s
- 6 chips stagger in from `{y:30, autoAlpha:0}` at 1.0s, 0.18s stagger

**Transition to next:** crossfade 0.4s at 32s

---

### Scene 3: Proof (the 3 tools that made this video)

**Window:** 32s → 47.4s
**Scene file:** `scenes/03-features.html`

**Visual:** 3 horizontal bands stacked vertically (Geist; develop-blue `#0a72ef` accent words):
- **01. Vercel design system.** *Geist typography. Black on white. Shadow-as-border. The brand DNA, vendored — not approximated.*
- **02. ElevenLabs · Whisper · Freesound.** *Voice generated. Timing verified. Score licensed CC-BY. The audio pipeline, end to end.*
- **03. Headless Chrome render.** *Fifteen minutes from prompt to MP4. Deterministic. Re-runnable. Yours to edit.*

**Voiceover (33.4s → ~46.0s):**
> "This video proves the loop. Vercel design system. ElevenLabs voiceover. Whisper-verified timing. Freesound score. Headless Chrome render. Fifteen minutes, not three weeks."

**Animation:**
- 3 bands `fromTo({x:-30, autoAlpha:0} → {x:0, autoAlpha:1}, 0.5s, power3.out, stagger:0.55)` at 0.4s

**Transition to next:** crossfade 0.4s at 47s

---

### Scene 4: CTA (install + URL)

**Window:** 47s → 60s (held final frame)
**Scene file:** `scenes/04-cta.html`

**Visual:**
- Install command pill on dark `#0a0a0a`: `/hve-spielberg` (no required argument — matches canonical CLI)
- Hairline rule below
- Brand wordmark "hve-spielberg" in Geist 600 at 96px, letter-by-letter stagger
- URL row in Geist Mono 32px: `github.com/` (muted) + `nebrass/hve-spielberg` (primary)
- Meta line in Geist 400 at 24px — "MIT · open source · your turn to ship something good"
- Held final 2s (no exit animation; this is the closing scene)

**Voiceover (48.4s → ~58.5s):**
> "Slash Aitch Vee Ee Spielberg, in Claude Code. Free, open source on GitHub at nebrass slash hve dash spielberg. Your turn to ship something good."

**Animation:**
- Install pill `fromTo({y:40, autoAlpha:0} → {y:0, autoAlpha:1}, 0.6s, expo.out)` at 0.3s
- Hairline rule width 0→540 over 0.7s at 0.9s
- Wordmark letters stagger in from `{y:20, autoAlpha:0}` at 1.1s (0.06s stagger)
- URL row at 2.2s
- Meta line at 2.9s
- Held from ~3.4s through scene end

**Transition to next:** *none — closing scene, ends on held final frame*
