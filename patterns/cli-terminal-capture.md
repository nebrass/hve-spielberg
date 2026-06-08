# CLI / Terminal Capture — asciinema + agg

How to produce a **professional terminal clip** for a hve-spielberg CLI scene
when the storyboard calls for *real* command output (a deploy log, a build
spinner, an interactive prompt). For the dependency-free fallback, see the
"authored terminal" path documented inline in
`workflows/phase-2-capture.md` (the `templates/scene-terminal.html` archetype).

The chrome-devtools MCP cannot screencast a terminal — there is no DOM page.
For real terminal motion we record with [asciinema](https://github.com/asciinema/asciinema),
post-process the cast, then render it to MP4 with
[agg](https://github.com/asciinema/agg). The clip is then composed via the
Layer-A `templates/scene-terminal-clip.html` archetype, which wraps the video
in a macOS-style window for brand parity with screenshot mockups.

## When to use this path

Pick the **asciinema path** when:

- The motion is the point (a streaming build log, a progress bar, animated
  spinners, a TUI like `htop`/`lazygit`, a real `npm install` cascade).
- The duration is short (≤ 8s of meaningful action) and you want the *real*
  cadence, not a synthetic one.
- You're recording your own machine and can scrub secrets cleanly.

Pick the **authored-terminal path** (`templates/scene-terminal.html`) when:

- Output is short (≤ 5 lines) and a deterministic typewriter reveal reads
  cleaner than real-time scroll.
- The command takes long enough to be boring without heavy editing.
- You don't have `asciinema` + `agg` installed and don't want a new dep.
- The environment is sensitive (production hosts, real credentials in PATH).

## Feature detection (already wired)

`SKILL.md` Prerequisites and `workflows/phase-2-capture.md` Capture-source
detection both probe `command -v asciinema` and `command -v agg`. If either
is missing the workflow degrades to the authored-terminal path and tells the
user. Do not hard-fail.

## Install

```bash
# macOS
brew install asciinema agg

# Debian / Ubuntu
sudo apt install asciinema
cargo install --git https://github.com/asciinema/agg   # agg has no apt package

# Arch
sudo pacman -S asciinema
yay -S agg-bin

# Any OS (pip fallback for asciinema)
pipx install asciinema
```

Verify:

```bash
asciinema --version    # 2.x+
agg --version          # 1.4+
```

## Recording (pre-flight)

The cast is **as professional as the shell you record in.** Spend 60 seconds
preparing the environment — it's the difference between a polished clip and a
debug log.

1. **Clean shell, no secrets.** Open a fresh terminal in a throwaway dir.
   - `unset HISTFILE` to avoid leaking shell history into TUI prompts.
   - `env | grep -iE 'token|key|secret|password'` should be empty in the
     window. Use a sub-shell with `env -i HOME=$HOME PATH=$PATH SHELL=$SHELL bash`
     if you need a hard reset.
   - Hide personal data: real names, customer hostnames, internal URLs.
2. **Brand-aligned prompt.** Set a minimal prompt that matches the video's
   visual identity. A noisy oh-my-zsh prompt reads as amateur.
   ```bash
   export PS1='$ '                              # bash
   PROMPT='%F{green}$%f '                       # zsh
   set fish_greeting "" ; function fish_prompt; printf '$ '; end   # fish
   ```
3. **Sized window, fixed font.** The render width must equal the agg output
   width (default `144 cols × 32 rows`). Resize the terminal before
   recording — agg captures cols/rows from the cast header, so a resize
   mid-record produces a jagged frame.
   ```bash
   printf '\e[8;32;144t'   # request 32 rows × 144 cols (most modern terms)
   ```
4. **Theme.** Dark background reads best in video and matches the
   `scene-terminal-clip.html` chrome. Disable transparency.
5. **Pacing.** Type at a deliberate pace — real keystrokes look more
   authentic than pasted commands. asciinema preserves your timing.

## Recording

Two modes — both produce a `.cast` JSON file you can edit before rendering.

### A. Drive a single command

```bash
asciinema rec --cols 144 --rows 32 \
  --idle-time-limit 1.5 \
  --command "npm run deploy" \
  cast.cast
```

- `--idle-time-limit 1.5` collapses any pause longer than 1.5s to 1.5s.
  This is the single most important post-production lever — without it, a
  `npm install` clip is 90% empty waiting frames.
- `--command` exits when the command exits, giving a clean tail.

### B. Drive a shell interactively (for multi-step demos)

```bash
asciinema rec --cols 144 --rows 32 --idle-time-limit 1.5 cast.cast
# ... type commands ...
exit                                              # ends the recording
```

## Editing the cast (optional, recommended)

The `.cast` file is newline-delimited JSON: the first line is the header,
each subsequent line is `[time_seconds, "o", "text"]`. You can hand-edit it.

Common edits:

- **Trim a slow tail.** Open in your editor, delete trailing lines whose
  `time` exceeds the desired duration. Update no other field.
- **Speed up a section.** Multiply the `time` field of a contiguous block by
  `0.5` (2× faster). Keep monotonic ordering — don't let times go backwards.
- **Redact a string.** Find-replace the literal token in the `text` field.
  Quote handling: the value is a JSON string, so backslash-escape `"` and
  control bytes (asciinema already does this on capture).

Re-validate by playing it back: `asciinema play cast.cast`.

## Render to MP4

`agg` renders a `.cast` to GIF by default; for hve-spielberg we want MP4.
Two routes — pick the one that lands on PATH.

### Route 1 — agg → MP4 directly (agg ≥ 1.5)

```bash
agg \
  --cols 144 --rows 32 \
  --font-size 28 \
  --theme monokai \
  --speed 1.0 \
  --fps-cap 30 \
  cast.cast public/clips/scene-{NN}-{slug}.mp4
```

### Route 2 — agg → GIF → MP4 via ffmpeg (older agg)

```bash
agg --cols 144 --rows 32 --font-size 28 --theme monokai \
    cast.cast cast.gif

ffmpeg -y -i cast.gif \
  -movflags +faststart \
  -pix_fmt yuv420p \
  -vf "fps=30,scale=trunc(iw/2)*2:trunc(ih/2)*2" \
  public/clips/scene-{NN}-{slug}.mp4
```

The `scale=trunc(iw/2)*2:trunc(ih/2)*2` filter forces even dimensions —
H.264 requires it and a raw agg GIF will sometimes be odd-width.

### Theme palette → brand parity

| `--theme` | Vibe | Pairs with palette |
|---|---|---|
| `monokai` | Warm dev-default | `bold-energetic`, `warm-editorial` |
| `solarized-dark` | Calm corporate | `clean-corporate`, `dark-premium` |
| `dracula` | High-contrast purple | `neon-electric`, `jewel-rich` |
| `nord` | Cool Nordic | `clean-corporate`, `nature-earth` |
| `gruvbox-dark` | Retro warm | `warm-editorial` |
| `github-dark` | Neutral grey | Most palettes |

For a custom theme pass `--theme bg,fg,palette` with explicit hex
(e.g. `--theme 0a0a0a,eaeaea,...`). Match the scene's `background` so the
clip blends seamlessly with the wrapper.

## Quality gate (in addition to the Phase 2 footage gate)

Before accepting a terminal clip:

- **Font size ≥ 24px effective** in the rendered frame. Agg's default is
  small; bump `--font-size` to 28–32 for 1920×1080 compositions.
- **No prompt cruft.** No `(env)` markers, no git branch names from
  oh-my-zsh, no virtualenv indicators (unless they're the story).
- **No long idle gaps.** If the clip has > 1s of motionless frames,
  re-render with a lower `--idle-time-limit`.
- **Aspect.** Agg renders 144×32 → roughly 16:5. The clip wrapper
  (`scene-terminal-clip.html`) crops/letterboxes inside its window chrome,
  but if your composition is 9:16 prefer 80×40 cols and a larger font.
- **Audio.** Cast files have no audio. The clip is muted by design — the
  voiceover narrates over it.

## Wiring into a scene

After the MP4 is at `public/clips/scene-{NN}-{slug}.mp4`:

1. Author the scene from `templates/scene-terminal-clip.html` into
   `scenes/{NN}-terminal-clip.html`. Replace `NN` and `slug` and adjust the
   window title (`zsh`, `npm`, `deploy`) to match the command.
2. The wrapper's `data-composition-id`, animation, and clip-frame chrome are
   pre-wired — never animate the `<video>` itself, animate the `.term-frame`
   wrapper per the *no img-dimension tween* DON'T.
3. Phase 4 root composition picks the clip up automatically (HyperFrames
   auto-syncs `<video>` `currentTime` to the scene window).

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Cast plays at wrong size | `--cols`/`--rows` flags missing on `rec` | Re-record; cast header is authoritative |
| MP4 is letterboxed weirdly | agg cols/rows ≠ rec cols/rows | Pass the same `--cols`/`--rows` to `agg` |
| Render fails: "height not divisible by 2" | agg GIF odd-width | Use the ffmpeg `scale=trunc(...)*2` filter |
| Spinner shows blank chars | Terminal font missing glyphs | `agg --font-family "JetBrains Mono"` (or the font installed on the render host) |
| Output trails off mid-line | `asciinema rec --command` killed by SIGINT | Re-run; let the command exit naturally, or use interactive mode + `exit` |
| Text reads too small in render | Default `--font-size 14` | Use `--font-size 28` or larger for 1080p |

## See also

- `templates/scene-terminal-clip.html` — the clip-wrapper scene archetype
- `templates/scene-terminal.html` — the authored (no-dep) fallback
- `workflows/phase-2-capture.md` § "Recording a CLI scene (terminal)"
- asciinema docs: <https://docs.asciinema.org/>
- agg repo: <https://github.com/asciinema/agg>
