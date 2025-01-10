import zmq

# Create a ZeroMQ context
context = zmq.Context()

# Create a subscriber socket
subscriber = context.socket(zmq.SUB)

# Connect to the publisher
subscriber.connect("tcp://127.0.0.1:5556")

# Subscribe to all topics (empty string means no filtering)
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

print("Subscriber connected to tcp://127.0.0.1:5556. Waiting for messages...")

try:
    while True:
        # Receive messages
        message = subscriber.recv_string()
        print(f"Received message: {message}")
except KeyboardInterrupt:
    print("Subscriber shutting down.")
finally:
    subscriber.close()
    context.term()