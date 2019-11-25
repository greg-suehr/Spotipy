SpotiPI
=========

Spotipy is a lightweight Python library for the Spotify Web API. Learn more:
  - https://spotipy.readthedocs.io/en/latest/
  - https://developer.spotify.com/documentation/web-api/
  - https://developer.spotify.com/documentation/web-api/reference/object-model/
SpotiPI is a lightweight data cache and analysis environment built on the API.

## Datastore

The interesting piece of the application is Datastore.

Datastore maps an API's GET requests to a library of (identifier, data) mappings. API
requests are preprocessed to store and reload data from a local database to limit the
number of API calls.

Note: each /application/ implements its own Datastore. Multi-user analyses of a single
application should share a single Datastore.


## Analysis Environment

The analysis environment comprsises:
  - A SQLite database for local storage of Spotify user, track, and artist data
  - Several imported python modules, including `spotipy`
  - Several convenience functions (`> .help` to view all commands)
  - An run definition prompt and analysis runner


## Playlist Management

SpotiPI combines the Spotify Web API with some quick statistics to recommend edits
to user playlists. Predefined analyses include:
  - .flow: Resort a playlist to smooth transitions of MOOD, BPM, DANCEABILITY, etc
  - .trim: Recommend songs to cut to reduce variance in MOOD, BPM, DANCEABILITY, etc
  - .merge: Recommend playlists combinations based on MOOD, BPM, DANCEABILITY, etc