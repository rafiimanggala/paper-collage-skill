# Photos, cutouts and texture

Everything must be free to use in an ad: CC0 or public domain only. Record every source in `assets/credits.md` (title, creator, landing page, licence, what you changed).

## 1. Find photos

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/openverse_search.py" "stressed woman" --source rawpixel,stocksnap
```

- Search for the emotion, not the topic, in one or two words: "stressed woman", "tired man", "relieved", "celebrating", "confused". Longer queries often return nothing. Topic photos (a wedding, a crash) are often busy or grim.
- Prefer plain, light backgrounds with background on every side of the subject. Where the subject touches the frame edge the sticker gets a straight side; that only looks right at the bottom, where `--cut-y` cuts anyway.
- Download the image URL the search prints: StockSnap 960w and rawpixel `editor_1024` are big enough for a 900 px sticker and carry no watermark. The larger rawpixel rendition is watermarked and StockSnap full size sits behind a bot check, so skip both. Flickr results vary; check the licence field is `cc0` or `pdm`.
- Avoid logos, readable brand names, and recognisable private people in sensitive situations.
- Grim or graphic subjects (injuries, wrecks) read better as a toy, a diagram or a document than as a real photo.

## 2. Cut people into stickers

```bash
npx hyperframes remove-background raw/woman.jpg -o raw/woman-cut.png
python3 "${CLAUDE_SKILL_DIR}/scripts/diecut.py" sticker raw/woman.jpg --alpha raw/woman-cut.png \
  --cut-y 1450 --erode 2 -o assets/cut/person-woman.png
```

- `--cut-y` cuts the body straight across (chest or waist) in source pixels and gives it one clean bottom edge, the classic sticker look.
- `--erode 2` to `4` pulls a soft matte inward so no rim of the old background survives.
- If the matte is still wrong (hair, a second person), crop first with `--box x0,y0,x1,y1` or pick another photo. Do not fall back to circles or rectangles for people.

## 3. Props

- An object on a white background: `diecut.py prop raw/clock.jpg --box ... -o assets/cut/prop-clock.png`. Lower `--white` (for example 200) to swallow soft shadows; `--keep` drops small stray pieces.
- Anything else: remove-background, then `sticker` with `--width 520 --border 10`.
- Things that are really paper (tickets, forms, passports, receipts, phone screens) look better drawn in CSS: see `docs.css` and the `doc` / `prop` helpers.

## 4. Photo prints

`diecut.py print raw/street.jpg --box 0,0,1024,1024 -o assets/cut/photo-street.png` gives a rectangular print with a flat white frame. Use it for places and scenes; it pops like a prop.

## 5. Paper texture

The template ships `assets/tex/crumpled.png`. To make another from a CC0 crumpled-paper photo:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/paper_texture.py" raw/paper.jpg --rotate -o assets/tex/crumpled.png
```

It keeps the folds, removes uneven lighting and dust, and centres the brightness at 0.90 for a multiply layer.
