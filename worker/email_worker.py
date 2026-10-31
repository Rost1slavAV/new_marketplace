import asyncio
import json
import aio_pika

async def process_message(message: aio_pika.IncomingMessage):


    async with message.process():
        data = json.loads(message.body.decode())
        email = data.get("email")
        name = data.get("name")


        print(f'Отправлено приветственное письмо для {name} на "{email}"')

        await asyncio.sleep(1)


async def main():
    connection = await aio_pika.connect_robust(
        host="rabbitmq",
        port=5672,
        login="guest",
        password="guest",
    )

    async with connection:
        channel = await connection.channel()

        await channel.set_qos(prefetch_count=1)


        queue = await channel.declare_queue("email_queue", durable=True)

        await queue.consume(process_message)

        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())