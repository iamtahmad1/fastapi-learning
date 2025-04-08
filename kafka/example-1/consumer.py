from confluent_kafka import Consumer
import json
import time

c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'signup-group',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['user-signups'])

print("🟢 Listening to signup events...")
while True:
    msg = c.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("⚠️ Error:", msg.error())
        continue

    event = json.loads(msg.value().decode('utf-8'))
    print(f"\n👤 New User Signup: {event}")
    print(f"📧 Sending welcome email to {event['email']}")
    print(f"📊 Pushing analytics for {event['user_id']}")
    time.sleep(1)
