#!/usr/bin/env python3
"""Voeg een Instagram-tip van Gorans vrouw toe aan private/tips.json.
Voorbeeld:
  python3 tools/add_tip.py --section eten --text "Leuk restaurant aan het strand" --url https://www.instagram.com/p/XXXX/ --type post --sync
Secties: voor-vertrek, de-reis, aankomst, resort, eten, activiteiten, villa, praktisch
"""
import argparse, json, os, subprocess, sys, datetime, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIPS = os.path.join(ROOT, "private", "tips.json")
GIDS = os.path.join(ROOT, "private", "gids.json")
p = argparse.ArgumentParser()
p.add_argument("--section", required=True)
p.add_argument("--text", required=True, help="Korte omschrijving in het Nederlands")
p.add_argument("--title", default="", help="Optionele titel, bv. naam van restaurant of plek")
p.add_argument("--url", default="", help="Link naar post/reel/plek (https)")
p.add_argument("--type", default="", help="post, reel, link, plaats, bericht")
p.add_argument("--topic", default="", help="Optioneel onderwerp binnen het onderdeel, bv. visum, inpakken")
p.add_argument("--date", default="", help="Datum van het bericht, alleen als bekend (bv. 2026-10-12 of '15–17 okt 2026')")
p.add_argument("--media", default="", choices=["","video","foto"], help="video (filmpje/reel) of foto; leeg als onbekend")
p.add_argument("--account", default="", help="Instagram-account van de post, bv. @krabi.escape")
p.add_argument("--sync", action="store_true", help="Daarna direct ./sync.sh draaien")
a = p.parse_args()
ids = [s["id"] for s in json.load(open(GIDS, encoding="utf-8"))["sections"]]
if a.section not in ids:
    sys.exit(f"Onbekende sectie '{a.section}'. Kies uit: {', '.join(ids)}")
if a.url and not re.match(r"^https?://", a.url):
    sys.exit("URL moet met http:// of https:// beginnen")
data = json.load(open(TIPS, encoding="utf-8")) if os.path.exists(TIPS) else {"tips": []}
tip = {k: v for k, v in {"section": a.section, "title": a.title, "text": a.text, "url": a.url,
       "type": a.type, "topic": a.topic, "date": a.date, "account": a.account, "media": a.media,
       "added": datetime.date.today().isoformat()}.items() if v}
if any(t.get("text") == tip["text"] and t.get("url", "") == tip.get("url", "") for t in data["tips"]):
    sys.exit("Deze tip staat er al in.")
data["tips"].append(tip)
os.makedirs(os.path.dirname(TIPS), exist_ok=True)
json.dump(data, open(TIPS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"Tip toegevoegd aan '{a.section}' (totaal {len(data['tips'])} tips).")
if a.sync:
    subprocess.run([os.path.join(ROOT, "sync.sh")], check=True)
