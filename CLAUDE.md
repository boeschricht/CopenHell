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

## Spotify-playliste

`CreateCopenhellPlaylist.py` opretter/opdaterer en Spotify-playliste kaldet "Copenhell favorites" med de 3 mest populære sange per band fra programmet.

### Afhængigheder

```
pip3 install spotipy
```

### Credentials

Scriptet læser credentials fra miljøvariabler:

```
export SPOTIFY_CLIENT_ID=...
export SPOTIFY_CLIENT_SECRET=...
```

Disse er oprettet på [developer.spotify.com](https://developer.spotify.com/dashboard).

### Spotify-app konfiguration

- Redirect URI: `http://127.0.0.1:8888/callback`
- Scopes: `playlist-read-private`, `playlist-modify-private`, `playlist-modify-public`
- APIs used: Web API
- Brugerens Spotify-email skal tilføjes under User Management i dashboardet

### Auth-flow (første gang / efter token-udløb)

Spotipy kan ikke åbne browser interaktivt fra Claude Code. Kør i stedet:

1. Generer auth-URL og åbn den i browseren — spotipy printer den hvis `open_browser=False` sættes
2. Log ind på Spotify og godkend
3. Paste redirect-URL'en (`http://127.0.0.1:8888/callback?code=...`) tilbage
4. Token caches i `.cache` (ikke i git)

Efterfølgende kørsler bruger det cachede token automatisk.

### Kør scriptet

```
SPOTIFY_CLIENT_ID=... SPOTIFY_CLIENT_SECRET=... python3 CreateCopenhellPlaylist.py
```

### Kendte begrænsninger (Spotify Development Mode)

- `POST /v1/users/{id}/playlists` returnerer 403 — brug `/me/playlists` i stedet (allerede implementeret)
- `GET /artists/{id}/top-tracks` er blokeret — scriptet bruger søgning + popularitetssortering i stedet
- `search`-endpointet i spotipy sender ugyldige parametre — scriptet kalder API'et direkte med `requests`

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
