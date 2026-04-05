# Phase 4: Production (Remotion)

Build the Remotion video composition using storyboard, screenshots, and design components.

## Step 4.1: Scaffold Remotion Project

```bash
yes "" | npx create-video@latest --blank --no-git {project-name}
cd {project-name}
npm install
npm install lucide-react
```

Set composition to **1920x1080** (full HD):
```tsx
<Composition width={1920} height={1080} fps={30} durationInFrames={duration * 30} ... />
```

## Step 4.2: Import Screenshots

Copy captured screenshots into the Remotion project:
```bash
cp -r ../public/screenshots/ public/screenshots/
```

## Step 4.3: Import Design Components

Copy branded components from Phase 3:
```bash
cp -r ../src/components/ src/components/
```

## Step 4.4: Build Scene Compositions

Follow the storyboard from Phase 1 scene by scene. For each scene:

1. Create a scene component that uses the branded wrappers from Phase 3
2. Embed screenshots in browser mockups with 3D perspective
3. Add text overlays, stats, and animations
4. Apply transitions between scenes

**Use `remotion-best-practices` skill** for all Remotion patterns:
- `spring()` for natural motion
- `interpolate()` for precise timing
- `Sequence` and `Series` for scene ordering
- `TransitionSeries` for transitions between scenes

**Framing & sizing guidelines (from promo-video):**
- Fill the frame — elements should be large and confident
- Headlines: 60-90px minimum. Subtext: 32-44px
- Browser mockups: 60-80% of frame width
- Padding from edges: 60-100px
- If a scene feels empty, scale up elements

**Browser mockup pattern:**
```tsx
<div style={{
  transform: `perspective(1000px) rotateY(-5deg) rotateX(3deg)`,
  boxShadow: '0 30px 60px rgba(0,0,0,0.4)',
  borderRadius: 12,
  overflow: 'hidden',
}}>
  <Img src={staticFile('screenshots/scene-01-dashboard.png')} />
</div>
```

## Step 4.5: Preview

Launch Remotion Studio:
```bash
npx remotion studio
```

Ask:
```json
{
  "questions": [{
    "question": "How does the video look? Ready for voiceover and music?",
    "header": "Preview",
    "options": [
      { "label": "Looks good, proceed", "description": "Add voiceover and music" },
      { "label": "Needs changes", "description": "I'll give feedback" }
    ],
    "multiSelect": false
  }]
}
```

Iterate on feedback before proceeding.

## Output

- Complete Remotion composition in `src/`
- Previewable in Remotion Studio

## Checkpoint

> "Video composition built. [N] scenes, [duration]s, all screenshots integrated.
>
> Ready to move to Phase 5: Audio & Render?"
