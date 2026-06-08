# Phase 2: Capture (Chrome DevTools)

Automatically capture **artifacts** (still screenshots and/or recorded clips) for use in video scenes.

## Capture artifacts: stills and clips

Phase 2 produces **capture artifacts**: still screenshots in `public/screenshots/`
and/or recorded clips in `public/clips/`. A scene's `Capture:` field (from the
storyboard) decides which. Recording sources (Chrome screencast for web, the
terminal path for CLI) are wired in **Layer B**; in Layer A, clip scenes consume
a `public/clips/scene-{NN}-{slug}.mp4` produced by any source (including a
user-supplied file). Stills remain the default and the fallback.

### Capture-source detection (graceful, never hard-fail)

A scene's `Capture:` value selects a source; each is feature-detected and degrades cleanly:

- `screencast` (web): usable only if the chrome-devtools MCP exposes `screencast_start`
  AND the server was started with `--experimentalScreencast=true`. Detect by attempting
  it; if the tool is absent or it errors about the flag, **fall back to `take_screenshot`**,
  set the scene's `Capture: screenshot`, and tell the user how to enable it:
  restart the chrome-devtools MCP server with `--experimentalScreencast=true`.
- `terminal` (CLI): the default path is dependency-free (author a terminal scene from real
  output, see "Recording a CLI scene"). The optional `asciinema`→video path is used only if
  `asciinema` and `agg` are on PATH; otherwise use the default authored-scene path.
- `supplied`: the user provides `public/clips/scene-{NN}-{slug}.mp4` directly.

Stills remain the universal fallback — a missing source never blocks Phase 2.

### Recording a web scene (screencast)

When `Capture: screencast` and screencast is available (see detection above):

1. Size the viewport to the composition canvas: `mcp__chrome-devtools__resize_page`
   to the Phase-1 dimensions (e.g. 1920×1080) so the recording matches render size.
2. Navigate to the scene's view and let it settle (`navigate_page` + `wait_for`).
3. `mcp__chrome-devtools__screencast_start` with `filePath: "public/clips/scene-{NN}-{slug}.mp4"`.
4. Drive the scripted interaction with the existing input tools (`click`, `wait_for`,
   `evaluate_script` for scroll). Keep the meaningful action **one continuous take** —
   never cut mid-action.
5. `mcp__chrome-devtools__screencast_stop`. Keep the clip short (≤ ~8s) unless it's a
   deliberate real-time beat (e.g. a live process); over-long clips bloat render + repo.
6. Verify the file exists and is non-empty (`ffprobe` duration > 0). If screencast was
   unavailable or the file is empty, fall back to `take_screenshot` for this scene and
   record `Capture: screenshot` in the storyboard.

The recorded `public/clips/scene-{NN}-{slug}.mp4` is consumed by the Layer-A clip-scene
archetype (`templates/scene-clip.html`) in Phase 3 — no extra wiring here.

### Recording a CLI scene (terminal)

CLI tools cannot be screencast (no DOM page). Two paths — pick by the
storyboard's intent and what's installed.

**Default — authored terminal scene (deterministic, no dependency):**
1. Run the real command and capture its stdout (a Bash run, trimmed to the salient lines).
2. Author a scene from `templates/scene-terminal.html` into `scenes/{NN}-terminal.html`,
   replacing `CMD` with the real command and the `.oline` rows with the real output.
3. This is an authored **scene** (not a clip) — it composes like any Phase-3 scene; no
   `public/clips/` file is produced. It is deterministic and on-brand.

**Recommended for motion-heavy CLI — true real-time recording with `asciinema` + `agg`:**

Use this when the *motion is the point* (streaming build logs, spinners,
TUIs like `lazygit`/`htop`, an interactive prompt). For full guidance —
pre-flight, cast editing, theme/font choices, troubleshooting — see
[`patterns/cli-terminal-capture.md`](../patterns/cli-terminal-capture.md).

Quick path (only when both `asciinema` and `agg` are on PATH; otherwise fall
back to the authored-terminal path):

1. **Prep the shell.** Open a clean terminal, set a minimal prompt, scrub
   secrets from the environment, resize to 144×32:
   ```bash
   unset HISTFILE
   export PS1='$ '
   printf '\e[8;32;144t'
   ```
2. **Record.** `--idle-time-limit` collapses dead air — without it most
   `npm install` clips are 90% waiting frames:
   ```bash
   asciinema rec --cols 144 --rows 32 --idle-time-limit 1.5 \
     --command "<cmd>" cast.cast
   ```
3. **(Optional) Edit the cast.** The `.cast` is line-delimited JSON
   (`[time, "o", "text"]`). Trim the tail, redact strings, or speed up
   sections by halving `time` values. See the pattern doc.
