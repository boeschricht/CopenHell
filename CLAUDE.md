# Fest Egnen 2025 – Kalenderside

Statisk hjemmeside til Fest Egnen-festivalen (19.–20. juni 2025). Giver besøgende mulighed for at tilføje sceneprogrammer direkte til deres kalender-app.

## Struktur

- `index.html` — hele sitet (single-page, ingen build-step)
- `live-stage.ics` — Live Stage program
- `360-dj-stage.ics` — 360 DJ Stage program
- `vi-elsker-stage.ics` — Vi Elsker Stage program
- `bodega-royal.ics` — Bodega Royal program

## Hosting

Sitet er hostet på GitHub Pages: `https://boeschricht.github.io/Festegnen/`

ICS-filerne skal serveres fra GitHub Pages (ikke `raw.githubusercontent.com`), da raw.githubusercontent.com sender filer med `Content-Type: text/plain`, hvilket får kalender-apps til at afvise dem. GitHub Pages serverer `.ics`-filer korrekt som `text/calendar`.

## Kalender-links

`webcal://`-links bruges til "Tilføj til kalender"-knapperne — disse åbner direkte i kalender-appen på iOS/macOS. Download-links bruger `https://` til manuel import (Android/Google Kalender).
