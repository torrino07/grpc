import redis

# Create a Redis client
client = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)

# Create a pubsub object
pubsub = client.pubsub()

# Subscribe to all channels (using pattern matching)
pubsub.psubscribe('*')

print("Subscriber connected to Redis. Waiting for messages...")

try:
    for message in pubsub.listen():
        if message['type'] == 'pmessage':
            print(f"Received message: {message['data']} on channel: {message['channel']}")
except KeyboardInterrupt:
    print("Subscriber shutting down.")
finally:
    pubsub.close()