# Phase 3: Design (frontend-design Integration)

Generate brand-matched Remotion scene components using the `frontend-design` skill.

## Step 3.1: Extract Brand from Screenshots

Analyze the captured screenshots to identify the app's design language:

- **Color palette** — dominant colors, accent colors, background colors
- **Typography** — font families, sizes, weights
- **Spacing** — padding, margins, gaps
- **Shape language** — border radius, shadows, borders
- **Visual style** — glassmorphism, flat, material, neumorphism

Create a `visual-brief.md` summarizing the brand:

```markdown
## Visual Brief

### Colors
- Primary: #3b82f6
- Secondary: #8b5cf6
- Background: #0f172a (dark) / #ffffff (light)
- Text: #f8fafc / #1e293b
- Accent: #22c55e

### Typography
- Headlines: Inter Bold, 60-90px
- Body: Inter Regular, 32-44px
- Mono: JetBrains Mono (for code)

### Style
- Border radius: 12px
- Shadows: large, soft (0 20px 60px rgba(0,0,0,0.3))
- Glass effects: backdrop-blur(20px), semi-transparent backgrounds
```

## Step 3.2: Invoke frontend-design Skill

Use the `frontend-design` skill to generate Remotion-compatible scene components:

```
Invoke: /frontend-design
Context: "Generate Remotion video scene components matching this brand..."
```

Request these components:
1. **SceneWrapper** — Full-frame background with brand colors, gradient, or pattern
2. **TitleSlide** — Animated headline + subtitle for opening/closing scenes
3. **FeatureCard** — Screenshot in browser mockup + title + description overlay
4. **StatDisplay** — Animated counter/stat with label
5. **CTAScene** — Call-to-action with button, URL, and branding

Each component must:
- Be a valid Remotion component (uses `useCurrentFrame()`, `interpolate()`, `spring()`)
- Accept props for customization (text, colors, timing)
- Match the extracted brand colors and typography
- Use 1920x1080 (full HD) as the base frame size
- Follow animation guidelines from `remotion-best-practices`

## Step 3.3: Review Components

Launch Remotion Studio to preview each component:

```bash
npx remotion studio
```

Ask the user to review:

```json
{
  "questions": [{
    "question": "How do the branded components look?",
    "header": "Review",
    "options": [
      { "label": "Looks great", "description": "Proceed to production" },
      { "label": "Needs refinement", "description": "I'll give feedback" }
    ],
    "multiSelect": false
  }]
}
```

## Output

- `visual-brief.md` — brand analysis
- `src/components/` — generated Remotion scene components

## Checkpoint

> "Design components ready. [N] branded components generated matching your app's style.
>
> Ready to move to Phase 4: Production?"
