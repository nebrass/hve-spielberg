# Phase 1: Storytelling

Build the narrative structure and visual plan. Reads `context.md` from Phase 0.

## The creative brief — user-owned selections (present them, don't decide them)

This phase collects the choices that define how the video looks and sounds. **These are the
user's to make, not yours to infer** (see `SKILL.md` § "creative instinct governs craft, not the
user's choices"). Steps 1.1–1.5 each present a `{"questions": [...]}` block — you **must** surface
every one as a native prompt, even when your Phase-0 analysis makes the "obvious" choice feel
settled. Pre-highlight a smart default and say why you recommend it, but let the user pick. The
levers, in order:

| Step | Choice | Never skip because… |
|---|---|---|
| 1.1 | Duration · Theme (light/dark) · Aspect ratio | "it's obviously a 60s 16:9" — the user may want a 9:16 short |
| 1.2 | **Visual identity / design system** (10 brands, a named style, or derive) | "it's a dev tool, so Vercel" — brand is the single most visible choice; always show the picker |
| 1.3 | Voiceover voice | "Matilda is the default" — voice sets the whole tone |
| 1.5 | Section transition · speed | "crossfade is fine" — the user may want the branded swoosh |

Present them as a short sequence (or, if your runtime supports multi-question prompts, batch 1.1
together as shown). Record every answer in `project-plan.md`. Do not advance to the storyboard
until the identity (Step 1.2) and voice (Step 1.3) are chosen — a storyboard written before the
brand is picked bakes in the wrong look.

## Step 1.1: Duration & Theme

```json
{
  "questions": [
    {
      "question": "How long should the video be?",
      "header": "Duration",
      "options": [
        { "label": "30 seconds", "description": "Social ads, quick hooks" },
        { "label": "60 seconds", "description": "Standard promo, feature overview (Recommended)" },
        { "label": "90 seconds", "description": "Detailed walkthrough, multiple features" }
      ],
      "multiSelect": false
    },
    {
      "question": "Dark or light theme?",
      "header": "Theme",
      "options": [
        { "label": "Light mode", "description": "Clean, bright, professional" },
        { "label": "Dark mode", "description": "Modern, bold, dramatic" }
      ],
      "multiSelect": false
    },
    {
      "question": "What aspect ratio and canvas size?",
      "header": "Aspect",
      "options": [
        { "label": "16:9 — 1920×1080", "description": "Standard horizontal (YouTube, web, embeds) — Recommended for promos" },
        { "label": "9:16 — 1080×1920", "description": "Vertical for TikTok / Reels / Shorts" },
        { "label": "1:1 — 1080×1080", "description": "Square for Instagram feed / LinkedIn carousels" },
        { "label": "4:5 — 1080×1350", "description": "Portrait for Instagram feed (taller than 1:1)" }
      ],
      "multiSelect": false
    }
  ]
}
```

Record the choice in `project-plan.md`. Phase 3 scene templates and the Phase 4 root composition will use these dimensions for their `data-width` / `data-height`. Once chosen, the canvas size is locked — scene templates won't reflow gracefully across aspect ratios.

## Step 1.2: Visual Identity (3 strategies)

