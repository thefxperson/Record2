import pylast
import time

# API KEYS lmao don't push to github
"""API_KEY = "KEY"
API_SECRET = "SECRET"

# my info lmao also don't push
username = "USERNAME"
password_hash = pylast.md5("PASSWORD")"""

def lastfm_scrobble(api_key, api_secret, username, password_hash, song, artist, start_time=time.time()):
    lfm = pylast.LastFMNetwork(
        api_key=api_key,
        api_secret=api_secret,
        username=username,
        password_hash=password_hash,
    )

    # this works
    lfm.scrobble(artist, song, start_time)

def lastfm_art(api_key, api_secret, song, artist):
        lfm = pylast.LastFMNetwork(
            api_key=api_key,
            api_secret=api_secret
        )

        # TODO: create more robust art fetching system
        try:    #return track art if it exists
            return lfm.get_track(artist, song).get_cover_image(size=0)
        except IndexError as e: #otherwise use default
            return "None"
