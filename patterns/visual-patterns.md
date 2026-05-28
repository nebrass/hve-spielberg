# Visual Patterns — Animation Toolkit

Reference for animation choices in hve-spielberg productions. The renderer is **HyperFrames** (HTML + GSAP). Times are in **seconds**, not frames. All motion is authored as GSAP tweens on a paused timeline; HyperFrames drives playback.

## Easing Vocabulary

GSAP eases map to product-video moods. Pick the ease first — it carries more emotional weight than duration.

| Ease | Feel | Use For |
|------|------|---------|
| `power3.out` | Confident landing, no overshoot | Titles, headlines, value props |
| `power2.out` | Gentle settle | Body text, subtitles, fades |
| `back.out(1.4)` | Slight overshoot, playful | Stats, badges, callouts |
| `expo.out` | Fast then very gentle | Hero reveals, screenshot drops |
| `power1.inOut` | Continuous, mechanical | Counters, progress, scroll |
| `none` (linear) | No easing | Numeric counters, marquee loops |

Avoid `elastic` and `bounce` in product videos — they read as toy-like.

## Entrance Tweens

Author every entrance with `gsap.from()` — describe where the element comes **from**; its CSS resting state is the destination.

```html
<h1 id="hero" style="opacity:0">Your headline</h1>
<script>
  const tl = gsap.timeline({ paused: true });
  // Use fromTo with EXPLICIT end state — see "tl.from() stagger trap" below.
  tl.fromTo("#hero",
    { y: 40, opacity: 0 },
    { y: 0, opacity: 1, duration: 0.6, ease: "power3.out" },
    0.2);
  window.__timelines["scene-1"] = tl;
</script>
```

Key rules:

- The element's **resting style is its final state**. Don't animate to a position — animate **from** an offset to the rest position. HyperFrames inspects the rest layout to flag overlaps.
- Start `opacity: 0` inline on the element so the first paint is invisible.
- Times are seconds. The third positional arg to `tl.fromTo()` is the **absolute start time on the timeline**, not a delay.
- **Prefer `tl.fromTo()` over `tl.from()` whenever opacity is involved.** See trap below.

### The `tl.from()` stagger trap (read this before staggering opacity)

GSAP `tl.from()` records the END state at **registration time** by reading the element's *current computed style*. If the CSS rest state is `opacity: 0` (as it should be to prevent FOUC), the recorded end is also `opacity: 0` — so the animation goes `opacity 0 → 0`, never appearing.

The naive workaround — adding a `tl.to(..., { opacity: 1, duration: 0.01 })` snap right after the `tl.from(...)` — works for a single element but **breaks horribly with stagger**:

