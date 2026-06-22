import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

PROGRAM_URL = "https://copenhell.dk/program"
HEADERS = {"User-Agent": "Mozilla/5.0"}
PLAYLIST_NAME = "Copenhell Wednesday"
TRACKS_PER_ARTIST = 2
MUSIC_STAGES = {"helviti", "hades", "pandaemonium", "gehenna"}
CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
REDIRECT_URI = "http://127.0.0.1:8888/callback"


def scrape_wednesday_bands():
    r = requests.get(PROGRAM_URL, headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    bands = []
    for div in soup.select("div.grid-item"):
        classes = div.get("class", [])
        if "Onsdag" not in classes:
            continue
        if not any(c in MUSIC_STAGES for c in classes):
            continue
        name_tag = div.select_one("h2, h3, p")
        if name_tag and name_tag.get_text(strip=True):
            name = name_tag.get_text(strip=True)
        else:
            a = div.select_one("a[href*='/artist/']")
            if not a:
                continue
            slug = a["href"].rstrip("/").split("/")[-1]
            name = slug.replace("-", " ").title()
        bands.append(name)
    return bands


def get_or_create_playlist(sp, user_id):
    offset = 0
    while True:
        page = sp.current_user_playlists(limit=50, offset=offset)
        for pl in page["items"]:
            if pl["name"] == PLAYLIST_NAME and pl["owner"]["id"] == user_id:
                sp.playlist_replace_items(pl["id"], [])
                print(f"Ryddede eksisterende playlist: '{PLAYLIST_NAME}'")
                return pl["id"]
        if page["next"] is None:
            break
        offset += 50
    new_pl = sp._post("me/playlists", payload={"name": PLAYLIST_NAME, "public": False})
    print(f"Oprettede ny playlist: '{PLAYLIST_NAME}'")
    return new_pl["id"]


def get_top_tracks(token, band_name):
    search_name = band_name.replace(".", "")
    r = requests.get(
        "https://api.spotify.com/v1/search",
        params={"q": f"artist:{search_name}", "type": "track", "limit": 10},
        headers={"Authorization": f"Bearer {token}"},
    )
    r.raise_for_status()
    items = r.json()["tracks"]["items"]
    band_lower = band_name.lower().replace(".", "")
    items = [t for t in items if any(band_lower in a["name"].lower().replace(".", "") for a in t["artists"])]
    if not items:
        print(f"  [{band_name}] Ikke fundet på Spotify – springer over")
        return []
    items.sort(key=lambda t: t.get("popularity", 0), reverse=True)
    seen, unique = set(), []
    for t in items:
        if t["name"] not in seen:
            seen.add(t["name"])
            unique.append(t)
        if len(unique) == TRACKS_PER_ARTIST:
            break
    names = ", ".join(t["name"] for t in unique)
    print(f"  [{band_name}] {len(unique)} numre: {names}")
    return [(t["uri"], t.get("popularity", 0)) for t in unique]


def main():
    bands = scrape_wednesday_bands()
    print(f"Bands på onsdag ({len(bands)} stk): {', '.join(bands)}\n")

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope="playlist-read-private playlist-modify-private playlist-modify-public",
        )
    )

    user_id = sp.me()["id"]
    playlist_id = get_or_create_playlist(sp, user_id)
    token = sp.auth_manager.get_cached_token()["access_token"]

    all_tracks = []
    for band in bands:
        all_tracks.extend(get_top_tracks(token, band))

    all_tracks.sort(key=lambda t: t[1], reverse=True)
    all_uris = [uri for uri, _ in all_tracks]

    if all_uris:
        sp.playlist_add_items(playlist_id, all_uris)

    print(f"\nFærdig! {len(all_uris)} numre tilføjet til '{PLAYLIST_NAME}' (sorteret efter popularitet).")
    print(f"Bands fundet på Spotify: {len(set(uri for uri, _ in all_tracks)) // 1} tracks fra {len(bands)} bands")
    print(f"Forventede numre: {len(bands) * TRACKS_PER_ARTIST}, faktiske: {len(all_uris)}")


if __name__ == "__main__":
    main()
