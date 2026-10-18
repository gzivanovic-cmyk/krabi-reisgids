#!/usr/bin/env bash
# Krabi Reisgids sync (alleen Krabi-reisdata; nooit GO 4IT, IJS of AIS)
# Werkwijze:
#  1. Inhoud staat in private/gids.json (vaste teksten + bronnen) en private/tips.json (Instagram-tips van Gorans vrouw).
#     Nieuwe tip toevoegen: python3 tools/add_tip.py --section <id> --text "..." [--url ...] [--sync]
#  2. ./sync.sh -> bouwt data/gids.json (publiek, zonder wachtwoord; wel noindex) en pusht naar GitHub Pages.
# private/ en .password worden NOOIT gecommit.
set -euo pipefail
cd "$(dirname "$0")"
[ -f private/gids.json ] || { echo "private/gids.json ontbreekt"; exit 1; }
[ -f private/tips.json ] || echo '{"tips":[]}' > private/tips.json
python3 -m json.tool private/gids.json >/dev/null || { echo "gids.json ongeldig"; exit 1; }
python3 -m json.tool private/tips.json >/dev/null || { echo "tips.json ongeldig"; exit 1; }
python3 tools/build_public.py
[ -f data/gids.enc ] && git rm -q --cached data/gids.enc 2>/dev/null; rm -f data/gids.enc
git add -A
if git diff --cached --name-only | grep -Eq '^(private/|\.password)' || git ls-files | grep -Eq '^(private/|\.password)'; then echo "FOUT: geheime bestanden gestaged"; git reset -q; exit 1; fi
git diff --cached --quiet && { echo "Geen wijzigingen"; exit 0; }
git commit -qm "Sync reisgids $(date '+%Y-%m-%d %H:%M')"
git push -q origin HEAD:main
echo "Gepusht. Live: https://gzivanovic-cmyk.github.io/krabi-reisgids/"