1. At the timeline position, all elements snap to `opacity: 1` simultaneously (the `tl.to` doesn't stagger).
2. As each subsequent staggered `tl.from` activates, it re-applies its recorded from-state (`opacity: 0`), **re-hiding the element after a sibling has already revealed it**.

Visible symptom: every staggered element flashes briefly visible, then disappears suddenly as its own tween activates.

**Always use `tl.fromTo()` for opacity tweens** — both states are explicit, no current-state recording, no race with snap-hacks:

```js
// ✅ correct — works with stagger
tl.fromTo(".chip",
  { y: 30, opacity: 0 },
  { y: 0, opacity: 1, duration: 0.4, ease: "power3.out", stagger: 0.18 },
  1.0);

// ❌ wrong — flashes-then-disappears under stagger
tl.from(".chip", { y: 30, opacity: 0, duration: 0.4, stagger: 0.18 }, 1.0);
tl.to(".chip", { opacity: 1, duration: 0.01 }, 1.0);
```

The failure mode is silent — there's no console error or lint warning. Elements flash visible briefly, then disappear suddenly as their staggered tween activates. If you see this pattern in a render, the cause is almost always a `tl.from()` + stagger combo on opacity-bearing elements that have `opacity: 0` in CSS.

## Scene Entry Catalog

> These snippets use `autoAlpha`, not bare `opacity`. Scene elements rest at `visibility: hidden; opacity: 0` in CSS (see the DON'Ts below); `autoAlpha` tweens opacity *and* clears `visibility`, so the element actually appears. A plain `opacity` tween would leave `visibility: hidden` in place and the element would never show.

### Fade Up
Clean, professional. Default for headlines and body copy.

```js
tl.fromTo(".fade-up",
  { y: 40, autoAlpha: 0 },
  { y: 0, autoAlpha: 1, duration: 0.6, ease: "power3.out", stagger: 0.08 },
  0.2);
```

### Scale In
Energetic, modern. Good for badges, stat cards, CTAs.

```js
tl.fromTo(".scale-in",
  { scale: 0.85, autoAlpha: 0 },
  { scale: 1, autoAlpha: 1, duration: 0.55, ease: "back.out(1.4)" },
  0.3);
```

### Stagger
Multiple elements arriving in sequence — list items, feature pills, social proof logos.

```js
tl.fromTo(".feature-pill",
  { y: 24, autoAlpha: 0 },
  { y: 0, autoAlpha: 1, duration: 0.45, ease: "power2.out", stagger: 0.12 },
  0.4);
```

### Typewriter
Reveal headline word-by-word for emphasis. Wrap each word in a `<span class="word">` server-side or in setup.

```js
tl.fromTo(".word",
  { y: 12, autoAlpha: 0 },
  { y: 0, autoAlpha: 1, duration: 0.35, ease: "power2.out", stagger: 0.06 },
  0.2);
```

### Counter
Animate a number from 0 to a target. Use a proxy object — never tween `textContent` directly.

```js
const stat = { v: 0 };
tl.to(stat, {
  v: 12_500,
  duration: 2.2,
  ease: "power1.out",
  onUpdate: () => { document.getElementById("stat").textContent = Math.round(stat.v).toLocaleString(); }
}, 0.8);
```

## Screenshot Presentation

### Browser Mockup with 3D Tilt

Pure CSS — no GSAP needed for the tilt itself.

```html
<div class="mockup">
  <img src="public/screenshots/scene-01.png" alt="">
</div>

<style>
  .mockup {
    transform: perspective(1000px) rotateY(-5deg) rotateX(3deg);
    box-shadow: 0 30px 60px rgba(0,0,0,0.4);
    border-radius: 12px;
    overflow: hidden;
    max-width: 75%;
  }
  .mockup img { width: 100%; display: block; }
</style>
```

Animate the mockup's entrance with `gsap.from()` — `y`, `opacity`, `scale`. Keep the perspective static; animating perspective values is jittery.

### Floating Card
Screenshot with rounded corners + large soft shadow. Float in from below (`y: 60, opacity: 0, ease: "expo.out", duration: 0.9`).

### Device Frame
Wrap the `<img>` in a device frame `<div>` (laptop or phone). Frame is static — the screenshot **inside** can pan or scroll via a child wrapper translated by GSAP.

## Transition Ideas

Scene-to-scene transitions are authored at the **composition level**, not inside a scene. HyperFrames supports CSS transitions for most cases and shader transitions for cinematic moments.

| Transition | Best For | Implementation |
|------------|----------|---------------|
| Crossfade | Default everywhere | Outgoing scene `opacity: 1 → 0` on a `gsap.to()` synchronized with incoming `opacity: 0 → 1`. |
| Metallic Swoosh | Section changes, brand beats | See `metallic-swoosh.md` (CSS gradient + GSAP). |
| Zoom Through | Feature reveals | Outgoing `scale: 1 → 1.15, opacity: 1 → 0`; incoming `scale: 0.95 → 1, opacity: 0 → 1`. |
| Slide Up | Sequential narrative beats | Outgoing `y: 0 → -80, opacity → 0`; incoming `y: 60 → 0, opacity → 1`. |
| Wipe | Before/after reveals | Mask the outgoing scene with a CSS `linear-gradient` whose `background-position` is animated. |

Transition durations: 0.3–0.5s for crossfades, 0.5–0.8s for shine/wipe. Anything over 1s reads as sluggish in a 30–60s spot.

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
| Hero headline | 80–120px | Bold/Black |
| Section title | 60–80px | Bold |
| Subtitle | 40–56px | Medium |
| Body text | 32–44px | Regular |
| Caption | 24–32px | Regular |
| Stat number | 90–140px | Bold |

HyperFrames' `validate` enforces WCAG AA contrast (4.5:1 normal text, 3:1 large text ≥24px or ≥19px bold). Tiny text is *not* auto-flagged — self-police anything below 24px because it loses legibility at typical playback resolutions.

## DON'Ts (Critical)

- **No jitter or shake** — looks cheap; HyperFrames inspect will not catch this, you must self-police.
- **No full 360° rotations** — disorienting. Subtle `rotateY` ≤ 8° or `rotateZ` ≤ 4° only.
- **No exit animations on non-final scenes** — let the transition handle the exit. Animating the same element out and then transitioning the scene out is double-motion.
- **No `clipPath` for transitions** — produces anti-aliased black slivers between scenes. Use crossfade + shine instead (see `metallic-swoosh.md`).
- **Never animate `display`, `visibility`, or call `.play()` inside a timeline** — GSAP can't tween `display`/`visibility` (they're binary), and `.play()` from inside a timeline breaks HyperFrames' deterministic seek. Use `autoAlpha` (which tweens opacity AND toggles visibility) or `opacity` + `pointer-events: none`:
  ```js
  // ✅ correct — autoAlpha tweens opacity AND toggles visibility
  tl.fromTo("#el", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.5 }, 0.3);

  // ❌ wrong — visibility:hidden is binary, GSAP can't interpolate it
  tl.from("#el", { visibility: "hidden", duration: 0.5 }, 0.3);
  ```
- **Never animate `<img>` dimensions directly** — wrap each animated `<img>` in a non-timed `<div>` and tween the wrapper's `transform` (`scale`, `translate`). Animating `width`/`height` on the `<img>` causes layout recompute that breaks deterministic seek.
- **Never use `gsap.set()` at script-load time on elements that enter the timeline later** — sub-comp clips with `data-start > 0` aren't in the DOM at page load. Their elements don't exist yet, so `gsap.set("#late-element", ...)` is a no-op. Instead, use `tl.set(selector, vars, timePosition)` *inside the timeline* at or after the clip's `data-start`:
  ```js
  // ✅ correct — runs inside the timeline at t=5s, after #late-card exists
  tl.set("#late-card", { opacity: 0, x: -100 }, 5);
  tl.to("#late-card", { opacity: 1, x: 0, duration: 0.5 }, 5);

  // ❌ wrong — fires before #late-card is rendered, has no effect
  gsap.set("#late-card", { opacity: 0, x: -100 });
  tl.to("#late-card", { opacity: 1, x: 0, duration: 0.5 }, 5);
  ```
- **No tiny text** — below 24px is unreadable in rendered video. `validate` won't warn (it's contrast-only), so self-police.
