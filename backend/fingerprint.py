import acoustid
import json
import numpy
import asyncio
import sys

import numpy as np
import sounddevice as sd

# acoustid API key
"""f_keys = open("../secrets.json", "r")
text = f_keys.readline()
keys = json.loads(text)
api_key = keys["ACOUSTID_API_KEY"]
f_keys.close()

for score, rec_id, title, artist in acoustid.match(api_key, "./hurricane.mp3"):
    print(f"Matched {title} - {artist} with recording id {rec_id} and confidence {score}.")"""
#response = acoustid.match(api_key, "./diand.mp3", parse=False)
#print(response)

def acoustid_search(api_key, file_path):
    best_result = {}
    best_result["score"] = 0.0
    for score, rec_id, title, artist in acoustid.match(api_key, file_path):
        print(f"Matched {title} - {artist} with recording id {rec_id} and confidence {score}.", flush=True)
        if score > best_result["score"] and artist != None:
            best_result["rec_id"] = rec_id
            best_result["title"] = title
            best_result["artist"] = artist
            best_result["score"] = score

    return best_result


def my_acoustid_search(api_key, file_path, verbose=True):
    best_result = {}
    best_result["score"] = 0.0
    results = acoustid.match(api_key, file_path, parse=False)

    # check query status
    if results["status"] != "ok":
        if verbose:
            print("ERROR: no acoustid results")
        return best_result

    # parse query
    for result in results["results"]:
        if result["score"] > best_result["score"]:
            best_result["title"] = result["recordings"][0]["title"]
            best_result["score"] = result["score"]
            artists = ""
            for artist in result["recordings"][0]["artists"]:
                artists += artist["name"]
                if "joinphrase" in artist:
                    artists += artist["joinphrase"]

            best_result["artist"] = artists
            best_result["id"] = result["id"]
            best_result["duration"] = result["recordings"][0]["duration"]

    return best_result

# code from sounddevice's documentation/examples...
# https://python-sounddevice.readthedocs.io/en/0.4.4/examples.html
async def record_buffer(buffer, **kwargs):
    loop = asyncio.get_event_loop()
    event = asyncio.Event()
    idx = 0

    def callback(indata, frame_count, time_info, status):
        nonlocal idx
        if status:
            print(status)
        remainder = len(buffer) - idx
        if remainder == 0:
            loop.call_soon_threadsafe(event.set)
            raise sd.CallbackStop
        indata = indata[:remainder]
        buffer[idx:idx + len(indata)] = indata
        idx += len(indata)

    stream = sd.InputStream(callback=callback, dtype=buffer.dtype,
                            channels=buffer.shape[1], **kwargs)
    with stream:
        await event.wait()


async def my_acoustid_search_rec(api_key, file_path, verbose=True):
    best_result = {}
    best_result["score"] = 0.0
    # shape = (frames, channels) -- frames = sample_rate * time (sec)
    sr = 44100
    channels = 1
    duration = 5.0
    buffer = np.empty((int(sr*duration), channels), dtype=np.float32)
    asyncio.run(record_buffer(buffer))
    #results = acoustid.match(api_key, file_path, parse=False)
    fp = acoustid.fingerprint(sr, channels, iter(buffer))
    results = acoustid.lookup(api_key, fp, duration, "recordings", None)

    # check query status
    if results["status"] != "ok":
        if verbose:
            print("ERROR: no acoustid results")
        return best_result

    # parse query
    for result in results["results"]:
        if result["score"] > best_result["score"]:
            best_result["title"] = result["recordings"][0]["title"]
            best_result["score"] = result["score"]
            artists = ""
            for artist in result["recordings"][0]["artists"]:
                artists += artist["name"]
                if "joinphrase" in artist:
                    artists += artist["joinphrase"]

            best_result["artist"] = artists
            best_result["id"] = result["id"]
            best_result["duration"] = result["recordings"][0]["duration"]

    return best_result
