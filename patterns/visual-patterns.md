# Visual Patterns — Animation Toolkit

Reference guide for animation techniques in hve-spielberg video productions.

## Spring Physics

Use Remotion's `spring()` for natural, organic motion:

```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

// Gentle entrance
const scale = spring({ frame, fps, config: { damping: 200, stiffness: 100 } });

// Bouncy entrance
const bounce = spring({ frame, fps, config: { damping: 12, stiffness: 200 } });

// Quick snap
const snap = spring({ frame, fps, config: { damping: 200, stiffness: 400 } });
```

## Timing Curves

Use `interpolate()` for precise, predictable timing:

```tsx
import { interpolate, Easing } from 'remotion';

// Slide in from left
const translateX = interpolate(frame, [0, 20], [-100, 0], {
  extrapolateRight: 'clamp',
  easing: Easing.out(Easing.cubic),
});

// Fade in
const opacity = interpolate(frame, [0, 15], [0, 1], {
  extrapolateRight: 'clamp',
});
```

## Scene Entry Patterns

### Fade Up

Elements fade in while sliding up slightly — professional, clean.

### Scale In

Elements scale from 0.8 to 1.0 with spring physics — energetic, modern.

### Stagger

Multiple elements appear one after another with 5-8 frame delays — organized, structured.

### Typewriter

Text appears character by character — engaging for headlines.

## Screenshot Presentation

### Browser Mockup with 3D Tilt

```tsx
<div style={{
  transform: `perspective(1000px) rotateY(-5deg) rotateX(3deg)`,
  boxShadow: '0 30px 60px rgba(0,0,0,0.4)',
  borderRadius: 12,
  overflow: 'hidden',
}}>
  <Img src={staticFile('screenshots/scene-01.png')} />
</div>
```

### Floating Card

Screenshot with rounded corners, large shadow, slight rotation — premium feel.

### Device Frame

Screenshot inside a laptop/phone frame — realistic context.

## Transition Ideas

| Transition | Best For | Implementation |
|------------|----------|---------------|
| Crossfade | General purpose | `TransitionSeries` with `fade()` |
| Metallic Swoosh | Section changes | See `metallic-swoosh.md` |
| Zoom Through | Feature reveals | Scale up + opacity |
| Slide Up | Sequential content | TranslateY animation |
| Wipe | Before/after reveals | Gradient mask |

## Color Psychology

| Color | Feeling | Use For |
|-------|---------|---------|
| Blue (#3b82f6) | Trust, reliability | SaaS, enterprise |
| Purple (#8b5cf6) | Innovation, premium | AI, creative tools |
| Green (#22c55e) | Growth, success | Fintech, health |
| Orange (#f97316) | Energy, urgency | CTAs, highlights |
| Red (#ef4444) | Urgency, passion | Sales, alerts |

## Text Sizing Guide

| Element | Size Range | Weight |
|---------|-----------|--------|
| Hero headline | 80-120px | Bold/Black |
| Section title | 60-80px | Bold |
| Subtitle | 40-56px | Medium |
| Body text | 32-44px | Regular |
| Caption | 24-32px | Regular |
| Stat number | 90-140px | Bold |

## DON'Ts (Critical)

- **No CSS transitions** — Remotion uses frame-based animation, not CSS
- **No jitter/shake** — Looks cheap and unprofessional
- **No full 360 rotations** — Disorienting; subtle tilts only
- **No clipPath transitions** — Black sliver artifacts; use crossfade + shine
- **No tiny text** — If it's smaller than 28px, it won't be readable in video
