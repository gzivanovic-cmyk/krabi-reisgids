#!/usr/bin/env python3
"""Voeg een Instagram-tip toe aan private/tips.json.
Voorbeelden:
  python3 tools/add_tip.py --section eten --text "Leuk restaurant aan het strand" --url https://www.instagram.com/p/XXXX/ --media foto --sync
  python3 tools/add_tip.py --page filipijnen --section tips-kim --text "..." --quote "Omg" --account @iemand --media video --sync
Pagina's: krabi (standaard) en filipijnen. De geldige secties staan in content/gids.json of content/filipijnen.json.
"""
import argparse, json, os, subprocess, sys, datetime, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIPS = os.path.join(ROOT, "private", "tips.json")
PAGEFILE = {"krabi": ["content/gids.json", "private/gids.json"], "filipijnen": ["content/filipijnen.json"]}
p = argparse.ArgumentParser()
p.add_argument("--page", default="krabi", choices=list(PAGEFILE), help="Op welke pagina: krabi (standaard) of filipijnen")
p.add_argument("--section", required=True)
p.add_argument("--text", required=True, help="Korte omschrijving in het Nederlands")
p.add_argument("--title", default="", help="Optionele titel, bv. naam van restaurant of plek")
p.add_argument("--quote", default="", help="Letterlijke tekst van Kim (wordt getoond als Kim: \"...\")")
p.add_argument("--note", default="", help="Extra opmerking, bv. 'Gelabeld als AI-content op Instagram'")
p.add_argument("--url", default="", help="Link naar post/reel/plek (https)")
p.add_argument("--type", default="", help="post, reel, link, plaats, bericht")
p.add_argument("--topic", default="", help="Optioneel onderwerp binnen het onderdeel")
p.add_argument("--date", default="", help="Datum van het bericht, alleen als bekend")
p.add_argument("--media", default="", choices=["", "video", "foto"], help="video (filmpje/reel) of foto; leeg als onbekend")
p.add_argument("--account", default="", help="Instagram-account van de post, bv. @krabi.escape")
p.add_argument("--sync", action="store_true", help="Daarna direct ./sync.sh draaien")
a = p.parse_args()
gp = next(os.path.join(ROOT, f) for f in PAGEFILE[a.page] if os.path.exists(os.path.join(ROOT, f)))
ids = [s["id"] for s in json.load(open(gp, encoding="utf-8"))["sections"]]
if a.section not in ids:
    sys.exit(f"Onbekende sectie '{a.section}' voor pagina {a.page}. Kies uit: {', '.join(ids)}")
if a.url and not re.match(r"^https?://", a.url):
    sys.exit("URL moet met http:// of https:// beginnen")
data = json.load(open(TIPS, encoding="utf-8")) if os.path.exists(TIPS) else {"tips": []}
tip = {k: v for k, v in {"page": a.page if a.page != "krabi" else "", "section": a.section, "title": a.title, "text": a.text,
       "quote": a.quote, "note": a.note, "url": a.url, "type": a.type, "topic": a.topic, "date": a.date,
       "account": a.account, "media": a.media, "added": datetime.date.today().isoformat()}.items() if v}
if any(t.get("page", "krabi") == a.page and t.get("text") == tip["text"] and t.get("url", "") == tip.get("url", "") for t in data["tips"]):
    sys.exit("Deze tip staat er al in.")
data["tips"].append(tip)
os.makedirs(os.path.dirname(TIPS), exist_ok=True)
json.dump(data, open(TIPS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"Tip toegevoegd aan {a.page} / '{a.section}' (totaal {len(data['tips'])} tips).")
if a.sync:
    subprocess.run([os.path.join(ROOT, "sync.sh")], check=True)
