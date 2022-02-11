import time
import zmq
import json


# API Specification
# To initiate a remote function call, send JSON message:
# remote_call = {
#   "type": "CALL",
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
    "art": "https://lastfm.freetls.fastly.net/i/u/770x0/8a071c4b073625018de5f0ac58727511.jpg#8a071c4b073625018de5f0ac58727511",
}
song2 = {
    "song": "Unfuckwittable",
    "artist": "Kid Cudi",
    "art": "https://upload.wikimedia.org/wikipedia/en/c/c5/Kid-cudi-indicud-cover.jpg",
}
song3 = {
    "song": "Skinny Love",
    "artist": "Bon Iver",
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
