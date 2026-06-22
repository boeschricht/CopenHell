import os
import re
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

ICS_URL = "https://boeschricht.github.io/CopenHell/copenhell.ics"
CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
REDIRECT_URI = "http://127.0.0.1:8888/callback"
PLAYLIST_NAME = "Copenhell favorites"
TRACKS_PER_ARTIST = 3

# Disse er shows/events, ikke søgbare bands på Spotify
SKIP_BANDS = {"15 Years in Hell All Star Show"}


def fetch_bands_from_ics():
    response = requests.get(ICS_URL)
    response.raise_for_status()
    text = response.content.decode("utf-8")
    summaries = re.findall(r"^SUMMARY:(.+)$", text, re.MULTILINE)
    bands = []
    for summary in summaries:
        band = summary.split(" – ")[0].strip()
        if band not in SKIP_BANDS:
            bands.append(band)
    return bands


def get_or_create_playlist(sp, user_id):
    offset = 0
    while True:
        page = sp.current_user_playlists(limit=50, offset=offset)
        for playlist in page["items"]:
            if playlist["name"] == PLAYLIST_NAME and playlist["owner"]["id"] == user_id:
                sp.playlist_replace_items(playlist["id"], [])
                print(f"Ryddede eksisterende playlist: '{PLAYLIST_NAME}'")
                return playlist["id"]
        if page["next"] is None:
            break
        offset += 50
    new_playlist = sp._post("me/playlists", payload={"name": PLAYLIST_NAME, "public": False})
    print(f"Oprettede ny playlist: '{PLAYLIST_NAME}'")
    return new_playlist["id"]


def get_top_track_uris(token, band_name):
    search_name = band_name.replace(".", "")
    band_lower = band_name.lower().replace(".", "")

    r = requests.get(
        "https://api.spotify.com/v1/search",
        params={"q": search_name, "type": "artist", "limit": 5},
        headers={"Authorization": f"Bearer {token}"},
    )
    r.raise_for_status()
    artists = [a for a in r.json()["artists"]["items"] if band_lower in a["name"].lower().replace(".", "")]
    if not artists:
        print(f"  [{band_name}] Ikke fundet på Spotify – springer over")
        return []
    artist_id = artists[0]["id"]

    r2 = requests.get(
        "https://api.spotify.com/v1/search",
        params={"q": search_name, "type": "track", "limit": 10},
        headers={"Authorization": f"Bearer {token}"},
    )
    r2.raise_for_status()
    items = [t for t in r2.json()["tracks"]["items"] if t["artists"][0]["id"] == artist_id]
    if not items:
        print(f"  [{band_name}] Ingen egne tracks fundet – springer over")
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
    return [t["uri"] for t in unique]


def main():
    bands = fetch_bands_from_ics()
    print(f"Bands i kalenderen: {', '.join(bands)}\n")

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

    all_uris = []
    for band in bands:
        uris = get_top_track_uris(token, band)
        all_uris.extend(uris)

    if all_uris:
        sp.playlist_add_items(playlist_id, all_uris)
        print(f"\nFærdig! {len(all_uris)} numre tilføjet til '{PLAYLIST_NAME}'.")
    else:
        print("\nIngen numre at tilføje.")


if __name__ == "__main__":
    main()
