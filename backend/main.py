import time
import zmq

if __name__ == '__main__':
    # create ZMQ socket
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:3000")

    # listen for messages
    #while True:
    message = socket.recv()
    print(f"Server recieved request: {message}", flush=True)

    time.sleep(1)

    socket.send(b"World")
