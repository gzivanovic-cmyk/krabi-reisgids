# Krabi Reisgids

Openbare gezinsreisgids voor zes maanden proefwonen. Geen toegangsbeveiliging; noindex is geen privacybescherming.

- `content/gids.json`: vaste publiceerbare gids, checklist en tijdlijn (bronbestand sinds versie 3).
- `private/tips.json`: lokale Instagramtips; nooit committen.
- `data/gids.json`: openbare bundel. `python3 tools/build_public.py` bouwt deze opnieuw; zonder private tips blijven de huidige openbare tips behouden.
- `index.html`: weergave, fasefilters, afdrukken en lokale invulvelden.

Haal vóór lokale wijzigingen eerst de nieuwste versie op met `git pull --ff-only`. `sync.sh` haalt eveneens nieuwe commits op en stopt bij een conflict. Oude `private/gids.json` wordt alleen als fallback gebruikt als `content/gids.json` ontbreekt.

Persoonlijke planning en checklist staan alleen in de browser, zonder synchronisatie. Geen paspoort-, polis- of medische gegevens in deze repository plaatsen.
