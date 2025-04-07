import redis
import json
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

user_data = {"id": 1, "name": "Alice"}
r.set("user:1", json.dumps(user_data), ex=60)

cached_data = r.get("user:1")
if cached_data:
    user = json.loads(cached_data)
    print("From cache:", user)