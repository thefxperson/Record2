import time
import zmq
import json
import os
from fingerprint import acoustidSearch, myAcoustidSearch, myAcoustidSearchRec
from lastfm import lastfmArt, lastfmScrobble
import asyncio


def scrobbleSong(data, start_time, track = False, record = False):
    # load api keys
    f_keys = open("./secrets.json", "r")
    text = f_keys.readline()
    keys = json.loads(text)
    f_keys.close()

    # first, make a AcoustID API call:
    if record:
        best_result = asyncio.run(myAcoustidSearchRec(keys["ACOUSTID_API_KEY"]))
    else:
        best_result = myAcoustidSearch(keys["ACOUSTID_API_KEY"], data["path"])

    # no matches
    if best_result["score"] == 0.0:
        return (False, {"msg": "No matching songs.", "title": "Scrobble Error"})

    # then, submit a scrobble request to lastfm
    if track:
        lastfmScrobble(keys["LASTFM_API_KEY"], keys["LASTFM_API_SECRET"],
                        keys["LASTFM_USERNAME"], keys["LASTFM_PASS_HASH"],
                        best_result["title"], best_result["artist"],
                        start_time=start_time)

    art_url = lastfmArt(keys["LASTFM_API_KEY"], keys["LASTFM_API_SECRET"],
                         best_result["title"], best_result["artist"])

    # finally, return a payload to update GUI
    return (True, {
                   "song": best_result["title"],
                   "artist": best_result["artist"],
                   "duration": best_result["duration"],
                   "art": art_url})


def communicateWithService(filepath, curr_time):
    f = open(f"./backend/params.txt", "w")      # writs args to file
    f.write(filepath)
    f.write('\n')
    f.write(str(curr_time))
    f.close()
    time.sleep(1)                               # allow service to process response
    f = open("./backend/percentage-played.txt", "r")    # read response from service
    line = f.readline()
    f.close()
    os.remove("./backend/params.txt")
    return line

def scrobbleSongServiceHandler(decoded, socket):
    start_time = time.time()
    reply = scrobbleSong(decoded["data"], start_time)
    if reply[0]:    # if successful API lookup
        print(reply[1])
        while True:
            curr = int(time.time() - start_time)
            perc = communicateWithService(decoded["data"], curr)
            # update time and percent
            resp[1]["currTime"] = curr
            resp[1]["currPerc"] = perc

            socket.send(json.dumps({"fun": "updateSong", "data": reply[1]}).encode("ascii"))
            time.sleep(0.8)



if __name__ == '__main__':
    # create ZMQ socket
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://127.0.0.1:3001")

    # infinite loop to listen for RPCs
    # later refactor into a proper async model
    while True:
        # listen for a new message
        message = socket.recv()
        decoded = json.loads(message)
        print(f"FIRST RESP: {decoded}", flush=True)

        # call function specified in message
        if(decoded["fun"] == "scrobbleSong"):
            start_time = time.time()
            reply = scrobbleSong(decoded["data"], start_time, track=True)
            if reply[0]:    # if successful API lookup
                socket.send(json.dumps({"fun": "updateSong", "data": reply[1]}).encode("ascii"))
            else:
                socket.send(json.dumps({"fun": "errorMsg", "data": reply[1]}).encode("ascii"))
            continue
        elif(decoded["fun"] == "scrobbleMic"):
            start_time = time.time()
            # record for 5 sec and reply
            reply = scrobbleSong(None, start_time, track=False, record=True)
            if reply[0]:
                socket.send(json.dumps({"fun": "updateSong", "data": reply[1]}).encode("ascii"))
            else:
                socket.send(json.dumps({"fun": "errorMsg", "data": reply[1]}).encode("ascii"))
