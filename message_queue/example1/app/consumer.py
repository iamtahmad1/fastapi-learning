# consumer.py
import aio_pika
import asyncio
import json
from datetime import datetime

RABBITMQ_URL = "amqp://fastapi:fastapi@localhost/"

async def process_order(message: aio_pika.IncomingMessage):
    async with message.process():
        order = json.loads(message.body.decode())
        print(f"[{datetime.now().isoformat()}] [<] Received order: {order}")
        await asyncio.sleep(2)  # simulate processing
        print(f"[{datetime.now().isoformat()}] [✓] Finished processing order {order['order_id']}")

async def main():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("orders", durable=True)

    await queue.consume(process_order)
    print(f"[{datetime.now().isoformat()}] [*] Waiting for orders...")
    await asyncio.Future()  # keep the consumer running

if __name__ == "__main__":
    asyncio.run(main())