The single most visible choice in the whole video. **Always present this picker** — never
pre-select a strategy or a brand on the user's behalf from your Phase-0 read (that's the exact
"agent silently picked Vercel" failure). You may *recommend* one (e.g. "your commits look like a
dev tool — Vercel or Linear would fit") and pre-highlight it, but the user chooses. Three ways to
lock in the identity:

```json
{
  "questions": [{
    "question": "How should the visual identity be set?",
    "header": "Identity",
    "options": [
      { "label": "Use a curated design system", "description": "Pick a known brand: Stripe, Linear, Apple, Notion, Vercel, Airbnb, GitHub, Cal, Arc, Bento. Phase 3 copies design-systems/<name>/DESIGN.md straight into the project. Best when you want a specific brand's look." },
      { "label": "Pick a HyperFrames named style", "description": "Pick from 8 styles: Swiss Pulse, Velvet Standard, Deconstructed, Maximalist Type, Data Drift, Soft Signal, Folk Frequency, Shadow Cut. Phase 3 seeds DESIGN.md from the named style; still allows minor screenshot-based tuning." },
      { "label": "Derive from the captured screenshots", "description": "Phase 3 extracts colors, typography, and shape language from the app's own screenshots. Best when you want the video to match the product's existing look exactly." }
    ],
    "multiSelect": false
  }]
}
```

**If "Use a curated design system" is chosen**, immediately present the brand picker below — do not
pick a brand yourself.

### If "curated design system" was picked

Ask which one:

```json
{
  "questions": [{
    "question": "Which design system?",
    "header": "System",
    "options": [
      { "label": "Stripe", "description": "Premium fintech — sohne-var weight 300, blue-tinted shadows, deep navy. Payments / fintech / dev tools." },
      { "label": "Linear", "description": "Engineered minimalism — Inter, restrained accent, glass surfaces. Issue trackers, SaaS, productivity." },
      { "label": "Apple", "description": "Quiet authority — SF Pro, generous whitespace, neutral palette. Hardware, consumer launches." },
      { "label": "Notion", "description": "Editorial-software — soft warmth, hand-drawn touches, calm hierarchy. Productivity, docs, content tools." },
      { "label": "Vercel", "description": "Sharp black-on-white minimalism — Geist, dramatic monochrome. Dev infra, deploy platforms." },
      { "label": "Airbnb", "description": "Warm rounded — Cereal, generous radii, soft shadows. Travel, hospitality, consumer marketplaces." },
      { "label": "GitHub", "description": "Functional dark mode — high-contrast neutrals, monospace anchors. Code platforms, dev tools." },
      { "label": "Cal.com", "description": "Friendly OSS clarity — minimal palette, approachable type. Scheduling, OSS tools." },
      { "label": "Arc", "description": "Playful chrome — gradients, vivid colour. Browsers, consumer SaaS." },
      { "label": "Bento", "description": "Playful link-in-bio — bold colour blocks. Social, creator tools." }
    ],
    "multiSelect": false
  }]
}
```

Record `design_system: <slug>` in `project-plan.md` (slugs: `stripe`, `linear-app`, `apple`, `notion`, `vercel`, `airbnb`, `github`, `cal`, `arc`, `bento`). Phase 3 will copy `design-systems/<slug>/DESIGN.md` to the project root as `DESIGN.md`. See `design-systems/README.md` for catalog details and how to add more.

### If "HyperFrames named style" was picked

Ask which one:

```json
{
  "questions": [{
    "question": "Which HyperFrames named style?",
    "header": "Style",
    "options": [
      { "label": "Swiss Pulse", "description": "Clinical, precise — SaaS, dev tools, dashboards. Black + white + one accent. Helvetica/Inter. Cinematic Zoom transitions." },
      { "label": "Velvet Standard", "description": "Premium, timeless — luxury, enterprise, keynotes. Cross-Warp Morph transitions." },
      { "label": "Deconstructed", "description": "Industrial, raw — tech launches, security, punk. Glitch / Whip-Pan transitions." },
      { "label": "Maximalist Type", "description": "Loud, kinetic — big announcements, launches. Ridged Burn transitions." },
      { "label": "Data Drift", "description": "Futuristic, immersive — AI, ML, cutting-edge tech. Gravitational Lens / Domain Warp." },
      { "label": "Soft Signal", "description": "Intimate, warm — wellness, personal stories, brand. Thermal Distortion." },
      { "label": "Folk Frequency", "description": "Cultural, vivid — consumer apps, food, communities. Swirl Vortex / Ripple Waves." },
      { "label": "Shadow Cut", "description": "Dark, cinematic — dramatic reveals, security, exposé. Domain Warp." }
    ],
    "multiSelect": false
  }]
}
```

Record `style: <name>` in `project-plan.md`. Full descriptions live in the `hyperframes` skill at `visual-styles.md` (palette, fonts, motion feel, primary shader transition). For palette pairing see `hyperframes/palettes/*.md`.

### If "derive from screenshots" was picked

No follow-up. Phase 3 will run the full extraction workflow.

## Step 1.3: Voice Selection

```json
{
  "questions": [{
    "question": "What voice for the voiceover?",
    "header": "Voice",
    "options": [
      { "label": "Matilda", "description": "Warm, confident female — polished (Recommended)" },
      { "label": "Rachel", "description": "Calm, clear female — authoritative" },
      { "label": "Daniel", "description": "Authoritative male — broadcast tone" },
      { "label": "Josh", "description": "Friendly, conversational male" }
    ],
    "multiSelect": false
  }]
}
```

## Step 1.4: Narrative Structure

Based on mode:

### Promo Mode Structure
```
Scene 1: HOOK (0-5s)        — Attention-grabbing statement + key stat
Scene 2: PAIN (5-15s)       — 2-3 pain points the audience relates to
Scene 3: SOLUTION (15-20s)  — Product reveal + one-line value prop
Scene 4: FEATURES (20-45s)  — 3-5 feature highlights with UI screenshots
Scene 5: RESULTS (45-52s)   — Stats, outcomes, social proof
Scene 6: CTA (52-60s)       — Call to action + branding
```

### Showcase Mode Structure
```
Scene 1: INTRO (0-8s)       — Product name + what it is + hero screenshot
Scene 2: WALKTHROUGH (8-35s) — Feature-by-feature tour with screenshots
Scene 3: HIGHLIGHTS (35-50s) — Design details, UX choices, tech stack
Scene 4: CLOSER (50-60s)    — Key takeaway + links/contact
```

### Tutorial Mode Structure
```
Scene 0: COLD OPEN (0-6s)   — Show the finished payoff FIRST (the end result the viewer will achieve)
Scene 1: STEP 1 (6-Xs)      — Chapter "Step 1 of M" — one concrete goal; clip when capture is available
Scene 2: STEP 2 (...)       — Chapter "Step 2 of M" — next goal in task order
Scene N: STEP M (...)       — Chapter "Step M of M" — final goal; lands back on the payoff
Scene N+1: RECAP / NEXT     — Summarize the steps + where to go next (docs, install, repo)
```

Chapters are **task-ordered**: each scene is one step with a single concrete goal, labeled
on-screen "Step N of M" (from the storyboard `Step label:`/`Chapter:` fields — see Phase 3/4).
**Cold-open on the payoff** (spec §7.2d): scene 0 is a ~2–4s teaser of the finished end-state
so the viewer knows what they're building toward. Tutorial mode **prefers clip scenes**
(`Capture: screencast`/`terminal`) but does **not require** them — without capture, steps fall
back to stills and the step labels + captions carry the narrative (spec §7.3). Break any
continuous run >~90s with an authored recap beat (Phase 4) before the next step.

Adjust durations based on selected total length.

## Step 1.5: Transition Selection

```json
{
  "questions": [
    {
      "question": "What transition between main sections?",
      "header": "Sections",
      "options": [
        { "label": "Metallic swoosh", "description": "Diagonal gradient shine sweeps across" },
        { "label": "Zoom through", "description": "Scale up and push through" },
        { "label": "Fade", "description": "Classic smooth crossfade" },
        { "label": "Slide from bottom", "description": "Next scene pushes up" }
      ],
      "multiSelect": false
    },
    {
      "question": "Transition speed?",
      "header": "Speed",
      "options": [
        { "label": "Quick (0.4s)", "description": "Snappy, energetic" },
        { "label": "Medium (0.7s)", "description": "Balanced, professional" },
        { "label": "Slow (1.2s)", "description": "Dramatic, cinematic" }
      ],
      "multiSelect": false
    }
  ]
}
```

**If "Metallic swoosh" selected:** Read [../patterns/metallic-swoosh.md](../patterns/metallic-swoosh.md) before implementing. Uses crossfade + shine overlay — do NOT use clipPath.

## Step 1.6: Build Storyboard

For each scene, define:
- **Timecode** — start/end in seconds
- **Visual** — what appears on screen (screenshot reference, text, stats, mockup)
- **Voiceover** — what's being said (matched to visual content)
- **Animation** — how elements enter/exit
- **Transition** — how this scene connects to the next

Generate `storyboard.md` from `templates/storyboard.md`.

### Capture type per scene (optional)

Each scene defaults to a still **screenshot**. A scene may instead be a **clip**
(real motion footage) by setting `Capture:` to `screencast` (web app, Phase 2),
`terminal` (CLI tool — an authored animated terminal from real command output),
`terminal-clip` (CLI tool — a **real** recording: Phase 2 runs the command
autonomously via asciinema + agg; requires a `Command:` field with the exact
shell command and honors `Record timeout:`, default scene duration + 2s — see
`patterns/cli-terminal-capture.md`), or `supplied` (you provide the file).
Prefer `terminal-clip` over `terminal` when the command's real output matters
(deploys, test runs, scaffolding) — it degrades to the authored-terminal path
automatically if asciinema/agg aren't installed. Clip scenes use the clip
fields in the storyboard template (`Clip`, `Clip in/out`, `Speed`, `Captions`).
A clip scene's on-screen duration is the footage length (see Phase 4), so plan
the scene's slot around the real clip length. Clips are available in **all**
content modes; in `promo` they must be device-framed accents (Phase 4).

## Step 1.7: Which App Views to Capture

Based on the storyboard, list the specific app URLs/routes/views that need to be captured in Phase 2. For each scene that shows the app, define:
- URL or route to navigate to
- Specific element/state to capture (e.g., "dashboard with sample data", "modal open")
- Device viewport — match the chosen canvas: desktop 1920×1080 for 16:9; mobile 390×844 for 9:16; square viewport 1080×1080 for 1:1; mobile 390×488 (or desktop crop) for 4:5

## Checkpoint

> "Storyboard complete. [N] scenes, [duration]s total, [M] app views to capture.
>
> Ready to move to Phase 2: Capture?"
