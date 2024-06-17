import asyncio

from aiogram.exceptions import TelegramBadRequest
import logging
from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractIncomingMessage
from bot import get_bot
from services.queries.channel.orm import ChannelGateway
from config_data.config import settings

bot = get_bot()
logger = logging.getLogger(__name__)

async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        for channel in ChannelGateway.list():
            try:
                try:
                    print(channel.name, "".join(bytes.decode(message.body, encoding='utf-8')))
                    await bot.send_photo(channel.name, "".join(bytes.decode(message.body, encoding='utf-8')))
                except:
                    await bot.send_message(channel.name, "".join(bytes.decode(message.body, encoding='utf-8')))
                    pass
            except TelegramBadRequest:
                continue
            except:
                continue


async def broadcast() -> None:
    # Perform connection
    
    AMQP_USER = settings.rabbit_mq.AMQP_USER
    AMQP_PASS = settings.rabbit_mq.AMQP_PASS
    AMQP_HOST = settings.rabbit_mq.AMQP_HOST
    
    connection = await connect(f"amqp://{AMQP_USER}:{AMQP_PASS}@{AMQP_HOST}/")

    async with connection:
        # Creating a channel
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        logs_exchange = await channel.declare_exchange(
            "logs", ExchangeType.FANOUT,
        )

        # Declaring queue
        queue = await channel.declare_queue(exclusive=True)

        # Binding the queue to the exchange
        await queue.bind(logs_exchange)

        # Start listening the queue
        await queue.consume(on_message)

        await asyncio.Future()