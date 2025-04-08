from confluent_kafka import Producer
import json

p = Producer({'bootstrap.servers': 'localhost:9092'})

def delivery_report(err, msg):
    if err:
        print(f"❌ Failed: {err}")
    else:
        print(f"✅ Delivered to {msg.topic()} [{msg.partition()}]")

def send_signup_event(user_id: str, email: str):
    event = {"user_id": user_id, "email": email}
    p.produce(
        topic="user-signups",
        value=json.dumps(event),
        callback=delivery_report
    )
    p.flush()

# Simulate user signup
send_signup_event("u123", "test@example.com")
