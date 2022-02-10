import pylast
import time

# API KEYS lmao don't push to github
API_KEY = "KEY"
API_SECRET = "SECRET"

# my info lmao also don't push
username = "USERNAME"
password_hash = pylast.md5("PASSWORD")

lfm = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=password_hash,
)

# this works
lfm.scrobble("Kid Cudi", "Pursuit of Happiness", int(time.time())-250)
