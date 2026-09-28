"""Search Openverse for CC0 / public-domain photos (no API key). MIT License.

  python3 openverse_search.py "stressed woman"
  python3 openverse_search.py "alarm clock" --source rawpixel,stocksnap --json hits.json
Prints index, source, size, licence, title, landing page and image URL. Keep the landing page
and creator in assets/credits.md for every photo you use.
Tips: use one or two words ("stressed woman", "alarm clock"); long queries often return nothing.
The listed image URL (StockSnap 960w, rawpixel editor_1024, no watermark) is big enough for a 900 px
sticker; StockSnap full size sits behind a bot check, so do not scrape it.
"""
import argparse
import json
import urllib.parse
import urllib.request

API = "https://api.openverse.org/v1/images/"


def search(query, sources=None, page_size=20):
    params = {"q": query, "license": "cc0,pdm", "page_size": page_size, "mature": "false"}
    if sources:
        params["source"] = sources
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers={"User-Agent": "paper-collage-skill/1.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("query")
    p.add_argument("--source", help="comma list, e.g. rawpixel,stocksnap,flickr")
    p.add_argument("--n", type=int, default=20)
    p.add_argument("--json", help="also save the raw response here")
    a = p.parse_args()
    d = search(a.query, a.source, a.n)
    if a.json:
        with open(a.json, "w") as f:
            json.dump(d, f, indent=1)
    print("results:", d.get("result_count"))
    if not d.get("results"):
        print("nothing found: try one or two words, or drop --source")
    for i, r in enumerate(d.get("results", [])):
        print(i, r["source"], r.get("width"), r.get("height"), r["license"], "|", (r.get("title") or "")[:48],
              "|", r.get("foreign_landing_url"), "|", r["url"])


if __name__ == "__main__":
    main()
