# producer.py
import aio_pika
import json
from datetime import datetime

RABBITMQ_URL = "amqp://fastapi:fastapi@localhost/"

async def send_order_to_queue(order_data: dict):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.declare_queue("orders", durable=True)

    message = aio_pika.Message(body=json.dumps(order_data).encode())
    await channel.default_exchange.publish(message, routing_key="orders")

    print(f"[{datetime.now().isoformat()}] [>] Order published to RabbitMQ: {order_data}")

    await channel.close()
    await connection.close()
