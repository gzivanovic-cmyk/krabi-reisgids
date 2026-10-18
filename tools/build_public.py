#!/usr/bin/env python3
"""Bundelt private/gids.json + private/tips.json tot data/gids.json (publiek, zonder wachtwoord)."""
import json, os, re, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gids = json.load(open(os.path.join(ROOT, "private", "gids.json"), encoding="utf-8"))
tp = os.path.join(ROOT, "private", "tips.json")
tips = json.load(open(tp, encoding="utf-8")).get("tips", []) if os.path.exists(tp) else []
ids = {s["id"] for s in gids["sections"]}
for t in tips:
    if not t.get("section") or not t.get("text"): sys.exit(f"Tip zonder section/text: {t}")
    if t["section"] not in ids: sys.exit(f"Onbekende sectie in tip: {t['section']}")
    if t.get("url") and not re.match(r"^https?://", t["url"]): sys.exit(f"Ongeldige URL in tip: {t['url']}")
out = {"updated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "gids": gids, "tips": tips}
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
json.dump(out, open(os.path.join(ROOT, "data", "gids.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"Gebouwd: {len(gids['sections'])} onderdelen, {len(tips)} tips -> data/gids.json")
