"""The storyboard: edit this file, then run `python3 scripts/build.py`.

Each scene is one sub-composition. Times are scene-local seconds. Scenes play in order and
overlap by CONFIG["push"] seconds while the next one pushes up from the bottom; give a scene
an explicit "start" (seconds in the whole video) to pin it to a voiceover instead.

Scene keys:
  id        unique, used for the file name (compositions/<id>.html)
  dur       length in seconds
  bg        paper colour (CSS)
  seed      any integer; changes the torn edges and letter jitter
  world     list of element strings from collage_html (DOM order = stacking order)
  exit      optional, when everything pops out (default dur - 0.9)
  start     optional, pin the scene start (default: previous start + dur - push)
  backdrop  optional, "paper" (grid + crumple, default) or "plain"
  presenter optional, {"src": "assets/aroll/a1.mp4", "video": True, "frames": "0:1,2.5:1.12"}
"""
from collage_html import doc, drops, flight, label, prop, sticker, word, zzz

CONFIG = {
    "push": 0.4,             # scene overlap during the push transition
    "target_seconds": None,  # e.g. 50: play everything faster (nothing is cut) to hit this length
    "vo": None,              # e.g. "assets/vo/vo.wav": voiceover track, time-stretched with the video
    "words": None,           # e.g. "assets/vo/words.json": [{"w": "Hello", "s": 0.0, "e": 0.4}, ...] for captions
    "sfx": True,             # typing / pop / click / whoosh cues derived from the scene markup
}

SLEEP_DOC = (
    '<div class="ds-holes"></div><div class="ds-title"><div>Sleep</div><div>Schedule</div></div>'
    '<div class="ds-row"><span class="ds-box"></span><span class="ds-time">10:30 pm</span><span class="ds-what">lights out</span></div>'
    '<div class="ds-row"><span class="ds-box"></span><span class="ds-time">6:00 am</span><span class="ds-what">wake up</span></div>'
    '<div class="ds-row"><span class="ds-box ds-x"></span><span class="ds-time">no</span><span class="ds-what">phone in bed</span></div>'
)

PLAN_DOC = (
    '<div class="dp-clip"></div><div class="dp-paper"><div class="dp-kicker">WEEK 1</div><div class="dp-title">Workout Plan</div>'
    + "".join(f'<div class="dp-row"><span class="dp-day">{d}</span><span class="dp-what">{w}</span><span class="dp-box{x}"></span></div>'
              for d, w, x in (("Mon", "Squats 3×10", " dp-x"), ("Wed", "Run 5 km", ""), ("Fri", "Deadlifts", ""), ("Sun", "Rest (finally)", "")))
    + "</div>"
)

PASS_DOC = (
    '<div class="dq-main"><div class="dq-band">BOARDING PASS</div><div class="dq-route"><span>CGK</span>'
    '<svg class="dq-arrow" viewBox="0 0 52 24" aria-hidden="true"><path d="M2 12 H 46 M 34 2 L 48 12 L 34 22" fill="none" '
    'stroke="#1E1B18" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" /></svg><span>NRT</span></div>'
    '<div class="dq-fields"><div class="dq-field"><span class="dq-k">GATE</span><span class="dq-v">12</span></div>'
    '<div class="dq-field"><span class="dq-k">SEAT</span><span class="dq-v">24A</span></div>'
    '<div class="dq-field"><span class="dq-k">BOARDS</span><span class="dq-v">06:15</span></div></div></div>'
    '<div class="dq-stub"><div class="dq-code"></div></div>'
)

PASSPORT = (
    '<div class="pp-title">PASSPORT</div><svg class="pp-globe" viewBox="0 0 100 100" aria-hidden="true">'
    '<g fill="none" stroke="#E3C77A" stroke-width="3.5"><circle cx="50" cy="50" r="40" /><ellipse cx="50" cy="50" rx="17" ry="40" />'
    '<path d="M 10 50 H 90 M 17 30 H 83 M 17 70 H 83 M 50 10 V 90" /></g></svg><div class="pp-sub">TRAVEL DOCUMENT</div>'
)

# Beat inside every scene: setup label, document, prop, punch word 1, person, doodle, punch word 2, exit.
SCENES = [
    {
        "id": "s1-sleep", "dur": 6.0, "bg": "#C9CCF2", "seed": 11,
        "world": [
            label("fixing your", 0.3, "left: 88px; top: 720px; width: 900px", size=96),
            doc(SLEEP_DOC, "doc-sleep", 0.48, "left: 612px; top: 420px", rot=8),
            sticker("assets/cut/prop-clock.png", 0.9, "left: 440px; top: 330px; width: 220px", rot=-12),
            sticker("assets/cut/person-sleep.png", 1.35, "left: 170px; top: 940px; width: 760px", rot=-1.5, person=True),
            word("IMPOSSIBLE", 1.0, "left: 56px; top: 1290px", size=104),
            word("FRUSTRATING", 3.3, "right: 44px; top: 1455px", size=96),
            zzz(2.0, "left: 640px; top: 900px; width: 220px; height: 220px"),
        ],
    },
    {
        "id": "s2-gym", "dur": 6.0, "bg": "#F7CDB8", "seed": 23,
        "world": [
            label("starting a", 0.45, "left: 88px; top: 700px; width: 900px", size=96),
            doc(PLAN_DOC, "doc-plan", 0.62, "left: 590px; top: 392px", rot=-6),
            sticker("assets/cut/prop-dumbbell.png", 1.05, "left: 452px; top: 336px; width: 290px", rot=-18),
            sticker("assets/cut/person-gym.png", 1.6, "left: 190px; top: 920px; width: 700px", rot=1.5, person=True),
            word("INTIMIDATING", 1.25, "left: 46px; top: 1320px", size=100),
            word("EXHAUSTING", 3.5, "right: 50px; top: 1485px", size=100),
            drops(2.2, "left: 880px; top: 960px; width: 160px; height: 200px"),
        ],
    },
    {
        "id": "s3-travel", "dur": 6.0, "bg": "#F3DF9E", "seed": 37,
        "world": [
            label("booking a", 0.45, "left: 88px; top: 670px; width: 900px", size=96),
            doc(PASS_DOC, "doc-pass", 0.62, "left: 548px; top: 548px", rot=-9),
            prop(PASSPORT, "pp", 1.05, "left: 800px; top: 318px", rot=14),
            sticker("assets/cut/person-travel.png", 1.6, "left: 320px; top: 845px; width: 460px", rot=-1, person=True),
            word("OVERWHELMING", 1.25, "left: 40px; top: 1300px", size=92),
            word("EXPENSIVE", 3.5, "right: 56px; top: 1466px", size=104),
            flight("s3-route", 1.9, "M 70 1760 C 240 1600 420 1880 590 1740 S 880 1560 1000 1650"),
        ],
    },
]
