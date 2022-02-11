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
