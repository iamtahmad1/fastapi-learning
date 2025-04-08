from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from confluent_kafka import Producer
import json

app = FastAPI()

# Kafka setup
producer = Producer({
    'bootstrap.servers': 'localhost:9092'
})

# Pydantic model for input validation
class SignupRequest(BaseModel):
    user_id: str
    email: EmailStr

@app.post("/signup")
async def signup(data: SignupRequest):
    try:
        payload = json.dumps(data.dict())
        producer.produce("user-signups", value=payload)
        producer.flush()
        return {"status": "queued", "user_id": data.user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
