# Patterns Index — Wayfinding

Quick map: *"I need to do X"* → *"read this file."* hve-spielberg leans on the `hyperframes` skill for deep authoring guidance; this index keeps you from re-discovering which HF reference covers which situation.

## Local patterns (in this directory)

| File | What it covers |
|---|---|
| `visual-patterns.md` | Easing vocabulary, scene-entry tweens (fade-up, scale-in, stagger, typewriter, counter), screenshot mockups (browser, floating card, device frame), colour psychology, text sizing, project-wide DON'Ts |
| `metallic-swoosh.md` | Diagonal-shine transition between two scenes (inline in root timeline, not a sub-comp) |
| `marker-highlight.md` | 5 word-emphasis patterns: highlight, circle, burst, scribble, sketchout — for kicker lines, stat reveals, before/after |
| `transition-catalog.md` | One-page map of every CSS transition family + catalog blocks, mapped to product-video moments |
| `anti-slop.md` | Cardinal sins, soft tells, polish tells — distinguishes "shipped by a marketer" from "AI default output". Includes **§ AI Tool Promo Specifics** (dogfooding loop, show-don't-tell, 1-based phase numbering) and **§ CTA discipline** (full URL on screen, match canonical command). |
| `cli-terminal-capture.md` | Professional CLI scene recording via `asciinema` + `agg`: install, shell pre-flight (prompt, secrets, size), recording flags, cast editing, theme→palette pairing, MP4 render, quality gate, troubleshooting. Read when the storyboard calls for a real terminal clip; for the no-dep fallback see `templates/scene-terminal.html`. |

## HyperFrames skill references (in `~/.claude/skills/hyperframes/` or `~/.copilot/skills/hyperframes/`)

The `hyperframes` skill is invoked in Phases 3 and 4. Once invoked, these files are accessible. Read by-task, not by-default — loading the whole skill at once eats context.

### Strategic / structural

| Need | File | Use when |
|---|---|---|
| Pick a brand (10 vendored design systems) | `../design-systems/<slug>/DESIGN.md` | **Path A** — most specific. Pick when user says "make it look like Stripe / Linear / Notion". Skips Phases 3 extraction entirely. |
| Pick a visual style (one of 8 named identities) | `visual-styles.md` (HF skill) | **Path B** — medium. Pick a mood-based identity from HF's library. Skips Phase 3 extraction, allows minor tuning. |
| Pick a palette | `palettes/` (9 files: bold-energetic, clean-corporate, dark-premium, jewel-rich, monochrome, nature-earth, neon-electric, pastel-soft, warm-editorial) | Phase 3, when authoring DESIGN.md. Pair with a visual style. |
| Motion philosophy | `references/motion-principles.md` | Phase 3 + 4 — "easing is emotion, speed is weight, build/breathe/resolve, transitions are meaning." Read once per project. |
| House style defaults | `house-style.md` | When you don't have a strong opinion. Gives sensible defaults for motion, colour, type. |
| Composition patterns (picture-in-picture, slide show, title card) | `patterns.md` | Phase 4, when wiring the root index.html. |

### Authoring craft

| Need | File | Use when |
|---|---|---|
| Choose a transition | `references/transitions/catalog.md` + family files | Phase 4 Step 4.5. Start from our `transition-catalog.md` for the wayfinding; descend into HF's catalog when you need the implementation. |
| Word-emphasis patterns | `references/css-patterns.md` | Caption emphasis, multi-line variants. Our `marker-highlight.md` is product-video focused; this file has the full depth (mode cycling, per-word styling). |
| Typography (font pairing, OpenType data) | `references/typography.md` | Phase 3 DESIGN.md — picking fonts. Especially useful for stat-heavy scenes (tabular-nums). |
| Animated charts, counters, data viz | `data-in-motion.md` | Phase 3, when authoring stat scenes — bar races, ticking counters, line charts. |

### Audio + captions

| Need | File | Use when |
|---|---|---|
| Caption authoring | `references/captions.md` | On-screen captions synced to the voiceover. **Optional in `promo`/`showcase`** (default flow renders the transcript but doesn't bake captions). **REQUIRED in `tutorial` mode** on footage segments — see `workflows/phase-5-audio.md` § "Captions (REQUIRED in tutorial mode)" and spec §7.2 (silence-only segments exempt). |
| Caption-energy techniques (audio-reactive caption styling) | `references/dynamic-techniques.md` | High-energy spots — TikTok karaoke effects, beat-sync caption emphasis. |
| Audio-reactive animation | `references/audio-reactive.md` | When music is doing narrative work — beat-matched logo pulses, frequency-driven backgrounds. Pre-extract frequency bands to JSON; never use Web Audio API at render time. |
| Native TTS | `references/tts.md` | Phase 5 fallback when no `ELEVENLABS_API_KEY` — Kokoro-82M, 54 voices, 8 languages. |
| Transcript / SRT | `references/transcript-guide.md` | If you need word-level timestamps for caption sync (HF `transcribe` is an alternative to Whisper). |

### Implementation details

| Need | File | Use when |
|---|---|---|
| CSS pattern primitives (any drawing pattern) | `references/css-patterns.md` | See above. |
| Embedding HTML pages as scenes | `references/html-in-canvas.md` | If you want to drop a live web page into a video frame (rare; usually a screenshot is better). |
| Other dynamic techniques | `references/dynamic-techniques.md` | Advanced caption + emphasis combinations. |

## Decision flow

```
Phase 1 (storytelling)
  └─ Want a templated visual identity?
      ├─ Yes → visual-styles.md  (pick one of 8) + palettes/<name>.md
      └─ No  → Phase 3 will extract brand from screenshots → DESIGN.md

Phase 3 (design)
  ├─ Scene authoring → hyperframes skill SKILL.md + patterns.md
  ├─ Animation → ../visual-patterns.md (this repo)
  ├─ Charts/counters → data-in-motion.md
  └─ Emphasis on text → ../marker-highlight.md (this repo)

Phase 4 (production)
  ├─ Root composition wiring → hyperframes patterns.md (Top-Level Composition Example)
  ├─ Inter-scene transitions → ../transition-catalog.md (this repo) → HF references/transitions/
  └─ Quality gates → SKILL.md (Quality Checks section)

Phase 5 (audio)
  ├─ Voiceover → workflows/phase-5-audio.md
  ├─ Captions (optional) → references/captions.md
  └─ Audio-reactive flourishes → references/audio-reactive.md
```

## Convention

When a phase workflow says *"see the hyperframes skill for X"*, that's a hint to invoke `Skill(hyperframes)` and then read the specific reference file from this index. Don't load the whole skill — read the one file you need.
