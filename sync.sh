#!/usr/bin/env bash
# Krabi Reisgids sync (alleen Krabi-reisdata; nooit GO 4IT, IJS of AIS)
# Werkwijze:
#  1. Inhoud staat in private/gids.json (vaste teksten + bronnen) en private/tips.json (Instagram-tips van Gorans vrouw).
#     Nieuwe tip toevoegen: python3 tools/add_tip.py --section <id> --text "..." [--url ...] [--sync]
#  2. ./sync.sh -> versleutelt naar data/gids.enc en pusht naar GitHub Pages.
# Plaintext (private/) en .password worden NOOIT gecommit.
set -euo pipefail
cd "$(dirname "$0")"
[ -f private/gids.json ] || { echo "private/gids.json ontbreekt"; exit 1; }
[ -f private/tips.json ] || echo '{"tips":[]}' > private/tips.json
[ -f .password ] || { echo ".password ontbreekt"; exit 1; }
python3 -m json.tool private/gids.json >/dev/null || { echo "gids.json ongeldig"; exit 1; }
python3 -m json.tool private/tips.json >/dev/null || { echo "tips.json ongeldig"; exit 1; }
node encrypt.js private/gids.json private/tips.json data/gids.enc .password
git add -A
if git diff --cached --name-only | grep -Eq '^(private/|\.password)' || git ls-files | grep -Eq '^(private/|\.password)'; then echo "FOUT: geheime bestanden gestaged"; git reset -q; exit 1; fi
git diff --cached --quiet && { echo "Geen wijzigingen"; exit 0; }
git commit -qm "Sync reisgids $(date '+%Y-%m-%d %H:%M')"
git push -q origin HEAD:main
echo "Gepusht. Live: https://gzivanovic-cmyk.github.io/krabi-reisgids/"
