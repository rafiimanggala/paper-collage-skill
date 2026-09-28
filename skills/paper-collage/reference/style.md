# Look and motion spec

All numbers are what `template/assets/lib/collage.js` and `collage.css` do. Change them there, once, not per scene.

## Frame

- 1080x1920, 30 fps. Scenes about 5 to 8 s; a 6 s scene holds one idea.
- Background per scene: one flat pastel (`bg`), a white grid (2 px lines, 120 px cells, 38% white), and `assets/tex/crumpled.png` multiplied at 78%.
- Palette that works: mint `#BEE5D2`, periwinkle `#C9CCF2`, peach `#F7CDB8`, butter `#F3DF9E`, warm grey `#D9D6CE`. Ink `#1E1B18`, red `#D2402E`, paper `#F6F3EC`, sheets `#FFFDF7`.

## Paper strips

| Kind | Font | Size | Use |
|---|---|---|---|
| `label` | Newsreader 560, sentence case | 88 px (96 for short phrases) | setup phrase: "planning a" |
| `word` | Gloock caps | 92 to 104 px | punch word: "STRESSFUL" |
| `tag` | Gloock caps | 58 px | caption for a photo or sticker |

- Torn edges: a seeded `clip-path` polygon, nearly straight long edges and ragged short ends.
- Typing: letters appear 40 ms apart (45 ms for caps words, 28 ms for strings over 16 letters, override with `step`), each landing from scale 1.8 to 1 in 160 ms and dropping 14 px. Caps words get a seeded ransom-note jitter (3.5 px, 1.5 degrees, 4% scale).
- The paper grows from the left in 140 ms. Exit: letters delete from the end, 22 ms apart, then the paper collapses in 120 ms.

## Documents (`doc`)

Drop from 900 px above with a slight overshoot in 0.42 s, rotating from -16 degrees to their angle, then sway 0.5 degrees. Exit: scale down with a 12 degree twist.

## Stickers (`sticker`, `prop`, `pop`)

- Props: overshoot pop (back ease) in 0.3 s, rotating in from -30 degrees, then a 0.6 degree wobble.
- People: scale 0.5 to 1 with back ease in 0.34 s while rising 40 px; they leave 0.16 s after the props.
- Stamps (`anim="stamp"`): slam from 2.4x to 1x in 0.2 s. Swaps (`anim="swap"`): 0.1 s cut, for screens changing.
- Die-cut border: people 14 px at about 900 px wide, props 10 px at about 520 px, photo prints a flat 16 px frame at 760 px.

## Marks and doodles

- `mark`: SVG paths draw on in order over `dur` seconds (default 0.35), marker widths 12 to 16 px, round caps.
- `zzz`: three letters pop 0.24 s apart and float up. `drops`: three drops pop 0.14 s apart and bob. `flight`: a dashed route draws over 1.2 s with a paper plane on its tip.

## Scene motion

- The whole collage zooms in 3% over 6 s (`data-zoom`, 0 for talking heads).
- Push: the next scene slides up from the bottom in 0.4 s (in-out cubic) while the old one moves up 520 px.
- Everything in a scene leaves together at `exit`; nothing fades out on its own unless it has `out`. The last scene holds to the end unless it sets an `exit`.

## Sound

Typing under every strip, a pop for documents and stickers, a soft click for marks, stamps and doodles, a short whoosh on every push. `build.py` derives the cues from the markup; the files come from the HyperFrames media-use skill.
