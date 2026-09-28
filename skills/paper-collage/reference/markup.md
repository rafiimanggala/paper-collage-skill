# Markup contract

`collage_html.py` writes this markup; write it by hand only when not using the generator. Times are scene-local content seconds.

```html
<div id="s1-stage" class="cg-stage" data-seed="11" data-exit="5.1" data-push="1" data-pushout="5.6" style="--bg: #C9CCF2">
  <div class="cg-bg-grid"></div><div class="cg-bg-crumple"></div>
  <div class="cg-world">
    <div class="cg-strip cg-label" data-t="0.3" style="left: 88px; top: 720px">
      <div class="cg-paper"></div><div class="cg-text">fixing your</div>
    </div>
    <div class="cg-doc doc-sleep" data-t="0.48" data-rot="8" style="left: 612px; top: 420px">...</div>
    <img class="cg-prop" data-t="0.9" data-rot="-12" src="assets/cut/prop-clock.png" alt="" style="left: 440px; top: 330px; width: 220px" />
    <img class="cg-person" data-t="1.35" src="assets/cut/person-sleep.png" alt="" style="left: 170px; top: 940px; width: 760px" />
    <div class="cg-pop" data-t="4.6" data-rot="-10" data-anim="stamp" style="left: 700px; top: 1085px"><div class="stamp">NO.</div></div>
    <svg class="cg-draw" data-t="2.0" data-dur="0.3" width="780" height="90" viewBox="0 0 780 90" style="left: 130px; top: 700px">
      <path class="ink-red" d="M 12 58 C 210 36 500 52 766 26" stroke-width="16" />
    </svg>
  </div>
</div>
<script>Collage.scene("s1-sleep", "s1-stage", 6, 1);</script>
```

| Attribute | On | Meaning |
|---|---|---|
| `data-seed` | stage | torn edges and jitter |
| `data-exit` | stage | everything pops out (leave it off to hold to the end) |
| `data-push="1"` | stage | slides up from the bottom at t 0 |
| `data-pushout` | stage | slides up and away (next scene's start) |
| `data-zoom` | stage | slow zoom amount, default 0.03 |
| `data-t` | element | entry time |
| `data-rot` | element | resting angle in degrees |
| `data-out` | element | leave before the stage exit |
| `data-step` | strip | seconds between letters |
| `data-anim` | pop | `stamp` or `swap` |
| `data-dur` | draw | draw-on length |
| `data-kind` | doodle | `zzz`, `drops`, `flight` |
| `data-frames` | presenter | `t:scale,...` punch-in cuts |

`Collage.scene(id, stageId, duration, speed)`: the scene composition's `data-duration` must equal `duration / speed`. A strip's letters come from the text of `.cg-text`, so keep it plain text.
