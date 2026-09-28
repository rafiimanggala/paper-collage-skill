---
name: paper-collage
description: Use when making a vertical social video, ad, reel, or B-roll in a DIY paper collage, scrapbook, cut-out, or mixed-media stop-motion style (torn paper labels, die-cut photo stickers, crumpled grid paper), including collage cutaways between talking-head shots, rendered with HyperFrames.
---

# Paper Collage for HyperFrames

## Overview

A proven kit for the scrapbook ad look: pastel crumpled paper with a white grid, torn off-white strips whose serif letters type on, real photos of people cut out as stickers with a thick white border, paper objects drawn in code, marker doodles, everything popping in with overshoot and out together, scenes pushing up. Every element is a pure function of time (`render(t)`) read from `data-*` attributes, and all scenes are generated from one Python storyboard, so a timing change is a one-line edit and renders are seek-safe.

Do not rebuild the look from scratch: copy the template, it already contains the animation library, fonts, paper texture and three example scenes.

## Quick start

```bash
cp -R "${CLAUDE_SKILL_DIR}/template" ./my-collage && cd my-collage
python3 scripts/build.py                        # writes compositions/*.html and index.html
npx hyperframes check .                         # must pass
npx hyperframes snapshot . --at 1.5,3.5,8.5     # look at frames before rendering
npx hyperframes render . --workers 1 -q high -o renders/collage.mp4
```

Needs Node 22+, ffmpeg, Python 3.9+, and the HyperFrames skills (`npx hyperframes skills update`). The asset scripts also need `pip install pillow numpy scipy`.

## Workflow

1. **Storyboard table first**, one row per scene: setup phrase, document, prop, person and their emotion, punch word 1, punch word 2, doodle, paper colour.
2. **Assets**: draw documents in code (`assets/lib/docs.css`), find CC0 photos and cut them into stickers. Read `reference/assets.md` before touching photos.
3. **Write the storyboard in `scripts/scenes.py`** (helpers in `scripts/collage_html.py`, new document styles in `assets/lib/docs.css`), then `python3 scripts/build.py`. Never edit `compositions/*.html` or `index.html`; the build overwrites them and deletes scene files that left the storyboard. Replace the three example scenes rather than adding to them, and delete the example stickers in `assets/cut/` and their `credits.md` entries once nothing uses them.
4. **Check, snapshot, fix, render.** Look at the snapshots yourself and compare them with the look checklist below.

## The beat (per 6 s scene, scene-local seconds)

| t | Element | Helper |
|---|---|---|
| 0.3 | setup phrase types on | `label("planning a", ...)` |
| 0.48 | document drops in | `doc(html, "doc-x", ...)` |
| 0.9 | prop sticker pops | `sticker(src, ...)` or `prop(html, ...)` |
| 1.0 | punch word 1 | `word("STRESSFUL", ...)` |
| 1.35 | person sticker pops and rises | `sticker(src, ..., person=True)` |
| 2.0 | doodle | `zzz`, `drops`, `flight`, `mark` |
| 3.3 | punch word 2, below word 1 | `word("EXPENSIVE", ...)` |
| dur - 0.9 | everything pops out together (the last scene holds to the end) | scene `exit` |
| dur - 0.4 | next scene pushes up (0.4 s overlap) | automatic |

With a voiceover, put each punch word on the start of its spoken word (`CONFIG["words"]`). `CONFIG["target_seconds"]` speeds the whole piece up to a length without cutting anything; the voiceover is time-stretched with pitch kept.

## Look checklist (what makes it read as handmade)

- **A real person with a clear emotion** (stressed, confused, relieved), die-cut, big: 600 to 900 px wide in the lower middle. Props are real single objects or code-drawn paper things. No clip-art icons, no emoji.
- **Dense and layered**: the setup label, document and prop cluster in the upper half and overlap; the person overlaps the label; both punch words overlap the person's lower edge. Fill the frame down to about y 1600.
- **Punch words stack**: word 2 appears under word 1 and both stay until the exit. Both strips are off-white paper, never coloured blocks.
- **Paper, not noise**: the bundled `crumpled.png` (a real CC0 photo) multiplied over one flat pastel per scene, a new colour each scene. Ink `#1E1B18`, accent red `#D2402E`.
- **Type**: Newsreader for setup phrases and documents, Gloock caps for punch words, Archivo Black only for stamps and captions.
- **Tilted paper**: documents up to 10 degrees, props up to 18, stamps about -8; strips stay level or tilt at most 3 (`rot=`) so they read.
- **Motion pops, never fades**: letters land from 1.8x, stickers overshoot, documents drop and settle. Leave the easing in `collage.js` alone.
- Keep y 1100 to 1500 clear of important content if burned-in captions will sit there.

Full look and motion spec: `reference/style.md`. Raw markup contract (for hand-written scenes): `reference/markup.md`.

## Talking-head cutaways

A scene can be a talking head instead of paper: add `"presenter": {"src": "assets/aroll/a1.mp4", "video": True, "frames": "0:1,2.5:1.12"}` (or a still image with `"video": False`). Strips, tags and stamps still work on top of it. Keep the presenter scenes and collage scenes in the same storyboard so the push transitions line up.

## Common mistakes

| Symptom | Cause and fix |
|---|---|
| Words in a strip run together ("fixingyour") | A plain space collapses inside inline-block letters; `collage.js` uses a non-breaking space. Do not rewrite `splitLetters`. |
| Background removal looks ragged or has a halo | Pick photos on plain backgrounds, then `diecut.py sticker --erode 2 --cut-y <chest y>`: the matte is hardened, cut straight, and hidden under the white border. |
| Prop cutout keeps a grey shadow blob | `diecut.py prop --white 200`, crop to one object with `--box`, or use remove-background plus `sticker`. |
| Letters still typing when the scene exits | Exit must come after `t + 0.1 + letters x 0.045 + 0.3`; shorten the word or move `exit`. |
| Draw-on doodle shows nothing mid-stroke | Do not use `pathLength="1"`; `mark()` measures real path lengths. |
| Renders differ between runs or frames flicker | No `Math.random`, `Date`, CSS animations or transitions; use `Collage.rng(seed)` and `render(t)`. |
| Contrast warning on a rotated document | Known false positive: the audit measures axis-aligned boxes, so text on a tilted band is compared with the page behind it. |
| `text_occluded` error | Real when a sticker covers document text: move one of them. A tilted overlay on a sticker is a false positive; `stamp()` is exempt already, add `data-layout-allow-occlusion` to others. |
| `container_overflow` info on `.cg-world` | Expected: the slow scene zoom grows the world past the frame. |
| Stamp text runs off the frame | `stamp("OVER BUDGET", ..., size=44)`. |
| Lint warns the file is long or not split | Build scenes through `scenes.py`; it writes one sub-composition per scene. |
| `render` stops with "Low disk space" | HyperFrames needs 1 GB free. |
