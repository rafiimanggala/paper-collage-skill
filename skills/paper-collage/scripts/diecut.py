"""Turn photos into collage stickers and prints. MIT License.

  sticker  cutout with a thick white die-cut border and hardened edge
  prop     same, for an object shot on a plain white background (no alpha needed)
  print    rectangular photo print with a flat white frame

Examples:
  npx hyperframes remove-background raw/man.jpg -o raw/man-cut.png      # alpha for a person
  python3 diecut.py sticker raw/man.jpg --alpha raw/man-cut.png -o assets/cut/person-man.png --width 900 --cut-y 1450
  python3 diecut.py prop raw/flatlay.jpg --box 600,900,1500,1500 -o assets/cut/prop-dumbbell.png --width 520
  python3 diecut.py print raw/street.jpg -o assets/cut/photo-street.png --box 0,0,1024,1024

Sizes that read well at 1080x1920: people 900 px wide with a 14 px border, props 520 px with
10 px, prints 760 px with a 16 px frame. Needs: pip install pillow numpy scipy
"""
import argparse
import sys

import numpy as np
from PIL import Image, ImageEnhance
from scipy import ndimage as ndi


def enhance(img, bright=1.04, contrast=1.06, color=1.03):
    img = ImageEnhance.Brightness(img).enhance(bright)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    return ImageEnhance.Color(img).enhance(color)


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y) <= r * r


def largest_components(mask, keep_frac=0.02):
    lab, n = ndi.label(mask)
    if n == 0:
        sys.exit("diecut: the mask is empty (check the alpha file or the white threshold)")
    sizes = ndi.sum(mask, lab, range(1, n + 1))
    keep = [i + 1 for i, s in enumerate(sizes) if s >= sizes.max() * keep_frac]
    return np.isin(lab, keep)


def fill_small_holes(mask, max_area):
    holes = ndi.binary_fill_holes(mask) & ~mask
    lab, n = ndi.label(holes)
    if n == 0:
        return mask
    sizes = ndi.sum(holes, lab, range(1, n + 1))
    return mask | np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s <= max_area])


def white_bg_mask(rgb, thr=232, sat_thr=18):
    """Near-white background connected to the image border."""
    a = np.asarray(rgb).astype(np.int16)
    mn, mx = a.min(axis=2), a.max(axis=2)
    lab, _ = ndi.label((mn >= thr) & ((mx - mn) <= sat_thr))
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    return np.isin(lab, border[border > 0])


def bridge_bottom(m, border_px):
    """A subject cut straight across (chest, ground line) gets one clean straight bottom edge."""
    yb = np.where(m.any(axis=1))[0].max()
    xs = np.where(m[yb])[0]
    bar = np.zeros_like(m)
    bar[yb - border_px:yb + 1, xs.min():xs.max() + 1] = True
    return fill_small_holes(m | bar, (border_px * 6) ** 2)


def diecut(rgb, alpha, border_px, target_w, straight_bottom=False):
    """rgb: PIL RGB, alpha: float32 0..1 of the same size. Returns the RGBA sticker."""
    ys, xs = np.where(alpha > 0.5)
    if len(ys) == 0:
        sys.exit("diecut: nothing opaque in the alpha")
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgb, alpha = rgb.crop((x0, y0, x1, y1)), alpha[y0:y1, x0:x1]
    inner_w = target_w - 2 * border_px
    size = (inner_w, max(1, round(rgb.height * inner_w / rgb.width)))
    rgb = rgb.resize(size, Image.LANCZOS)
    sa = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).resize(size, Image.LANCZOS)).astype(np.float32) / 255.0
    sa = np.clip((sa - 0.25) / 0.5, 0, 1)  # harden the soft matte edge
    pad = 2 * border_px + 6
    sa_p = np.zeros((sa.shape[0] + 2 * pad, sa.shape[1] + 2 * pad), np.float32)
    sa_p[pad:-pad, pad:-pad] = sa
    rgb_p = np.full(sa_p.shape + (3,), 255, np.float32)
    rgb_p[pad:-pad, pad:-pad] = np.asarray(rgb).astype(np.float32)
    m = largest_components(sa_p > 0.5, keep_frac=0.01)
    m = fill_small_holes(m, (border_px * 3) ** 2)
    m = ndi.binary_closing(m, structure=disk(border_px))  # soften notches before the border grows
    if straight_bottom:
        m = bridge_bottom(m, border_px)
    border_a = np.clip(border_px + 0.5 - ndi.distance_transform_edt(~m), 0, 1)
    sa_p = np.where(border_a > 0, sa_p, 0)
    out_rgb = rgb_p * sa_p[..., None] + 255.0 * (1 - sa_p[..., None])
    img = Image.fromarray(np.dstack([out_rgb, border_a * 255]).clip(0, 255).astype(np.uint8), "RGBA")
    return img.crop(img.getchannel("A").point(lambda v: 255 if v > 0 else 0).getbbox())


