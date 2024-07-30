import asyncio
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
        encode_list = "".join(bytes.decode(message.body, encoding='utf-8')).split("<!#!>")
        message_dict = {}
        for kw in encode_list:
            logger.info(f'KW: {kw.split("<!&!>")}')
            message_dict[kw.split("<!&!>")[0]] = kw.split("<!&!>")[1]
        for channel in ChannelGateway.list():
            try:
                if message_dict['type'] == 'photo':
                    photo_url = settings.s3_client.s3_signature + message_dict['file_path']
                    await bot.send_photo(channel.name, photo_url, caption=message_dict['text'])
                if message_dict['type'] == 'video':
                    photo_url = settings.s3_client.s3_signature + message_dict['file_path']
                    await bot.send_video(channel.name, photo_url, caption=message_dict['text'])
                if message_dict['type'] == 'text':
                    await bot.send_message(channel.name, message_dict['text'])
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