# Phase 2: Capture (Chrome DevTools)

Automatically capture app/website screenshots for use in video scenes.

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