def open_cropped(path, box, mode):
    img = Image.open(path).convert(mode)
    return img.crop(tuple(int(v) for v in box.split(","))) if box else img


def cmd_sticker(a):
    rgb = enhance(open_cropped(a.src, a.box, "RGB"))
    alpha = np.asarray(open_cropped(a.alpha, a.box, "RGBA").getchannel("A")).astype(np.float32) / 255.0
    if alpha.shape != (rgb.height, rgb.width):
        sys.exit("diecut: --alpha must have the same size as the photo")
    if a.erode:  # pull a soft matte edge inward so no rim of the old background survives
        alpha = ndi.grey_erosion(alpha, footprint=disk(a.erode))
    if a.cut_y:  # source y, measured after --box
        alpha[a.cut_y:, :] = 0
    return diecut(rgb, alpha, a.border or 14, a.width or 900, straight_bottom=bool(a.cut_y))


def cmd_prop(a):
    rgb = open_cropped(a.src, a.box, "RGB")
    fg = ~white_bg_mask(rgb, a.white)
    fg = largest_components(ndi.binary_opening(fg, structure=disk(2)), keep_frac=a.keep)
    fg = fill_small_holes(fg, fg.size * 0.004)
    alpha = ndi.gaussian_filter(fg.astype(np.float32), 1.2)
    return diecut(enhance(rgb), alpha, a.border or 10, a.width or 520)


def cmd_print(a):
    img = enhance(open_cropped(a.src, a.box, "RGB"), 1.03, 1.05, 1.02)
    frame, out_w = a.border or 16, a.width or 760
    inner_w = out_w - 2 * frame
    img = img.resize((inner_w, round(img.height * inner_w / img.width)), Image.LANCZOS)
    out = Image.new("RGB", (out_w, img.height + 2 * frame), (255, 255, 255))
    out.paste(img, (frame, frame))
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=("sticker", "prop", "print"))
    p.add_argument("src", help="source photo")
    p.add_argument("-o", "--out", required=True, help="output PNG")
    p.add_argument("--alpha", help="sticker: PNG whose alpha is the subject mask (remove-background output)")
    p.add_argument("--width", type=int, help="output width in px (default 900 sticker, 520 prop, 760 print)")
    p.add_argument("--border", type=int, help="white border in px (default 14 sticker, 10 prop, 16 print)")
    p.add_argument("--cut-y", type=int, default=0, help="sticker: cut the subject straight across at this source y")
    p.add_argument("--erode", type=int, default=0, help="sticker: shrink the matte by this many px first")
    p.add_argument("--white", type=int, default=232, help="prop: min channel value counted as white background (lower it to swallow soft shadows)")
    p.add_argument("--keep", type=float, default=0.25, help="prop: keep pieces at least this fraction of the biggest one")
    p.add_argument("--box", help="crop the source first: x0,y0,x1,y1 in px (isolate one object, frame a print)")
    a = p.parse_args()
    if a.mode == "sticker" and not a.alpha:
        p.error("sticker needs --alpha (run `npx hyperframes remove-background` first)")
    img = {"sticker": cmd_sticker, "prop": cmd_prop, "print": cmd_print}[a.mode](a)
    img.save(a.out, optimize=True)
    print(a.out, img.size)


if __name__ == "__main__":
    main()
