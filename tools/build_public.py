#!/usr/bin/env python3
"""Bundelt de vaste gidsen en private/tips.json tot de openbare reisgids.
  krabi:      content/gids.json       + tips zonder 'page' (of page 'krabi') -> data/gids.json
  filipijnen: content/filipijnen.json + tips met page 'filipijnen'          -> data/filipijnen.json
De vaste gidsen staan in git, zodat een lokale sync updates behoudt.
Alleen publiceerbare inhoud in content/; persoonlijke documenten blijven privé.
Ontbreekt private/tips.json, dan blijven de huidige openbare tips per pagina behouden.
"""
import json, os, re, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = {
    "krabi": (["content/gids.json", "private/gids.json"], "data/gids.json"),
    "filipijnen": (["content/filipijnen.json"], "data/filipijnen.json"),
}
tp = os.path.join(ROOT, "private", "tips.json")
alltips = None
if os.path.exists(tp):
    with open(tp, encoding="utf-8") as f:
        alltips = json.load(f).get("tips", [])
    for t in alltips:
        if t.get("page", "krabi") not in PAGES:
            sys.exit("Onbekende pagina in tip: " + str(t.get("page")))
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
for page, (sources, dst) in PAGES.items():
    gp = next((os.path.join(ROOT, s) for s in sources if os.path.exists(os.path.join(ROOT, s))), None)
    if not gp:
        sys.exit("Geen bronbestand voor pagina " + page)
    with open(gp, encoding="utf-8") as f:
        gids = json.load(f)
    public = os.path.join(ROOT, dst)
    if alltips is not None:
        tips = [t for t in alltips if t.get("page", "krabi") == page]
    elif os.path.exists(public):
        with open(public, encoding="utf-8") as f:
            tips = json.load(f).get("tips", [])
    else:
        tips = []
    ids = {s["id"] for s in gids["sections"]}
    for t in tips:
        if not t.get("section") or not t.get("text"):
            sys.exit("Tip zonder section/text")
        if t["section"] not in ids:
            sys.exit(f"Onbekende sectie in tip ({page}): " + t["section"])
        if t.get("url") and not re.match(r"^https?://", t["url"]):
            sys.exit("Ongeldige URL in tip")
    out = {"updated": now, "gids": gids, "tips": tips}
    os.makedirs(os.path.dirname(public), exist_ok=True)
    with open(public, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Gebouwd {page}: {len(gids['sections'])} onderdelen, {len(tips)} tips -> {dst}")
