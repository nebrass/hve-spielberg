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

Pick the **asciinema path** (skill-driven; see "Recording mode — autonomous"
below) when:

- The motion is the point (a streaming build log, a progress bar, animated
  spinners, a TUI like `htop`/`lazygit`, a real `npm install` cascade).
- The duration is short (≤ 8s of meaningful action) and you want the *real*
  cadence, not a synthetic one.
- The command is **non-interactive** — it runs to completion (or to a
  timeout) without needing keyboard input. asciinema's `--command` mode
  lets the skill execute it autonomously via its Bash tool; the user
  never touches the keyboard.

Pick the **authored-terminal path** (`templates/scene-terminal.html`) when:

- Output is short (≤ 5 lines) and a deterministic typewriter reveal reads
  cleaner than real-time scroll.
- The command takes long enough to be boring without heavy editing.
- You don't have `asciinema` + `agg` installed and don't want a new dep.
- The command genuinely needs a human at the keyboard (interactive prompts,
  mouse-driven TUIs).
- The environment is sensitive in ways `env -i` can't fully sanitize.

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

## Recording mode — **autonomous (skill-driven)**

The skill executes `asciinema` itself via its Bash tool. **The user does
not open a terminal or run anything by hand.** This works because
`asciinema rec --command "<cmd>"` is non-interactive: asciinema allocates
its own PTY, runs the command headless, captures stdout/stderr with
timing, and exits when the command exits.

Three things make autonomous recording reliable:

- **`--command`** — non-interactive single-shot mode. No stdin needed.
- **`timeout Ns`** — bounds runaway / non-terminating commands (`htop`,
  dev servers). Exit code 124 is non-fatal; the partial cast up to the
  timeout is still valid and renderable.
- **`env -i …`** — scrubs the parent environment so stray tokens, custom
  `PS1`, oh-my-zsh git status, virtualenv markers, etc. don't leak into
  the recording's PTY.

The single autonomous sequence (also reproduced in
`workflows/phase-2-capture.md`):

```bash
# Record — non-interactive, PTY-isolated, timeout-bounded.
timeout 60s env -i HOME="$HOME" PATH="$PATH" SHELL=/bin/bash PS1='$ ' \
  asciinema rec --cols 144 --rows 32 --idle-time-limit 1.5 \
    --command "<cmd-from-storyboard>" \
    public/clips/scene-{NN}-{slug}.cast \
  || true

# Render — also autonomous.
agg --cols 144 --rows 32 --font-size 28 --theme monokai --fps-cap 30 \
  public/clips/scene-{NN}-{slug}.cast \
  public/clips/scene-{NN}-{slug}.mp4

# Verify.
ffprobe -v error -show_entries format=duration -of csv=p=0 \
  public/clips/scene-{NN}-{slug}.mp4
```

The storyboard carries the inputs the skill needs:

```
Capture: terminal-clip
Command: shipfast deploy --env staging
Record timeout: 8s          # scene duration + ~2s
```

Why `--idle-time-limit 1.5` matters: an unmodified `npm install` cast is
~90% motionless waiting frames. With `--idle-time-limit` set, every pause
longer than 1.5s collapses to 1.5s, giving a clip that *feels* real-time
without dragging.

### Edge cases the autonomous path handles

- **Long-running / non-terminating commands.** `timeout` bounds them. Set
  the storyboard's `Record timeout` to `scene_duration + ~2s` so the
  recorded footage matches the slot.
- **Commands needing piped input.** Wrap in `bash -c`:
  ```bash
  --command "bash -c 'printf \"y\\n\" | npm uninstall foo'"
  ```
- **Commands needing secrets** (e.g. an API key). Inject *only* the needed
  variable into the scrubbed env:
  ```bash
  env -i HOME=$HOME PATH=$PATH SHELL=/bin/bash PS1='$ ' \
      DEPLOY_TOKEN="$DEPLOY_TOKEN" \
    asciinema rec ...
  ```
  The token is in the PTY's process env but **never echoed to the
  recording** — asciinema captures stdout, not env dumps.
- **TTY allocation failure** (rare; some sandboxes). If `asciinema rec`
  errors with *"could not allocate pty"*, fall back to GNU `script`:
  ```bash
  script -qc "<cmd>" /dev/null      # produces a typescript file
  ```
  Convert by prepending an asciinema v2 header line
  `{"version":2,"width":144,"height":32}` and timing-stamping each line;
  if that's too brittle for the scene, fall back to the authored-terminal
  path.
- **Commands genuinely needing a human** (interactive prompts, mouse-driven
  TUIs). Out of scope for autonomous mode — switch the storyboard's
  `Capture:` to `terminal` (authored-typewriter path) or `supplied`
  (user provides their own MP4).

## Recording mode — interactive (sub-case)

For multi-step demos where you *want* a human typing for cadence and
authenticity, the same tools work as a hand-recorded session:

```bash
asciinema rec --cols 144 --rows 32 --idle-time-limit 1.5 cast.cast
# ... type commands ...
exit
```

The pre-flight checklist (clean shell, brand prompt, sized window, dark
theme, deliberate pacing) applies. The skill does not drive this mode —
it's a user-side path for scenes where deterministic `--command` mode
won't capture the intent. Drop the resulting cast into the storyboard's
expected location (`public/clips/scene-{NN}-{slug}.cast`) and the skill
will pick up from the render step.

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
