# CopenHell 2026 – Kalenderside

Statisk hjemmeside til CopenHell-festivalen (24. og 26. juni 2026). Giver besøgende mulighed for at tilføje hele programmet direkte til deres kalender-app.

## Struktur

- `index.html` — hele sitet (single-page, ingen build-step)
- `copenhell.ics` — samlet program for begge dage (alle scener)

## Hosting

Sitet er hostet på GitHub Pages: `https://boeschricht.github.io/CopenHell/`

ICS-filerne skal serveres fra GitHub Pages (ikke `raw.githubusercontent.com`), da raw.githubusercontent.com sender filer med `Content-Type: text/plain`, hvilket får kalender-apps til at afvise dem. GitHub Pages serverer `.ics`-filer korrekt som `text/calendar`.

## Kalender-links

`webcal://`-links bruges til "Tilføj til kalender"-knapperne — disse åbner direkte i kalender-appen på iOS/macOS. Download-links bruger `https://` til manuel import (Android/Google Kalender).

## Program

### Onsdag 24. juni
- 18:00–19:15 · Alice Cooper – Helvíti
- 19:30–20:30 · Suicidal Tendencies – Hades
- 21:00–23:00 · Iron Maiden – Helvíti

### Fredag 26. juni
- 12:30–13:15 · Defecto – Hades
- 16:00–17:00 · Trivium – Helvíti
- 17:15–18:15 · P.O.D. – Hades
- 20:30–21:30 · Morild – Gehenna
- 21:30–23:00 · 15 Years in Hell All Star Show – Helvíti
- 23:15–00:45 · Anthrax – Hades
