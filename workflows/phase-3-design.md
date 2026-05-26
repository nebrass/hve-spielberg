# Phase 3: Design (HyperFrames scene templates)

Translate the visual identity captured in Phase 2 into a `DESIGN.md` and a set of brand-matched HTML scene templates. Output is consumed by Phase 4 (composition assembly).

The authoring engine is **HyperFrames** (HTML + GSAP). There is no React, no JSX, no `useCurrentFrame`. Scene timing is expressed in **seconds** via `data-start` and `data-duration` attributes; motion is authored as GSAP tweens on paused timelines.

## Step 3.1: Seed DESIGN.md (3 strategies)

Pick the most specific path that Phase 1 Step 1.2 set up.

### Path A — Curated design system (fastest)

**If Phase 1 recorded `design_system: <slug>`** in `project-plan.md` (one of `stripe`, `linear-app`, `apple`, `notion`, `vercel`, `airbnb`, `github`, `cal`, `arc`, `bento`), the brand specification ships with the skill. Copy it straight into the project root:

```bash
cp ${SKILL_DIR}/design-systems/<slug>/DESIGN.md ./DESIGN.md
```

Every preset includes the sections a HyperFrames composition actually needs: atmosphere, palette, typography, depth, **motion** (the section that distinguishes a video preset from a generic web spec), per-scene-type applications, and brand-specific anti-patterns. See `design-systems/README.md` for the catalog.

Then skim the captured screenshots only for **product-specific overrides**: a custom logo wordmark, a screenshot that suggests a different shade of the brand's accent colour, or a UI element worth referencing in a feature scene. Note these as **additions** to the seeded DESIGN.md, not replacements. Skip the rest of this section.

### Path B — HyperFrames named style (medium)

**If Phase 1 recorded `style: <name>`** (Swiss Pulse, Velvet Standard, Deconstructed, Maximalist Type, Data Drift, Soft Signal, Folk Frequency, Shadow Cut), invoke `Skill(hyperframes)` and read `visual-styles.md` for that style's palette, type, and motion feel. Pre-fill DESIGN.md from those values; skim the screenshots only to spot any conflicting brand cue worth overriding. Skip the rest of this section.

### Path C — Derive from screenshots (default)

Analyze the captured screenshots to identify the app's design language:

- **Color palette** — dominant colors, accent colors, surface/background, on-surface text
- **Typography** — font families (web-safe or Google Fonts equivalents), weight ladder, size relationships
- **Spacing** — padding, margins, gaps
- **Shape language** — border radius, shadow elevation, border treatment
- **Visual style** — glassmorphism, flat, material, neumorphism, brutalist, editorial

Write `DESIGN.md` at the project root. We use this as the design contract — it satisfies the HyperFrames Visual Identity Gate (which otherwise accepts a `visual-style.md`, a named style preset, or a 3-question fallback):

```markdown
## Design Contract

### Palette
- Primary:    #3b82f6
- Secondary:  #8b5cf6
- Surface:    #0f172a (dark) | #ffffff (light)
- On-surface: #f8fafc | #1e293b
- Accent:     #22c55e

### Typography
- Display:  Inter Bold, 80–120px
- Headline: Inter Bold, 60–80px
- Body:     Inter Regular, 32–44px
- Mono:     JetBrains Mono (for code excerpts)

### Shape
- Radius:    12px (cards), 999px (pills)
- Shadow:    0 30px 60px rgba(0,0,0,0.35)
- Borders:   1px hsl(220 14% 24%) for dark, 1px hsl(220 14% 90%) for light

### Motion Defaults
- Entrance ease: power3.out
- Stagger:       0.08–0.12s
- Transition:    crossfade 0.4s; metallic-swoosh between major sections only
```

The Phase 4 composition will reference values from this file; do not hard-code colors or font sizes in scene templates that aren't also documented here.

## Step 3.2: Author Scene Templates via the HyperFrames Skill

Invoke the `hyperframes` skill and request authoring of brand-matched scene templates. Each template is a **standalone HTML file** that will later be loaded as a sub-composition by the Phase 4 root `index.html`.

```
Invoke: Skill(hyperframes)
Context: "Author scene templates for {project-name}, using the palette and
typography defined in DESIGN.md. Output one HTML file per scene archetype
below into scenes/. Each file is a complete sub-composition with paused
GSAP timeline registered on window.__timelines."
```

Request these scene archetypes (adapt to mode — promo or showcase):

| File | Purpose |
|---|---|
| `scenes/00-title-card.html` | Animated headline + subtitle for opening/closing |
| `scenes/01-pain-point.html` | Statement scene: large text, optional icon, restrained motion |
| `scenes/02-feature.html` | Browser mockup + title + supporting copy |
| `scenes/03-stat.html` | Animated counter + label, used for proof points |
| `scenes/04-cta.html` | Call to action: headline, button, URL, brand sign-off |

