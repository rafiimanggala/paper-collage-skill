"""Make a crumpled-paper multiply overlay (greyscale 1080x1920, mean about 0.90). MIT License.

Start from any CC0 photo of crumpled paper; folds are kept, lighting and dust are removed.
  python3 paper_texture.py raw/paper.jpg -o assets/tex/crumpled.png
Use it as .cg-bg-crumple (mix-blend-mode: multiply) over the scene colour.
Needs: pip install pillow numpy scipy
"""
import argparse

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

W, H = 1080, 1920


def build(src, rotate, mean, std):
    g = Image.open(src).convert("L")
    if rotate:
        g = g.rotate(90, expand=True)
    scale = max(W / g.width, H / g.height)
    g = g.resize((round(g.width * scale), round(g.height * scale)), Image.LANCZOS)
    x0, y0 = (g.width - W) // 2, (g.height - H) // 2
    g = np.asarray(g.crop((x0, y0, x0 + W, y0 + H))).astype(np.float32) / 255.0
    g = ndi.gaussian_filter(g, 0.8)                                # soften upscale and jpeg grain
    med = ndi.median_filter(g, size=15)
    g = np.where(ndi.binary_dilation((med - g) > 0.10, iterations=3), med, g)  # drop dust specks
    flat = g / np.maximum(ndi.gaussian_filter(g, 60), 1e-3)       # remove uneven lighting
    out = np.clip(mean + (flat - flat.mean()) / flat.std() * std, 0, 1)
    return np.clip(out - (out.mean() - mean), 0, 1)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("src")
    p.add_argument("-o", "--out", required=True)
    p.add_argument("--rotate", action="store_true", help="rotate a landscape photo to portrait first")
    p.add_argument("--mean", type=float, default=0.90, help="overall brightness of the overlay")
    p.add_argument("--std", type=float, default=0.045, help="fold strength")
    a = p.parse_args()
    out = build(a.src, a.rotate, a.mean, a.std)
    Image.fromarray((out * 255).round().astype(np.uint8), "L").save(a.out, optimize=True)
    print(a.out, "mean=%.3f std=%.3f" % (out.mean(), out.std()))


if __name__ == "__main__":
    main()
