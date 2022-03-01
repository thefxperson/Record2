import time
import zmq
import json
import os
from fingerprint import acoustid_search
from lastfm import lastfm_art, lastfm_scrobble


def scrobbleSong(data):
    # load api keys
    #print(os.getcwd())
    f_keys = open("./secrets.json", "r")
    text = f_keys.readline()
    keys = json.loads(text)
    f_keys.close()

    # first, make a AcoustID API call:
    best_result = acoustid_search(keys["ACOUSTID_API_KEY"], data["path"])
    print(best_result, flush=True)

    # no matches
    if best_result["score"] == 0.0:
        return (False, None)

    # then, submit a scrobble request to lastfm
    lastfm_scrobble(keys["LASTFM_API_KEY"], keys["LASTFM_API_SECRET"],
                    keys["LASTFM_USERNAME"], keys["LASTFM_PASS_HASH"],
                    best_result["title"], best_result["artist"],
                    start_time=time.time())

    art_url = lastfm_art(keys["LASTFM_API_KEY"], keys["LASTFM_API_SECRET"],
                         best_result["title"], best_result["artist"])

    # finally, return a payload to update GUI
    return (True, {
                   "song": best_result["title"],
                   "artist": best_result["artist"],
                   "duration": best_result["duration"],
                   "art": art_url})


# API Specification
# To initiate a remote function call, send JSON message:
# remote_call = {
#   "function": "function_name",
#   "args": [arg1, arg2, ...]
# }
#
# If you recieve a message of type CALL,
#   1. Call the function passed in the JSON object
#   2. Pass the args in the JSON object
#   3. Return tuple (REPLY, DATA)
#
# REPLYING TO MESSAGES
def handle_request(message):
    # decode byte-string JSON to dict
    decoded = json.loads(message)

    # check if request is GET or POST
    if decoded["type"] == "CALL":
        handle_get(message["data"])
    elif decoded["type"] == "RETURN":
        handle_post(message["data"])

def handle_post(message):
    pass

def handle_get(message):
    pass

song1 = {
    "song": "Devil in a New Dress",
    "artist": "Kanye West, Rick Ross",
    "duration": 352,
    "art": "https://lastfm.freetls.fastly.net/i/u/770x0/8a071c4b073625018de5f0ac58727511.jpg#8a071c4b073625018de5f0ac58727511",
}
song2 = {
    "song": "Unfuckwittable",
    "artist": "Kid Cudi",
    "duration": 276,
    "art": "https://upload.wikimedia.org/wikipedia/en/c/c5/Kid-cudi-indicud-cover.jpg",
}
song3 = {
    "song": "Skinny Love",
    "artist": "Bon Iver",
    "duration": 239,
    "art": "https://upload.wikimedia.org/wikipedia/en/e/e0/Bon_iver_album_cover.jpg",
}
songs = [song1, song2, song3]

if __name__ == '__main__':
    # create ZMQ socket
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://127.0.0.1:3001")

    # listen for messages
    #while True:
    message = socket.recv()
    decoded = json.loads(message)
    print(f"Server recieved request: {decoded}", flush=True)

    time.sleep(1)
    data = {
        "type": "POST",
        "data": "World"
    }

    socket.send(json.dumps(data).encode("ascii"))

    time.sleep(3)

    # test comms
    for song in songs:
        data = {
            "fun": "updateSong",
            "data": song
        }

        socket.send(json.dumps(data).encode("ascii"))
        time.sleep(5)

    # infinite loop to listen for RPCs
    # later refactor into a proper async model but idgaf rn
    while True:
        # listen for a new message
        message = socket.recv()
        decoded = json.loads(message)
        print(decoded, flush=True)

        # call function specified in message
        if(decoded["fun"] == "scrobbleSong"):
            reply = scrobbleSong(decoded["data"])
            if reply[0]:    # if successful API lookup
                print(reply[1])
                socket.send(json.dumps({"fun": "updateSong", "data": reply[1]}).encode("ascii"))
            continue
