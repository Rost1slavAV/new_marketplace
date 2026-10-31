import json
import aio_pika
from core.config import settings


async def publish_welcome_email(email: str, name: str):
    """
    Публикует задачу на отправку приветственного письма в RabbitMQ.
    """
    connection = await aio_pika.connect_robust(
        host="rabbitmq",
        port=5672,
        login="guest",
        password="guest"
    )

    async with connection:
        channel = await connection.channel()


        queue = await channel.declare_queue("email_queue", durable=True)


        message_body = json.dumps({"email": email, "name": name}).encode()
        message = aio_pika.Message(body=message_body)


        await channel.default_exchange.publish(
            message,
            routing_key=queue.name
        )

        print(f" [x] Задача на отправку письма для {email} отправлена в очередь")