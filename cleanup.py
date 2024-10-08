"""Spotify Playlist Duplicate Removal"""


import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
CLIENT_ID = "REDACTED"
CLIENT_SECRET = "REDACTED"
REDIRECT_URI = "http://localhost:3000"
SCOPE = "playlist-modify-private"

# Spotify API object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

# Get the user's playlists
playlists = sp.current_user_playlists()

# Check if playlists are found
if playlists:
    print("Playlists found!")
else:
    print("No playlists found.")

# Access a specific playlist by ID
playlist_id = "5NqWAsteIOP4cdMa5QsbzV"

# Fetch playlist details
playlist = sp.playlist(playlist_id)

# Print playlist name and total number of tracks
print(f"Playlist: {playlist['name']}")
print(f"Total tracks: {playlist['tracks']['total']}")

# Get the playlist tracks
def get_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])
    print(f"Fetched {len(tracks)} tracks initially.")

    # Loop through all tracks and fetch next pages if available
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
        print(f"Fetched {len(tracks)} tracks in total so far...")

    print(f"Total tracks fetched: {len(tracks)}")
    return tracks

# Delete duplicate tracks from the playlist
def delete_duplicate_tracks(playlist_id):
    tracks = get_playlist_tracks(playlist_id)
    track_uris = set()
    duplicate_tracks = []

    # Collect duplicate tracks
    for idx, track in enumerate(tracks):
        track_uri = track['track']['uri']
        track_name = track['track']['name']
        print(f"Track {idx+1}: {track_name} ({track_uri})")

        if track_uri in track_uris:
            duplicate_tracks.append(track_uri)  
            print(f"Duplicate found: {track_name} ({track_uri})")
        else:
            track_uris.add(track_uri)

    # Batch process duplicates removal (100 tracks max per API call)
    if duplicate_tracks:
        batch_size = 100
        for i in range(0, len(duplicate_tracks), batch_size):
            batch = duplicate_tracks[i:i + batch_size]
            sp.playlist_remove_all_occurrences_of_items(playlist_id, batch)
            print(f"Removed {len(batch)} duplicate tracks.")
    else:
        print("No duplicate tracks found.")

# Call the function 
delete_duplicate_tracks(playlist_id)