Each scene template must:

- Be a valid HyperFrames **sub-composition** — the root is a `<div data-composition-id="…" data-width="{W}" data-height="{H}">` wrapped in a `<template>` (per HyperFrames `patterns.md`). Use the canvas dimensions chosen in Phase 1 (1920×1080, 1080×1920, 1080×1080, or 1080×1350). Sub-comps loaded via `data-composition-src` *require* this `<template>` wrapper; only the root `index.html` skips it.
- Author the **resting layout first** in static CSS, then layer GSAP entrance tweens via `gsap.from()`. Never animate to a position — animate from an offset to the rest position.
- Initialize and register the timeline: `window.__timelines = window.__timelines || {}; window.__timelines["<composition-id>"] = tl;` (paused).
- Use palette and typography tokens from `DESIGN.md`. Reference colors and fonts inline; HyperFrames embeds supported fonts automatically.
- Place every visible animated element at `opacity: 0` inline so the first paint is invisible.
- Use the canvas dimensions selected in Phase 1 — do not hard-code 1920×1080 if the project is vertical or square.

### Scene template skeleton

```html
<template id="scene-00-title-card-template">
  <div data-composition-id="scene-00-title-card"
       data-width="1920" data-height="1080"> <!-- swap for 1080×1920 / 1080×1080 / 1080×1350 if vertical / square / portrait -->

    <h1 id="title" style="opacity:0">Your headline here</h1>
    <p  id="subtitle" style="opacity:0">Supporting copy</p>

    <style>
      [data-composition-id="scene-00-title-card"] {
        position: absolute; inset: 0;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        background: #0f172a;             /* from DESIGN.md surface */
        color: #f8fafc;                  /* from DESIGN.md on-surface */
        font-family: "Inter", sans-serif;
      }
      [data-composition-id="scene-00-title-card"] #title    { font-size: 96px; font-weight: 800; }
      [data-composition-id="scene-00-title-card"] #subtitle { font-size: 44px; margin-top: 24px; }
    </style>

    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      // Always use fromTo() for opacity tweens. tl.from() with CSS opacity:0
      // rest state causes a flash-then-disappear bug under stagger.
      // See patterns/visual-patterns.md § "tl.from() stagger trap".
      tl.fromTo("#title",
        { y: 40, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, ease: "power3.out" },
        0.2);
      tl.fromTo("#subtitle",
        { y: 24, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.5, ease: "power2.out" },
        0.5);
      window.__timelines["scene-00-title-card"] = tl;
    </script>
  </div>
</template>
```

The `data-composition-id` value on the inner `<div>` must match the `data-composition-id` on the loader in the Phase 4 root `index.html`.

Animation pattern reference: `patterns/visual-patterns.md`.
Transition pattern reference (when an archetype owns its own outgoing flourish): `patterns/metallic-swoosh.md`.

**Before authoring a scene from scratch**, check the HyperFrames catalog — blocks like `app-showcase`, `ui-3d-reveal`, `data-chart`, `logo-outro`, and `reddit-post` are drop-in sub-compositions that cover most product-video archetypes. See Phase 4 Step 4.2 for the `npx hyperframes add <name>` workflow. Pulling a catalog block is almost always faster than hand-authoring an equivalent scene.

## Step 3.3: Preview and Iterate

Run the HyperFrames preview server against the `scenes/` directory to open each template in a scrubbable timeline UI:

```bash
npx hyperframes preview scenes/00-title-card.html
```

Iterate one scene at a time. Common issues to fix before moving on:

- Overlapping elements at rest (run `npx hyperframes inspect scenes/00-title-card.html --samples 5` — per-scene templates need fewer samples than full compositions)
- Text contrast failures (run `npx hyperframes validate scenes/00-title-card.html`)
- Animations that imply an exit (Phase 4 transitions own the exit — see DON'Ts in `SKILL.md`)

Then ask the user:

```json
{
  "questions": [{
    "question": "How do the branded scene templates look?",
    "header": "Review",
    "options": [
      { "label": "Looks great", "description": "Proceed to composition assembly (Phase 4)" },
      { "label": "Needs refinement", "description": "I'll give specific feedback per scene" }
    ],
    "multiSelect": false
  }]
}
```

## Output

- `DESIGN.md` — design contract (palette, typography, shape, motion defaults)
- `scenes/*.html` — brand-matched HyperFrames scene templates
- `scenes/assets/` — any decorative assets (icons, brand marks) referenced by templates

Phase 2 screenshots already live at `public/screenshots/`; Phase 4 will reference both directories from the root composition.

## Checkpoint

> "Design contract and [N] scene templates ready. Palette + typography locked in `DESIGN.md`. Templates previewed individually and pass `hyperframes inspect`.
>
> Ready to move to Phase 4: Composition assembly?"
