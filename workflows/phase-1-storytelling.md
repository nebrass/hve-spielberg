# Phase 1: Storytelling

Build the narrative structure and visual plan. Reads `context.md` from Phase 0.

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
    }
  ]
}
```

## Step 1.2: Voice Selection

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

## Step 1.3: Narrative Structure

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

Adjust durations based on selected total length.

## Step 1.4: Transition Selection

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

## Step 1.5: Build Storyboard

For each scene, define:
- **Timecode** — start/end in seconds
- **Visual** — what appears on screen (screenshot reference, text, stats, mockup)
- **Voiceover** — what's being said (matched to visual content)
- **Animation** — how elements enter/exit
- **Transition** — how this scene connects to the next

Generate `storyboard.md` from `templates/storyboard.md`.

## Step 1.6: Which App Views to Capture

Based on the storyboard, list the specific app URLs/routes/views that need to be captured in Phase 2. For each scene that shows the app, define:
- URL or route to navigate to
- Specific element/state to capture (e.g., "dashboard with sample data", "modal open")
- Device viewport (desktop 1920x1080 or mobile 390x844)

## Checkpoint

> "Storyboard complete. [N] scenes, [duration]s total, [M] app views to capture.
>
> Ready to move to Phase 2: Capture?"
