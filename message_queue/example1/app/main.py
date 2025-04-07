# main.py
from fastapi import FastAPI, Request
from producer import send_order_to_queue
from datetime import datetime

app = FastAPI()

@app.post("/order")
async def create_order(request: Request):
    data = await request.json()
    order_data = {
        "order_id": data.get("order_id"),
        "user_id": data.get("user_id"),
        "items": data.get("items", []),
        "timestamp": datetime.now().isoformat()
    }

    await send_order_to_queue(order_data)
    return {"status": "queued", "order": order_data}

