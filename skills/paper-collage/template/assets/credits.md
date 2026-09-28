# Credits: bundled example assets

All source images come from the Openverse API (https://api.openverse.org), license filter CC0 / PDM only.
No attribution is legally required for CC0 or PDM, it is listed here for traceability.

Stocksnap note: the full-resolution file is served by a form POST to `https://stocksnap.io/photo/download`
(field `photoId=<ID>`), there is no static full-size URL. The raw copy was stored at 3000 px on the long side.
Rawpixel note: only the `editor_1024` rendition is used because it has no watermark (the 1300 px rendition is watermarked).

## cut/person-sleep.png
- Title: Business Man
- Creator: Direct Media (https://stocksnap.io/author/145556)
- Source: stocksnap
- License: CC0 1.0
- Landing page: https://stocksnap.io/photo/business-man-TNKLX6MUWC
- Download: POST https://stocksnap.io/photo/download, photoId=TNKLX6MUWC (Openverse url: https://cdn.stocksnap.io/img-thumbs/960w/TNKLX6MUWC.jpg)
- Edit: background removed (hyperframes remove-background), laptop removed, cut straight at chest level, white die-cut border 14 px.

## cut/person-gym.png
- Title: Athlete Resting
- Creator: Direct Media (https://stocksnap.io/author/145556)
- Source: stocksnap
- License: CC0 1.0
- Landing page: https://stocksnap.io/photo/athlete-resting-TZEVVEI8BL
- Download: POST https://stocksnap.io/photo/download, photoId=TZEVVEI8BL (Openverse url: https://cdn.stocksnap.io/img-thumbs/960w/TZEVVEI8BL.jpg)
- Edit: background removed, water bottle restored with a manual mask, cut straight at chest level, border 14 px.

## cut/person-travel.png
- Title: Fashion Model
- Creator: Daria Shevtsova (https://instagram.com/dash.shevtsova)
- Source: stocksnap
- License: CC0 1.0
- Landing page: https://stocksnap.io/photo/fashion-model-YVWBHIROVS
- Download: POST https://stocksnap.io/photo/download, photoId=YVWBHIROVS (Openverse url: https://cdn.stocksnap.io/img-thumbs/960w/YVWBHIROVS.jpg)
- Edit: background removed, full body sitting on a vintage suitcase, cut straight at the ground line, border 14 px.

## cut/prop-clock.png
- Title: Alarm clock green
- Creator: rawpixel (no individual creator listed)
- Source: rawpixel
- License: CC0 1.0
- Landing page: https://www.rawpixel.com/image/5939627/alarm-clock-green
- Download: https://images.rawpixel.com/editor_1024/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvc2sxNDI3LWltYWdlLWt3eW5ycDFoLmpwZw.jpg
- Edit: white background flood-filled out, contact shadow removed, border 10 px. Small maker text on the dial ("Peter", "Made in Germany") is tiny and not a logo.

## cut/prop-dumbbell.png
- Title: Fitness Weights
- Creator: Healthy Living (https://stocksnap.io)
- Source: stocksnap
- License: CC0 1.0
- Landing page: https://stocksnap.io/photo/fitness-weights-TDRGG50ZRR
- Download: POST https://stocksnap.io/photo/download, photoId=TDRGG50ZRR (Openverse url: https://cdn.stocksnap.io/img-thumbs/960w/TDRGG50ZRR.jpg)
- Edit: only the single dumbbell kept from the flat lay, soft shadow removed, border 10 px.

## tex/crumpled.png
- Title: Free paper crumpled texture background
- Creator: rawpixel (no individual creator listed)
- Source: rawpixel
- License: CC0 1.0
- Landing page: https://www.rawpixel.com/image/5911010/image-background-texture-public-domain
- Download: https://images.rawpixel.com/editor_1024/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvcHgxNDQyOTY5LWltYWdlLWt3dnZ2ZHNkLmpwZw.jpg
- Edit: grayscale, rotated to portrait, scaled to 1080x1920, lighting flattened, dust specks removed, remapped to mean 0.90 (std 0.045). Use as a multiply layer.

## fonts/Gloock-Regular.ttf, fonts/Newsreader.ttf, fonts/ArchivoBlack-Regular.ttf
- Gloock (Duarte Pinto), Newsreader (Production Type) and Archivo Black (Omnibus-Type), from Google Fonts
- License: SIL Open Font License 1.1, see fonts/OFL-*.txt

## sfx/*.mp3 (not bundled)
- Copied at build time from the HyperFrames media-use skill (Pixabay Content License), see scripts/build.py
