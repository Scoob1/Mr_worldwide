import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import mysql.connector

# Load .env vars
load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# Setup Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0Akley11",
    database="mr_worldwide"
)
cursor = conn.cursor()

# Get Pitbull's artist data
results = sp.search(q="Pitbull", type="artist", limit=1)
artist = results["artists"]["items"][0]

# Insert artist
cursor.execute("""
    INSERT IGNORE INTO artists (id, name, genres, popularity, followers)
    VALUES (%s, %s, %s, %s, %s)
""", (
    artist["id"],
    artist["name"],
    ", ".join(artist["genres"]),
    artist["popularity"],
    artist["followers"]["total"]
))

# Get albums
albums = sp.artist_albums(artist["id"], album_type="album", country="US", limit=50)["items"]
seen_albums = set()

for album in albums:
    if album["id"] in seen_albums:
        continue
    seen_albums.add(album["id"])

    # Insert album
    cursor.execute("""
        INSERT IGNORE INTO albums (id, artist_id, name, release_date, total_tracks, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        album["id"],
        artist["id"],
        album["name"],
        album["release_date"],
        album["total_tracks"],
        album["images"][0]["url"] if album["images"] else None
    ))

    # Get tracks for each album
    tracks = sp.album_tracks(album["id"])["items"]
    for track in tracks:
        cursor.execute("""
            INSERT IGNORE INTO tracks (id, album_id, name, duration_ms, explicit, track_number, preview_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            track["id"],
            album["id"],
            track["name"],
            track["duration_ms"],
            track["explicit"],
            track["track_number"],
            track["preview_url"]
        ))

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("Dale!")

