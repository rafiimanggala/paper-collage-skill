"""Markup helpers for paper-collage scenes. MIT License.

Every function returns an HTML string for one collage element. Times (t, out) are scene-local
content seconds and become data-t / data-out; styles are plain CSS positions in the 1080x1920
frame. assets/lib/collage.js animates whatever these helpers emit.
"""
from html import escape


def _common(t, rot=None, out=None, extra=""):
    attrs = f' data-t="{t}"'
    if rot:
        attrs += f' data-rot="{rot}"'
    if out is not None:
        attrs += f' data-out="{out}"'
    return attrs + extra


def _strip(kind, text, t, style, rot=None, size=None, step=None, out=None):
    extra = f' data-step="{step}"' if step else ""
    size_css = f' style="font-size: {size}px"' if size else ""
    return (f'<div class="cg-strip cg-{kind}"{_common(t, rot, out, extra)} style="{style}">'
            f'<div class="cg-paper"></div><div class="cg-text"{size_css}>{escape(text, quote=False)}</div></div>')


def label(text, t, style, rot=None, size=None, out=None):
    """Setup phrase on a torn strip, small serif, sentence case ("planning a")."""
    return _strip("label", text, t, style, rot, size, None, out)


def word(text, t, style, rot=None, size=None, step=None, out=None):
    """Punch word on a torn strip, big serif caps with ransom-note jitter ("STRESSFUL")."""
    return _strip("word", text, t, style, rot, size, step, out)


def tag(text, t, style, rot=None, size=None, out=None):
    """Small caps caption strip for a sticker or photo."""
    return _strip("tag", text, t, style, rot, size, None, out)


def doc(inner, cls, t, style, rot=None, out=None):
    """Paper object drawn in code (class from docs.css); drops in from above."""
    return f'<div class="cg-doc {cls}"{_common(t, rot, out)} style="{style}">{inner}</div>'


def sticker(src, t, style, rot=None, person=False, out=None):
    """Die-cut photo cutout (PNG with white border). person=True pops bigger and rises."""
    cls = "cg-person" if person else "cg-prop"
    return f'<img class="{cls}"{_common(t, rot, out)} src="{src}" alt="" style="{style}" />'


def prop(inner, cls, t, style, rot=None, out=None):
    """Small object drawn in code (a passport, a ticket) that pops in like a sticker."""
    return f'<div class="cg-prop {cls}"{_common(t, rot, out)} style="{style}">{inner}</div>'


def pop(inner, t, style, rot=None, anim=None, cls="", out=None):
    """Any element that pops in; anim="stamp" slams down, anim="swap" cuts in."""
    extra = f' data-anim="{anim}"' if anim else ""
    return f'<div class="cg-pop {cls}"{_common(t, rot, out, extra)} style="{style}">{inner}</div>'


def stamp(text, t, style, rot=-8, size=None, out=None):
    """Red rubber stamp ("NO.", "OVER BUDGET"). size: font size in px (long text needs a smaller one).
    Marked as an allowed overlap: the occlusion lint probes axis-aligned boxes, so a tilted stamp
    over a sticker is reported as hidden text even when it reads fine."""
    fs = f' style="font-size: {size}px"' if size else ""
    return pop(f'<div class="stamp" data-layout-allow-occlusion{fs}>{escape(text, quote=False)}</div>',
               t, style, rot, "stamp", "", out)


def mark(t, dur, w, h, style, paths, out=None):
    """Hand-drawn marker strokes that draw on in order. paths: [(ink, d, stroke_width)],
    ink is "ink-red" or "ink-dark" (or your own class with a stroke colour).
    Positioned in frame coordinates: it does not follow a document's drop and settle, so a circle
    around a value on a document lands close, not exact. Draw it after the document has settled."""
    body = "".join(f'<path class="{ink}" d="{d}" stroke-width="{sw}" />' for ink, d, sw in paths)
    attrs = _common(t, None, out, ' data-dur="%s"' % dur)
    return (f'<svg class="cg-draw"{attrs} width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" style="{style}" aria-hidden="true">{body}</svg>')


def zzz(t, style):
    """Three z's floating up (sleep, boredom). style positions a ~220x220 box."""
    bits = "".join(f'<span class="cg-bit cg-z" style="left: {x}px; top: {y}px; font-size: {s}px">{c}</span>'
                   for x, y, s, c in ((0, 130, 64, "z"), (56, 64, 86, "z"), (124, -20, 116, "Z")))
    return f'<div class="cg-doodle" data-kind="zzz" data-t="{t}" style="{style}">{bits}</div>'


def drops(t, style, fill="#8FD0EE"):
    """Three bobbing sweat or water drops. style positions a ~160x200 box."""
    shape = ('<path d="M28 4 C 40 26 52 40 52 52 A 24 24 0 0 1 4 52 C 4 40 16 26 28 4 Z" fill="{f}" stroke="#1E1B18" '
             'stroke-width="{w}" stroke-linejoin="round" /><path d="M16 50 C 16 58 20 63 26 65" fill="none" '
             'stroke="#FFFFFF" stroke-width="{w}" stroke-linecap="round" />')
    bits = "".join(f'<svg class="cg-bit" style="left: {x}px; top: {y}px" width="{w}" height="{h}" viewBox="0 0 56 78" '
                   f'aria-hidden="true">{shape.format(f=fill, w=sw)}</svg>'
                   for x, y, w, h, sw in ((70, 0, 56, 78, 4), (0, 70, 44, 62, 4.5), (92, 110, 38, 53, 5)))
    return f'<div class="cg-doodle" data-kind="drops" data-t="{t}" style="{style}">{bits}</div>'


def flight(uid, t, d):
    """Paper plane flying a dashed route. d is an SVG path in frame coordinates (1080x1920);
    uid must be unique in the project (it names the mask)."""
    return (
        f'<svg class="cg-doodle" data-kind="flight" data-t="{t}" width="1080" height="1920" viewBox="0 0 1080 1920" '
        f'style="left: 0; top: 0" aria-hidden="true"><defs><mask id="{uid}-mask" maskUnits="userSpaceOnUse" x="0" y="0" '
        f'width="1080" height="1920"><path class="cg-route-mask" d="{d}" fill="none" stroke="#FFFFFF" stroke-width="18" '
        f'stroke-linecap="round" /></mask></defs><path class="cg-route" d="{d}" fill="none" stroke="#1E1B18" '
        f'stroke-width="5" stroke-dasharray="3 17" stroke-linecap="round" mask="url(#{uid}-mask)" />'
        '<g class="cg-plane"><path d="M 30 0 L -20 -19 L -11 0 L -20 19 Z" fill="#F6F3EC" stroke="#1E1B18" '
        'stroke-width="4" stroke-linejoin="round" /><path d="M 30 0 L -11 0" fill="none" stroke="#1E1B18" '
        'stroke-width="3" stroke-linecap="round" /></g></svg>'
    )
