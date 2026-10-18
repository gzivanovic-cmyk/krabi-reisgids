#!/usr/bin/env python3
"""Bundelt content/gids.json en private/tips.json tot de openbare reisgids.
De vaste gids staat sinds versie 3 in git, zodat een lokale sync updates behoudt.
Alleen publiceerbare inhoud in content/gids.json; persoonlijke documenten blijven privé.
"""
import json, os, re, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gp = os.path.join(ROOT, "content", "gids.json")
if not os.path.exists(gp):
    gp = os.path.join(ROOT, "private", "gids.json")
with open(gp, encoding="utf-8") as f:
    gids = json.load(f)
tp = os.path.join(ROOT, "private", "tips.json")
public = os.path.join(ROOT, "data", "gids.json")
if os.path.exists(tp):
    with open(tp, encoding="utf-8") as f:
        tips = json.load(f).get("tips", [])
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
        sys.exit("Onbekende sectie in tip: " + t["section"])
    if t.get("url") and not re.match(r"^https?://", t["url"]):
        sys.exit("Ongeldige URL in tip")
out = {"updated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "gids": gids, "tips": tips}
os.makedirs(os.path.dirname(public), exist_ok=True)
with open(public, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"Gebouwd: {len(gids['sections'])} onderdelen, {len(tips)} tips -> data/gids.json")
