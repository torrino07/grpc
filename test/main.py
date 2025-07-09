import zmq

def run():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:5554")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    try:
        while True:
            message = socket.recv()
            decoded_message = message.decode('utf-8')
            print(f"Received: {decoded_message}")
    except KeyboardInterrupt:
        print("Subscriber stopped.")

if __name__ == "__main__":
    run()