from base64 import encode
from aio_pika import DeliveryMode, ExchangeType, Message, connect
from config_data.config import settings

async def set_task(message: str) -> None:
    # Perform connection
    AMQP_USER = settings.rabbit_mq.AMQP_USER
    AMQP_PASS = settings.rabbit_mq.AMQP_PASS
    AMQP_HOST = settings.rabbit_mq.AMQP_HOST
    
    connection = await connect(f"amqp://{AMQP_USER}:{AMQP_PASS}@{AMQP_HOST}/")

    async with connection:
        # Creating a channel
        channel = await connection.channel()

        logs_exchange = await channel.declare_exchange(
            "logs", ExchangeType.FANOUT,
        )

        message_body = b"".join(
            arg.encode() for arg in message
        )
        
        # Sending the message
        await logs_exchange.publish(Message(
            message_body,
            delivery_mode=DeliveryMode.PERSISTENT,
        ),
        routing_key="info",
        )
    

