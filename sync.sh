#!/usr/bin/env bash
# Krabi Reisgids sync (alleen Krabi-reisdata; nooit GO 4IT, IJS of AIS)
# Werkwijze:
#  1. Inhoud staat in content/gids.json (vaste teksten + bronnen) en private/tips.json (Instagram-tips van Gorans vrouw).
#     Nieuwe tip toevoegen: python3 tools/add_tip.py [--page filipijnen] --section <id> --text "..." [--url ...] [--sync]
#     Filipijnen-pagina: content/filipijnen.json + tips met --page filipijnen -> data/filipijnen.json (filipijnen.html)
#  2. ./sync.sh -> bouwt data/gids.json (publiek, zonder wachtwoord; wel noindex) en pusht naar GitHub Pages.
# private/ en .password worden NOOIT gecommit.
set -euo pipefail
cd "$(dirname "$0")"
# Haal wijzigingen eerst op; overschrijf geen nieuwere online versie.
git pull --ff-only
# build_public.py behoudt bestaande tips als private/tips.json ontbreekt.
python3 tools/build_public.py
[ -f data/gids.enc ] && git rm -q --cached data/gids.enc 2>/dev/null; rm -f data/gids.enc
git add -A
if git diff --cached --name-only | grep -Eq '^(private/|\.password)' || git ls-files | grep -Eq '^(private/|\.password)'; then echo "FOUT: geheime bestanden gestaged"; git reset -q; exit 1; fi
git diff --cached --quiet && { echo "Geen wijzigingen"; exit 0; }
git commit -qm "Sync reisgids $(date '+%Y-%m-%d %H:%M')"
git push -q origin HEAD:main
echo "Gepusht. Live: https://gzivanovic-cmyk.github.io/krabi-reisgids/ en https://gzivanovic-cmyk.github.io/krabi-reisgids/filipijnen.html"