4. **Render to MP4.**
   ```bash
   agg --cols 144 --rows 32 --font-size 28 --theme monokai --fps-cap 30 \
     cast.cast public/clips/scene-{NN}-{slug}.mp4
   ```
   If `agg` outputs only GIF on this host (older versions), pipe through
   ffmpeg with `-vf "fps=30,scale=trunc(iw/2)*2:trunc(ih/2)*2" -pix_fmt yuv420p`
   to land on an even-dimension H.264 MP4.
5. **Compose** the scene from `templates/scene-terminal-clip.html` into
   `scenes/{NN}-terminal-clip.html` — it wraps the MP4 in a macOS-style
   window for brand parity with browser-mockup scenes. Animate the
   `.term-frame` wrapper, never the `<video>` itself.
6. **Verify** the file exists, is non-empty, and `ffprobe` reports a sane
   duration. The Footage-quality gate (below) applies — bonus checks:
   font ≥ 24px effective, no prompt cruft (`(venv)`, oh-my-zsh git status),
   no idle gaps > 1s, theme contrast matches the scene background.

If either tool is missing, do **not** prompt the user to install — fall back
to the authored-terminal path and tell them once: *"asciinema/agg not
detected — using the authored terminal scene. Install with `brew install
asciinema agg` to record real terminal motion."*

## Step 2.1: Get App URL

```json
{
  "questions": [{
    "question": "What's the app URL to capture?",
    "header": "URL",
    "options": [
      { "label": "localhost:3000", "description": "Local dev server (default React/Next.js)" },
      { "label": "localhost:5173", "description": "Local dev server (Vite)" },
      { "label": "Deployed URL", "description": "I'll provide the URL" }
    ],
    "multiSelect": false
  }]
}
```

If the app isn't running, offer to start it:
```bash
# Detect and start dev server
if [ -f "package.json" ]; then
  npm run dev &
  sleep 5
fi
```

## Step 2.2: Navigate and Capture

For each view defined in the storyboard (Phase 1, Step 1.6):

1. **Navigate** to the URL:
   - Use `mcp__chrome-devtools__navigate_page` with `type: "url"` and the target URL
   - Wait for page load with `mcp__chrome-devtools__wait_for`

2. **Set viewport** for consistent captures:
   - Desktop: `mcp__chrome-devtools__emulate` with viewport `1920x1080x2` (retina)
   - Mobile: `mcp__chrome-devtools__emulate` with viewport `390x844x3,mobile,touch`

3. **Interact** if needed (click buttons, open modals, fill forms):
   - Take a snapshot first: `mcp__chrome-devtools__take_snapshot`
   - Click elements: `mcp__chrome-devtools__click` with uid from snapshot
   - Wait for state: `mcp__chrome-devtools__wait_for` with target text

4. **Capture** the screenshot:
   - `mcp__chrome-devtools__take_screenshot` with `filePath: "public/screenshots/scene-{NN}-{description}.png"`
   - For full-page captures: set `fullPage: true`

5. **Repeat** for each storyboard scene

## Step 2.3: Capture Gallery

After all screenshots are taken, present them to the user:

```bash
ls -la public/screenshots/
```

Show each screenshot with its scene number. Ask:

```json
{
  "questions": [{
    "question": "Screenshots look good? Any views to recapture or add?",
    "header": "Review",
    "options": [
      { "label": "All good", "description": "Proceed to design phase" },
      { "label": "Recapture some", "description": "I'll specify which ones" },
      { "label": "Add more views", "description": "I need additional screenshots" }
    ],
    "multiSelect": false
  }]
}
```

### Footage quality gate

Before accepting any recorded clip, check (retake if it fails):

- **Resolution** matches the composition canvas; **fps ≥ 30**.
- **No dev artifacts** in frame: browser notifications, autofill dropdowns, devtools/console
  overlays, extension badges, or personal data (emails, tokens, real names).
- **The meaningful action is one clean, uninterrupted take** (no mid-action cut, no stray
  cursor jitter, no accidental clicks).
- **Duration** within the scene's planned slot (Phase 4 will footage-lock it).

In the Phase-2 gallery review, present each clip and prompt the user to **accept or retake**.
A rejected clip falls back to a screenshot or a re-record.

## Capture Tips

- **Wait for animations** — Use `wait_for` to ensure page is fully loaded before capturing
- **Hide cookie banners** — Use `evaluate_script` to hide overlay elements:
  ```javascript
  () => {
    document.querySelectorAll('[class*="cookie"], [class*="consent"], [class*="banner"]')
      .forEach(el => el.style.display = 'none');
  }
  ```
- **Dark mode** — If storyboard specifies dark theme, use `mcp__chrome-devtools__emulate` with `colorScheme: "dark"`
- **Retina quality** — Always use devicePixelRatio 2+ for crisp screenshots in video

## Output

Screenshots saved to `public/screenshots/scene-{NN}-{description}.png`

## Checkpoint

> "Captured [N] screenshots from [URL].
>
> Ready to move to Phase 3: Design?"
